# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate,Recaptcha
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

GENDER_SET=[T('Male'),T('Female')]

auth.settings.extra_fields['auth_user']= [
Field('gender',requires=IS_IN_SET(GENDER_SET, zero=T('--choose Gender--'))),    
Field('dob', 'date',label=T('Date of Birth'),notnull=True),
Field('profile_picture','upload'),
  ]

def name_of(user): 
	if(db.auth_user(user)):
		return db.auth_user(user).first_name+" "+ db.auth_user(user).last_name
	else:
		return "Unknown"
 
## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail=auth.settings.mailer
mail.settings.server ='gae'
mail.settings.sender ='moustafa@cmpsamurai.com'
mail.settings.login = 'moustafa@cmpsamurai.com:Alpha1Me007'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False

#auth.settings.register_next = URL('default','registration', args='verify_email')
auth.settings.verify_email_next = URL('home','index')
auth.messages.verify_email=T("Thank you for registering to PerfectFeels :) \n ")+auth.messages.verify_email
auth.settings.register_captcha = Recaptcha(request,'6LeBluISAAAAADvoBWrEZhLxm_kAFGvdA-ozU9f2', '6LeBluISAAAAAMoZbAG1gnnKevwcjgxOau1CzbZZ',error_message=T('invalid'), label=T('Verify You are Human:'),use_ssl=True)


## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
