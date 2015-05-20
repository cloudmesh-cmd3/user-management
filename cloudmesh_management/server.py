from flask import Flask
from cloudmesh_management.user import Users

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/management/api/v1.0/users', methods=['GET'])
def list_users():
    user = Users()
    user.list_users()

if __name__ == '__main__':
    app.run(debug=True, port=30000)