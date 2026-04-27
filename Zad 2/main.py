import pandas as pd

url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")

print(df.shape[0])
print(df.shape[1])
print(df.head())

customers = df[['CustomerID', 'Country']].dropna().drop_duplicates(subset=['CustomerID'])
products = df[['StockCode', 'Description']].drop_duplicates(subset=['StockCode'])
orders = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo'])
order_items = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]

dates = pd.DataFrame()
dates['InvoiceDate'] = df['InvoiceDate'].drop_duplicates()
dates['Year'] = pd.to_datetime(dates['InvoiceDate'], format='mixed').dt.year
dates['Month'] = pd.to_datetime(dates['InvoiceDate'], format='mixed').dt.month

print(customers['CustomerID'].is_unique)
print(products['StockCode'].is_unique)
print(orders['InvoiceNo'].is_unique)

print(order_items['StockCode'].isin(products['StockCode']).all())
print(order_items['InvoiceNo'].isin(orders['InvoiceNo']).all())

customers.to_csv("customers.csv", index=False, sep=';')
products.to_csv("products.csv", index=False)
orders.to_csv("orders.csv", index=False)
order_items.to_csv("order_items.csv", index=False)
dates.to_csv("dates.csv", index=False)

print("Model 3NF nie jest wygodny do analiz, bo dane są w wielu tabelach i trzeba je łączyć, co jest wolniejsze i bardziej skomplikowane.")