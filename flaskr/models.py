from mongoengine import Document, StringField, DateTimeField, ReferenceField, EmailField, DictField, CASCADE
from datetime import datetime

class SiteUser(Document):
    name = StringField(required=True, max_length=100)
    address = EmailField()
    password = StringField(required=True)
    role = ReferenceField(required=True, reverse_delete_rule=CASCADE)
    permissions = DictField(required=True)

class Post(Document):
    title = StringField(required=True, max_length=200)
    body = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())
    author = ReferenceField(SiteUser, required=True, reverse_delete_rule=CASCADE)

class Role(Document):
    name = StringField(required=True)
    permissions = DictField(required=True)