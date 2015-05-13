from cloudmesh_database.dbconn import get_mongo_db, DBConnFactory
from cloudmesh_management.user import User
from cloudmesh_base.util import HEADING
from cloudmesh_database.dbconn import get_mongo_dbname_from_collection

from cloudmesh_management.user import Users


class TestAddUserFromFile:
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


    def test_adduserfromfile(self):
        HEADING()
        """
        Test to add user from file
        """
        user = Users()
        print "User count before addition: ", User.objects().count()
        file_path = "etc/cloudmesh_user_info.yaml"
        user.create_user_from_file(file_path)
        print "User count after addition: ", User.objects().count()



