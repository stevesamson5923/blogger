#https://app.contentful.com/spaces/ma8yestsieel/entries/3HVaJns38bklqrpiJhVsEN
#https://www.contentful.com/developers/docs/python/sdks/
#https://www.contentful.com/developers/docs/python/tutorials/getting-started-with-contentful-and-python/

#TUTORIAL
#https://github.com/contentful/contentful-management.py
# OR
#https://contentful.github.io/contentful-management.py/

#pip install contentful_management
#pip install contentful

#Code for accessing content delivery API

import contentful


client = contentful.Client('ma8yestsieel', 'wZlWVFpPoaOfi244sP0IGERYKa4ZLZ6X2qdUmChiiks')


#FIRST WAY
entries = client.entries()

#for entry in entries:
#    print(entry)

entry_id = '3HVaJns38bklqrpiJhVsEN'
firstpost = client.entry(entry_id)

print(firstpost.title)
print(firstpost.subtitle)
print(firstpost.image)

#SECOND WAY
post_by_title = client.entries({'content_type': 'post', 'order': 'fields.title'})
for entry in post_by_title :
	print(entry.title)

#TO get assets
assets = client.assets()

for asset in assets:
	print(asset.url())
