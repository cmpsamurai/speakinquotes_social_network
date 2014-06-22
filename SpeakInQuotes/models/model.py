
me, a0, a1 ,a2 = auth.user_id, request.args(0), request.args(1) , request.args(2)

########################################################################
#_____________________ CATEGORY   _____________________________________#
   
db.define_table('category',
  Field('name'), 
  Field('ordernono'),format='%(name)s'
 )

initial_categories=[
                    {'name':'Relationships','ordernono':'1'}, 
                    {'name':'Family & Friends','ordernono':'2'},
                    {'name':'Health & Wellness','ordernono':'3'},  
                    {'name':'Culture','ordernono':'4'},
                    {'name':'Community','ordernono':'5'},
                    {'name':'Education','ordernono':'6'},
                    {'name':'Arts','ordernono':'7'},
                    {'name':'Habits','ordernono':'8'},
                   ]

#if not db(db.category).select():
#    db.category.bulk_insert(initial_categories)


db.define_table('subcategory',
                Field('category',db.category),
                Field('name'),
                Field('orderno')
                ,format='%(name)s'
             )



initial_subcategories=[
                        {'category':'1','name':'Affairs', 'orderno':'1'},
                        {'category':'1','name':'Broken Hearts & Betrayal', 'orderno':'1'},
                        {'category':'1','name':'Crushes & Obsessions', 'orderno':'1'},
                        {'category':'1','name':'Divorce', 'orderno':'1'},
                        {'category':'1','name':'First Love', 'orderno':'1'},
                        {'category':'1','name':'Intimacy', 'orderno':'1'},
                        {'category':'1','name':'Marriage', 'orderno':'1'},
                        {'category':'1','name':'Romance & True Love', 'orderno':'1'},
                        {'category':'1','name':'Struggles', 'orderno':'1'},
                        
                        {'category':'2','name':'Family Struggles', 'orderno':'1'},
                        {'category':'2','name':'Fatherhood', 'orderno':'1'},
                        {'category':'2','name':'Loss in the Family', 'orderno':'1'},
                        {'category':'2','name':'Loss of a Child', 'orderno':'1'},
                        {'category':'2','name':'Loss of a Friend', 'orderno':'1'},
                        {'category':'2','name':'Loss of a Pet', 'orderno':'1'},
                        {'category':'2','name':'Pets', 'orderno':'1'},
                        {'category':'2','name':'Loneliness', 'orderno':'1'},
                         
                         
                         
                        {'category':'3','name':'Addiction', 'orderno':'1'},
                        {'category':'3','name':'Suicide', 'orderno':'1'},
                        {'category':'3','name':'Depression', 'orderno':'1'},
                        {'category':'3','name':'Image & Weight', 'orderno':'1'},
                        {'category':'3','name':'Image & Weight', 'orderno':'1'},
                        {'category':'3','name':'Self Improvement', 'orderno':'1'},
                        {'category':'3','name':'Self Harm', 'orderno':'1'},
                        {'category':'3','name':'Phobias', 'orderno':'1'},
                      
                      
                        {'category':'4','name':'Books', 'orderno':'1'}, 
                        {'category':'4','name':'Fiction', 'orderno':'1'}, 
                        {'category':'4','name':'Hobbies', 'orderno':'1'}, 
                        {'category':'4','name':'Religion', 'orderno':'1'}, 
                        {'category':'4','name':'Travel', 'orderno':'1'}, 
                        {'category':'4','name':'Phobias', 'orderno':'1'}, 
                        {'category':'4','name':'Politics', 'orderno':'1'},
                        {'category':'4','name':'foods', 'orderno':'1'}, 
                        
                        {'category':'7','name':'Poetry', 'orderno':'1'}, 
                        {'category':'7','name':'Music', 'orderno':'1'}, 
                        {'category':'7','name':'Writings', 'orderno':'1'},
                        
                        {'category':'5','name':'Community Development', 'orderno':'1'},
                        {'category':'5','name':'Helping others', 'orderno':'1'},
                        
                        {'category':'6','name':'College', 'orderno':'1'},
                        {'category':'6','name':'School', 'orderno':'1'},
                        
                        {'category':'8','name':'Sports', 'orderno':'1'},
                        {'category':'8','name':'Smoking', 'orderno':'1'},
                       ]


#if not db(db.subcategory).select():
#    db.subcategory.bulk_insert(initial_subcategories)
    
    
def get_category_name(id):
    catid=db.subcategory(id).category
    #return db.category(db.category.id=catid).name
    pass

def get_category_picker():
    cascade = CascadingSelect(db.category,db.subcategory)
    cascade.prompt = lambda table: T("Pick a")+" "  + T(str(table))
    cat_picker = SQLFORM.factory(
        Field('category',db.subcategory,widget=cascade.widget))
    cat_picker['_id']='category_picker'
    submit = cat_picker.element('input',_type='submit') 
    submit['_style'] = 'display:none; ' 
    cat_picker.element('select').attributes['_onChange'] = 'document.forms["category_picker"].submit();'
    return cat_picker
    
    
########################################################################
#______________________ Quote Author __________________________________#

db.define_table('quote_author',
  Field('name',notnull=True),
  Field('bio', 'text', notnull=True),
  Field('posted_on', 'datetime', readable=False, writable=False),
  Field('picture','upload')
  ,format='%(name)s'
  )




########################################################################
#______________________ Quotes ___________________________________##

db.define_table('quotes',
  Field('body', 'text', notnull=True),
  Field('posted_on', 'datetime', readable=False, writable=False),
  Field('num_comments','integer',readable=False,writable=False),
  Field('favorites','integer', readable=False, writable=False),
  Field('subcategory',db.subcategory,notnull=True),
  Field('category',db.category, readable=False, writable=False,notnull=False,default=0),
  Field('author','string' ,readable=False, writable=False, notnull=True,default="Unknown"	),
  Field('is_user','boolean', required=True, default=False, readable=False, writable=False),
  Field('approved','boolean', required=True, default=False, readable=False, writable=False),
  Field('posted_by', 'reference auth_user', readable=False, writable=False,default=auth.user),
  )

  
cascade = CascadingSelect(db.category,db.subcategory)
cascade.prompt = lambda table: T("Pick a")+" "  + T(str(table))
db.quotes.subcategory.widget = cascade.widget
db.quotes.subcategory.requires=IS_NOT_EMPTY()
db.define_table('quotes_comment',
  Field('posted_by', 'reference auth_user', readable=False, writable=False,default=auth.user),
  Field('qid', db.quotes,readable=False,writable=False),
  Field('body', 'text', notnull=True),
  Field('posted_on', 'datetime', readable=False, writable=False),)



db.define_table('quotes_favorite',
  Field('fav_quote', 'reference quotes'),
  Field('posted_by', 'reference auth_user', readable=False, writable=False,default=auth.user),
  Field('posted_on', 'datetime', readable=False, writable=False),
  Field('category', 'reference category'),
  )



    


def get_quotes_comment_box(qid):
    db.quotes_comment.qid.default=qid
    db.quotes_comment.posted_on.default=request.now
    db.quotes_comment.body.label=T("Your Comment ")
    quotes_box=crud.create(db.quotes_comment)
    return quotes_box
    
def get_quotes_search_form():
	db.quotes.id.readable=False 
	db.quotes.category.readable=True
	db.quotes.author.readable=True
	db.quotes.approved.readable=True
	query=((db.quotes))
	fields = (db.quotes.id, db.quotes.body, db.quotes.category,db.quotes.approved, db.quotes.author)


	
	headers = {'quotes.id':   'ID',
           'quotes.body': 'Quote Body',
           'quotes.category': 'Quote Category',
           'quotes.approved': 'Quote Approved Yet ?',
           'quotes.author': 'Quote Author' }
	default_sort_order=[~db.quotes.posted_on]
	
	form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=False, deletable=False, editable=False, maxtextlength=64, paginate=25, csv=False)
	return form

    

    
##################################################################################
#__________________________________________ LINKS_______________________________
db.define_table('link', 
  Field('origin', 'reference auth_user'),
  Field('target', 'reference auth_user'),
  Field('requested_on', 'datetime'),
  )
  
########################################################################################


#___________________________________  Notifications ____________________________________

NOTIFICATION_TYPES=['new_quote','new_comment']

db.define_table('notifications', 
  Field('not_type', requires=IS_IN_SET(NOTIFICATION_TYPES, zero=T('--choose notification type--')) ),
  Field('not_origin', 'reference auth_user',notnull=True),
  Field('not_target', 'reference auth_user',notnull=True),
  Field('not_story',db.quotes,notnull=True),
  Field('posted_on', 'datetime', readable=False, writable=False),
  Field('seen','boolean', required=True, default=False, readable=False, writable=False),
  )

#______________________________________________________________________________________________________________

def get_user_search_form(): 
	user_search_form=SQLFORM.factory(Field('search_key',notnull=True,label="Please Enter Username / Email"),submit_button="Search")
	return user_search_form
