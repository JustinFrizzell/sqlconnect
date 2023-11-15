EXEC [dbo].[InsertEventLog]
    @SubjectArea = N'Finance',
    @ProcessName = N'QuarterlyReportGeneration',
    @InstanceID = N'Q3-2023',
    @EventData = '<EventData><Detail>Report generated successfully</Detail></EventData>'