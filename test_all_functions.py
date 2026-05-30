import pandas as pd
import sys
import os
import traceback

# Add the path to the functions folder (adjust to your actual path)
functions_path = r"C:\Users\179518\Desktop\All Files\Data Science\Second semester\Hardware & Software_2nd_semester\bibliometrix-python\functions"
sys.path.append(functions_path)

# Import functions
from functions.get_annualproduction import get_annual_production
from functions.get_averagecitations import get_average_citations
from functions.get_relevantsources import get_relevant_sources
from functions.get_relevantauthors import get_relevant_authors

# Load your standardized data
df = pd.read_csv("advanced_standardized_data.csv", sep=';')

# Wrapper class
class DataWrapper:
    def __init__(self, df):
        self.data = df
    def get(self):
        return self.data

wrapped = DataWrapper(df)

# Test each function
tests = [
    ("Annual Production", get_annual_production, []),
    ("Average Citations", get_average_citations, []),
    ("Relevant Sources", get_relevant_sources, [10]),
    ("Relevant Authors", get_relevant_authors, [10, "n_docs"]),
]

print("Column names:", df.columns.tolist())
print("TC NaN count:", df['TC'].isna().sum() if 'TC' in df.columns else "TC missing")
print("PY NaN count:", df['PY'].isna().sum() if 'PY' in df.columns else "PY missing")

for name, func, args in tests:
    try:
        result = func(wrapped, *args)
        print(f"✅ {name} passed")
    except Exception as e:
        print(f"❌ {name} failed: {e}")
        print(traceback.format_exc())