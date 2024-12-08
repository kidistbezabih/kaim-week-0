# src/utils.py

import pandas as pd

def calculate_summary_statistics(df):
    """
    Calculates summary statistics (mean, median, std dev, range, variance) for each numeric column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input data.

    Returns:
    pd.DataFrame: A DataFrame containing the summary statistics.
    """
    # Select only numeric columns for summary statistics
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    mean_values = df[numeric_columns].mean()
    median_values = df[numeric_columns].median()
    std_dev_values = df[numeric_columns].std()
    range_values = df[numeric_columns].max() - df[numeric_columns].min()
    variance_values = df[numeric_columns].var()

    summary_stats = pd.DataFrame({
        'Mean': mean_values,
        'Median': median_values,
        'Std Dev': std_dev_values,
        'Range': range_values,
        'Variance': variance_values
    })

    return summary_stats
