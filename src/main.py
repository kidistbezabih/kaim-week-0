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

# Check if there are any CSV files
if not data_files:
    raise FileNotFoundError("No CSV files found in the data/ directory.")

# Load the first CSV file
dataset_path = os.path.join(data_dir, data_files[0])
df = pd.read_csv(dataset_path)

# Display summary statistics
st.title("Summary Statistics")
st.write(df.describe())
