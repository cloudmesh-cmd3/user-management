"""
    Generate the classes for Users and Projects depending on the
    contents of the users and projects YAML file
"""

import yaml
from cloudmesh_database.dbconn import get_mongo_dbname_from_collection, get_mongo_db, DBConnFactory
from cloudmesh_base.locations import config_file
from cloudmesh_base.util import path_expand
from cloudmesh_management.base_user import User
from cmd3.console import Console
from functools import wraps
from cloudmesh_management.mongo import Mongo
from cloudmesh_base.util import banner

DB_CLASS_FIELDS = ""
DB_CLASS_DICT = {}
UI_CLASS_FIELDS = ""
KEYS = "keys = ["


def implement():
    print "Yet to be implemented."


def build_db_field(item):
    """
    The function is used to build the description of mongoengine
    fields depending on the type in the YAML file description.
    An example of item is given below:
    {'title': {'required': True, 'type': 'text', 'label': 'Title'}}

    :param item:
    :return: string in the following format:
                title = StringField(required=True)
    """

    for keys, values in item.items():
        field_entry = keys
        field_type = ""
        required = ""
        default_value = ""
        if isinstance(values, dict):
            for key, value in values.items():
                if key in ['required', 'type']:
                    if key == 'required':
                        required = key + "=" + str(value)
                    elif key == 'type':
                        if value in ['text', 'textarea', 'dropdown', 'password']:
                            field_type = "StringField"
                        elif value == 'checkbox':
                            field_type = "StringField"
                            default_value = "no"
                        elif value == 'email':
                            field_type = "EmailField"
        if default_value and required:
            field_entry = '{0} = {1}({2}, default={3})' \
                .format(field_entry, field_type, required, default_value)
        elif default_value and not required:
            field_entry = '{0} = {1}(default={2})' \
                .format(field_entry, field_type, default_value)
        else:
            field_entry = '{0} = {1}({2})' \
                .format(field_entry, field_type, required)
        return field_entry


def traverse_db_data(datum):
    """
    The function is used to parse the YAML dict and look for
    fields and then call build_db_field to get a string representation
    of the field as per mongoengine class requirement

    :param datum:
    :return: Description of mongoengine class fields in string format
    """
    global DB_CLASS_FIELDS
    for key, value in datum.items():
        if isinstance(value, dict):
            traverse_db_data(value)
        else:
            if key == 'fields':
                for item in value:
                    entry = build_db_field(item)
                    DB_CLASS_FIELDS = "{0}{1}{2}".format(DB_CLASS_FIELDS, entry, "\n\t")
    return DB_CLASS_FIELDS


def build_ui_field(item):
    """
    The function is used to build the description of mongoengine
    fields depending on the type in the YAML file description.
    An example of item is given below:
    {'title': {'required': True, 'type': 'text', 'label': 'Title'}}

    :param item:
    :return: string in the following format:
                title = StringField(required=True)
    """

    for keys, values in item.items():
        field_entry = keys
        field_type = ""
        required = ""
        default_value = ""
        if isinstance(values, dict):
            for key, value in values.items():
                if key in ['required', 'type']:
                    if key == 'required':
                        required = key + "=" + str(value)
                    elif key == 'type':
                        if value in ['text', 'textarea', 'dropdown']:
                            field_type = "StringField"
                        elif value == 'textarea':
                            field_type = "TextAreaField"
                        elif value == 'dropdown':
                            field_type = "SelectField"
                        elif value == 'checkbox':
                            field_type = "StringField"
                            default_value = "no"
                        elif value == 'email':
                            field_type = "EmailField"
        if default_value and required:
            field_entry = '{0} = {1}({2}, default={3})' \
                .format(field_entry, field_type, required, default_value)
        elif default_value and not required:
            field_entry = '{0} = {1}(default={2})' \
                .format(field_entry, field_type, default_value)
        else:
            field_entry = '{0} = {1}({2})' \
                .format(field_entry, field_type, required)
        return field_entry, keys


def traverse_ui_data(datum):
    """
    The function is used to parse the YAML dict and look for
    fields and then call build_ui_field to get a string representation
    of the field for the flask GUI Page

    :param datum:
    :return: Description of flask GUI fields in string format
    """
    global UI_CLASS_FIELDS
    global KEYS
    for key, value in datum.items():
        if isinstance(value, dict):
            traverse_ui_data(value)
            # if key not in ('cloudmesh','user', 'meta'):
            # KEYS = KEYS + "\"" + key + "\"" + ","
        else:
            if key == 'fields':
                for item in value:
                    entry, keys = build_ui_field(item)
                    UI_CLASS_FIELDS = "{0}{1}{2}".format(UI_CLASS_FIELDS, entry, "\n\t")
                    KEYS = KEYS + "\"" + keys + "\"" + ","
    return UI_CLASS_FIELDS, KEYS


def user_fields():
    filename = config_file("/cloudmesh_user_intf.yaml")
    data = yaml.load(open(filename))
    fields = traverse_db_data(data)
    print fields
    return fields


def country_list():
    filename = config_file("/cloudmesh_country.yaml")
    data = yaml.load(open(filename))
    countries = []
    for key, value in data.items():
        item = ''
        item = item + str(value.encode(encoding='UTF-8', errors='strict')) + "(" + str(key) + ")"
        countries.append(item)
    countries.sort()
    countries.insert(0, 'United States(US)')
    print countries
    pass


def states_list():
    filename = config_file("/cloudmesh_states.yaml")
    data = yaml.load(open(filename))
    states = []
    for key, value in data.items():
        item = ''
        item = item + str(value['name']) + "(" + str(key) + ")"
        states.append(item)
    states.sort()
    states.insert(0, 'Other(OTH)')
    print states
    pass


def disciplines_list():
    filename = config_file("/cloudmesh_disciplines.yaml")
    data = yaml.load(open(filename))
    disciplines = []
    for key, value in data.items():
        item = ''
        item += str(value['name'])
        disciplines.append(item)
    disciplines.sort()
    disciplines.insert(0, 'Other(OTH)')
    print disciplines
    pass


def project_fields():
    filename = config_file("/cloudmesh_project_intf.yaml")
    data = yaml.load(open(filename))
    fields = traverse_db_data(data)
    print fields
    return fields


def get_current_user():
    filename = path_expand("~/.cloudmesh/{0}/{1}".format("accounts", ".config"))
    with open(filename, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
        username = cfg['user']
    return username


def get_current_user_role():
    filename = path_expand("~/.cloudmesh/{0}/{1}".format("accounts", ".config"))
    with open(filename, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
        username = cfg['user']
    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}
    ##
    ##
    obj = Mongo()
    obj.check_mongo()
    ##
    ##
    get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
    found = User.objects(username=username).only('roles').first()
    return found.roles
    pass

def error_response():
    Console.error("You are not authorized to access the resource.")
    pass


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            authorized = False
            user_roles = get_current_user_role()
            for item in user_roles:
                if item in roles:
                    authorized = authorized or True
                else:
                    authorized = authorized or False
            if not authorized:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@requires_roles('admin')
def notify_user(username, message):
    print "Message to be sent: {0}".format(message)
    pass


# def requires_roles(*roles):
#     def wrapper(f):
#         @wraps(f)
#         def wrapped(*args, **kwargs):
#             if get_current_user_role() not in roles:
#                 return error_response()
#             return f(*args, **kwargs)
#         return wrapped
#     return wrapper

if __name__ == '__main__':
    # country_list()
    # user_fields()
    # states_list()
    # disciplines_list()
    notify_user("donny", "Test Message")