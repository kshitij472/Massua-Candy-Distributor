import pandas as pd

file_path = "data/massua.csv"

df = pd.read_csv(file_path)

print(df.head())

print("\nColumns in dataset:")
print(df.columns)

print("\nShape of dataset:")
print(df.shape)