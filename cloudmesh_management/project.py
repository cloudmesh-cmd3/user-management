import json
import uuid
import sys

from cloudmesh_database.dbconn import get_mongo_db, DBConnFactory
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cmd3.console import Console
from tabulate import tabulate
from texttable import Texttable
from bson.objectid import ObjectId
# from cloudmesh_management.base_classes import User, Project, SubUser
from cloudmesh_management.base_project import Project
from cloudmesh_management.base_user import User
from mongoengine import fields

ROLES_LIST = ["lead", "member", "alumni"]


def implement():
    print "TO BE IMPLEMENTED"
    return


def update_document(document, data_dict):
    def field_value(field, values):
        if field.__class__ in (fields.ListField, fields.SortedListField):
            if values:
                return str(values).split(", ")
            else:
                return []

        if field.__class__ in (
            fields.EmbeddedDocumentField,
            fields.GenericEmbeddedDocumentField,
            fields.ReferenceField,
            fields.GenericReferenceField
        ):
            pass
            # return field.document_type(**value)
        else:
            return values

    [setattr(
        document, key,
        field_value(document._fields[key], value)
    ) for key, value in data_dict.items()]
    return document


class Projects(object):
    """
    Convenience object to manage multiple projects
    """

    def __init__(self):
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        self.projects = Project.objects()
        self.users = User.objects()

    def __str__(self):
        """
        not implemented
        """
        implement()

    @classmethod
    def find(cls):
        return Project.objects()

    @classmethod
    def objects(cls):
        """
        Returns the projects
        """
        return Project.objects()

    @classmethod
    def save(cls, project):
        """
        Adds a project to the database but only after it has been verified

        :param project: the project id
        :type project: uuid
        """
        project.save()

    @classmethod
    def add_user(cls, user_name, project_id, role):
        """
        Adds a member to the project.

        :param role: the role of the user
        :type role: String
        :param user_name: the username
        :type user_name: String
        :param project_id: the project id
        """

        if role not in ROLES_LIST:
            Console.error("Invalid role `{0}`".format(role))
            return

        """adds members to a particular project"""
        user = User.objects(username=user_name).first()
        project = Project.objects(project_id=project_id).first()
        if project:
            if user and role != 'alumni':
                if role == "member":
                    Project.objects(project_id=project_id).update_one(push__members=user)
                    User.objects(username=user_name).update_one(push__projects=project)
                    Console.info("User `{0}` added as Project member.".format(user_name))
                elif role == "lead":
                    Project.objects(project_id=project_id).update_one(push__lead=user)
                    Console.info("User `{0}` set as Lead.".format(user_name))
                else:
                    Console.error("Role `{0}` cannot be amended".format(role))
            elif role == "alumni":
                Project.objects(project_id=project_id).update_one(push__alumnis=user_name)
                Console.info("User `{0}` added as Alumni.".format(user_name))
            else:
                Console.error("The user `{0}` has not registered with Future Systems".format(user_name))
        else:
            Console.error("The project `{0}` is not registered with Future Systems".format(project_id))

    @classmethod
    def remove_user(cls, user_name, project_id, role):
        if role not in ROLES_LIST:
            Console.error("Invalid role `{0}`".format(role))
            return
        user = User.objects(username=user_name).first()
        if user and role != "alumni":
            if role == "member":
                Project.objects(project_id=project_id).update_one(pull__members=user)
                Console.info("User `{0}` removed as Project member.".format(user_name))
            elif role == "lead":
                Project.objects(project_id=project_id).update_one(pull__lead=user)
                Console.info("User `{0}` removed as Project lead.".format(user_name))
        elif role == "alumni":
            Project.objects(project_id=project_id).update_one(pull__alumnis=user)
            Console.info("User `{0}` removed as alumni.".format(user_name))
        else:
            Console.error("The user `{0}` has not registered with Future Systems".format(user_name))


    @classmethod
    def find_users(cls, project, role):
        '''returns all the members of a particular project

        :param role: the role of the user
        :type role: String
        :param project: the project id
        :type project: uuid
        '''
        if role not in ROLES_LIST:
            Console.error("Invalid role `{0}`".format(role))
            return
        if role == "member":
            return project.members
        elif role == "lead":
            return project.leads
        elif role == "lead":
            return project.alumni

    @classmethod
    def find_by_id(cls, id):
        '''
        finds projects by if

        :param id: the project id
        :type id: uuid
        '''
        """Finds a project by the given id"""
        found = Project.objects(projectid=id)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None
            # User ID or project ID

    @classmethod
    def find_by_category(cls, category):
        '''
        find the project by category

        :param category: the category
        :type category: String
        '''
        """Finds and returns all project in that category"""
        found = Project.objects(categories=category)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    @classmethod
    def find_by_keyword(cls, keyword):
        '''
        finds a projects matching a keyword

        :param keyword: a keyword
        :type keyword: String
        '''
        """Finds and returns all projects with the entered keyword"""
        found = Project.objects(keyword=keyword)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    @classmethod
    def add(cls, project):
        """
        Adds a project

        :param project: the username
        :type project: String
        """

        if not project.status:
            project.status = 'pending'
        if (project.project_id is None) or (project.project_id == ""):
            found = False
            proposed_id = None
            project.project_id = proposed_id
        project.save()


    @classmethod
    def create_project_from_file(cls, file_path):
        # implement()
        # return
        try:
            filename = path_expand(file_path)
            file_config = ConfigDict(filename=filename)
        except:
            Console.error("Could not load file, please check filename and its path")
            return

        try:
            project_config = file_config.get("cloudmesh", "project")
            project = Project()
            project_id = uuid.uuid4()
            project_config.update({'project_id': project_id})
            update_document(project, project_config)
        except:
            Console.error("Could not get project information from yaml file, "
                          "please check you yaml file, users information must be "
                          "under 'cloudmesh' -> 'project' -> project1..." + str(sys.exc_info()[0]))
            return

        try:
            cls.add(project)
            Console.info("Project created in the database.")
        except:
            Console.error("Project creation in database failed, " + str(sys.exc_info()))
        return

    @classmethod
    def str_to_list(cls, string):
        split_list = string.split(",")
        return split_list

    @classmethod
    def list_projects(cls, display_fmt=None, project_id=None):
        req_fields = ["title", "status", "lead", "managers", "members", "project_id"]
        try:
            if project_id is None:
                projects_json = Project.objects.only(*req_fields).to_json()
                projects_dict = json.loads(projects_json)
                if projects_dict:
                    if display_fmt != 'json':
                        cls.display(projects_dict, project_id)
                    else:
                        cls.display_json(projects_dict, project_id)
                else:
                    Console.info("No projects in the database.")
            else:
                projects_json = Project.objects(project_id=project_id).to_json()
                projects_list = json.loads(projects_json)
                for item in projects_list:
                    projects_dict = item
                cls.display_two_column(projects_dict)
        except:
            Console.error("Oops.. Something went wrong in the list projects method " + sys.exc_info())
        pass


    @classmethod
    def display_two_column(cls, table_dict=None):
        if table_dict:
            ignore_fields = ['_cls', '_id', 'date_modified', 'date_created']
            table = Texttable(max_width=100)
            rows = [['Property', 'Value']]
            for key, value in table_dict.iteritems():
                if key not in ignore_fields:
                    items = []
                    # print key, " - ", value
                    # managers, lead, project_id, members,
                    if key == "lead":
                        entry = ""
                        for item in value:
                            user = User.objects.get(id=ObjectId(item.get('$oid')))
                            entry += user.firstname + " " + user.lastname + ","
                        entry = entry.strip(',')
                        items.append(key.replace('_', ' ').title())
                        items.append(entry)
                        rows.append(items)
                    elif key == "members":
                        entry = ""
                        for item in value:
                            user = User.objects.get(id=ObjectId(item.get('$oid')))
                            entry += user.firstname + " " + user.lastname + ","
                        entry = entry.strip(',')
                        items.append(key.replace('_', ' ').title())
                        items.append(entry)
                        rows.append(items)
                    elif key == "managers":
                        entry = ""
                        for item in value:
                            user = User.objects.get(id=ObjectId(item.get('$oid')))
                            entry += user.firstname + " " + user.lastname + ","
                        entry = entry.strip(',')
                        items.append(key.replace('_', ' ').title())
                        items.append(entry.encode('ascii', 'ignore'))
                        rows.append(items)
                    elif key == "project_id":
                        items.append(key.replace('_', ' ').title(), )
                        items.append(value.get('$uuid').encode('ascii', 'ignore'))
                        rows.append(items)
                    else:
                        items.append(key.replace('_', ' ').title())
                        if (key in ['agreement_software', 'agreement_documentation', 'join_notification',
                                    'agreement_slides', 'join_open', 'agreement_support', ]):
                            if isinstance(value, list):
                                items.append(' , '.join(value))
                            else:
                                if value == 1:
                                    items.append("True")
                                else:
                                    items.append(("False"))
                        else:
                            if isinstance(value, list):
                                items.append(' , '.join(value))
                            else:
                                items.append(value)
                        rows.append(items)
            try:
                if rows:
                    table.add_rows(rows)
            except:
                print sys.exc_info()[0]
            print table.draw()
        pass

    # @classmethod
    # def reorder(cls, rows_list=None):
    # row_order = [16, 7, 2, 37, 35, 22, 30, 10, 24, 4, 35, 32, 1, 30, 21, 23, 15, 3, 29, 28, 20, 33, 13, 8, 18, 17,
    #                  26, 5, 6, 19, 25, 12, 30, 37, 27, 34, 9, 39, 14, 29, 11]
    #     if rows_list:
    #         rows_list = [rows_list[i] for i in row_order]
    #     return rows_list
    #     pass

    @classmethod
    def display(cls, project_dicts=None, project_id=None):
        if bool(project_dicts):
            values = []
            for entry in project_dicts:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    if key == "lead":
                        entry = ""
                        if value:
                            for item in value:
                                user = User.objects.get(id=ObjectId(item.get('$oid')))
                                entry += user.firstname + " " + user.lastname + ","
                            entry = entry.strip(',')
                            items.append(entry)
                        else:
                            items.append("No leads")
                    elif key == "members":
                        entry = ""
                        if value:
                            for item in value:
                                user = User.objects.get(id=ObjectId(item.get('$oid')))
                                entry += user.firstname + " " + user.lastname + ","
                            entry = entry.strip(',')
                            items.append(entry)
                        else:
                            items.append("No members")
                    elif key == "managers":
                        entry = ""
                        if value:
                            for item in value:
                                user = User.objects.get(id=ObjectId(item.get('$oid')))
                                entry += user.firstname + " " + user.lastname + ","
                            entry = entry.strip(',')
                            items.append(entry)
                        else:
                            items.append("No managers")
                    elif key == "project_id":
                        items.append(value.get('$uuid').encode('ascii', 'ignore'))
                    else:
                        items.append(value)
                    headers.append(key.replace('_', ' ').title())
                values.append(items)

            # Re-order the columns as per our requirement
            # header order 5, 0, 3, 2, 1, 4 => project_id, status, title, lead, managers, members
            header_order = [5, 0, 3, 2, 1, 4]
            headers = [headers[i] for i in header_order]
            new_values = [[x[5], x[0], x[3], x[2], x[1], x[4]] for x in values]
            table_fmt = "fancy_grid"
            table = tabulate(new_values, headers, table_fmt)
            separator = ''
            try:
                seperator = table.split("\n")[1].replace("|", "+")
            except:
                separator = "-" * 50
            print separator
            print table
            print separator
        else:
            if project_id:
                Console.error("No project in the system with name '{0}'".format(project_id))

    @classmethod
    def display_json(cls, project_dict=None, project_id=None):
        if bool(project_dict):
            # pprint.pprint(user_json)
            print json.dumps(project_dict, indent=4)
        else:
            if project_id:
                Console.error("No project in the system with name '{0}'".format(project_id))


    @classmethod
    def clear(cls):
        """removes all projects from the database"""
        for project in Project.objects:
            project.delete()

    @classmethod
    def delete_project(cls, project_id=None):
        if project_id:
            try:
                project = Project.objects(project_id=project_id)
                if project:
                    project.delete()
                    Console.info("Project with id `{0}` removed from the database.".format(project_id))
                else:
                    Console.error("Project with id `{0}` does not exist.".format(project_id))
            except:
                Console.error("Oops! Something went wrong while trying to remove a project")
        else:
            Console.error("Please specify the project to be removed")

    @classmethod
    def amend_project_status(cls, project_id=None, new_status=None):
        current_status = ""
        if project_id:
            try:
                current_status = cls.get_project_status(project_id)
            except:
                Console.error("Oops! Something went wrong while trying to get project status")

            if new_status == "active":
                if current_status in ["pending", "blocked"]:
                    cls.set_project_status(project_id, new_status)
                else:
                    Console.error("Cannot activate project. Project is not in pending/blocked status.")
            elif new_status == "block":
                if current_status in ["active", "pending"]:
                    cls.set_project_status(project_id, "blocked")
                else:
                    Console.error("Cannot block project. Project is not active or pending.")
            elif new_status == "close":
                if current_status in ["active", "pending", "blocked"]:
                    cls.set_project_status(project_id, "closed")
                else:
                    Console.error("Cannot close project. Project is not active/pending/blocked.")
            elif new_status == "open":
                if current_status  == "closed":
                    cls.set_project_status(project_id, "pending")
                else:
                    Console.error("Cannot close project. Project is not closed.")
        else:
            Console.error("Please specify the project to be amended")

    @classmethod
    def get_project_status(cls, project_id):
        if project_id:
            try:
                project = Project.objects(project_id=project_id).only('status')
                if project:
                    for entry in project:
                        return entry.status
            except:
                Console.error("Oops! Something went wrong while trying to get user status")
        else:
            Console.error("Please specify the user get status")


    @classmethod
    def set_project_status(cls, project_id, status):
        if project_id:
            try:
                Project.objects(project_id=project_id).update_one(set__status=status)
            except:
                Console.error("Oops! Something went wrong while trying to amend project status")
        else:
            Console.error("Please specify the project to be amended")
