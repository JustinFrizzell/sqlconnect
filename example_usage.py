import SQLconnect as sc

connection = sc.SQLconnector("WorldWideImporters")
df = connection.sql_query("query.sql")

print(df.head())
