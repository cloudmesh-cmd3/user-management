from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_management.cloudmeshobject import CloudmeshObject
from mongoengine import *



class User(CloudmeshObject):
    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}

    """
    Hidden Fields
    """
    status = StringField(required=True, default='pending')
    userid = UUIDField()
    
    """
    User Fields
    """
    username = StringField(required=True)
    email = EmailField(required=True)
    password = StringField()
    confirm = StringField()
    title = StringField(required=True)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    phone = StringField(required=True)
    url = StringField(required=True)
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    institution = StringField(required=True)
    institutionrole = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    advisor = StringField(required=True)
    country = StringField(required=True)
    projects = ListField(ReferenceField('Project'))