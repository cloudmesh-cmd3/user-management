from cloudmesh_management.user import SubUser
# from management import Account
# from projects import project_information
# from projects import resource_requirement
from cloudmesh_management.project import Project
# from user_dict import *
from docopt import docopt
from mongoengine import *
import random

connect('user', port=27777)


class UserProject():

    def __init__(self):
        pass

    accounts = Account.objects()
    projects = Project.objects()

    title = ""
    category = ""
    #keywords = ""
    contact = ""
    #members = ""
    #alumni = ""
    #nsf_grant_number = ""
    #nsf_grant_url = ""
    results = ""
    nsf_Agreement = ""		#Yes/No
    slide_collection_agreement = ""	#Yes/No
    other = ""

    def add_project(self):
        user_name = raw_input("User name: ")
        for account in Account.objects:
            if account.username == user_name:
                user_account = account
        self.title = raw_input("Project title: ")
        self.contact = raw_input("Project contact: ")
        self.results = raw_input("Results: ")
        self.nsf_Agreement = raw_input("NSF Agreement (Yes or No): ")
        self.slide_collection_agreement = raw_input("Slide Collection Agreement (Yes or No): ")
        self.other = raw_input("Other: ")
        project = Project(project_title = self.title,
                          lead = user_account, manager = user_account,
                          contact = self.contact, results = self.results,
                          nsf_Aggreement = self.nsf_Agreement,
                          slide_collection_aggreement = self.slide_collection_agreement,
                          other = self.other )
        project.save()
        print project.project_title


    #account.project = self.title refernce and list field

    def generate_random(self):
        pass

    def generate_project(self):
        pass

    def list_project(self):
        project = Project.objects()
        for project in Project.objects():
            print
            print project.project_title, ":", project
            print

    def del_project(self):
        user_name = raw_input("User name: ")
        for project in Project.objects:
            if project.lead.username == user_name:
                project.delete()

c = UserProject()

c.add_project()
c.list_project()
#c.del_project()
