from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING

from cloudmesh_management.generate import generate_users
from cloudmesh_management.generate import generate_projects


class TestGenerate:
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

    def test_generate(self):
        HEADING()

        """
        Test to generate 10 users and 10 projects
        """
        self._xyz()
        generate_users(10)
        generate_projects(10)
        #
        # banner("Find")
        # #print users.find()
        # banner("Find [0]")
        # #print users.find()[0]
        #
        # projects = Project.objects()
        # print projects.count()
        # pprint (projects[0])

