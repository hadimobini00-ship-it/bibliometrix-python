import pandas as pd
import sys
import os

# Add the project root to sys.path to ensure local imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the corrected function name
from functions.get_annualproduction import get_annual_production


# Create a helper class to mimic the custom data object the function expects
class DataWrapper:
    def __init__(self, df):
        self.data = df

    def get(self):
        return self.data


# 1. Load your standardized data
file_path = "advanced_standardized_data.csv"

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Run main.py first to generate it.")
else:
    df = pd.read_csv(file_path, sep=';')

    # 2. Run the function
    try:
        print("Running analysis...")

        # Wrap the DataFrame to satisfy the .get() requirement
        wrapped_df = DataWrapper(df)

        # Capture both the figure and the data returned by the function
        fig, pub_data = get_annual_production(wrapped_df)

        print("Function passed!")
        print("--- First 5 rows of calculated annual production ---")
        print(pub_data.head())

    except Exception as e:
        print(f"Function crashed! Error: {e}")
        import traceback

        traceback.print_exc()