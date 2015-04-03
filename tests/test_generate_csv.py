from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.util import HEADING
from cloudmesh_management.user import Users
import csv
from faker import Factory


class TestGenerate:
    yaml_dir = "~/.cloudmesh_yaml"
    firstname = "gergor"

    def setup(self):
        # HEADING()
        db_name = get_mongo_dbname_from_collection("manage")
        if db_name:
            meta = {'db_alias': db_name}
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        pass

    def teardown(self):
        # HEADING()
        pass


    def test_generate(self):
        HEADING()
        fake = Factory.create()

        spam_writer = csv.writer(open('users.csv', 'wb'), delimiter=',')
        x = 1
        while x in range(5):
            print x
            firstname = fake.first_name()
            print firstname
            prefix = fake.prefix()
            status = "pending"
            title = prefix[0]
            lastname = fake.last_name().encode('ascii', 'ignore')
            email = fake.safe_email()
            username = firstname.lower()
            active = False
            password = fake.word()
            confirm = fake.word()
            phone = fake.phone_number()
            department = "IT"
            institution = fake.company()
            institutionrole = "Graduate Student"
            address = fake.address()
            country = "US"
            citizenship = "US"
            bio = fake.paragraph()
            url = fake.url()
            advisor = fake.name()
            projects = []
            spam_writer.writerow([firstname, status, title, lastname, email, username, active, password,
                                  confirm, phone, department, institution, institutionrole, address, country,
                                  citizenship, bio, url, advisor, projects])
            x += 1



