from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.project import Projects


class TestListProjects:
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

    def test_listprojects(self):
        HEADING()
        """
        Test to list projects in default format followed by JSON format
        """
        project = Projects()
        print "Listing in default format"
        project.list_projects()
        print "Listing in JSON format"
        project.list_projects(display_fmt='json')



