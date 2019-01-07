
# These are all the necessary imports of packages and libraries for the web application.
from flask import Flask, flash, redirect, render_template, request,escape, session, abort, url_for, render_template_string
from flask_ldap3_login import LDAP3LoginManager
from flask_ldap3_login.forms import LDAPLoginForm
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user
from qlikConnect import qlikRender as qlikConnect
from datetime import timedelta
import os
import logging
from logging.handlers import RotatingFileHandler

# setting up the loggers to know about the logs.
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler('flaskpython.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.ERROR)


# Initializing and configuring the flask application with LDAP.
app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['LDAP_HOST'] = 'peg4.pksi.com'
app.config['LDAP_PORT'] = 389
app.config['LDAP_PROTOCOL_VERSION'] = 3
app.config['LDAP_BASE_DN'] = 'dc=pksi,dc=com'
app.config['LDAP_USER_DN'] = 'ou=PEG3'
app.config['LDAP_USER_LOGIN_ATTR'] = 'cn'
app.config['LDAP_USER_RDN_ATTR'] = 'cn'
app.config['LDAP_GROUP_OBJECT_FILTER'] = '(objectclass=inetOrgPerson)'
app.config['LDAP_BIND_USER_DN'] = None
app.config['LDAP_BIND_USER_PASSWORD'] = None
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'spinumalla@pksi.com'
app.config['MAIL_PASSWORD'] = 'sbp@pksi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.logger.setLevel('DEBUG')
app.logger.addHandler(file_handler)

login_manager = LoginManager(app)      # Login Manager used for managing the flask application logging.
ldap_manager = LDAP3LoginManager(app)  # LDAP Manager used for managing the LDAP Login.
users = {}                             # Initializing the users


class User(UserMixin):
    def __init__(self, dn, username, data):                   # Creating the user objects
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn


@login_manager.user_loader                                    # Loading the users from sessions
def load_user(id):
    if id in users:
        return users[id]
    return None


@ldap_manager.save_user                                       # Saving the users from LDAP.
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user

