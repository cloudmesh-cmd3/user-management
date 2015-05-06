import json
import sys
import yaml

from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cmd3.console import Console
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
from texttable import Texttable
from mongoengine import fields


# from cloudmesh_management.base_classes import SubUser, Project
from cloudmesh_management.base_user import User
from cloudmesh_management.base_project import Project

STATUS = ('pending', 'approved', 'blocked', 'denied', 'active', 'suspended')


def implement():
    print "IMPLEMENT ME"


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


'''
def generate_password_hash(password)
    # maybe using passlib https://pypi.python.org/pypi/passlib
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password'''


def read_user(filename):
    """
    Reads user data from a yaml file

    :param filename: The file name
    :type filename: String of the path
    """
    stream = open(filename, 'r')
    data = yaml.load(stream)
    user = User(
        status=data["status"],
        username=data["username"],
        title=data["title"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        url=data["url"],
        citizenship=data["citizenship"],
        bio=data["bio"],
        password=data["password"],
        userid=data["userid"],
        phone=data["phone"],
        projects=data["projects"],
        institution=data["institution"],
        department=data["department"],
        address=data["address"],
        country=data["country"],
        advisor=data["advisor"],
        message=data["message"],
    )
    return user


# noinspection PyBroadException
class Users(object):
    """
    Convenience object to manage several users
    """

    def __init__(self):
        # config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        # port = config['cloudmesh']['server']['mongo']['port']

        # db = connect('manage', port=port)
        self.users = User.objects()

        db_name = get_mongo_dbname_from_collection("manage")
        if db_name:
            meta = {'db_alias': db_name}

            # get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    @classmethod
    def objects(cls):
        """
        Returns the users
        """
        return cls.users

    @classmethod
    def get_unique_username(cls, proposal):
        """
        Gets a unique username from a proposal. This is achieved while appending a number at the end.

        :param proposal: the proposed username
        :type proposal: String
        """
        new_proposal = proposal.lower()
        num = 1
        username = User.objects(username=new_proposal)
        while username.count() > 0:
            new_proposal = proposal + str(num)
            username = User.objects(username=new_proposal)
            num += 1
        return new_proposal

    @classmethod
    def add(cls, user):
        """
        Adds a user

        :param user: the username
        :type user: User object
        """
        user.username = cls.get_unique_username(user.username)
        user.set_date_deactivate()
        if cls.validate_email(user.email):
            user.save()
        else:
            Console.error("A user with the e-mail `{0}` already exists".format(user.email))

    @classmethod
    def delete_user(cls, user_name=None):
        if user_name:
            try:
                user = User.objects(username=user_name)
                if user:
                    user.delete()
                    Console.info("User " + user_name + " removed from the database.")
                else:
                    Console.error("User with the name '{0}' does not exist.".format(user_name))
            except:
                Console.error("Oops! Something went wrong while trying to remove a user")
        else:
            Console.error("Please specify the user to be removed")

    @classmethod
    def amend_user_status(cls, user_name=None, new_status=None):
        current_status = ""
        if user_name:
            try:
                current_status = cls.get_user_status(user_name)
            except:
                Console.error("Oops! Something went wrong while trying to get user status")

            if new_status == "approved":
                if current_status in ["pending", "denied"]:
                    cls.set_user_status(user_name, new_status)
                else:
                    Console.error("Cannot approve user. User not in pending status.")
            elif new_status == "active":
                if current_status in ["approved", "suspended", "blocked"]:
                    cls.set_user_status(user_name, new_status)
                else:
                    Console.error("Cannot activate user. User not in approved or suspended status.")
            elif new_status == "suspended":
                if current_status == "active":
                    cls.set_user_status(user_name, new_status)
                else:
                    Console.error("Cannot suspend user. User not in active status.")
            elif new_status == "blocked":
                if current_status == "active":
                    cls.set_user_status(user_name, new_status)
                else:
                    Console.error("Cannot block user. User not in active status.")
            elif new_status == "denied":
                if current_status in ["approved", "pending"]:
                    cls.set_user_status(user_name, new_status)
                else:
                    Console.error("Cannot deny user. User not in approved or pending status.")
        else:
            Console.error("Please specify the user to be amended")

    @classmethod
    def set_user_status(cls, user_name, status):
        if user_name:
            try:
                User.objects(username=user_name).update_one(set__status=status)
            except:
                Console.error("Oops! Something went wrong while trying to amend user status")
        else:
            Console.error("Please specify the user to be amended")

    @classmethod
    def get_user_status(cls, user_name):
        if user_name:
            try:
                user = User.objects(username=user_name).only('status')
                if user:
                    for entry in user:
                        return entry.status
            except:
                Console.error("Oops! Something went wrong while trying to get user status")
        else:
            Console.error("Please specify the user get status")

    @classmethod
    def validate_email(cls, email):

        """
        Verifies if the email of the user is not already in the users.
        :param email: email id of the user
        :return: true or false
        """
        user = User.objects(email=email)
        valid = user.count() == 0
        return valid

    @classmethod
    def find(cls, email=None):
        """
        Returns the users based on the given query.
        If no email is specified all users are returned.
        If the email is specified we search for the user with the given e-mail.

        :param email: email
        :type email: email address
        """
        if email is None:
            return User.objects()
        else:
            found = User.objects(email=email)
            if found.count() > 0:
                return User.objects()[0]
            else:
                return None

    @classmethod
    def find_user(cls, username):
        """
        Returns a user based on the username

        :param username:
        :type username:
        """
        return User.object(username=username)

    @classmethod
    def clear(cls):
        """
        Removes all elements form the mongo db that are users
        """
        try:
            for user in User.objects:
                user.delete()
            Console.info("Users cleared from the database.")
        except:
            Console.error("Oops! Something went wrong while trying to clear the users from database")

    @classmethod
    def list_users(cls, disp_fmt=None, username=None):
        # req_fields = ["username", "title", "firstname", "lastname",
        # "email", "phone", "url", "citizenship",
        #               "institution", "institutionrole", "department",
        #               "advisor", "address", "status", "projects"]
        req_fields = ["username", "firstname", "lastname",
                      "email", "phone", "institution", "institutionrole",
                      "advisor", "address", "status", "projects"]
        try:
            if username is None:
                user_json = User.objects.only(*req_fields).to_json()
                user_dict = json.loads(user_json)
                if user_dict:
                    if disp_fmt != 'json':
                        cls.display(user_dict, username)
                    else:
                        cls.display_json(user_dict, username)
                else:
                    Console.info("No users in the database.")
            else:
                user_json = User.objects(username=username).to_json()
                users_list = json.loads(user_json)
                for item in users_list:
                    users_dict = item
                    if users_dict:
                        if disp_fmt != 'json':
                            cls.display_two_columns(users_dict)
                        else:
                            cls.display_json(users_dict, username)
                    else:
                        Console.error("User not in the database.")
        except:
            Console.error("Oops.. Something went wrong in the list users method " + sys.exc_info()[0])

    @classmethod
    def list_projects(cls, user_name=None):
        required_fields = ["username", "firstname", "lastname", "projects"]
        try:
            if user_name:
                user_json = User.objects.only(*required_fields).to_json()
                user_dict = json.loads(user_json)
                if user_dict:
                    cls.display(user_dict, user_name)
                else:
                    Console.info("No user details available in the database.")
        except:
            Console.error("Please provide a username.")

    @classmethod
    def display(cls, user_dicts=None, user_name=None):
        if bool(user_dicts):
            values = []
            table = Texttable(max_width=180)
            for entry in user_dicts:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    if key == "projects":
                        project_entry = ""
                        if value:
                            for itm in value:
                                user_project = Project.objects(id=ObjectId(itm.get('$oid'))).only('title',
                                                                                                  'project_id').first()
                                project_entry = project_entry + user_project.title + ", "
                        items.append(project_entry)
                    else:
                        items.append(value)
                    headers.append(key.replace('_', ' ').title())
                values.append(items)
                table.add_row(items)
            table.header(headers)
            print table.draw()
        else:
            if user_name:
                Console.error("No user in the system with name '{0}'".format(user_name))

    @classmethod
    def display_two_columns(cls, table_dict=None):
        if table_dict:
            ignore_fields = ['_cls', '_id', 'date_modified', 'date_created', 'password', 'confirm']
            table = Texttable(max_width=100)
            rows = [['Property', 'Value']]
            for key, value in table_dict.iteritems():
                if key not in ignore_fields:
                    items = [key.replace('_', ' ').title()]
                    if isinstance(value, list):
                        if value:
                            if key == "projects":
                                project_entry = ""
                                for itm in value:
                                    user_project = Project.objects(id=ObjectId(itm.get('$oid'))) \
                                        .only('title', 'project_id').first()
                                    project_entry = project_entry + user_project.title + ", "
                                project_entry.strip(', ')
                                items.append(project_entry)
                            else:
                                items.append(' , '.join(value))
                        else:
                            items.append('None')
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

    @classmethod
    def display_json(cls, user_dict=None, user_name=None):
        if bool(user_dict):
            print json.dumps(user_dict, indent=4)
        else:
            if user_name:
                Console.error("No user in the system with name '{0}'".format(user_name))

    @classmethod
    def create_user_from_file(cls, file_path):
        try:
            filename = path_expand(file_path)
            file_config = ConfigDict(filename=filename)
        except:
            Console.error("Could not load file, please check filename and its path")
            return

        try:
            user_config = file_config.get("cloudmesh", "user")
            user_name = user_config['username']
            user = User()
            update_document(user, user_config)
        except:
            Console.error("Could not get user information from yaml file, "
                          "please check you yaml file, users information must be "
                          "under 'cloudmesh' -> 'users' -> user1...")
            return

        try:
            if cls.check_exists(user_name) is False:
                cls.add(user)
                Console.info("User created in the database.")
            else:
                Console.error("User with user name " + user_name + " already exists.")
                return
        except:
            Console.error("User creation in database failed, " + str(sys.exc_info()))
            return

    @classmethod
    def check_exists(cls, user_name):
        return len(User.objects(username=user_name)) > 0

    @classmethod
    def set_password(cls, user_name, passwd):
        pass_hash = sha256_crypt.encrypt(passwd)
        try:
            User.objects(username=user_name).update_one(set__password=pass_hash)
            Console.info("User password updated.")
        except:
            Console.error("Oops! Something went wrong while trying to set user password")


def verified_email_domain(email):
    """
    not yet implemented. Returns true if the e-mail is in a specified domain.

    :param email:
    :type email:
    """
    domains = ["indiana.edu"]

    for domain in domains:
        if email.endswith() == domain:
            return True
    return False
