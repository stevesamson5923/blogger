from tkinter import ttk
import random

USER_NAME='GUEST'

login_content_type = None
login_entries = None
asset_entries = None

space_id = 'ma8yestsieel'
blog_content_type = None
blog_entries = None
post_title = []
created_on = []

initial_data_loaded =False
central_note= None
posts_list = None
def set_notebook(root):
    global central_note
    central_note = ttk.Notebook(root,width=1350,height=610)
    central_note.pack()

def get_notebook():
    return central_note

def blog_content_api_call(client):
    #print('blog api call')
    global blog_content_type
    blog_content_type = client.content_types(space_id, 'master').find('blogData')

def change_user_name(name):
    global USER_NAME
    USER_NAME = name
    
def get_user_name():
    return USER_NAME

def get_blog_data(user_name,client):
    #print('blogdata')
    global blog_entries,initial_data_loaded
    blog_content_api_call(client)
    blog_entries = blog_content_type.entries().all()
    index=0
    for b in blog_entries:        
        if b.authorname == user_name:
            #print(b.posttitle)
            post_title.insert(index,b.posttitle)
            created_on.insert(index,b.created_on)
            #initial_data_loaded = True
        index = index + 1        
    initial_data_loaded = True       
def gettitle():
    return post_title

def getdate():
    return created_on

def set_post_list(post_list):
    global posts_list
    posts_list = post_list

def get_post_list():
    return posts_list

def get_description(title,auth):
    global blog_entries
    blog_entries = blog_content_type.entries().all()
    for b in blog_entries:
        if b.posttitle == title and b.authorname == auth:
            #print('Here: ',b.posttitle)
            desc = b.description
            #print(desc)
            return desc


def get_lastdate(title,auth):
    global blog_entries
    blog_entries = blog_content_type.entries().all()
    for b in blog_entries:
        if b.posttitle == title and b.authorname == auth:
            #print('match')
            #print('Here: ',b.posttitle)
            lastMod = b.last_modified
            #print(lastMod)
            return lastMod
    