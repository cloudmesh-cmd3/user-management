from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_management.cloudmeshobject import CloudmeshObject
from mongoengine import *


class Committee(CloudmeshObject):
    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}

    reviewers = ListField(ReferenceField('User'))
    reviews = ListField(StringField())