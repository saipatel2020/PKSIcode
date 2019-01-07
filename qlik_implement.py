from libfiles import *                                                     # importing required packages from libfiles.


def qlik_render():                                                         # function used to authenticate with Qlik.
    print (current_user)
    print (current_user.data)
    title = str(current_user.data['title'][0])
    if 'query' in request.args:
        global usecase
        usecase = request.args['query']
        if usecase in config.QlikUserRoles.get(str(title)):
            print (str(current_user.data['uid'][0]))
            global q
            q = qlikConnect.QlikRendering(server=config.QlikServer,port=config.QlikPort,
                                                  certificate=config.QlikCertificate,
                                                  root=config.QlikRoot,
                                                  userdirectory=config.QlikUserDirectory,
                                                  userid= str(current_user.data['uid'][0]))
        else:
                flash("you are not authorized to access dashboards. Please contact admin for adding to database")
                return redirect(url_for('home'))


def qlik_reports(option):                                                 # function used to get BI reports from Qlik.
    qlik_render()
    print("Hi " + option + "_" + str.upper(str(current_user.data['preferredLanguage'][0]))+"_"+usecase)
    app_name = option+"_"+str.upper(str(current_user.data['preferredLanguage'][0]))+"_"+usecase
    print(app_name)
    url = q.create_qs_sheet_app_url(option+"_"+ str.upper(str(current_user.data['preferredLanguage'][0])),app_name)
    print(url)
    if config.IfIframeUse:
        template = """
                         <iframe src ="""+ url+""" style="width:100%;height:90%;border:none;">
                         <h5><a href='/logout'>Logout</a></h5></iframe>"""

        return render_template_string(template)
    else:
        return url

