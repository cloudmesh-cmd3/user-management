from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.user import Users


class TestListUsers:
    yaml_dir = "~/.cloudmesh_yaml"

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


    def test_listusers(self):
        HEADING()

        """
        Test to list users in default format followed by JSON format
        """

        user = Users()
        print "Listing users in default format"
        user.list_users()
        print "Listing users in JSON format"
        user.list_users(display_fmt='json')



