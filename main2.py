import pandas as pd

df_1 = pd.read_excel("results.xlsx")
df_2 = pd.read_excel("results2.xlsx")

for index, line in enumerate(df_1.values):
    print(df_1.values[index] == line)
