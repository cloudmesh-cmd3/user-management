from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner
from pprint import pprint
from cloudmesh_management.user import User, Users
from cloudmesh_management.project import Project, Projects
from cloudmesh_management.generate import generate_users
from cloudmesh_management.generate import generate_projects
import os
 
class TestGenerate:

    yaml_dir = "~/.cloudmesh_yaml"
    firstname="gergor"

    def setup(self):
        # HEADING()
        self.db = "hallo"
        pass
    
    def teardown(self):
        # HEADING()
        pass

    def _xyz(self):
        print("hallo")

    def test_generate(self):
        HEADING()

        self._xyz()
        generate_users(10)
        generate_projects(3)    

        banner("Find")
        #print users.find()
        banner("Find [0]")
        #print users.find()[0]

        projects = Project.objects()
        print projects.count()
        pprint (projects[0])

