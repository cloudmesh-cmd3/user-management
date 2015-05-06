from pprint import pprint
from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner

from cloudmesh_management.project import Project, Projects
from cloudmesh_management.user import SubUser


class TestGenerate:
    yaml_dir = "~/.cloudmesh_yaml"
    firstname = "gergor"

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
        display_fmt = 'json'
        project_id = 'dbe4baed060242549c92fda3d047fb92'
        project.list_projects(project_id=project_id)



