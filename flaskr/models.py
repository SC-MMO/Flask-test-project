from mongoengine import Document, StringField, DateTimeField, ReferenceField, EmailField
from datetime import datetime

class SiteUser(Document):
    name = StringField(required=True, max_length=100)
    address = EmailField()
    password = StringField(required=True)

    

class Post(Document):
    title = StringField(required=True, max_length=200)
    body = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())
    author = ReferenceField(SiteUser, required=True)
    username = StringField()

















    # meta = {
    #     'ordering': ['-created_at'],  # newest blogs first
    #     'indexes': ['author', 'created_at'],
    # }