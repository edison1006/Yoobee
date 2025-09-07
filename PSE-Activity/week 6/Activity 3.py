import pandas as pd

df = pd.read_parquet("PSE-Activity/week 6/employees_multilevel.parquet")

sorted_df = df.sort_values(by=["hire_year", "hire_month"])

print(sorted_df)