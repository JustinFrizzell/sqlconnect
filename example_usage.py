import SQLconnect as sc

# Set up database connections, all configuration is handled with connections.yaml and .env
connection_logger = sc.SQLconnector("Logger")
connection_WWI = sc.SQLconnector("WorldWideImporters")

# Assign the results of a query to a pandas DataFrame
df = connection_WWI.sql_to_df(r"example/query.sql")

command = """EXEC [dbo].[InsertEventLog]
    @SubjectArea = N'Finance',
    @ProcessName = N'QuarterlyReportGeneration',
    @InstanceID = N'Q3-2023',
    @EventData = '<EventData><Detail>Report generated successfully</Detail></EventData>'"""

# Execute commands
connection_logger.execute_sql_str(command)
connection_logger.execute_sql(r"example/command.sql")

# Explore the dataframe with Pandas
print(df.describe())
