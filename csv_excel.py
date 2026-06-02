import pandas as pd
df = pd.read_csv("advanced_standardized_data.csv", sep=';')
df.to_excel("advanced_standardized_data.xlsx", index=False)