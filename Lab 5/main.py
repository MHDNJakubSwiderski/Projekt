import pandas as pd
import os

csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

dfs = []
for file in csv_files:
    temp_df = pd.read_csv(file, encoding='unicode_escape')
    if 'Invoice' in temp_df.columns:
        temp_df = temp_df.rename(columns={'Invoice': 'InvoiceNo', 'Price': 'UnitPrice', 'Customer ID': 'CustomerID'})
    dfs.append(temp_df)

df = pd.concat(dfs, ignore_index=True)

df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed')
df['Month'] = df['InvoiceDate'].dt.to_period('M')
df['Year'] = df['InvoiceDate'].dt.year

print("Zadanie 1")
print(df.groupby('Country')['TotalPrice'].sum().nlargest(10))

print("\n\nZadanie 2")
print(df.groupby('Month')['TotalPrice'].sum().idxmax())

print("\n\nZadanie 3")
print(pd.pivot_table(df, values='TotalPrice', index='Country', columns='Month', aggfunc='sum'))

print("\n\nZadanie 4")
yearly_sales = df.groupby(['Country', 'Year'])['TotalPrice'].sum().reset_index()
print(yearly_sales.loc[yearly_sales.groupby('Country')['TotalPrice'].idxmax()])

print("\n\nZadanie 5")
product_sales = df.groupby(['Country', 'Description'])['TotalPrice'].sum().reset_index()
print(product_sales.sort_values(['Country', 'TotalPrice'], ascending=[True, False]).groupby('Country').head(5))