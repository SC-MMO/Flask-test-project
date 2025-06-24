from mongoengine import Document, StringField, DateTimeField, ReferenceField, EmailField, DictField, FileField, CASCADE
from datetime import datetime

class Image(Document):
    name = StringField(required=True)
    image_file = FileField(required=True)

class Role(Document):
    name = StringField(required=True)
    permissions = DictField(required=True)

class SiteUser(Document):
    name = StringField(required=True, max_length=100)
    address = EmailField()
    password = StringField(required=True)
    role = ReferenceField(Role, required=True, reverse_delete_rule=CASCADE)
    profile_pic = ReferenceField(Image, required=True, delete_rule=CASCADE)

class Post(Document):
    title = StringField(required=True, max_length=200)
    body = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    author = ReferenceField(SiteUser, required=True, reverse_delete_rule=CASCADE)