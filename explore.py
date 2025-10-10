import pandas as pd

df = pd.read_csv("financial_transactions.csv")
print(df.shape)
print(df.dtypes)
print(df.columns.tolist())

