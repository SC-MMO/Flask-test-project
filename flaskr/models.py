from mongoengine import Document, StringField

class SiteUser(Document):
    name = StringField(required=True)
    address = StringField()
    password = StringField(required=True)