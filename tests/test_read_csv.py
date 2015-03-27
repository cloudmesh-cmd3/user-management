import csv
import sys

from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING


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

        f = open('users.csv', 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                print row
        finally:
            f.close()



