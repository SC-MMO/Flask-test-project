from mongoengine import Document, StringField

class Peasant(Document):
    name = StringField(required=True)
    address = StringField()
    password = StringField(required=True)

class KingKong(Document):
    name = StringField(required=True)
    address = StringField()
    password = StringField(required=True)