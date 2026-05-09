import pandas as pd

# ZADANIE 1
df = pd.read_csv("Online_Retail.csv", encoding="latin1")
df = df.dropna(subset=['CustomerID'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] >= 0)]
df = df.drop_duplicates()
df['CustomerID'] = df['CustomerID'].astype(int)

# Dodany argument format='mixed' eliminuje ostrzeżenie
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed')
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day

df['TotalSales'] = df['Quantity'] * df['UnitPrice']
fact_sales = df[['InvoiceNo', 'StockCode', 'CustomerID', 'InvoiceDate', 'Quantity', 'TotalSales']]
fact_sales.to_csv("fact_sales.csv", index=False)

# ZADANIE 2
df1 = pd.read_csv("Online_Retail.csv", encoding="latin1")
df2 = pd.read_excel("online_retail_II.xlsx")

print("--- 2.1 ---")
print("Czy struktura danych jest identyczna? Nie, nazwy kolumn (np. CustomerID vs Customer ID) lub formaty dat mogą się różnić w zależności od źródła.")
print("Czy dane można od razu połączyć? Nie, wymagają weryfikacji i ujednolicenia schematu.\n")

print("--- 2.2 ---")
df2.rename(columns={'Customer ID': 'CustomerID', 'Price': 'UnitPrice'}, inplace=True, errors='ignore')

# Dodany argument format='mixed' eliminuje ostrzeżenie
df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'], format='mixed')
df2['InvoiceDate'] = pd.to_datetime(df2['InvoiceDate'], format='mixed')

print("Który schemat przyjąć jako docelowy? Schemat z Online_Retail.csv bez spacji w nazwach.")
print("Czy wszystkie kolumny są potrzebne? Tylko kluczowe do tabeli faktów (InvoiceNo, StockCode, CustomerID, InvoiceDate, Quantity, UnitPrice).\n")

print("--- 2.3 ---")
print("Jak rozpoznać duplikat? Sprawdzając unikalność kombinacji kluczowych kolumn (np. InvoiceNo, StockCode, Quantity).")
print("Co zrobić z konfliktem danych? Usunąć duplikaty i zachować nowszy rekord w przypadku niespójności.")
print("Które źródło jest bardziej wiarygodne? Traktujemy je równorzędnie, polegając na dacie transakcji.\n")

print("--- 2.4 ---")
df1 = df1.dropna(subset=['CustomerID'])
df2 = df2.dropna(subset=['CustomerID'])

df_all = pd.concat([df1, df2], ignore_index=True)
df_all = df_all.drop_duplicates()

print("Czy użyć concat czy merge? Concat, ponieważ dodajemy wiersze (historię) z drugiego pliku o tej samej strukturze.")
print("Czy zachować wszystkie rekordy? Nie, zachowujemy tylko połączone, oczyszczone i unikalne rekordy.\n")

df_all.to_csv("fact_sales_integrated.csv", index=False)