import json
import re
import os

from pymongo import MongoClient
from cloudmesh_database.dbconn import DBConnFactory
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.locations import config_file
from cmd3.console import Console
from bson import json_util
from bson.json_util import dumps


def implement():
    Console.info("Yet to be implemented..")


class DBUtil:
    _collection = None
    _database = None
    _coll_conn = None
    _db_conn = None
    _conn = None
    DB_CONFIG = None

    def __init__(self):
        pass

    def connect(self, **kwargs):
        """
        The method is used to get a connection to a specified database. The hostname and port is being read from the
        cloudmesh_server.yaml file. If the username and password is not mentioned as part of the command line
        arguments, the details are read from the cloudmesh_server.yaml file. If the details are not available in the
        yaml file, it tried to connect without the credentials.

        :param kwargs:
                    Can contain credentials for authentication to the database.

        :return:
                Connection object to the specified server.
        """
        self.DB_CONFIG = {}
        config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        mongo_config = config.get("cloudmesh", "server", "mongo")
        #
        self.DB_CONFIG["host"] = mongo_config["host"]
        self.DB_CONFIG["port"] = int(mongo_config["port"])
        self.DB_CONFIG["username"] = mongo_config["username"]
        self.DB_CONFIG["password"] = mongo_config["password"]
        #
        for key, value in kwargs.iteritems():
            if key == "user_name":
                if value:
                    self.DB_CONFIG["username"] = value
            elif key == "pwd":
                if value:
                    self.DB_CONFIG["password"] = value

        if self.DB_CONFIG["username"] and self.DB_CONFIG["password"]:
            uri = "mongodb://{0}:{1}@{2}:{3}".format(self.DB_CONFIG["username"],
                                                     self.DB_CONFIG["password"],
                                                     self.DB_CONFIG["host"],
                                                     self.DB_CONFIG["port"])
        else:
            uri = "mongodb://{0}:{1}".format(self.DB_CONFIG["host"],
                                             self.DB_CONFIG["port"])

        try:
            return MongoClient(uri)
        except:
            Console.error("Failed to connect to Mongoclient DB. May be an authentication issue.\n\t ")
        pass

    def serialize(self, **kwargs):
        """
        The method is used to export the data from the requested collection into a json file

        :param kwargs:
                    Can contain a collection name, database name, credentials for authentication to
                    the database.

                    If a collection name is not specified, it tries to export all the collections within the
                    database.
        :return:
                Saves the data into a json file named after the collection. The file will be saved under
                dump/<database>/
        """
        username = None
        password = None
        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
            elif key == "db":
                self._database = value
            elif key == "user_name":
                username = value
            elif key == "pwd":
                password = value
        #
        if self._database:
            self._conn = self.connect(user_name=username, pwd=password)
            if self._conn:
                self._db_conn = self._conn[self._database]
                if not self._collection == "*":
                    self._coll_conn = self._db_conn[self._collection]
                    #
                    dir_name = "dump"
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                    sub_dir = dir_name+"/"+self._database
                    if not os.path.exists(sub_dir):
                        os.makedirs(sub_dir)
                    json_file = sub_dir+"/"+self._collection+".json"
                    if self._db_conn:
                        docs = self._coll_conn.find()
                        if self._coll_conn.find().count() > 0:
                            with open(json_file, "w") as outfile:
                                dump = dumps([doc for doc in docs])
                                outfile.write(dump)
                            Console.info(" Collection - {0} - written to file - {1}".format(self._collection, json_file))
                        else:
                            Console.info("Looks like collection is empty.")
                    else:
                        Console.error("Error in getting connection to the collection..")
                else:
                    # implement()
                    for item in self._db_conn.collection_names(include_system_collections=False):
                        self._coll_conn = self._db_conn[item]
                        #
                        dir_name = "dump"
                        if not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        sub_dir = dir_name+"/"+self._database
                        if not os.path.exists(sub_dir):
                            os.makedirs(sub_dir)
                        json_file = sub_dir+"/"+item+".json"
                        if self._db_conn:
                            docs = self._coll_conn.find()
                            if self._coll_conn.find().count() > 0:
                                with open(json_file, "w") as outfile:
                                    dump = dumps([doc for doc in docs])
                                    outfile.write(dump)
                                Console.info(" Collection - {0} - written to file - {1}".format(item, json_file))
                            else:
                                Console.info("Looks like the collection \"{0}\" is empty.".format(item))
                        else:
                            Console.error("Error in getting connection to the collection..")
            if self._conn:
                try:
                    self._conn.close()
                except:
                    Console.error("Error in closing connection..")
        else:
            Console.error("Please specify a database name.")
        pass

    def de_serialize(self, **kwargs):
        """
        The method is used to import the data in the provided json file into a collection within the database

        :param kwargs:
                    Can contain a collection name, database name, file name, directory name containing the json files,
                     credentials for authentication to the database.

                    If a collection name is not specified, uses the name of the file as the collection name or name of
                    the files in the specified directory as the collection name.
        :return:
                None
        """

        filename = None
        username = None
        password = None
        dir_name = None

        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
            elif key == "db":
                self._database = value
            elif key == "file":
                filename = value
            elif key == "dir":
                dir_name = value
            elif key == "user_name":
                username = value
            elif key == "pwd":
                password = value
        #
        if self._database:
            if filename is None and dir_name is None:
                Console.error("Please specify a filename or a directory name that contains the data to be imported.")
                return

            if filename:
                if not self._collection:
                    sep1_idx = filename.rfind('/')
                    if sep1_idx == -1:
                        sep1_idx = 0
                    if filename.rfind('.') != -1:
                        self._collection = filename[sep1_idx+1:filename.rfind('.')]
                    else:
                        self._collection = filename[sep1_idx:]

                self._db_conn = DBConnFactory.getconn(self._database)
                if self._collection not in self._db_conn.collection_names():
                    self._db_conn.create_collection(self._collection)
                #
                self._conn = self.connect(user_name=username, pwd=password)
                if self._conn:
                    f = None
                    try:
                        f = open(filename, "rb")
                        bson_data = f.read()
                        json_data = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)', r'{"$oid": "\1"}', bson_data)
                        json_data = re.sub(r'Date\s*\(\s*(\S+)\s*\)', r'{"$date": \1}', json_data)
                        data = json.loads(json_data, object_hook=json_util.object_hook)
                        _db = self._conn[self._database]
                        c = _db[self._collection]
                        for x in data:
                            c.insert(x)
                        count = c.count()
                        Console.info("{0} records imported into {1}.".format(count, self._collection))
                    except IOError:
                        Console.error("File not found: {0}".format(filename))

                if self._conn:
                    try:
                        self._conn.close()
                    except:
                        Console.error("Error in closing connection..")

            if dir_name:
                if os.path.isdir(dir_name):
                    if os.listdir(dir_name):
                        for file_item in os.listdir(dir_name):
                            if file_item.endswith(".json"):
                                if file_item.rfind('.') != -1:
                                    self._collection = file_item[0:file_item.rfind('.')]
                                else:
                                    self._collection = filename[0:]

                            Console.info(self._collection)

                            self._db_conn = DBConnFactory.getconn(self._database)
                            if self._collection not in self._db_conn.collection_names():
                                self._db_conn.create_collection(self._collection)
                            #
                            self._conn = self.connect(user_name=username, pwd=password)
                            if self._conn:
                                f = None
                                try:
                                    f = open(dir_name+"/"+file_item, "rb")
                                    bson_data = f.read()
                                    json_data = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)', r'{"$oid": "\1"}', bson_data)
                                    json_data = re.sub(r'Date\s*\(\s*(\S+)\s*\)', r'{"$date": \1}', json_data)
                                    data = json.loads(json_data, object_hook=json_util.object_hook)
                                    _db = self._conn[self._database]
                                    c = _db[self._collection]
                                    for x in data:
                                        c.insert(x)
                                    count = c.count()
                                    Console.info("{0} records imported into {1}.".format(count, self._collection))
                                except IOError:
                                    Console.error("Error in opening file: {0}".format(filename))

                            if self._conn:
                                try:
                                    self._conn.close()
                                except:
                                    Console.error("Error in closing connection..")
                    else:
                        Console.error("Source Directory - {0} - is empty.".format(dir_name))
                    return
                else:
                    Console.error("Invalid Source Directory - {0}.".format(dir_name))
        else:
            Console.error("Please specify a target database.")
        pass


if __name__ == "__main__":
    db = DBUtil()
    db.connect(collection="manage")
    # db.serialize(db="manage", collection="user")