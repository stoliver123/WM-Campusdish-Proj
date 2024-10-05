import pandas as pd

df = pd.read_csv('our_df.csv')
# print(df)

df.rename(columns={'Unnamed: 0':'Food'}, inplace=True)

print(df)