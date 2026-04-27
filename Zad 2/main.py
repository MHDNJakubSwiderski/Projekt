import pandas as pd

# ZADANIE 1
url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")
print("Zadanie 1:")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(df.head(), "\n")

# ZADANIE 2
print("Zadanie 2:")
encje = {
    "Customer": {"Klucz główny": "CustomerID", "Podstawowe atrybuty": ["Country"]},
    "Product": {"Klucz główny": "StockCode", "Podstawowe atrybuty": ["Description"]},
    "Orders": {"Klucz główny": "InvoiceNo", "Podstawowe atrybuty": ["InvoiceDate", "CustomerID"]},
    "OrderItems": {"Klucz główny": ("InvoiceNo", "StockCode"), "Podstawowe atrybuty": ["Quantity", "UnitPrice"]}
}
for nazwa, detale in encje.items():
    print(f"{nazwa}: {detale}")
print("\n")

# ZADANIE 3
print("Zadanie 3:")
customers = df[['CustomerID', 'Country']].dropna(subset=['CustomerID']).drop_duplicates(subset=['CustomerID'])
products = df[['StockCode', 'Description']].drop_duplicates(subset=['StockCode'])
orders = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo'])
order_items = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]

dates = pd.DataFrame()
dates['InvoiceDate'] = df['InvoiceDate'].drop_duplicates()
dates['Date_dt'] = pd.to_datetime(dates['InvoiceDate'], format='mixed')
dates['Year'] = dates['Date_dt'].dt.year
dates['Month'] = dates['Date_dt'].dt.month

print("Utworzono znormalizowane ramki danych.")
print(f"Test unikalności PK - Customers: {customers['CustomerID'].is_unique}")
print(f"Test unikalności PK - Products: {products['StockCode'].is_unique}")
print(f"Test unikalności PK - Orders: {orders['InvoiceNo'].is_unique}\n")

# ZADANIE 4
print("Zadanie 4:")
print("Dlaczego niewygodny do OLAP: Znormalizowana struktura obniża wydajność analityczną przy odczycie.")
print("Co wymaga wielu joinów: Każde zapytanie raportujące i agregujące.")