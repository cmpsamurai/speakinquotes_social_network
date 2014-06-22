# coding: utf8
@auth.requires_login()
def index(): 
	redirect(URL('quotes','famous'))
	return locals()

@auth.requires_login()
def famous():
	response.title=T("Famous Quotes")
	response.subtitle=T("Quotes by authors from history")
	categories = cache.ram('categories',lambda:db(db.category).select(orderby=db.category.ordernono).as_dict(),1800)
	return locals()
	
	
@auth.requires_login()
def user():
	response.title=T("User Quotes")
	response.subtitle=T("Where Users Express their Feelings")
	categories = cache.ram('categories',lambda:db(db.category).select(orderby=db.category.ordernono).as_dict(),1800)
	return locals()
         	
@auth.requires_login()	
def create():
	response.title=T("Create Quote")
	response.subtitle=T("Share Your Quote With the world")
	db.quotes.is_user.default=True
	db.quotes.approved.default=True
	db.quotes.posted_by.default=auth.user
	db.quotes.posted_on.default=request.now
	db.quotes.author.readable=db.quotes.author.writable=True
	quote_create = SQLFORM(db.quotes)
	umyfollowers = db(db.link.target==me).select().as_dict()		
	if quote_create.process(onvalidation=update_category).accepted:
		for follower in umyfollowers:
			if not ( umyfollowers[follower]['id'] ==me):
				db.notifications.insert(not_story=quote_create.vars.id , posted_on=request.now,not_origin=me ,not_target=umyfollowers[follower]['id'],seen=False,not_type="new_quote")
		redirect(URL('quotes','view',args=(str(quote_create.vars.id))))
	return locals()
	
@auth.requires_login()	
def update_category(form):
	if  form.vars.subcategory:
		 db.quotes.category.default=str(form.vars.category_name) 
	else:
		form.errors.subcategory = T('must insert a value')
		  

@auth.requires_login()
def edit():
    experience=db.experience(request.args(0))
    if (experience==None or experience.posted_by!=me):
        redirect(URL('experiences','view',args=(a0)))
    db.experience.subcategory.writable = False 
    form = SQLFORM(db.experience,a0,showid = False,deletable=True)
    
    if form.process().accepted:
    
        experience=db.experience(a0)
        if experience:
            redirect(URL('experiences','view',args=(str(form.vars.id))))
        else:
            redirect(URL('experiences','index'))
    return locals()
    


@auth.requires_login()
def view():
	quote=db.quotes(request.args(0))
	if(quote==None or quote.approved==False):
		redirect(URL('quotes','index'))
	session.curr_category=quote.category
	session.curr_subcategory=quote.subcategory
	previous_vote=db.quotes_favorite(fav_quote=request.args(0),posted_by=me)
	previous_seen= db((db.notifications.not_story==request.args(0))&(db.notifications.not_target==me)).select()
	if previous_seen:
		for story in previous_seen:
			db(db.notifications.id == story.id).update(seen=True)
	return locals()


@auth.requires_login()
def post():
	comment_box=get_quotes_comment_box(request.args(0))

	if(comment_box).accepted:
		story=db.quotes(request.args(0))
		val=story.num_comments
		if val==None: val=0
		val=val+1
		story.update_record(num_comments=val)
		
		if not (story.posted_by==me):
			previous_notification=db((db.notifications.not_story==request.args(0))&(db.notifications.not_origin==me) & (db.notifications.not_type=="new_comment")& (db.notifications.not_target==story.posted_by)).select()
			if not (previous_notification):
				db.notifications.insert(not_story=story.id , posted_on=request.now,not_origin=me ,not_target=story.posted_by,seen=False,not_type="new_comment")
			else:
				db(db.notifications.id == previous_notification[0].id).update(seen=False,posted_on=request.now)
				db.commit()
		quote_comments=db((db.quotes_comment.qid==request.args(0))).select(limitby=(0,40), orderby=db.quotes_comment.posted_on)
		for commenter in quote_comments:
					if not(commenter.posted_by==me):
						previous_notification=db((db.notifications.not_story==request.args(0))&(db.notifications.not_origin==me) & (db.notifications.not_type=="new_comment")& (db.notifications.not_target==commenter.posted_by)).select()
						if not (previous_notification):
							db.notifications.insert(not_story=story.id , posted_on=request.now,not_origin=me ,not_target=commenter.posted_by,seen=False,not_type="new_comment")
						else:
							db(db.notifications.id == previous_notification[0].id).update(seen=False,posted_on=request.now)
	else:
		quote_comments=db((db.quotes_comment.qid==request.args(0))).select(limitby=(0,40), orderby=db.quotes_comment.posted_on)					 	
	
	return locals()



  
@auth.requires_login()
def List_Quotes():
    if len(request.args)>2: 
		page=int(request.args[2])
    else: page=0
    items_per_page=NUM_QUOTES_INPAGE
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #rows=db((db.quotes.subcategory==request.args[0])& (db.quotes.approved==True)).select(limitby=limitby, orderby=~db.quotes.posted_on)
    if str(request.args[0])=='user':
		rows = cache.ram('userquotesinsubcategory'+request.args[1]+"-"+str(page),lambda:db((db.quotes.subcategory==request.args[1])& (db.quotes.approved==True) & (db.quotes.is_user==True)).select(limitby=limitby, orderby=~db.quotes.posted_on).as_dict(),60)
    elif str(request.args[0])=='famous':
		rows = cache.ram('famousquotesinsubcategory'+request.args[1]+"-"+str(page),lambda:db((db.quotes.subcategory==request.args[1])& (db.quotes.approved==True) & (db.quotes.is_user==False)).select(limitby=limitby, orderby=~db.quotes.posted_on).as_dict(),60)
    return dict(Quotes=rows,page=page,items_per_page=items_per_page)


@auth.requires_login()	
def Fetch_Subcategoris():
	subcategories = cache.ram('subcategories'+request.args(1),lambda:db(db.subcategory.category==request.args(1)).select().as_dict(),1800)
	return locals();
	
	

    
@auth.requires_login()
def favorite():
    if not request.env.request_method=='POST': raise HTTP(400)
    quote_id,Mode=request.args(0),request.args(1)
    
    previous_vote=db.quotes_favorite(fav_quote=quote_id,posted_by=auth.user.id)
    quote=db.quotes(db.quotes.id==quote_id)
    value=quote.favorites

    if previous_vote==None:
        if value==None:
            value=1
        else:
            value=value+1
        db(db.quotes.id == quote_id).update(favorites=value)
        db.quotes_favorite.insert(fav_quote=quote_id , posted_on=request.now,posted_by=me,category=quote.category)
        db.commit()
        return "jQuery('#favorite').parent().html('%s');"%(T('Quote added to Favorites')) 
    else:
        value=value-1
        db(db.quotes.id == quote_id).update(favorites=value)
        db(db.quotes_favorite.fav_quote==quote_id , db.quotes_favorite.posted_by==me).delete()
        db.commit()
        return "jQuery('#favorite').parent().html('%s');"%(T('Quote removed from Favorites ')) 
        
        
@auth.requires_login()
def delete_comment():
    if not request.env.request_method=='POST': raise HTTP(400)
    comment_id=request.args(0)
    comment=db.quotes_comment(db.quotes_comment.id==comment_id)
    quote=db.quotes(db.quotes.id==comment.qid)
    value=quote.num_comments
    if comment.posted_by==me:
        db(db.quotes_comment.id==comment_id , db.quotes_favorite.posted_by==me).delete()
        value=value-1
        db(db.quotes.id == quote.id).update(num_comments=value)
        db.commit()
        return "jQuery('#comment_delete-"+comment_id+"').parent().html('%s');"%(T('Deleted')) 

@auth.requires_login()    
def search():
	response.title=T("Search Quotes")
	response.subtitle=T("Search The Quotes Database")
	if 'view' in request.args:
		redirect(URL('quotes','view',args=(request.args(2))))

	form=get_quotes_search_form()
	return locals()

