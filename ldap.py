from libfiles import *


class Ldap:
    from ldap3 import Server,Connection, ALL, NTLM,ObjectDef,Reader
    server = Server('peg4.pksi.com', get_info=ALL)
    conn = Connection(server, user="cn=admin,dc=pksi,dc=com", password="secret")
    conn.bind()

    @classmethod
    def add_user_ldap(cls, ch):
        cls.ch = ch
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
        for key, val in ch.items():
            print('cn={},ou=PEG3,dc=pksi,dc=com'.format(key))
            cursor.execute("select LASTNAME from [dbo].[USER_INFORMATION_FINAL] where FIRSTNAME=?",key)
            lname = cursor.fetchall()
            print(lname[0][0])
            cursor.execute("select EMAIL from [dbo].[USER_INFORMATION_FINAL] where FIRSTNAME=?",key)
            maile = cursor.fetchall()
            print(maile[0][0])
            cursor.execute("select USERPASSWORD from [dbo].[USER_INFORMATION_FINAL] where FIRSTNAME=?",key)
            upwd = cursor.fetchall()
            print(upwd[0][0])
            print(val)
            cls.conn.add('cn={},ou=PEG3,dc=pksi,dc=com'.format(key), 'inetOrgPerson', {'givenName':  key, 'displayName': key, 'sn': lname[0][0], 'mail': maile[0][0], 'userPassword': upwd[0][0], 'title': val,'uid': key, 'preferredLanguage':'r'})
            c = cls.conn.search('ou=PEG3,dc=pksi,dc=com','(&(objectClass = inetOrgPerson)(cn = {}))'.format(key))
            print(c)

    @classmethod
    def check_user_ldap(cls, ch):
        for key, val in ch.items():
            if cls.conn.search('ou=PEG3,dc=pksi,dc=com', '(&(objectClass = inetOrgPerson)(cn = {}))'.format(key)):
                flash('Your request is pending. Please wait for admin approval.')
                return render_template('register.html')
