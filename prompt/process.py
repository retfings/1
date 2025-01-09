import pandas as pd


data = pd.read_excel('data.xlsx')
data['Data Type'] = data['Data Type'].ffill()
data['Data Type'] = data['Data Type'].ffill()
data.to_csv('data.csv')