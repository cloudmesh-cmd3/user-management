import string
import os
import sys
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cmd3.console import Console


class CodeGenerator:
    """
    The class contains methods that is used to provide the necessary formatting for the python statement
    to be written to a file.
    """
    def __init__(self):
        self.level = 0
        self.tab = "    "
        self.code = []
        self.etc_path = ""
        self.filename = ""

    def end(self):
        return string.join(self.code, "")

    def write(self, snippet):
        """
        The method is used to add the provided "snippet" according to the tab level. For example,
            if the level is 0,
                it appends it as code[some line number] = "snippet"
            if the level is 1,
                it appends it as code[some line number] = "    snippet"
        :param snippet:
                String to be written to the file
        :return:
                None
        """
        self.code.append(self.tab * self.level + snippet)

    def newline(self):
        self.code.append("\n")

    def indent(self):
        """
        Method is used to add a tab
        :return:
        """
        self.level += 1

    def dedent(self):
        """
        Method is used to remove a tab.
        :return: None
        """
        if self.level == 0:
            print "Syntax error in CodeGenerator:", sys.exc_info()
            raise
        self.level -= 1

    def write_to_file(self, snippet, filename):
        """
        Method is used to write the "snippet" into the "filename" being passed
        :param snippet:
                Contains the content of the file to be written
        :param filename:
                File name to which the contents would be written to.
        :return:
                True is write was successful
                False, for any issues
        """
        target = None
        self.etc_path = os.sep.join(os.getcwd().split(os.sep)[:-1])+"/etc/"
        if not os.path.exists(self.etc_path):
            os.makedirs(self.etc_path)
        self.filename = self.etc_path+filename+".py"
        try:
            target = open(self.filename, 'w+')
        except IOError:
            Console.error("Error in opening the file.")
            return False
        else:
            if target:
                try:
                    target.write(snippet)
                except IOError:
                    Console.error("Error in writing to file")
                    return False
            target.close()
            return True



class SourceCode:

    def __init__(self):
        pass

    @classmethod
    def parse(cls, class_type=None):
        """
        The method is used to parse the contents of the yaml file and generate the python code for the same. At the
        moment the method tries to read the file from ~/.cloudmesh. Depending on the class_type, it looks for the file
        "cloudmesh_user.yaml" or "cloudmesh_project.yaml"

        :param class_type:
                    class_type can be either user or project.

                    If a collection name is not specified, uses the name of the file as the collection name.
        :return:
                Writes the contents to a file under the etc directory. if an "etc" directory does not exist, it creates
                one. The file name would be either "user.py" or "project.py" depending on the class_type
        """
        code = CodeGenerator()
        file_path = "~/.cloudmesh/cloudmesh_" + class_type + ".yaml"
        try:
            filename = path_expand(file_path)
            file_config = ConfigDict(filename=filename)
        except:
            Console.error("Could not load file, please check filepath: {0}".format(file_path))
            return
        try:
            if class_type == "user":
                code.write("from cloudmesh_database.dbconn import get_mongo_dbname_from_collection")
                code.newline()
                code.write("from cloudmesh_management.cloudmeshobject import CloudmeshObject")
                code.newline()
                code.write("from mongoengine import *")
                code.newline()
                code.newline()
                code.newline()
                code.write("class "+class_type.title()+"(CloudmeshObject):")
                code.newline()
                code.indent()
                code.write("db_name = get_mongo_dbname_from_collection(\"manage\")")
                code.newline()
                code.write("if db_name:")
                code.newline()
                code.indent()
                code.write("meta = {'db_alias': db_name}")
                code.newline()
                code.dedent()
                code.newline()
                code.write("\"\"\"")
                code.newline()
                code.write("Hidden Fields")
                code.newline()
                code.write("\"\"\"")
                code.newline()
                code.write("status = StringField(required=True, default='pending')")
                code.newline()
                code.write("userid = UUIDField()")
                code.newline()
                #
                code.write("\n")
                code.write("\"\"\"")
                code.newline()
                code.write("User Fields")
                code.newline()
                code.write("\"\"\"")
                code.newline()
                #
                config = file_config.get("cloudmesh", "user", "fields")
                for _item in config:
                    for key in _item:
                        field = key
                        field_type = ""
                        is_required = _item[key].get('required')
                        if _item[key].get('type') in ['text', 'textarea', 'dropdown', 'password']:
                            field_type = "StringField"
                            if is_required:
                                field_type += "(required=True)"
                        elif _item[key].get('type') == 'checkbox':
                            if len(_item[key].get('options')) > 1:
                                options = str(_item[key].get('options'))
                                if is_required:
                                    field_type = "ListField(choices="+options+", required=True)"
                            else:
                                field_type = "BooleanField(required=True)"
                        elif _item[key].get('type') == 'email':
                            field_type = "EmailField"
                            if is_required:
                                field_type += "(required=True)"
                        line = field+" = "+field_type
                        code.write(line)
                        code.newline()
                code.write("projects = ListField(ReferenceField('Project'))")
                # print code.end()

                if not code.write_to_file(code.end(), class_type):
                    Console.error("Error while trying to write to file.")
                    pass

            elif class_type == "project":
                code.write("from cloudmesh_database.dbconn import get_mongo_dbname_from_collection")
                code.newline()
                code.write("from cloudmesh_management.cloudmeshobject import CloudmeshObject")
                code.newline()
                code.write("from mongoengine import *")
                code.newline()
                code.newline()
                code.newline()
                code.write("class "+class_type.title()+"(CloudmeshObject):")
                code.newline()
                code.indent()
                code.write("db_name = get_mongo_dbname_from_collection(\"manage\")")
                code.newline()
                code.write("if db_name:")
                code.newline()
                code.indent()
                code.write("meta = {'db_alias': db_name}")
                code.newline()
                code.dedent()
                code.newline()
                code.write("\"\"\"")
                code.newline()
                code.write("Hidden Fields")
                code.newline()
                code.write("\"\"\"")
                code.newline()
                code.write("status = StringField(required=True, default='pending')")
                code.newline()
                code.write("project_id = UUIDField()")
                code.newline()
                #
                code.write("\n")
                code.write("\"\"\"")
                code.newline()
                code.write("Project Fields")
                code.newline()
                code.write("\"\"\"")
                code.newline()
                #
                config = file_config.get("cloudmesh", "project", "fields")
                for _item in config:
                    for key in _item:
                        field = key
                        field_type = ""
                        is_required = _item[key].get('required')
                        if _item[key].get('type') in ['text', 'textarea', 'dropdown', 'password']:
                            if _item[key].get('reference'):
                                field_type = "ListField(ReferenceField('"+str(_item[key].get('reference')).title()+"'))"
                            elif _item[key].get('options'):
                                options = str(_item[key].get('options'))
                                field_type = "StringField(choices="+options+", required=True)"
                            else:
                                field_type = "StringField"
                                if is_required:
                                    field_type += "(required=True)"
                                else:
                                    field_type += "()"
                        elif _item[key].get('type') == 'checkbox':
                            if len(_item[key].get('options')) > 1:
                                options = str(_item[key].get('options'))
                                field_type = "ListField(choices="+options+", required=True)"
                            else:
                                field_type = "BooleanField(required=True)"
                        elif _item[key].get('type') == 'email':
                            field_type = "EmailField"
                            if is_required:
                                field_type += "(required=True)"
                        elif _item[key].get('type') == 'url':
                            field_type = "URLField"
                            if is_required:
                                field_type += "(required=True)"
                            else:
                                field_type += "()"
                        line = field+" = "+field_type
                        code.write(line)
                        code.newline()
                # print code.end()
                if not code.write_to_file(code.end(), class_type):
                    Console.error("Error while trying to write to file.")
                    pass

        except:
            Console.error("Error while reading file.")
        pass


if __name__ == '__main__':
    generator = SourceCode
    types = ['user', 'project']
    for item in types:
        generator.parse(class_type=item)

