#https://www.contentfulcommunity.com/t/api-upload-images/975/9
#https://app.contentful.com/
#https://contentful.github.io/contentful-management.py/
import contentful_management
import json

management_api = "CFPAT-ilH5jr5ioiOuNvh1Ior2QjEs4_mIP7Q3B1DpEcsD1K8"

client = contentful_management.Client(management_api)

#ORGANIZATION : talpuri

#Retrieving all spaces:
#spaces = client.spaces().all()
#print(spaces)

#Retrieveing one space by ID:

space_id = 'ma8yestsieel'

blog_space = client.spaces().find(space_id)
print(blog_space)

#Deleting a space:
'''client.spaces().delete('blog_space_id')

# or if you already fetched the space

blog_space.delete()
'''

'''
#Creating a new space:
new_blog_space = client.spaces().create({'name': 'My Blog 2', 'default_locale': 'en-US'})
# default_locale is optional

#In the case your user belongs to multiple organizations, you’re required to send an organization ID:
new_blog_space = client.spaces().create({'name': 'My Blog', 'organization_id': 'my_org_id'})

#ORGANIZATION : talpuri
'''

#Updating a space:
#blog_space.update({'name': 'The new space'})

# or directly editing it's properties

#blog_space.name = 'Ye Olde Blog'
#blog_space.save()

#blog_space = client.spaces().find(space_id)
#print(blog_space)

#Space Memberships : Retrieving all memberships on a space:
#memberships = client.memberships(space_id).all()
#print(memberships)
# or if you already have a fetched space

#memberships = blog_space.memberships().all()


#Retrieveing one membership by ID:
'''membership = client.memberships('my_space_id').find('membership_id')

# or if you already have a fetched space

membership = blog_space.memberships().find('membership_id')
''' 

#Deleting an membership:
'''client.memberships('my_space_id').delete('membership_id')

# or if you already have a fetched space

space.memberships().delete('membership_id')

# or if you already have fetched the membership

memberships.delete()
'''


#Retrieving all Organizations you belong to:
#organizations = client.organizations().all()

#print(organizations)

#Retrieving your User information:
user = client.users().me()
print(user)

#Environments
#For all resources that depend on an environment but don’t have environments explicitly enabled. You should use 'master' as environment_id.

#Retrieving all environments on a space:
#environments = client.environments(space_id).all()

# or if you already have a fetched space

#environments = blog_space.environments().all()
#for env in environments:
#    print(env)

#Assets
#Retrieving all assets on a space:

'''
assets = client.assets(space_id, 'master').all()

for asset in assets:
	print(asset.url())
# or if you already have a fetched environment
'''

#Retrieving asset id
environment = blog_space.environments().find('master')

#environment.assets().delete('553456')
'''
assets = environment.assets().all()
for a in assets:
    #print(a.id)
    if a.id == '5554456':
        #a.publish()
        print('see',a.is_published)
''' 

'''
#Retrieving a specific asset info
environment = blog_space.environments().find('master')
asset_id = '68V77LU6Fxks3IlqehHHIy'

asset = environment.assets().find(asset_id)
print(asset.url())
'''

''' 
#Deleting an asset:
client.assets('my_space_id', 'environment_id').delete('asset_id')

# or if you already have a fetched environment

environment.assets().delete('asset_id')

# or if you already fetched the asset

asset.delete()
'''

'''
file_attributes = {
    'fields': {
        'file': {
            'en-US': {
                'fileName': '05-03.jpg' ,
                'contentType': 'Post',
                'upload': 'https://url.to/05-03.jpg',
            }
        }
    }
}
environment = blog_space.environments().find('master')
new_asset = environment.assets().create(
    'new_asset_id',
    file_attributes
)
#new_asset.process()
new_asset.publish()
'''

''' 
asset.update(other_file_attributes)

# or directly editing it's properties

asset.file['file_name'] = 'other_file.png'
asset.save()
''' 

#Archiving and Unarchiving an asset:

#asset.archive()
#asset.unarchive()

#Publishing or Unpublishing an asset:

#asset.publish()
#asset.unpublish()

#Checking if an asset is published:
#asset.is_published

#Checking if an asset is updated:
#asset.is_updated

#retrieving  all entries
#entries = client.entries(space_id, environment).all()
#for e in entries:
#    print(e)
# or if you already have a fetched environment

#entries = environment.entries().all()
#for e in entries:
#    print(e.title)
# or if you already have a fetched content type

#entries_for_content_type = content_type.entries().all()
    
#get all id of entries
#entries = client.entries(space_id, 'master').all()
#for e in entries:
#    print(e.id)
    
#Retrieving an entry by ID:
'''
#entry = client.entries('my_space_id', 'environment_id').find('entry_id')
entry = environment.entries().find('3HVaJns38bklqrpiJhVsEN')
print(entry.title)
print(entry.subtitle)
print(entry.author)
#print(entry.content)
#print(entry.image.id)
asset = environment.assets().find(entry.image.id)
print(asset.url())
'''


'''
Deleting an entry

client.entries('my_space_id', 'environment_id').delete('entry_id')

# or if you already have a fetched environment

environment.entries().delete('entry_id')

# or if you already fetched the entry

entry.delete()
'''

'''
#Creating an entry:

entry_attributes = {
    'content_type_id': 'post',
    'fields': {
        'title': {
            'en-US': 'Python tkinter and contentful'
        },
        'subtitle': {
            'en-US': 'Develop app using above technologies and sell it online'
        },
        'author': {
            'en-US': 'Von Russom'
        },
        'content': {
            'en-US': 'GUI based app to manage content to sell tickets or books or can also be used in banks'
        }        
    }
}

new_entry = environment.entries().create(
    '22113344',
    entry_attributes
)

new_entry.publish()
'''

'''
#Updating and entry
entry_attributes = {
    'content_type_id': 'post',
    'fields': {
        'title': {
            'en-US': 'Python tkinter and contentful'
        },
        'subtitle': {
            'en-US': 'Develop app using above technologies and sell it online'
        },
        'author': {
            'en-US': 'Von Russom'
        },
        'content': {
            'en-US': 'GUI based app to manage content to sell tickets or books or can also be used in banks'
        }        
    }
}
'''

'''
#updating asset through entry
entry = environment.entries().find('3HVaJns38bklqrpiJhVsEN')  #given entry id
#entry.update(entry_attributes)

asset = environment.assets().find(entry.image.id)
#print(dir(entry.image))
#print(dir(asset))# = 'other_file.png'
print(asset.is_published)
d = asset.fields()
print(d)
print(d['title'])
d2 = d['file']
#for k in d2.keys():
#    print(k)
#    print(d2.get(k))
#asset.file['fileName'] = 'other_file.png'
#asset.save()

#print(d2['filename'])

#print(asset.url())

#entry.title = 'My Super Post'
#entry.author= 'Spyder steve'
#entry.save()
#entry.publish()


# or directly updating it's properties

#entry.title = 'My Super Post'
#entry.save()
'''

'''
NOT WORKING
print('new test')
entry_attributes = {
    'content_type_id': 'post',
    'fields': {
        'title': {
            'en-US': 'My Fourth Post'
        },
        'subtitle': {
            'en-US': 'Third post to check if creating entry working or not'
        },
        'author':{
             'en-US': 'Spyde python'           
        },
        'slug':{
             'en-US': 'third-post'           
        },
        'content':{
             'en-US':'In the document model of MongoDB Atlas, data becomes like code in the form of JSON '       
        }
    }
}
        
#attr_json = json.dumps(entry_attributes)

new_entry = client.entries(space_id, 'master').create(
    'fourth-post-id',
    attr_json
)
new_entry.publish()
print(new_entry.is_published)
''' 

#WORKING successfully created new entry
#entry_attributes = {
#    'content_type_id': 'simplepost',
#    'fields': {
#        'title': {
#            'en-US': 'My second Post'
#        },
#    }
#}
#
#
#new_entry = client.entries(space_id, 'master').create(
#    'sec-post-id',
#    entry_attributes
#)
#new_entry.publish()

#Try to update the recent entry
#entry = client.entries(space_id, 'master').find('sec-post-id')

#update_entry_attributes = {
#    'content_type_id': 'simplepost',
#    'fields': {
#        'title': {
#            'en-US': entry.title
#        },
#        'quantity': {
#            'en-US': 4
#        }
#    }
#}
#entry.update(update_entry_attributes)
#entry.publish()

#OR ANOTHER WAY to update is 
#entry = client.entries(space_id, 'master').find('3rTRC3NhYvHdEEse4GLtOb')
#entry.quantity = 6
#entry.title = 'Changed Post'
#entry.save()
#entry.publish()

'''
# WORKING HOW TO UPLOAD IMAGE AS AN ENTRY
new_upload = blog_space.uploads().create('03-05.jpg')
ass = client.assets(space_id, 'master').create(
   'asset_steve_img_id',
   {
     'fields': {
       'file': {
         'en-US': {
           'fileName': 'cauliflower.png',
           'contentType': 'image/png',
           'uploadFrom': new_upload.to_link().to_json()
         }
       }
     }
   }
 )
ass.process()
ass.publish()


entry_attributes = {
    'content_type_id': 'imagepost',
    'fields': {
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
new_entry = client.entries(space_id, 'master').create(
    'first-image-id',
    entry_attributes
)
new_entry.publish()
'''
