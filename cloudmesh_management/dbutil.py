from cloudmesh_database.dbconn import get_mongo_dbname_from_collection, get_mongo_db


class Database:
    _collection = []
    _database = None
    _conn = None

    def __init__(self):
        pass

    def connect(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
        self._conn = get_mongo_db(self._collection)
        if self._conn:
            print self._conn
        else:
            print "Error in getting connection to {0}".format(self._collection)
        pass

    def serialize(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key == "collection":
                self._collection = value
            elif key == "db":
                self._database = value
        print "Database = {0}, Collection = {1}".format(self._database, self._collection)
        pass


if __name__ == "__main__":
    db = Database()
    db.connect(collection="manage")
    # db.serialize(db="manage", collection="user")