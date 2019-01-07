import datetime
QlikServer='peg3.pksi.com'
QlikPort=4243
QlikCertificate=('E:/Work/BKAnalyticsCopy/ExternalCertificates/client.pem',
                 'E:/Work/BKAnalyticsCopy/ExternalCertificates/client_key.pem')
QlikRoot='E:/Work/BKAnalyticsCopy/ExternalCertificates/root.pem'
QlikUserDirectory='PEG3'
QlikHrStream = "HR"
QlikBkStream = "Banking"
QlikLgStream = "Logistics"
QlikHcStream = "HealthCare"
QlikBkApps = "General Banking"
QlikLgApp = "Driver Retention Dashboard"
QlikHcApp = "General Healthcare"
QlikHrApps = ["Attrition","Forecasting","Employability","Profiling","Loyalty","General Summary"]
QlikUserRoles = {"HR":["General Summary"],
                 "Compensation Analyst":["Forecasting","General Summary"],
                 "HR Manager":["Attrition","Forecasting","Employability","Profiling","Loyalty","General Summary"],
                 "HR Lead":["Attrition","Forecasting","Employability","Profiling","Loyalty","General Summary"],
                 "HR Recruiter": ["Employability","General Summary"],
                 "HR Director":["Attrition","Forecasting","Employability","Profiling","Loyalty","General Summary"],
                 "admin":["Attrition","Forecasting","Employability","Profiling","Loyalty","General Summary"]
                 }
FirmName = ""
IfIframeUse = False
ConnectString = """
                    DRIVER={SQL Server};
                    SERVER= 66.147.236.155;
                    UID= webuser1;
                    PWD= Pegasus@1212;
                """
y = datetime.datetime.now()
time_st = y.strftime("%b-%d-%Y %I:%M %p")
