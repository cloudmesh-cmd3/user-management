from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.base_user import User
from cloudmesh_management.base_project import Project

from cloudmesh_management.project import Projects


class TestAddProjectMember:
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

    def test_addprojectmember(self):
        HEADING()
        """
        Test to add a member to an existing project
        """

        self._xyz()
        user = User.objects.first()
        project = Project.objects.first()
        user_name = user.username
        project_id = project.project_id
        project = Projects()
        project.add_user(user_name, project_id, 'member')
        project.list_projects(project_id=project_id)


