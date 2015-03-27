from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.project import Projects


from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_base.locations import config_file
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cmd3.console import Console
from cloudmesh_management.base_classes import SubUser, Project
from passlib.hash import sha256_crypt
import yaml
import json
import sys
from texttable import Texttable

class TestGenerate:

    yaml_dir = "~/.cloudmesh_yaml"
    firstname="gergor"

    def setup(self):
        # HEADING()
        db_name = get_mongo_dbname_from_collection("manage")
        if db_name:
            meta = {'db_alias': db_name}
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        pass
    
    def teardown(self):
        # HEADING()
        pass


    def test_generate(self):
        HEADING()

        project = Projects()
        file_path = "etc/cloudmesh_project_info.yaml"
        project.create_project_from_file(file_path)



