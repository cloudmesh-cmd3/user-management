import string
import os
import sys
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cmd3.console import Console


class CodeGenerator:
    def __init__(self):
        self.level = 0
        self.tab = "    "
        self.code = []
        self.etc_path = ""
        self.filename = ""

    def end(self):
        return string.join(self.code, "")

    def write(self, snippet):
        self.code.append(self.tab * self.level + snippet)

    def newline(self):
        self.code.append("\n")

    def indent(self):
        self.level += 1

    def dedent(self):
        if self.level == 0:
            print "Syntax error in CodeGenerator:", sys.exc_info()
            raise
        self.level -= 1

    def write_to_file(self, snippet, filename):
        self.etc_path = os.sep.join(os.getcwd().split(os.sep)[:-1])+"/etc/"
        self.filename = self.etc_path+filename+".py"
        target = open(self.filename, 'w+')
        target.write(snippet)
        target.close()


class SourceCode:

    def __init__(self):
        pass

    @classmethod
    def parse(cls, class_type=None):
        code = CodeGenerator()
        file_path = "~/.cloudmesh/cloudmesh_" + class_type + ".yaml"
        try:
            filename = path_expand(file_path)
            file_config = ConfigDict(filename=filename)
        except:
            Console.error("Could not load file, please check filename and its path")
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
                try:
                    code.write_to_file(code.end(), class_type)
                except:
                    print "Unexpected error:", sys.exc_info()
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
                code.write_to_file(code.end(), class_type)
        except:
            print "Error while reading file"
        pass


if __name__ == '__main__':
    generator = SourceCode
    types = ['user', 'project']
    for item in types:
        generator.parse(class_type=item)

