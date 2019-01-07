from libfiles import *                        # importing all the required packages and libraries.
import qlik_bi                         # importing the Qlik file
import usermail
import ldap


@app.route('/')
def home():                                                                     # Default route function
    if 'username' in session:
        return render_template('index.html',company = config.FirmName)
    return render_template('login_test.html', company=config.FirmName)


@app.route('/login', methods=['GET', 'POST'])                                    # Login route function
def do_admin_login():                                                               # variable to store the selected domain of the user
    select = request.form.get('choice')
    print(select)
    uname = request.form.get('username')
    print(uname)
    if request.method == 'POST':
        form = LDAPLoginForm(request.form)
        if form.validate_ldap():                                                # Checking the ldap users
            # Successfully logged in, We can now access the saved user object
            # via form.user.
            print ("successfully logged in")
            session['username'] = request.form['username']
            login_user(form.user) # Tell flask-login to log them in.
            print(current_user.data)
            for ke,vi in current_user.data.items():
                print(ke)
                print(vi[0])
                if (ke == 'title' and vi[0] == 'admin'):
                    return render_template('postadmin.html', company=config.FirmName)
            # dbconn.Db.add_user(current_user)                                    # Adding the users to the database.
            return domain_check(select,uname)
        return redirect(url_for('logout'))
    else:
        return render_template('login_test.html',company = config.FirmName)


@app.route('/admin')
def screen():
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
    cursor.execute("select FIRSTNAME+LASTNAME as UserName from [dbo].[USER_INFORMATION_FINAL] where [Approved] is NULL")
    data = cursor.fetchall()
    print(data)
    return render_template('adminlatest.html',data=data)


@app.route('/check_approve', methods=['POST'])
def check_approve():
    if request.method == 'POST':
        import pyodbc
        import datetime
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = '66.147.236.155,1433'
        database = 'pksi_Hrwebapp'
        username = 'webuser1'
        password = 'Pegasus@1212'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        a = request.form
        print(a)
        u1=[]
        p1=[]
        ap1=[]
        u1=a.getlist('username')
        p1=a.getlist('Privileges')
        for i in u1:
            x =a.getlist(i)
            ap1.append(x)
        print(u1)
        print(p1)
        print(ap1)
        global Newusers
        Newusers = {}
        for j in range(0,len(ap1)):
            print (ap1[j][0])
            if ( 'approve' in str(ap1[j]) ):
                #print("inside {} {}".format(ap1[j][0],u1[j][0]))
                #x = str(datetime.datetime.now())
                print (str(p1[j]))
                #s = cursor.execute("UPDATE [dbo].[USER_INFORMATION_FINAL] SET [Approved] = 'True', [TimeStamp] = ?, [Role]= ? WHERE [FIRSTNAME] like ?",(config.time_st,str(p1[j]),str(u1[j])))
                y = datetime.datetime.now()
                time_st = y.strftime("%b%d %Y %I:%M %p")
                s = "UPDATE [dbo].[USER_INFORMATION_FINAL] SET [Approved] = 'True', [TimeStamp] = '"+time_st+"' , [Role]='" + str(p1[j]) + "' WHERE [FIRSTNAME] like '" + str(u1[j]) + "'"
                print(s)
                cursor.execute(s)
                usr = []
                usr = u1[j]
                print(usr)
                Newusers[usr] = p1[j]
                cnxn.commit()
            elif ('reject1' in str(ap1[j])):
                print("Reject1")
            else:
                print("inside")
                print (u1[j])
                s = "UPDATE [dbo].[USER_INFORMATION_FINAL] SET [Approved] = 'False', [TimeStamp] = SYSDATETIMEOFFSET() WHERE [FIRSTNAME] like '"+str(u1[j])+"'"
                print(s)
                cursor.execute(s)
                cnxn.commit()
        print(Newusers)
        obj = ldap.Ldap()
        obj.add_user_ldap(Newusers)
        usermail.user_mail(Newusers)
        print('check2')
        return redirect(url_for('screen'))


@app.route('/bulkadd')
def bulk_user_add():
    return render_template('charts.html')


def domain_check(select, uname):                                                             # Checking the selected domain of the user to redirect them to their
                                                                                        # respective landing page.
    if(select=='HR'):
        global ob
        ob = HR()                                                                   # Creating HR instance
        return redirect(url_for('home')) # Send them home
    elif(select=='BANKING'):
            ob = BANKING()
            return render_template('bkindex.html',company = config.FirmName)
    elif(select=='LOGISTICS'):
        if uname == "Pksiguest1":
            ob = LOGISTICS()                                                        # Creating Logistics Instance
            return ob.lgqliksinglesignon()
        else:
            return redirect(url_for('logout'))
    else:
        if uname == "Pksiguest1":
            ob = HEALTHCARE()                                                       # Creating Health care Instance
            return ob.hcqliksinglesignon()
        else:
            return redirect(url_for('logout'))


@app.route('/qliksso')
def qliksinglesignon_logic():                                                       # function for getting HR Qlik reports.
    #ob = session["object"]
    global ob
    ob = HR()
    #print(ob)
    reports = ob.hrqliksinglesignon()
    print(reports)
    return redirect(reports)


@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        global fn
        fn = request.form.get('companyname')
#        print(fn)
        global ln
        ln = request.form.get('name')
        global email
        email = request.form.get('email')
        print(email)
        global ph
        ph = request.form.get('usrtel')
        global pwd
        pwd = request.form.get('password')
        import pyodbc
        import datetime
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = '66.147.236.155,1433'
        database = 'pksi_Hrwebapp'
        username = 'webuser1'
        password = 'Pegasus@1212'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        cursor.execute("select EMAIL from [dbo].[USER_INFORMATION_FINAL] where APPROVED is NULL")
        rows = cursor.fetchall()
        print(rows)
        cursor.execute("select EMAIL from [dbo].[USER_INFORMATION_FINAL] where APPROVED='True'")
        approved_users = cursor.fetchall()
        print(approved_users)
        for item in rows:
            if item[0] == email:
                flash('Your request is pending. Please wait for admin approval.')
                return render_template('postregister.html')
        for ch in approved_users:
            if ch[0] == email:
                flash('You are already a registered user. Please do not re-register.')
                return render_template('postregister.html')
        y = datetime.datetime.now()
        time_st = y.strftime("%b-%d-%Y %I:%M %p")
        print(time_st)
        cursor.execute("INSERT INTO [dbo].[USER_INFORMATION_FINAL]([FIRSTNAME],[LASTNAME],[EMAIL],[PHONENUMBER],[UserPASSWORD],[Username],[RegisteredTimeStamp]) VALUES (?,?,?,?,?,?,?)",fn,ln,email,ph,
                       pwd, '0',time_st)
        cnxn.commit()
        cursor.execute("select * from [dbo].[USER_INFORMATION_FINAL]")
        u_data = cursor.fetchall()
        print(u_data)
        flash('Thank you for Registering. You were successfully signed up!. Your request is pending!.')
        return render_template('postregister.html')
    return render_template('register.html')


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        fn = request.form.get('companyname')
        ln = request.form.get('name')
        email = request.form.get('email')
        ph = request.form.get('usrtel')
        pwd = request.form.get('password')
        from ldap3 import Server,Connection, ALL, NTLM,ObjectDef,Reader
        server = Server('peg4.pksi.com', get_info=ALL)
        conn = Connection(server, user="cn=admin,dc=pksi,dc=com", password="secret")
        conn.bind()
        obj_inetorgperson = ObjectDef('inetOrgPerson', conn)
        r = Reader(conn, obj_inetorgperson, 'dc=pksi,dc=com')
        from ldap3 import MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
        conn.modify('cn= current_user.data.cn[0],ou=PEG3,dc=pksi,dc=com', {'givenName': [(MODIFY_REPLACE, [fn])]}, controls=None)
        conn.modify('cn= current_user.data.cn[0],ou=PEG3,dc=pksi,dc=com', {'sn': [(MODIFY_REPLACE, [ln])]}, controls=None)
        conn.modify('cn= current_user.data.cn[0],ou=PEG3,dc=pksi,dc=com', {'mail': [(MODIFY_REPLACE, [email])]}, controls=None)
        conn.modify('cn= current_user.data.cn[0],ou=PEG3,dc=pksi,dc=com', {'mobile': [(MODIFY_REPLACE, [ph])]}, controls=None)
        conn.modify('cn= current_user.data.cn[0],ou=PEG3,dc=pksi,dc=com', {'userPassword': [(MODIFY_REPLACE, [pwd])]}, controls=None)
        r.search()
        print(r[2])
        flash('Your account has been updated !')
        session.pop('username',None)
    return render_template('myaccount.html')


@app.route("/logout")
def logout():                                                                       # logging out the user session.
    session.pop('username',None)
    return render_template('login_test.html',company = config.FirmName)


class HR:
    def hrqliksinglesignon(self):                                                   # method for implementing the Qlik functions
        # Get attribute from request
        g = qlik_bi.Qlik()
        return qlik_bi.qlik_reports(config.QlikHrStream)


class BANKING:
    def bkqliksinglesignon(self):                                                   # method for retrieving banking qlik reports
        # Get attribute from request
        print (current_user)
        print (current_user.data)
        title = str(current_user.data['title'][0])
        q = qlikConnect.QlikRendering(server=config.QlikServer,port=config.QlikPort,
                          certificate=config.QlikCertificate,
                          root=config.QlikRoot,
                          userdirectory=config.QlikUserDirectory,
                          userid= str(current_user.data['uid'][0]))
        url = q.create_qs_sheet_app_url(config.QlikBkStream,config.QlikBkApps)
        print (url)
        return redirect(url)


class LOGISTICS:
    def lgqliksinglesignon(self):                                                  # method for retrieving logistics qlik reports
        # Get attribute from request
        print (current_user)
        print (current_user.data)
        title = str(current_user.data['title'][0])
        q = qlikConnect.QlikRendering(server=config.QlikServer,port=config.QlikPort,
                          certificate=config.QlikCertificate,
                          root=config.QlikRoot,
                          userdirectory=config.QlikUserDirectory,
                          userid= str(current_user.data['uid'][0]))
        url = q.create_qs_sheet_app_url(config.QlikLgStream,config.QlikLgApp)
        print (url)
        return redirect(url)


class HEALTHCARE:
    def hcqliksinglesignon(self):                                                 # method for retrieving health care qlik reports
        print (current_user)
        print (current_user.data)
        title = str(current_user.data['title'][0])
        q = qlikConnect.QlikRendering(server=config.QlikServer,port=config.QlikPort,
                          certificate=config.QlikCertificate,
                          root=config.QlikRoot,
                          userdirectory=config.QlikUserDirectory,
                          userid= str(current_user.data['uid'][0]))

        url = q.create_qs_sheet_app_url(config.QlikHcStream, config.QlikHcApp)
        print(url)
        return redirect(url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3800)


