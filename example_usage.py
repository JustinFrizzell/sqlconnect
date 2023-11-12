import SQLconnect as sc

# Establish a connection to the database
connection = sc.SQLconnector("WorldWideImporters")

# Assign the results of a query to a pandas DataFrame
df = connection.query_to_df("query.sql")

# Print the top 5 rows
print(df.head(5))
