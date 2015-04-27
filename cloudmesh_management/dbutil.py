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

    def connect(self):
        self.DB_CONFIG = {}
        config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        mongo_config = config.get("cloudmesh", "server", "mongo")
        self.DB_CONFIG["host"] = mongo_config["host"]
        self.DB_CONFIG["port"] = int(mongo_config["port"])
        self.DB_CONFIG["username"] = mongo_config["username"]
        self.DB_CONFIG["password"] = mongo_config["password"]
        uri = "mongodb://{0}:{1}@{2}:{3}".format(self.DB_CONFIG["username"],
                                                 self.DB_CONFIG["password"],
                                                 self.DB_CONFIG["host"],
                                                 self.DB_CONFIG["port"])
        try:
            return MongoClient(uri)
        except:
            Console.error("Failed to connect to Mongoclient DB:\n\t "+uri)
        pass

    def serialize(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
            elif key == "db":
                self._database = value
        #
        self._conn = self.connect()
        self._db_conn = self._conn[self._database]
        if not self._collection == "*":
            self._coll_conn = self._db_conn[self._collection]
            #
            dir_name = "dump"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            json_file = dir_name+"/"+self._collection+".json"
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
            implement()
            # for item in self._db_conn.collection_names(include_system_collections=False):
            #     print item

        if self._conn:
            try:
                self._conn.close()
            except:
                Console.error("Error in closing connection..")
        pass

    def de_serialize(self, **kwargs):
        filename = None
        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
            elif key == "db":
                self._database = value
            elif key == "file":
                filename = value
        #
        self._db_conn = DBConnFactory.getconn(self._database)
        if self._collection not in self._db_conn.collection_names():
            self._db_conn.create_collection(self._collection)
        #
        with open(filename, "rb") as f:
            bson_data = f.read()
            json_data = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)', r'{"$oid": "\1"}', bson_data)
            json_data = re.sub(r'Date\s*\(\s*(\S+)\s*\)', r'{"$date": \1}', json_data)
            data = json.loads(json_data, object_hook=json_util.object_hook)
            self._conn = self.connect()
            _db = self._conn[self._database]
            c = _db[self._collection]
            for x in data:
                c.insert(x)
        count = c.count()
        Console.info("{0} records imported into {1}.".format(count, self._collection))
        if self._conn:
            try:
                self._conn.close()
            except:
                Console.error("Error in closing connection..")
        pass



if __name__ == "__main__":
    db = DBUtil()
    db._connect(collection="manage")
    # db.serialize(db="manage", collection="user")