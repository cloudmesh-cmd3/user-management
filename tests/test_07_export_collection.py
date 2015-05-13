from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING

from cloudmesh_management.generate import generate_users
from cloudmesh_management.generate import generate_projects
from cloudmesh_management.dbutil import DBUtil


class TestExportCollection:
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

    def _xyz(self):
        print("hallo")

    def test_exportcollection(self):
        HEADING()

        """
        Test to export a collection in json format to a directory named "dumps"
        """
        self._xyz()
        db = DBUtil()
        db.serialize(db="manage", collection="cloudmesh_object")


