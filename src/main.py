import os
import pandas as pd
import streamlit as st

# Get the base directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the data directory path
data_dir = os.path.join(base_dir, '../data/')

# Check if the data directory exists
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"The directory {data_dir} does not exist. Please ensure the data/ folder is correctly placed.")

# List all CSV files in the data directory
data_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

# Data Quality Check

# Check if there are any CSV files
if not data_files:
    raise FileNotFoundError("No CSV files found in the data/ directory.")

# Load the first CSV file
dataset_path = os.path.join(data_dir, data_files[0])
df = pd.read_csv(dataset_path)

# Display summary statistics
st.title("Summary Statistics")
st.write(df.describe())


# Check for missing values
st.subheader("Missing Values Check")
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
st.write("Missing Values Summary:")
st.write(pd.DataFrame({"Missing Count": missing_values, "Percentage": missing_percentage}))

# Identify negative values in specific columns
st.subheader("Negative Value Check")
columns_to_check_positive = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
negative_values = {col: (df[col] < 0).sum() for col in columns_to_check_positive}
st.write("Negative Values Summary:")
st.write(pd.DataFrame(negative_values.items(), columns=["Column", "Negative Count"]))

# Outlier Detection using IQR method
st.subheader("Outlier Detection")
def detect_outliers(column):
    Q1 = df[column].quantile(0.25)  # First quartile
    Q3 = df[column].quantile(0.75)  # Third quartile
    IQR = Q3 - Q1  # Interquartile range
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)].shape[0]

outlier_summary = {col: detect_outliers(col) for col in ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']}
st.write("Outlier Summary:")
st.write(pd.DataFrame(outlier_summary.items(), columns=["Column", "Outlier Count"]))

# Optional: Highlight rows with potential data quality issues
st.subheader("Rows with Issues")
rows_with_issues = df[
    (df[columns_to_check_positive] < 0).any(axis=1) |  # Any negative values
    ((df['GHI'] > 1200) | (df['DNI'] > 1200) | (df['DHI'] > 1200))  # Extreme high values for irradiance
]
st.write(f"Number of rows with issues: {len(rows_with_issues)}")
if len(rows_with_issues) > 0:
    st.write(rows_with_issues.head())


# Time Series Analysis

# Parse the Timestamp column
st.subheader("Time Series Analysis")
if 'Timestamp' in df.columns:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])  # Remove rows with invalid timestamps
    df.set_index('Timestamp', inplace=True)  # Set Timestamp as index for easier plotting
    
    # Extract time-based features
    df['Month'] = df.index.month
    df['Hour'] = df.index.hour

    # Plot GHI, DNI, DHI, and Tamb over time
    st.write("**Line Chart of Solar Irradiance and Temperature Over Time**")
    st.line_chart(df[['GHI', 'DNI', 'DHI', 'Tamb']])
    
    # Group by month and plot aggregated data
    st.write("**Monthly Averages of Solar Irradiance and Temperature**")
    monthly_data = df[['GHI', 'DNI', 'DHI', 'Tamb']].groupby(df['Month']).mean()
    st.bar_chart(monthly_data)

    # Group by hour and plot aggregated data
    st.write("**Hourly Averages of Solar Irradiance and Temperature**")
    hourly_data = df[['GHI', 'DNI', 'DHI', 'Tamb']].groupby(df['Hour']).mean()
    st.line_chart(hourly_data)
else:
    st.warning("The dataset does not contain a 'Timestamp' column for time series analysis.")
