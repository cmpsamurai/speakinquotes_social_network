# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################



@auth.requires_login()    
def index():
	response.title=T("Manage Your Connections")
	response.subtitle=T("Manage Your Followings and Followers")
	user_search_box = get_user_search_form()
	if user_search_box.process().accepted:
		if (all(ord(c) < 128 for c in user_search_box.vars.search_key)):
			redirect(URL('connections','search',args=(user_search_box.vars.search_key)))
		session.flash="Please enter an english text"
		redirect(URL('connections','index'))
		
	return locals()


@auth.requires_login()    
def search():
	if len(request.args)==0: redirect(URL('connections','index'))
	response.title=T("Search Users")
	response.subtitle=T("find your friends on SpeakInQuotes")
	user_search_box = get_user_search_form()
	if user_search_box.process().accepted:
		if (all(ord(c) < 128 for c in user_search_box.vars.search_key)):
			redirect(URL('connections','search',args=(user_search_box.vars.search_key)))
		session.flash="Please enter an english text"
		redirect(URL('connections','search',args=("None")))
			
	if len(request.args)>0:
		rows=  db((db.auth_user.email==request.args[0])).select().as_dict()
		items_per_page=NUM_FRIENDS_INPAGE
		if not rows:
			rows = db((db.auth_user.username==request.args[0])).select().as_dict()
	return dict(Connections=rows,items_per_page=items_per_page,user_search_box=user_search_box)
	
	
@auth.requires_login()
def List_Followers():
    if len(request.args)>1: 
		page=int(request.args[1])
    else: page=0
    items_per_page=NUM_FRIENDS_INPAGE
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows = db((db.link.target==me)).select(limitby=limitby, orderby=~db.link.requested_on).as_dict()
    return dict(Connections=rows,page=page,items_per_page=items_per_page)


@auth.requires_login()
def List_Following():
    if len(request.args)>1: 
		page=int(request.args[1])
    else: page=0
    items_per_page=NUM_FRIENDS_INPAGE
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows = db((db.link.origin==me)).select(limitby=limitby, orderby=~db.link.requested_on).as_dict()
    return dict(Connections=rows,page=page,items_per_page=items_per_page)

