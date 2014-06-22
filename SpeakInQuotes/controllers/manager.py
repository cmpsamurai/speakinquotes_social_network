# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################



@auth.requires_membership('manager')    
def index():
	response.title=T("Manager's Control Panel")
	response.subtitle=T("Manage The Quotes")
	db.quotes.id.readable=False 
	db.quotes.category.readable=db.quotes.category.writable=True
	db.quotes.approved.readable=db.quotes.approved.writable=True
	db.quotes.posted_on.default=request.now
	db.quotes.author.readable=db.quotes.author.writable=True
	db.quotes.is_user.readable=db.quotes.is_user.writable=True
	
	
	query=((db.quotes))
	fields = (db.quotes.id, db.quotes.body,db.quotes.subcategory,db.quotes.category,db.quotes.approved, db.quotes.author,db.quotes.posted_on,db.quotes.favorites,db.quotes.posted_by)
	headers = {'quotes.id':   'ID',
           'quotes.body': 'Quote Body',
           'quotes.category': 'Quote Category',
           'quotes.subcategory': 'Quote Sub Category',
           'quotes.approved': 'Quote Approved Yet ?',
           'quotes.author': 'Quote Author',
           'quotes.posted_on': 'Quote Posted ON',
           'quotes.favorites': 'Quote Favorites',
           'quotes.posted_by': 'Quote Posted By' }
	default_sort_order=[~db.quotes.posted_on]
	
	form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=True, deletable=True, editable=True, maxtextlength=64, paginate=25, csv=True)
	
	if 'view' in request.args:
		redirect(URL('quotes','view',args=(request.args(2))))
	return locals()


