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
	if not(request.args) or not (db.auth_user(request.args[0])):
		redirect(URL('home','index'))
	categories = cache.ram('categories',lambda:db(db.category).select(orderby=db.category.ordernono).as_dict(),1800)
	user = cache.ram('user_data'+request.args(0),lambda:db(db.auth_user.id==request.args[0]).select().as_dict(),120)
	user=user[user.keys()[0]]
	print user
	previous_follow=db.link(origin=me,target=request.args(0))
	return locals()


@auth.requires_login()
def List_User_Quotes():
    if len(request.args)>2: 
		page=int(request.args[2])
    else: page=0
    items_per_page=NUM_QUOTES_INPAGE
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows = cache.ram('q_u'+request.args(0)+"-"+request.args(1)+"-"+str(page),lambda:db((db.quotes.posted_by==request.args(0))&( db.quotes.category==request.args[1] )).select(limitby=limitby,orderby=~db.quotes.posted_on).as_dict(),120)   
    #rows=db((db.quotes_favorite.posted_by==request.args[0])&( db.quotes_favorite.category==request.args[1] )).select(limitby=limitby, orderby=~db.quotes_favorite.posted_on)
    return dict(Quotes=rows,page=page,items_per_page=items_per_page)


@auth.requires_login()
def follow():
    #if not request.env.request_method=='POST': raise HTTP(400)
    
    previous_follow=db.link(origin=me,target=request.args(0))
    user=db.auth_user(request.args(0))
    if not user:
		return 

    if previous_follow==None:
        db.link.insert(origin=me , requested_on=request.now,target=request.args(0))
        db.commit()
        return "jQuery('#follow').parent().html('%s');"%(T('User Followed')) 
    else:
		db((db.link.origin==me) & (db.link.target==request.args(0))).delete()
		db.commit()
		return "jQuery('#follow').parent().html('%s');"%(T('User Unfollowed')) 
