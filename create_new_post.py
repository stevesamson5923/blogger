import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox, Scrollbar,Canvas
from tkinter import Menu, filedialog
from PIL import ImageTk, Image
from datetime import datetime
import random
import threading
import time
import contentful_management
import values as v
from tkinter import ttk
import urllib.request
import os

client = None
blog_space = None
blogdata_content_type = None
space_id = 'ma8yestsieel'
management_api = "CFPAT-ilH5jr5ioiOuNvh1Ior2QjEs4_mIP7Q3B1DpEcsD1K8"
post_entries = None
asset_entries = None

def contentful_api():
    global blogdata_content_type,blog_space,client
    management_api = "CFPAT-ilH5jr5ioiOuNvh1Ior2QjEs4_mIP7Q3B1DpEcsD1K8"
    client = contentful_management.Client(management_api)
    blog_space = client.spaces().find(space_id)
    blogdata_content_type = client.content_types(space_id, 'master').find('blogData')
    
contentful_api()

def fetch_entries():
    global post_entries
    post_entries = blogdata_content_type.entries().all()

def get_entry_id():
    new_id = random.randint(200000,300000)
    already_present = False
    for l in post_entries:
        if l.id == new_id:
            already_present = True
            break
    if already_present:
        get_entry_id()
    else:
        return new_id
    
def get_new_asset_id():
    new_id = random.randint(100000,200000)
    already_present = False
    for a in asset_entries:
        if a.id == new_id:
            already_present = True
            break
    if already_present:
        get_new_asset_id()
    else:
        return new_id
    
def update_api(author,title,s):
    #print('API',author,title)
    fetch_entries()
    new_image_upload = blog_space.uploads().create(os.getcwd()+"//addphoto.png")
    ass = client.assets(space_id, 'master').create(
                    get_new_asset_id(),
                    {
                            'fields': {
                                    'file': {
                                            'en-US': {
                                                    'fileName': f'{v.get_user_name()}.png',
                                                    'contentType': 'image/jpg',
                                                    'uploadFrom': new_image_upload.to_link().to_json()
                                                    }
                                                }
                                            }
                                            }
                                            )
    ass.process()
    ass.publish()
        
    get_asset_entries()
    
    entry_attributes = {
                    'content_type_id': 'blogData',
                    'fields': {
                            'authorname': {
                                    'en-US': author
                                    },
                            'posttitle': {
                                    'en-US': title
                                    },
                            'description': {
                                    'en-US': "Please enter blog description here"
                                    },
                            'createdOn': {
                                    'en-US': s
                                    },      
                            'lastModified': {
                                    'en-US': s
                                    },      
                            'wallpaper': {
                                    'en-US': {
                                            'sys': {
                                                    'id': ass.sys['id'], #asset is of type Asset, created ealier
                                                    'linkType': 'Asset',
                                                    'type': 'Link',
                                                    }
                                            }
                                        },
                                    }
                                }

    
#    entry_attributes = {
#                    'content_type_id': 'blogData',
#                    'fields': {
#                            'authorname': {
#                                    'en-US': author
#                                    },
#                            'posttitle': {
#                                    'en-US': title
#                                    },
#                            'createdOn':{
#                                    'en-US':s
#                                    }
#                                }
#                            }
    new_entry = client.entries(space_id, 'master').create(get_entry_id(),entry_attributes)
    new_entry.publish()
    
def get_asset_entries():
    global asset_entries
    asset_entries = client.assets(space_id, 'master').all()
    
get_asset_entries()

def get_blog_data_entry_id(auth,title):
    blog_entries = blogdata_content_type.entries().all()
    for b in blog_entries:
        if b.authorname == auth and b.posttitle == title:
            return b.id

def download_user_image(URL):
    #os.remove("wallpaper.jpg")
    URL = "https:" + URL
    with urllib.request.urlopen(URL) as url:
        with open('wallpaper.jpg', 'wb') as f:
            f.write(url.read())
            
def get_wallpaper(title,author):
    
    global blog_entries
    blog_entries = blogdata_content_type.entries().all()
    for b in blog_entries:
        if b.posttitle == title and b.authorname == author:
            cur_entry_wall_id = b.wallpaper.id
            asset = client.assets(space_id, 'master').find(cur_entry_wall_id)
            download_user_image(asset.url())

class NewPostFrame:
    def __init__(self,main_frame1,row,column):
        self.main_frame = main_frame1
        self.row = row
        self.col = column
        self.user = v.get_user_name()
        self.post_added_flag = False
        self.f = Frame(self.main_frame,width=270,height=130,bg='white',highlightbackground="#35c9cc",highlightthickness=2)
        self.f.pack_propagate(0)
        self.title = Label(self.f,text='Create New Post',bg='white',font=('Helvetica',18,'bold'))
        self.msg = Label(self.f,text='',fg='#ba040a',bg='#fff',font=('Helvetica',8))
        self.a = tk.StringVar()        
        self.a.set('Enter post title')
        self.pst = ''
        self.post_name = Entry(self.f,textvariable=self.a,fg='#d7d9d2')
        self.post_name.bind('<FocusIn>',self.empty_box)
        self.post_name.bind('<FocusOut>',self.fill_user_box)
        self.post_name.bind('<Key>',self.change_text_color)        
        self.add_post_but = Button(self.f,text='Create Post',bg='#35c9cc',fg='white',font=('Helvetica',12,'bold'))
        self.add_post_but.bind('<Button-1>',self.create_a_new_post)
        self.post_list = []
        self.post_title = v.gettitle()
        self.post_date = v.getdate()
        self.initial_load()
        self.display()
    def initial_load(self):
        row=0
        column=0
        for index,p in enumerate(self.post_title):
            P = Post_frame(self.main_frame,self.post_title[index],row,column,self.user,self.post_date[index])
            column=column+1
            if column > 3:
                row= row + 1
                column = 0
            self.post_list.insert(index,P)
        v.set_post_list(self.post_list)
        self.row=row
        self.col = column
    def create_a_new_post(self,event):
        self.pst = self.a.get()
        if self.a.get() == '' or self.a.get() == 'Enter post title':
            self.msg.configure(text='Please enter title first')    
        else:            
            d = datetime.today()
            s = d.strftime('%d/%m/%y')
            P = Post_frame(self.main_frame,self.a.get(),0,0,self.user,s)
            self.post_list.insert(0,P)  #add new post at the beginning
            v.set_post_list(self.post_list)
            self.col = self.col + 1
            if self.col == 4:
                self.row = self.row + 1
                self.col = 0 
            for index,p in enumerate(self.post_list):
                if index != 0:
                    if self.post_list[index-1].col < 3:
                        p.row = self.post_list[index-1].row
                        p.col = self.post_list[index-1].col + 1
                        p.display()
                    else:
                        p.row = self.post_list[index-1].row + 1
                        p.col = 0
                        p.display()      
        self.display()
        self.user = v.get_user_name()
        self.post_added_flag = True
        #d = datetime.today()
        #s = d.strftime('%d/%m/%y')
        update_api(self.user,self.a.get(),s) 
    def display(self):
        self.f.grid(row=self.row,column=self.col,padx=10,pady=10)
        self.title.pack(side='top',padx=5,pady=5,anchor='w')
        self.msg.pack(side='top',padx=5,anchor='w')
        self.post_name.pack(side='left',padx=5,pady=5,ipadx=5,ipady=5)
        self.add_post_but.pack(side='left',padx=5,pady=5)
    def empty_box(self,event):
        #print(event.widget)
        if event.widget.get() == 'Enter post title':
            self.post_name.delete(0,END)
    def fill_user_box(self,event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Enter post title')
            self.post_name.configure(fg='#d7d9d2')
    def change_text_color(self,event):
        event.widget.configure(fg='#000') 
        self.msg.configure(text='')

tab_list = dict()
tab_index = 0

class Post_frame(Frame):
    def __init__(self,main_frame1,title,row,column,user,date):
        self.main_frame = main_frame1
        self.row = row
        self.col = column
        self.title = title
        self.author = user
        self.f = Frame(self.main_frame,width=270,height=130,bg='white',highlightbackground="#35c9cc",highlightthickness=2)
        self.f.grid_propagate(0)
        self.title = Label(self.f,text=self.title,bg='white',font=('Helvetica',18,'bold'))
        self.edit_post_but = Button(self.f,text='Edit Post',bg='#35c9cc',fg='white',font=('Helvetica',12,'bold'),command=lambda:self.edit_post(title,user,date))
        #self.edit_post_but.bind('<Button-1>',lambda x:self.edit_post(self.title))
        self.delete_post_but = Button(self.f,text='Delete Post',bg='#ba040a',fg='white',font=('Helvetica',12,'bold'))
        self.delete_post_but.bind('<Button-1>',self.delete_post)      
        self.date =date
        self.post_date = Label(self.f,text='Created on:'+self.date,bg='white',fg='#7a7a78',font=('Helvetica',8,'italic'))
        self.status = Label(self.f,text='',bg='#fff',fg='#ba040a',font=('Helvetica',8))                            
        self.display()
        #update(self.author,self.title)
        #self.update_blog_thread = threading.Thread(target=self.update)
        #self.update_blog_thread.start()
    def display(self):
        self.f.grid(row=self.row,column=self.col,padx=5,pady=10)
        self.title.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky='w')
        self.edit_post_but.grid(row=1,column=0,padx=5,pady=5,sticky='w')
        self.delete_post_but.grid(row=1,column=1,padx=5,pady=5,sticky='w')
        self.post_date.grid(row=2,column=0,padx=5,pady=5,sticky='w')
        self.status.grid(row=2,column=1,padx=5,pady=5,sticky='e')
    def edit_post(self,title,author,date):
        global tab_index
        #print(title)
        self.central_notebook = v.get_notebook()
        desc = v.get_description(title,author)
        get_wallpaper(title,author)
        wallpaper_name = 'wallpaper.jpg'
        tab_list[f'{title}'] = tab_index + 1
        tab_index = tab_index + 1
        new_tab = New_Window(self.central_notebook,title,author,date,desc,wallpaper_name)    
    def delete_post(self,event):
        pass

class New_Window():
    def __init__(self,central_notebook,title,auth,date,desc,wall_name):
        self.book = central_notebook
        self.title = title
        self.auth = auth
        self.date = date
        self.desc = desc
        self.wall_photo = wall_name
        self.lastMod = v.get_lastdate(title,auth)
        self.f = Frame(self.book,width=1200,height=550,bg='#fff')
        self.title_head = Label(self.f,text=self.title,font=('Lucida Sans',24),bg='#4fd1c8',fg='#fff',width=80,height=2)
        self.content_frame = Frame(self.f,width=1050,height=610,bg='#fff')
        self.title_lbl = Label(self.content_frame,text='Title',font=('Lucida Sans',12),bg='#fff')
        self.t = tk.StringVar()
        self.t.set(self.title)
        self.title_entry = Entry(self.content_frame,textvariable=self.t,font=('Lucida Sans',12))
        self.desc_lbl = Label(self.content_frame,text='Description',font=('Lucida Sans',12),bg='#fff')
        self.desc_box = Text(self.content_frame, height=10, width=100) 
        self.desc_box.insert(END,self.desc)
        self.filename_upload = os.getcwd()+'//wallpaper.jpg'  
        self.upload_option = Label(self.content_frame,text='Upload Picture',font=('Lucida Sans',12,'underline'),bg='#fff',cursor='hand2',fg='#177aeb')
        self.upload_option.bind('<Button-1>',lambda x:self.upload_picture())
        
        new_filename = ImageTk.PhotoImage(Image.open(self.wall_photo).resize((150,120)))
        self.wallpaper_image = Label(self.content_frame,image=new_filename,bg='#fff')
        self.wallpaper_image.image = new_filename
                                     
        self.info_tab_frame = Frame(self.f,width=300,height=610,bg='#fff')
        self.info_notebook = ttk.Notebook(self.info_tab_frame,width=300,height=610)
        self.activity_frame = Frame(self.info_notebook,width=300,height=610,bg='#fff')
        pub_img = ImageTk.PhotoImage(Image.open('pub.png').resize((200,40))) 
        self.pub_but = Button(self.activity_frame,image=pub_img,relief=FLAT,bg='#fff')#,bg='#4fd1c8'),width=30,height=1)
        self.pub_but.image = pub_img
        self.pub_but.bind('<Button-1>',lambda x:self.publish_entry(auth,self.t.get(),self.date,self.desc_box.get(1.0,tk.END)))
        delete_img = ImageTk.PhotoImage(Image.open('delete.png').resize((200,40))) 
        self.del_but = Button(self.activity_frame,image=delete_img,relief=FLAT,bg='#fff')#,bg='#ba040a',width=30,height=1)
        self.del_but.image = delete_img
        close_img = ImageTk.PhotoImage(Image.open('close.png').resize((200,40))) 
        self.close_but = Button(self.activity_frame,image=close_img,relief=FLAT,bg='#fff')#,fg='#fff',bg='#32cf5b',width=30,height=1)
        self.close_but.image = close_img
        self.close_but.bind('<Button-1>',lambda x:self.close_tab(title))
        self.info_frame = Frame(self.info_notebook,width=300,height=610,bg='#fff')
        self.auth_lbl = Label(self.info_frame,text='Author: '+self.auth,bg='#fff')
        self.creat_dt = Label(self.info_frame,text='Created On: '+self.date,bg='#fff')
        self.last_dt = Label(self.info_frame,text='Last Modified: '+self.lastMod,bg='#fff')
                            
        self.display()
    def publish_entry(self,auth,title,date,desc):
        #print(desc)
        print('inside entry')
        new_image_upload = blog_space.uploads().create(self.filename_upload)
        print('after upload')
        ass = client.assets(space_id, 'master').create(
                    get_new_asset_id(),
                    {
                            'fields': {
                                    'file': {
                                            'en-US': {
                                                    'fileName': f'{v.get_user_name()}.png',
                                                    'contentType': 'image/jpg',
                                                    'uploadFrom': new_image_upload.to_link().to_json()
                                                    }
                                                }
                                            }
                                            }
                                            )
        ass.process()
        ass.publish()
        
        get_asset_entries()
        
        lastmod = datetime.today()
        lastmod = lastmod.strftime('%d-%m-%y')
        #print('till here')
        print('before entry')
        entry_attributes = {
                    'content_type_id': 'blogData',
                    'fields': {
                            'authorname': {
                                    'en-US': auth
                                    },
                            'posttitle': {
                                    'en-US': title
                                    },
                            'description': {
                                    'en-US': desc
                                    },
                            'createdOn': {
                                    'en-US': date
                                    },      
                            'lastModified': {
                                    'en-US': lastmod
                                    },      
                            'wallpaper': {
                                    'en-US': {
                                            'sys': {
                                                    'id': ass.sys['id'], #asset is of type Asset, created ealier
                                                    'linkType': 'Asset',
                                                    'type': 'Link',
                                                    }
                                            }
                                        },
                                    }
                                }
        #print('Create attributes')
        cur_blog_id = get_blog_data_entry_id(auth,title)
        #print('got ID')
        cur_entry = blogdata_content_type.entries().find(cur_blog_id)
        #print('Got Entry')
        cur_entry.update(entry_attributes)
        print('Entry uploaded')
        #print('Updated Entry')
        cur_entry.publish()
        if cur_entry.is_published:
            print('Blog has been updated')
        
    def close_tab(self,title):
        self.book.hide(tab_list[title])
        
    def upload_picture(self):
        self.filename_upload = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        new_filename = ImageTk.PhotoImage(Image.open(self.filename_upload).resize((150,120)))
        #self.wallpaper_image = Label(self.content_frame,image=new_filename,bg='#fff')
        #self.wallpaper_image = new_filename            
        #self.wallpaper.configure(image=new_filename)
        #self.wallpaper_image.grid(row=5,column=0,padx=10,pady=3,sticky='w')
        self.wallpaper_image.configure(image=new_filename)
        self.wallpaper_image.image = new_filename
    
    def display(self):    
        self.f.pack(fill='both',expand=1)            
        self.book.add(self.f,text=self.title)
        self.book.select(tab_list[self.title])
        
        self.title_head.pack(side='top',pady=(0,10),anchor='nw')
        self.content_frame.pack(side='left',anchor='nw')                
        self.title_lbl.grid(row=0,column=0,padx=10,pady=3,sticky='w')
        self.title_entry.grid(row=1,column=0,padx=10,pady=3,ipadx=5,ipady=10,sticky='w')
        self.desc_lbl.grid(row=2,column=0,padx=10,pady=3,sticky='w')
        self.desc_box.grid(row=3,column=0,padx=10,pady=3,sticky='w')
        self.upload_option.grid(row=4,column=0,padx=10,pady=3,sticky='w')
        self.wallpaper_image.grid(row=5,column=0,padx=10,pady=3,sticky='w')
        
        self.info_tab_frame.pack(side='left',anchor='e',padx=(200,0))
        self.info_notebook.pack(anchor='e')
        self.activity_frame.pack()
        self.info_notebook.add(self.activity_frame,text='Activity')
        self.pub_but.pack(side='top',padx=20,pady=(10,2),anchor='w')
        self.del_but.pack(side='top',padx=20,pady=2,anchor='w')
        self.close_but.pack(side='top',padx=20,pady=2,anchor='w')
        
        self.info_frame.pack(fill='both',expand=1)
        self.info_notebook.add(self.info_frame,text='Genral Info')
        self.auth_lbl.pack(side='top',padx=20,pady=10,anchor='w')
        self.creat_dt.pack(side='top',padx=20,pady=10,anchor='w')
        self.last_dt.pack(side='top',padx=20,pady=10,anchor='w')
#        