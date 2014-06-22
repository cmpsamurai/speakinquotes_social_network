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
	categories = cache.ram('categories',lambda:db(db.category).select(orderby=db.category.ordernono).as_dict(),1800)
	quoteofday=db((db.quotes_favorite)).select(limitby=(0,1), orderby=~db.quotes_favorite.posted_on)
	return locals()


@auth.requires_login()
def List_Favorite_Quotes():
    if len(request.args)>1: 
		page=int(request.args[1])
    else: page=0
    items_per_page=NUM_QUOTES_INPAGE
    limitby=(page*items_per_page,(page+1)*items_per_page+1)   
    rows=db((db.quotes_favorite.posted_by==me)&( db.quotes_favorite.category==request.args[0] )).select(limitby=limitby, orderby=~db.quotes_favorite.posted_on)
    return dict(Quotes=rows,page=page,items_per_page=items_per_page)


@auth.requires_login()
def List_User_Notifications():
    if len(request.args)>0: 
		page=int(request.args[0])
    else: page=0
    items_per_page=NUM_NOTIFICATIOS_INPAGE	
    limitby=(page*items_per_page,(page+1)*items_per_page+1)   
    rows=db((db.notifications.not_target==me)).select(limitby=limitby, orderby=~db.notifications.posted_on)
    #rows=db((db.notifications.not_to==me)).select(limitby=limitby, orderby=~db.notifications.posted_on)
    return dict(Notifications=rows,page=page,items_per_page=items_per_page)



