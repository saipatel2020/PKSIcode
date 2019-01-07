from mlogic import app


def user_mail(ch1):
    from flask_mail import Mail, Message
    mailer = Mail(app)
    import pyodbc
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = '66.147.236.155,1433'
    database = 'pksi_Hrwebapp'
    username = 'webuser1'
    password = 'Pegasus@1212'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    for k,v in ch1.items():
        cursor.execute("select EMAIL from [dbo].[USER_INFORMATION_FINAL] where FIRSTNAME=?",k)
        ml = cursor.fetchall()
#        print(ml[0][0])
        print(ml)
        msg = Message('Hello', sender='spinumalla@pksi.com', recipients = [ml[0][0]])
        msg.body = "Hi %s. Your request is approved. You can now use the PKSI HR Analytics Portal." %k
        mailer.send(msg)
#       return "Sent"
    for key, val in ch1.items():
        print(key)
        msg = Message('QLIKADMINACCESS', sender='spinumalla@pksi.com', recipients = ['santhosha@pksi.com'])
        msg.body = "User request is approved. Please give access for user %s to use the PKSI HR Analytics Portal." %key
        mailer.send(msg)
        print('check1')
    cnxn.close()
