from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.user import Users


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

        user = Users()
        display_fmt='json'
        user_name = 'gregg'
        user.list_users(disp_fmt='json', username=user_name)



