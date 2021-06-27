import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox, Scrollbar,Canvas
from tkinter import Menu, filedialog
from PIL import ImageTk, Image
import contentful_management
import random
#import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
import random
import threading
import time
import webbrowser
import urllib.request
import create_new_post as cnp
import values as v
import os

# setting up the tkinter window
root = tk.Tk()
width = 1350
height = 680
root.geometry(f"{width}x{height}+0+0")
root.resizable(0,0)
root.title("Library Management System")

text_color = '#54def0'

management_api = "CFPAT-ilH5jr5ioiOuNvh1Ior2QjEs4_mIP7Q3B1DpEcsD1K8"
client = contentful_management.Client(management_api)
space_id = 'ma8yestsieel'
blog_space = client.spaces().find(space_id)
#print(blog_space)
login_content_type = None
login_entries = None
asset_entries = None

def login_content_api_call():
    global login_content_type,login_entries,asset_entries
    login_content_type = client.content_types(space_id, 'master').find('blogLogin')
    login_entries = login_content_type.entries().all()

def fetch_entries():
    global login_content_type,login_entries
    login_entries = login_content_type.entries().all()

def get_asset_entries():
    global asset_entries
    asset_entries = client.assets(space_id, 'master').all()

login_content_api_call()
get_asset_entries()

main_menu_font = font.Font(family='Times New Roman', size=10, weight='bold')

menubar = Menu(root)  
file = Menu(menubar, tearoff=0)  
file.add_command(label="New")  
file.add_command(label="Open")  
file.add_command(label="Save")  
file.add_command(label="Save as...")  
file.add_command(label="Close")  
  
file.add_separator()  

file.add_command(label="Exit", command=root.destroy)  
  
menubar.add_cascade(label="File", menu=file) 

edit = Menu(menubar, tearoff=0)  
edit.add_command(label="Undo")  
edit.add_separator()    
edit.add_command(label="Cut")  
edit.add_command(label="Copy")  
edit.add_command(label="Paste")  
edit.add_command(label="Delete")  
edit.add_command(label="Select All")  
menubar.add_cascade(label="Edit", menu=edit)  

root.config(menu=menubar)  

def download_user_image(URL):
    URL = "https:" + URL
    with urllib.request.urlopen(URL) as url:
        with open('profile_photo.jpg', 'wb') as f:
            f.write(url.read())

log = None
reg = None
real_password=''
real_confirm_pass=''
username_available = False

def get_new_asset_id():
    new_id = random.randint(300000,400000)
    already_present = False
    for a in asset_entries:
        if a.id == new_id:
            already_present = True
            break
    if already_present:
        get_new_asset_id()
    else:
        return new_id


def register_screen():
    global log,reg
    if log != None:
        log.destroy()
        log=None
        
    reg = tk.Toplevel(root,bg='#fff') 
    #log.wm_attributes('-fullscreen', 'true')
    reg.overrideredirect(True)
    #log.wm_attributes('-fullscreen', 'true')
    # sets the title of the 
    # Toplevel widget 
    reg.title("New Window") 
    
    def check_username_available_or_not(user_name):
        global login_entries
        if len(user_name) > 1:
            pass
        else:
            login_content_api_call()
        #print(user_name)
        for l in login_entries:
            if l.loginname == user_name:
                username_avail_msg.configure(text='Sorry this username is already taken',fg='#ba040a')
                return False
        username_avail_msg.configure(text='This username is available',fg='#64fa2d')
        return True

    def empty_box(event):
        #print(event.widget)
        if event.widget.get() == 'Please enter password':
            password.delete(0,END)
        elif event.widget.get() == 'Please enter username':
            username.delete(0,END)
        elif event.widget.get() == 'Please enter password again':
            password2.delete(0,END)
        else:
            pass
    def fill_user_box(event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Please enter username')
    
    def fill_pass_box(event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Please enter password')
            
    def fill_pass2_box(event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Please enter password again')
    def check_username_availability(event):
        #print('Hello '+a)
        global username_available
        #event.widget.config(fg='#000')
        username.configure(fg='#000')
        user_name = event.widget.get()
        #user_name = username.get()
        #user_name = a
        username_available = check_username_available_or_not(user_name)
                             
    def change_text_color(event):
        global real_password
        if (event.keycode>=97 and event.keycode<=122) or (event.keycode>=65 and event.keycode<=90) or (event.keycode>=48 and event.keycode<=57):
            event.widget.configure(fg='#000')
            real_password = real_password+event.keysym#event.widget.get()
            event.widget.delete(0,END)
            event.widget.insert(0,'*'*len(real_password))
        elif event.keycode == 8:
            real_password = real_password[0:len(real_password)-1]
        
    def change_text_color2(event):
        #if event.widget.get() == 'Please enter password again':        
        global real_confirm_pass
        if (event.keycode>=97 and event.keycode<=122) or (event.keycode>=65 and event.keycode<=90) or (event.keycode>=48 and event.keycode<=57):            
            event.widget.configure(fg='#000')
            real_confirm_pass = real_confirm_pass+event.keysym#event.widget.get()
            event.widget.delete(0,END)
            event.widget.insert(0,'*'*len(real_confirm_pass))
            if real_password != real_confirm_pass:
                message.configure(text='Passwords donot match')
            else:
                message.configure(text='')
        elif event.keycode == 8:
            real_confirm_pass = real_confirm_pass[0:len(real_confirm_pass)-1]
            if real_password != real_confirm_pass:
                message.configure(text='Passwords donot match')
            else:
                message.configure(text='')
        
        
    def get_entry_id():
        new_id = random.randint(100000,200000)
        already_present = False
        for l in login_entries:
            if l.id == new_id:
                already_present = True
                break
        if already_present:
            get_entry_id()
        else:
            return new_id
    
    def register_user():
        global real_confirm_pass,real_password
        u = username.get()
        p = real_password
        cp = real_confirm_pass
        print(p)
        if username_available:
            if p == cp:
                message.configure(text='')
                #login_content_api_call() #fetched all entries from
                                
                new_image_upload = blog_space.uploads().create('addphoto.png')
                ass = client.assets(space_id, 'master').create(
                        get_new_asset_id(),
                        {
                            'fields': {
                                    'file': {
                                            'en-US': {
                                                    'fileName': f'{u}.png',
                                                    'contentType': 'image/png',
                                                    'uploadFrom': new_image_upload.to_link().to_json()
                                                    }
                                                }
                                            }
                                        }
                                    )
                ass.process()
                ass.publish()
            
                #update local asset id list
                get_asset_entries()
                #entry_of_cur_user = login_content_type.entries().find(USERS_ENTRY_ID)
                entry_attributes = {
                    'content_type_id': 'blogLogin',
                    'fields': {
                            'loginname': {
                                    'en-US': u
                                    },
                            'password': {
                                    'en-US': p
                                    },
                            'confirmpass': {
                                    'en-US': cp
                                    },
                            'profilephoto': {
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
            
                #entry_of_cur_user.update(entry_attributes)
                #entry_of_cur_user.publish()

#                entry_attributes = {
#                        'content_type_id': 'blogLogin',
#                        'fields': {
#                                'loginname': {
#                                        'en-US': u
#                                        },
#                                'password':{
#                                        'en-US': p
#                                        },
#                                'confirmpass':{
#                                        'en-US':cp
#                                        },
#                                        }
#                                }
 
                new_entry = client.entries(space_id, 'master').create(
                        get_entry_id(),
                        entry_attributes
                        )
                new_entry.publish()
                fetch_entries()
                login()
            else:
                message.configure(text='Passwords donot match')
        else:
            return
            
    # sets the geometry of toplevel 
    reg.geometry("220x300+600+300") 
    Label(reg,text='Create account to get started',bg='#fff',fg=text_color,font=('Times New Roman',12,'bold')).pack(side='top',pady=10)
    
    username_avail_msg = Label(reg,text='',fg='#ba040a',bg='#fff',font=('Times New Roman',8,'bold'))   
    username_avail_msg.pack(side='top')
          
    a = tk.StringVar()
    a.set('Please enter username')
    username = Entry(reg,fg='#d7d9d2',textvariable=a,font=('Calibri Light',10,'bold'))
    username.bind('<FocusIn>',empty_box)
    username.bind('<FocusOut>',fill_user_box)
    username.bind('<KeyRelease>',check_username_availability)
    username.pack(side='top',pady=20,ipadx=10,ipady=5)
        
    b = tk.StringVar()
    b.set('Please enter password')
    password = Entry(reg,textvariable=b,fg='#d7d9d2',font=('Calibri Light',10,'bold'))
    password.bind('<FocusIn>',empty_box)
    password.bind('<FocusOut>',fill_pass_box)
    password.bind('<KeyRelease>',change_text_color)
    password.pack(side='top',pady=10,ipadx=10,ipady=5) 
    
    c = tk.StringVar()
    c.set('Please enter password again')
    password2 = Entry(reg,textvariable=c,fg='#d7d9d2',font=('Calibri Light',10,'bold'))
    password2.bind('<FocusIn>',empty_box)
    password2.bind('<FocusOut>',fill_pass2_box)
    password2.bind('<KeyRelease>',change_text_color2)
    password2.pack(side='top',pady=10,ipadx=10,ipady=5) 
    
    new_reg_img = ImageTk.PhotoImage(Image.open('register2.png').resize((75,30))) 
    new_reg_but = Button(reg,image=new_reg_img,relief=FLAT,bd=0,command=register_user)
    new_reg_but.image = new_reg_img
    new_reg_but.pack(side='top') 

    message = Label(reg,text='',fg='#ba040a',bg='#fff',font=('Times New Roman',8,'bold'))                  
    message.pack(side='top',pady=5)  
    #reg.mainloop() 

login_user_pass = ''   
USER_NAME = 'Guest'    
USERS_ENTRY_ID = ''

def login():
    global log,reg#,USER_NAME
    if reg != None:
        reg.destroy()
        reg = None
        
    log = tk.Toplevel(root,bg='#fff') 
    #log.wm_attributes('-fullscreen', 'true')
    log.overrideredirect(True)
    #log.wm_attributes('-fullscreen', 'true')
    # sets the title of the 
    # Toplevel widget 
    log.title("New Window") 
  
    # sets the geometry of toplevel 
    log.geometry("220x280+600+300") 
    #log.focus_force()
    Label(log,text='Enter your login credentials',bg='#fff',fg=text_color,font=('Times New Roman',12,'bold')).pack(side='top',pady=10)
        
    def empty_box(event):
        #print(event.widget)
        if event.widget.get() == 'Please enter password':
            password.delete(0,END)
        elif event.widget.get() == 'Please enter username':
            username.delete(0,END)
        else:
            pass
    def fill_user_box(event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Please enter username')
    
    def fill_pass_box(event):
        e = event.widget
        if e.get() == '':
            e.insert(0,'Please enter password')
    
    def change_text_color(event):
        event.widget.configure(fg='#000')        
    
    def change_text_color2(event):
        #event.widget.configure(fg='#000')  
        global login_user_pass
        if (event.keycode>=97 and event.keycode<=122) or (event.keycode>=65 and event.keycode<=90) or (event.keycode>=48 and event.keycode<=57):
            event.widget.configure(fg='#000')
            login_user_pass = login_user_pass+event.keysym#event.widget.get()
            event.widget.delete(0,END)
            event.widget.insert(0,'*'*len(login_user_pass))
        elif event.keycode == 8:
            login_user_pass = login_user_pass[0:len(login_user_pass)-1]
    
    def log_into_blog():
        global login_user_pass
        global login_entries, USER_NAME,USERS_ENTRY_ID
        u = username.get()
        #p = password.get()
        #print(u,login_user_pass)
        if login_entries is None:
            #print('call api')
            login_content_api_call()
        for l in login_entries:
            #print('inside for', l.loginname)
            if l.loginname == u:
                if l.password == login_user_pass:
                    message.configure(text='Welcome '+u,fg='#64fa2d')
                    log.after(1000,log.destroy)
                    logout_img = ImageTk.PhotoImage(Image.open('logout.png').resize((75,30))) 
                    login_but.configure(text='Logout',image=logout_img)
                    login_but.image = logout_img
                    v.change_user_name(u)
                    #print('Login: ',v.USER_NAME)
                    USERS_ENTRY_ID = l.id
                    v.get_blog_data(l.loginname,client)
                    return
                else:
                    message.configure(text='Incorrect Password',fg='#ba040a')
                    return
        else:
            message.configure(text='Sorry no account with this name',fg='#ba040a')
            return
    
    a = tk.StringVar()
    a.set('Please enter username')
    username = Entry(log,fg='#d7d9d2',textvariable=a,font=('Calibri Light',10,'bold'))
    username.bind('<FocusIn>',empty_box)
    username.bind('<FocusOut>',fill_user_box)
    username.bind('<Key>',change_text_color)
    username.pack(side='top',pady=20,ipadx=10,ipady=5)
        
    b = tk.StringVar()
    b.set('Please enter password')
    password = Entry(log,textvariable=b,fg='#d7d9d2',font=('Calibri Light',10,'bold'))
    password.bind('<FocusIn>',empty_box)
    password.bind('<FocusOut>',fill_pass_box)
    password.bind('<KeyRelease>',change_text_color2)
    password.pack(side='top',pady=10,ipadx=10,ipady=5) 

    login_img = ImageTk.PhotoImage(Image.open('login_button.png').resize((75,30))) 
    log_but = Button(log,text='login',image=login_img,command=log_into_blog,relief=FLAT,bd=0)
    log_but.image = login_img
    log_but.pack(side='top',pady=10) 
    
    new_acc_img = ImageTk.PhotoImage(Image.open('new account.png').resize((150,30))) 
    new_acc_but = Button(log,image=new_acc_img,relief=FLAT,bd=0,command=register_screen)
    new_acc_but.image = new_acc_img
    new_acc_but.pack(side='top') 

    message = Label(log,text='',fg='#ba040a',bg='#fff',font=('Times New Roman',8,'bold'))                  
    message.pack(side='top',pady=5)  

    #log.mainloop()       
ham = None     
close_but = None  

            
def window_open():
    global ham,close_but
    def ham_window():
        global USER_NAME,USERS_ENTRY_ID,login_content_type
        #print('open window')
        ham = tk.Toplevel(root,bg='#fff') 
        #log.wm_attributes('-fullscreen', 'true')
        ham.overrideredirect(True)
        ham.attributes('-topmost', True)
        #log.wm_attributes('-fullscreen', 'true')
        d=-200
        for i in range(210):        
            ham.geometry(f"200x670+{d}+50") 
            d=d+1
            time.sleep(0.001)
        def window_close():
            def close_slide_window():
                d=0
                for i in range(210):        
                    ham.geometry(f"200x670+{d}+50") 
                    d=d-1
                    time.sleep(0.001)
                ham.destroy()
            x2 = threading.Thread(target=close_slide_window).start()
        def change_img():
            #url = 'https://www.google.com'
            #webbrowser.open_new(url)
            global asset_entries
            def get_new_asset_id():
                new_id = random.randint(300000,400000)
                already_present = False
                for a in asset_entries:
                    if a.id == new_id:
                        already_present = True
                        break
                if already_present:
                    get_new_asset_id()
                else:
                    return new_id
                
            filename_upload = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
            new_filename = ImageTk.PhotoImage(Image.open(filename_upload).resize((110,90)))
            profile_lbl.image = new_filename            
            profile_lbl.configure(image=new_filename)
            
            new_image_upload = blog_space.uploads().create(filename_upload)
            ass = client.assets(space_id, 'master').create(
                    get_new_asset_id(),
                    {
                            'fields': {
                                    'file': {
                                            'en-US': {
                                                    'fileName': f'{v.get_user_name()}.png',
                                                    'contentType': 'image/png',
                                                    'uploadFrom': new_image_upload.to_link().to_json()
                                                    }
                                                }
                                            }
                                            }
                                            )
            ass.process()
            ass.publish()
            
            #update local asset id list
            get_asset_entries()
            entry_of_cur_user = login_content_type.entries().find(USERS_ENTRY_ID)
            entry_attributes = {
                    'content_type_id': 'blogLogin',
                    'fields': {
                            'loginname': {
                                    'en-US': entry_of_cur_user.loginname
                                    },
                            'password': {
                                    'en-US': entry_of_cur_user.password
                                    },
                            'confirmpass': {
                                    'en-US': entry_of_cur_user.confirmpass
                                    },
                            'profilephoto': {
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
            
            entry_of_cur_user.update(entry_attributes)
            entry_of_cur_user.publish()
            if entry_of_cur_user.is_updated:
                print('Updated')
                   
            
        slide_frame = Frame(ham,bg='#35c9cc',width=200,height=670)
        slide_frame.pack_propagate(0)
        slide_frame.pack()                    
        close_but = Button(slide_frame,text='x',fg='#fff',bg='#35c9cc',cursor='hand2',font=('Calibri',16,'bold'),relief=FLAT,command=window_close)
        close_but.pack(side='top',anchor='ne')
        
        #UPDATING PROFILE PHOTO OF CURRENT USER
        #print(USERS_ENTRY_ID)
        cur_entry = login_content_type.entries().find(USERS_ENTRY_ID)
        profile_image_asset = cur_entry.profilephoto.id
        #download_user_image(asset.url())
        asset = client.assets(space_id, 'master').find(profile_image_asset)
        download_user_image(asset.url())
        p = 'profile_photo.jpg'

        profile_img = ImageTk.PhotoImage(Image.open(p).resize((110,90))) 
        profile_lbl = Label(slide_frame,image=profile_img,relief=FLAT,bd=0,bg='#35c9cc',cursor='hand2')
        profile_lbl.image = profile_img
        profile_lbl.bind('<Button-1>',lambda x:change_img())
        profile_lbl.pack(side='top')
        
        #changing first letter to uppercase
        a = list(v.get_user_name())
        user_local =''
        a[0] = a[0].upper()
        for x in a:
            user_local = user_local + x
        v.change_user_name(user_local)
        
        profile_name = Label(slide_frame,text='Welcome '+v.get_user_name(),bg='#35c9cc',font=('Candara Light',18),fg='#fff')
        profile_name.pack(side='top')
    x1 = threading.Thread(target=ham_window).start()

    #cnp.update_api(newpost.post_list[0].author,newpost.post_list[0].title)

#def update_post_api():
#    while True:
#        if newpost.post_added_flag:
#            cnp.update_api(USER_NAME,newpost.pst)
#            newpost.post_added_flag = False
#            print(newpost.post_added_flag)
#        else:
#            pass

  
login_frame =Frame(root,bg='#fff',width=1350,height=50)
login_frame.pack_propagate(0)
login_frame.pack()


v.set_notebook(root)
central_note = v.get_notebook()

main_frame1 = Frame(central_note,width=1350,height=610,bg='#fff')
#main_frame2 = Frame(central_note,width=1350,height=610,bg='#fff')

main_frame1.pack(fill='both',expand=1)
#main_frame2.pack(fill='both',expand=1)

central_note.add(main_frame1,text='Home Page')
#central_note.add(main_frame2,text='red tab')

#create_new_post_frame(main_frame1,USER_NAME)
def post_load():
    while True:
        #print('initial load is ?')
        if v.initial_data_loaded:
            print('initial load is true')
            newpost = cnp.NewPostFrame(main_frame1,0,0)
            v.initial_data_loaded = False
            break

post_thread = threading.Thread(target = post_load).start()

#post_api_update = threading.Thread(target=update_post_api)
#post_api_update.start()

#ham_thread = threading.Thread(target=window_open)
hamburger_img = ImageTk.PhotoImage(Image.open('hamburger.png').resize((24,24)))
hamburger_but = Button(login_frame,image=hamburger_img,
                   bg='#fff',relief=FLAT,cursor='hand2',command=window_open)
hamburger_but.pack(side='left',padx=10)

register_img = ImageTk.PhotoImage(Image.open('register.png').resize((75,30))) 
register_but = Button(login_frame,image=register_img,font=('Indie Flower',12,'bold'),
                  bg='#fff',relief=FLAT,cursor='hand2',command=register_screen)
register_but.pack(side='right',padx=10)

login_img = ImageTk.PhotoImage(Image.open('login2.png').resize((75,30))) 
login_but = Button(login_frame,image=login_img,font=('Indie Flower',12,'bold'),
                  bg='#fff',relief=FLAT,cursor='hand2',command=login)
login_but.pack(side='right',padx=5)

root.mainloop()