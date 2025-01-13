import pandas as pd


# data = pd.read_excel('data.xlsx')
# print(data.head())
# data['Data Type'] = data['Data Type'].ffill()

# data.iloc[:, 1] = data.iloc[:, 1].ffill()
# data.to_csv('data.csv')
# print(data.head())


df = pd.read_csv('data.csv')
df.to_excel("new.data.xlsx")