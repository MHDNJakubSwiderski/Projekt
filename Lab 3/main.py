import pandas as pd
import numpy as np

print("\nZADANIE 1\n")

print("Wczytanie danych...")

df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

print("Rozmiar danych początkowych:", df.shape)

print("\nCZYSZCZENIE DANYCH")

df = df.dropna(subset=["CustomerID"])
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="mixed")
df = df.drop_duplicates()

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("Rozmiar danych po czyszczeniu:", df.shape)

print("\nZIARNO (GRANULARITY)")

print("Wybrane ziarno: Pojedyncza pozycja faktury (InvoiceNo + StockCode)")

print(
    "Wybrano ziarno na poziomie pojedynczej pozycji faktury (InvoiceNo + StockCode), "
    "ponieważ zapewnia najwyższy poziom szczegółowości i umożliwia szeroką analizę sprzedaży "
    "na poziomie produktu w ramach transakcji."
)

print("Możliwe analizy biznesowe:")
print("- sprzedaż produktów")
print("- analiza klientów i krajów")
print("- trendy czasowe")
print("- analiza koszyka zakupowego")

print("\nWYMIAR KLIENT")

dim_klient = df[["CustomerID", "Country"]].drop_duplicates().reset_index(drop=True)
dim_klient["KluczKlienta"] = range(1, len(dim_klient) + 1)
dim_klient = dim_klient[["KluczKlienta", "CustomerID", "Country"]]

print("Rozmiar DimKlient:", dim_klient.shape)

print("\nWYMIAR PRODUKT")

dim_produkt = df[["StockCode", "Description"]].drop_duplicates().reset_index(drop=True)
dim_produkt["KluczProduktu"] = range(1, len(dim_produkt) + 1)
dim_produkt = dim_produkt[["KluczProduktu", "StockCode", "Description"]]

print("Rozmiar DimProdukt:", dim_produkt.shape)

print("\nWYMIAR DATA")

dim_data = pd.DataFrame()
dim_data["Data"] = df["InvoiceDate"].dt.date.drop_duplicates()
dim_data["KluczDaty"] = range(1, len(dim_data) + 1)
dim_data["Rok"] = pd.to_datetime(dim_data["Data"]).dt.year
dim_data["Miesiac"] = pd.to_datetime(dim_data["Data"]).dt.month
dim_data["Dzien"] = pd.to_datetime(dim_data["Data"]).dt.day

dim_data = dim_data[["KluczDaty", "Data", "Rok", "Miesiac", "Dzien"]]

print("Rozmiar DimData:", dim_data.shape)

print("\nTABELA FAKTÓW")

fact_sprzedaz = df.copy()

fact_sprzedaz = fact_sprzedaz.merge(dim_klient, on=["CustomerID", "Country"], how="left")
fact_sprzedaz = fact_sprzedaz.merge(dim_produkt, on=["StockCode", "Description"], how="left")

fact_sprzedaz["Data"] = fact_sprzedaz["InvoiceDate"].dt.date

fact_sprzedaz = fact_sprzedaz.merge(dim_data, on="Data", how="left")

fact_sprzedaz = fact_sprzedaz[
    ["KluczKlienta", "KluczProduktu", "KluczDaty", "Quantity", "Revenue"]
]

print("Rozmiar FactSales:", fact_sprzedaz.shape)

print("\nZAPIS PLIKÓW")

dim_klient.to_csv("DimKlient.csv", index=False)
dim_produkt.to_csv("DimProdukt.csv", index=False)
dim_data.to_csv("DimData.csv", index=False)
fact_sprzedaz.to_csv("FactSprzedaz.csv", index=False)

print("Zapis zakończony")

print("\n\n ZADANIE 2")

print(" ROZSZERZENIE MODELU: DIM COUNTRY ")

dim_country = df[["Country"]].drop_duplicates().reset_index(drop=True)
dim_country["CountryKey"] = range(1, len(dim_country) + 1)

print("Rozmiar DimCountry:", dim_country.shape)


print("\n SCD TYPE 2 (KLIENT) ")

df_scd2 = df[["CustomerID", "Country"]].drop_duplicates().copy()

df_scd2 = df_scd2.sort_values("CustomerID")

df_scd2["DataOd"] = pd.to_datetime("2010-12-01")
df_scd2["DataDo"] = pd.to_datetime("2099-12-31")
df_scd2["CzyAktualny"] = 1

df_scd2["Wersja"] = df_scd2.groupby("CustomerID").cumcount() + 1

df_scd2.loc[df_scd2.duplicated("CustomerID", keep="last"), "CzyAktualny"] = 0

print("Przykład SCD2:")
print(df_scd2.head())


print("\n JAKOŚĆ MODELU ")

print("Model gwiazdy zawiera:")
print("- Fakt sprzedaży (FactSales)")
print("- Wymiary: Klient, Produkt, Data, Country")

print("Zastosowano klucze sztuczne oraz normalizację wymiarów.")


print("\n ANALIZA BIZNESOWA ")

print("Model umożliwia analizę:")
print("- sprzedaży według klientów i krajów")
print("- trendów czasowych (dzień/miesiąc/rok)")
print("- najlepiej sprzedających się produktów")
print("- zmian klientów w czasie (SCD2)")