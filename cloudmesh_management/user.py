from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_management.cloudmeshobject import CloudmeshObject
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.locations import config_file
from cloudmesh_base.util import path_expand
from cmd3.console import Console
from tabulate import tabulate
from passlib.hash import sha256_crypt
from mongoengine import *
import yaml
import datetime
import json
import sys

STATUS = ('pending', 'approved', 'blocked', 'denied','active','suspended')


def implement():
    print "IMPLEMENT ME"


'''
def generate_password_hash(password)
    # maybe using passlib https://pypi.python.org/pypi/passlib
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password'''


def read_user(filename):
    """
    Reads user data from a yaml file

    :param filename: The file anme
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


class User(CloudmeshObject):
    """
    This class is used to represent a Cloudmesh User
    """

    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}
    #
    # defer the connection to where the object is instantiated
    # get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    """
    User fields
    """

    username = StringField(required=True)
    email = EmailField(required=True)
    password = StringField()
    confirm = StringField()
    title = StringField(required=True)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    phone = StringField(required=True)
    url = StringField(required=True)
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    institution = StringField(required=True)
    institutionrole = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    advisor = StringField(required=True)
    country = StringField(required=True)

    """
    Hidden fields
    """

    status = StringField(required=True, default='pending')
    userid = UUIDField()
    projects = StringField()

    """
    Message received from either reviewers,
    committee or other users. It is a list because
    there might be more than one message
    """

    message = ListField(StringField())

    @classmethod
    def order(cls):
        """
        Order the attributes to be printed in the display
        method
        """
        try:
            return [
                ("username", cls.username),
                ("status", cls.status),
                ("title", cls.title),
                ("firstname", cls.firstname),
                ("lastname", cls.lastname),
                ("email", cls.email),
                ("url", cls.url),
                ("citizenship", cls.citizenship),
                ("bio", cls.bio),
                ("password", cls.password),
                ("phone", cls.phone),
                ("projects", cls.projects),
                ("institution", cls.institution),
                ("department", cls.department),
                ("address", cls.address),
                ("country", cls.country),
                ("advisor", cls.advisor),
                ("date_modified", cls.date_modified),
                ("date_created", cls.date_created),
                ("date_approved", cls.date_approved),
                ("date_deactivated", cls.date_deactivated),
            ]
        except Exception, e:
            return None

    @classmethod
    def hidden(cls):
        """
        Hidden attributes
        """
        return [
            "userid",
            "active",
            "message",
        ]


    # def save(self,db):
    # db.put({"firname":user.firname,...})

    def is_active(self):
        """
        Check if the user is active
        """
        d1 = datetime.datetime.now()
        return (self.active == True) and (datetime.datetime.now() < self.date_deactivate)

    @classmethod
    def set_password(cls, password):
        """
        Not implemented

        :param password:
        :type password:
        """
        #self.password_hash = generate_password_hash(password)
        pass

    @classmethod
    def check_password(cls, password):
        """
        Not implemented

        :param password:
        :type password:
        """
        # return check_password_hash(self.password_hash, password)
        pass

    @classmethod
    def json(cls):
        """
        Returns a json representation of the object
        """
        d = {}
        for (field, value) in cls.order():
            try:
                d[field] = value
            except:
                pass
        return d

    @classmethod
    def yaml(cls):
        """
        Returns the yaml object of the object.
        """
        return cls.__str__(fields=True, all=True)

    """
    def __str__(self, fields=False, all=False):
        content = ""
        for (field, value)  in self.order():
            try:
                if not (value is None or value == "") or all:
                    if fields:
                        content = content + field + ": "
                    content = content + value + "\n"
            except:
                pass
        return content
    """


class Users(object):
    """
    Convenience object to manage several users
    """

    def __init__(self):
        config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        port = config['cloudmesh']['server']['mongo']['port']

        # db = connect('manage', port=port)
        self.users = User.objects()

        db_name = get_mongo_dbname_from_collection("manage")
        if db_name:
            meta = {'db_alias': db_name}

        #         get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

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
            num = num + 1
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
                else:
                    Console.error("User with the name '{0}' does not exist.".format(user_name))
            except:
                Console.error("Oops! Something went wrong while trying to remove a user")
        else:
            Console.error("Please specify the user to be removed")

    @classmethod
    def amend_user_status(cls, user_name=None, status=None):
        if user_name:
            try:
                current_status = cls.get_user_status(user_name)
            except:
                Console.error("Oops! Something went wrong while trying to get user status")

            if status == "approved":
                if current_status in ["pending", "denied"]:
                    cls.set_user_status(user_name, status)
                else:
                    Console.error("Cannot approve user. User not in pending status.")
            elif status == "active":
                if current_status in ["approved", "suspended", "blocked"]:
                    cls.set_user_status(user_name, status)
                else:
                    Console.error("Cannot activate user. User not in approved or suspended status.")
            elif status == "suspended":
                if current_status == "active":
                    cls.set_user_status(user_name, status)
                else:
                    Console.error("Cannot suspend user. User not in active status.")
            elif status == "blocked":
                if current_status == "active":
                    cls.set_user_status(user_name, status)
                else:
                    Console.error("Cannot block user. User not in active status.")
            elif status == "denied":
                if current_status in ["approved", "pending"]:
                    cls.set_user_status(user_name, status)
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
            Console.error("Please specify the user to be amended")

    @classmethod
    def validate_email(cls, email):
        """
        Verifies if the email of the user is not already in the users.

        :param user: user object
        :type user: User
        :rtype: Boolean
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
        for user in User.objects:
            user.delete()


    @classmethod
    def list_users(cls, disp_fmt=None, username=None):
        req_fields = ["username", "title", "firstname", "lastname",
                      "email", "phone", "url", "citizenship",
                      "institution", "institutionrole", "department",
                      "advisor", "address", "status"]
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
                    Console.error("No users in the database.")
            else:
                user_json = User.objects(username=username).only(*req_fields).to_json()
                user_dict = json.loads(user_json)
                if user_dict:
                    if disp_fmt != 'json':
                        cls.display(user_dict, username)
                    else:
                        cls.display_json(user_dict, username)
                else:
                    Console.error("No users in the database.")
        except:
            print "Oops.. Something went wrong in the list users method", sys.exc_info()[0]
        pass

    @classmethod
    def display(cls, user_dicts=None, user_name=None):
        if bool(user_dicts):
            values = []
            for entry in user_dicts:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    items.append(value)
                    headers.append(key.replace('_', ' ').title())
                values.append(items)
            table_fmt = "orgtbl"
            table = tabulate(values, headers, table_fmt)
            separator = ''
            try:
                seperator = table.split("\n")[1].replace("|", "+")
            except:
                separator = "-" * 50
            print separator
            print table
            print separator
        else:
            if user_name:
                print "Error: No user in the system with name '{0}'".format(user_name)


    @classmethod
    def display_json(cls, user_dict=None, user_name=None):
        if bool(user_dict):
            # pprint.pprint(user_json)
            print json.dumps(user_dict, indent=4)
        else:
            if user_name:
                print "Error: No user in the system with name '{0}'".format(user_name)

    @classmethod
    def create_user_from_file(cls, file_path):
        try:
            filename = path_expand(file_path)
            file_config = ConfigDict(filename=filename)
        except:
            Console.error("Could not load file, please check filename and its path")
            return

        try:
            user_config = file_config.get("cloudmesh","user")
        except:
            Console.error("Could not get user information from yaml file, "
                      "please check you yaml file, users information must be "
                      "under 'cloudmesh' -> 'users' -> user1...")
            return

        try:
            user_name = user_config['username']
            user_string = "User("
            for key in user_config:
                # print key, " - ", user_config[key]
                user_string = user_string+key+"="+"\""+user_config[key]+"\","
            user_string += "status=\"pending\","
            user_string += ")"
            data = eval(user_string)
        except:
            Console.error("User object creation failed.")
            return

        try:
            if cls.check_exists(user_name) is False:
                cls.add(data)
                Console.info("User created in the database.")
            else:
                Console.error("User with user name "+user_name+" already exists.")
                return
        except:
            Console.error("User creation in database failed, "+str(sys.exc_info()[0]))
            return

    @classmethod
    def check_exists(cls, user_name):
        return User.objects(username=user_name) > 0

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
        if email.endswith():
            return True
    return False
