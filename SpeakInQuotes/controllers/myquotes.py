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
	response.title=T("My Quotes Manager")
	response.subtitle=T("Manage My Quotes")
	db.quotes.id.readable=False 
	db.quotes.category.readable=True
	db.quotes.approved.readable=True
	query=((db.quotes.posted_by==auth.user))
	fields = (db.quotes.id, db.quotes.body, db.quotes.category,db.quotes.approved, db.quotes.author)
	headers = {'quotes.id':   'ID',
           'quotes.body': 'Quote Body',
           'quotes.category': 'Quote Category',
           'quotes.approved': 'Quote Approved Yet ?',
           'quotes.author': 'Quote Author' }
	default_sort_order=[~db.quotes.posted_on]
	
	form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=False, deletable=True, editable=True, maxtextlength=64, paginate=25, csv=False)

	if 'view' in request.args:
		redirect(URL('quotes','view',args=(request.args(2))))
	return locals()


