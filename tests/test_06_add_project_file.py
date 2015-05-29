from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_management.project import Project
from cloudmesh_base.util import HEADING
from cloudmesh_management.project import Projects
from cloudmesh_management.mongo import Mongo


class TestAddProjectFromFile:
    yaml_dir = "~/.cloudmesh_yaml"

    def setup(self):
        # HEADING()
        db_name = get_mongo_dbname_from_collection("manage")
        if db_name:
            meta = {'db_alias': db_name}
        obj = Mongo()
        obj.check_mongo()
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        pass

    def teardown(self):
        # HEADING()
        pass

    def test_addprojectfromfile(self):
        HEADING()
        """
        Test to add a project from file
        """
        project = Projects()
        print "Project count before addition: ", Project.objects().count()
        file_path = "etc/cloudmesh_project_info.yaml"
        project.create_project_from_file(file_path)
        print "Project count after addition: ", Project.objects().count()




