from flask import Flask
from cloudmesh_management.user import Users
from cloudmesh_database.dbconn import get_mongo_db, DBConnFactory

app = Flask(__name__)

get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)


@app.route('/management/api/v1.0/users', methods=['GET'])
def list_users():
    user = Users()
    user.list_users()

if __name__ == '__main__':
    app.run(debug=True, port=30000)