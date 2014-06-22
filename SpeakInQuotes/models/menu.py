# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('SpeakInQuotes'),
                  _class="brand",_href=URL('default', 'index'))
response.title = T('SpeakInQuotes')
response.subtitle = T('The Quotes Sharing Network!')
response.description = 'SpeakInQuotes allows you to express your feelings using quotes and connects you with other people who love quotes like you :)'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Moustafa Mahmoud <Moustafa.Mahmoud.Fathy@outlook.com>'
response.meta.description = 'SpeakInQuotes allows you to express your feelings using quotes and connects you with other people who love quotes like you :)'



## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
##

if auth.is_logged_in():
    
    response.menu= [    
    (IMG(_src=URL('static','images/home.png'),_style="width:20px;",_title="Home"), False, URL('default','index'),),
    (IMG(_src=URL('static','images/profile.png'),_style="width:20px;",_title="Profile"), False, URL('profile','index',args=(auth.user.id)),),
    (IMG(_src=URL('static','images/history.png'),_style="width:20px;",_title="Famous & Historical Quotes"), False, URL('quotes','famous'),),
    (IMG(_src=URL('static','images/user-quotes.png'),_style="width:20px;",_title="User Quotes"), False, URL('quotes','user'),),
	(IMG(_src=URL('static','images/my-quotes.png'),_style="width:20px;",_title="My Quotes"), False, URL('myquotes','index'),),
	(IMG(_src=URL('static','images/user-connections.png'),_style="width:20px;",_title="My Connections"), False, URL('connections','index'),),
	] 
   
   
DEVELOPMENT_MENU = False
DEFAULT = lambda: None
import re

def newnavbar(prefix='Welcome', action=None,
               separators=(' [ ', ' | ', ' ] '), user_identifier=DEFAULT,
               referrer_actions=DEFAULT, mode='default'):
        def Anr(*a,**b):
            b['_rel']='nofollow'
            return A(*a,**b)
        referrer_actions = [] if not referrer_actions else referrer_actions
        asdropdown = (mode == 'dropdown')
        if isinstance(prefix, str):
            prefix = T(prefix)
        if prefix:
            prefix = prefix.strip() + ' '
        s1, s2, s3 = separators
        if URL() == action:
            next = ''
        else:
            next = '?_next='+ URL(args=request.args,
                                                vars=request.get_vars)
        href = lambda function: '%s/%s%s' % (action, function,
                                             next if referrer_actions is DEFAULT or function in referrer_actions else '')

        if auth.user:
            if user_identifier is DEFAULT:
                user_identifier = '%(first_name)s'
            if callable(user_identifier):
                user_identifier = user_identifier(self.user)
            elif ((isinstance(user_identifier, str) or
                  type(user_identifier).__name__ == 'lazyT') and
                  re.search(r'%\(.+\)s', user_identifier)):
                user_identifier = user_identifier % auth.user
            if not user_identifier:
                user_identifier = ''
            logout = Anr(T('Logout'), _href='logout')
            profile = Anr(T('Profile'), _href=href('profile'))
            password = Anr(T('Password'), _href=href('change_password'))
            bar = SPAN(
                prefix, user_identifier, s1, logout, s3, _class='auth_navbar')

            if asdropdown:
                logout = LI(Anr(I(_class='icon-off'), ' ' + T('Logout'), _href=URL('default','user',args=('logout')) ))  # the space before T('Logout') is intentional. It creates a gap between icon and text
                profile = LI(Anr(I(_class='icon-user'), ' ' +T('Profile'), _href=URL('profile','index',args=(auth.user.id))))
                password = LI(Anr(I(_class='icon-lock'), ' ' +T('Password'), _href=URL('default','user',args=('change_password'))))
                
                bar = UL(logout, _class='dropdown-menu')
                bar.insert(-1,profile)
                bar.insert(-1,password)
                
            if not asdropdown:
				bar.insert(-1, s2)
				bar.insert(-1, profile)
				bar.insert(-1, s2)
				bar.insert(-1, password)
        else:
            login = Anr(T('Login'), _href=href('login'))
            register = Anr(T('Register'), _href=href('register'))
            retrieve_username = Anr(
                T('Forgot username?'), _href=href('retrieve_username'))
            lost_password = Anr(
                T('Lost password?'), _href=href('request_reset_password'))
            bar = SPAN(s1, login, s3, _class='auth_navbar')

            if asdropdown:
                login = LI(Anr(I(_class='icon-off'), ' ' + T('Login'), _href=href('login')))  # the space before T('Login') is intentional. It creates a gap between icon and text
                register = LI(Anr(I(_class='icon-user'),
                              ' ' + T('Register'), _href=URL('default','user',args=('register'))))
                retrieve_username = LI(Anr(I(_class='icon-edit'), ' ' + T(
                    'Forgot username?'), _href=URL('default','user',args=('retrieve_username'))))
                lost_password = LI(Anr(I(_class='icon-lock'), ' ' + T(
                    'Lost password?'), _href=URL('default','user',args=('request_reset_password'))))
                bar = UL(login, _class='dropdown-menu')
            
            if not asdropdown:
				bar.insert(-1, s2)
            bar.insert(-1, register)
	   
            if not asdropdown:
                bar.insert(-1, s2)
            bar.insert(-1, retrieve_username)
	   
            if not asdropdown:
                bar.insert(-1, s2)
            bar.insert(-1, lost_password)

        if asdropdown:
            bar.insert(-1, LI('', _class='divider'))
            if auth.user:
                bar = LI(Anr(prefix, user_identifier, _href='#'),
                         bar, _class='dropdown')
            else:
                bar = LI(Anr(T('Login'), _href='#'),
                         bar, _class='dropdown')
        return bar
    
