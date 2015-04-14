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

    def _xyz(self):
        print("hallo")

    def test_generate(self):
        HEADING()

        self._xyz()
        user_name = 'nicolas'
        project_id = '5fda88ab86094cb6963f3b231f92ed9e'
        project = Projects()
        project.add_user(user_name, project_id, 'member')
        # user = User.objects(username=user_name).first()
        # print user
        # Project.objects(project_id=project_id).update_one(push__members=user)


