from cloudmesh_database.dbconn import get_mongo_db, DBConnFactory
from cloudmesh_management.project import Projects
from cloudmesh_management.user import Users
# from cloudmesh_management.base_classes import Project, SubUser
from cloudmesh_management.base_user import User
from cloudmesh_management.base_project import Project
from cmd3.console import Console
from faker import Factory
from pprint import pprint
import uuid

get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

# --------------------------------------------
# The generate class generates 10 random users
# --------------------------------------------

users = Users()
projects = Projects()

# http://www.joke2k.net/faker

fake = Factory.create()


def random_user():
    """
    Returns a random user in a dict

    :rtype: dict
    """
    firstname = fake.first_name()
    prefix = fake.prefix()
    data = User(
        status="pending",
        title=prefix[0],
        firstname=firstname,
        lastname=fake.last_name(),
        email=fake.safe_email(),
        username=firstname.lower(),
        active=False,
        password=fake.word(),
        phone=fake.phone_number(),
        department="IT",
        institution=fake.company(),
        institutionrole="Graduate Student",
        address=fake.address(),
        country="USA",
        citizenship="US",
        bio=fake.paragraph(),
        url=fake.url(),
        advisor=fake.name(),
        confirm=fake.word(),
        projects=[],
    )
    return data


def generate_users(n):
    """
    Generates n random users in an array containing dicts for users

    :param n: number of users
    :type n: integer
    :rtype: array of dicts
    """
    users.clear()
    for i in range(0, n):
        data = random_user()
        users.add(data)
    Console.info(str(n)+" users generated.")


def random_project():
    """
    Generates a random project in dict
    
    :rtype: dict
    """
    user = User.objects.first()

    data = Project(
        title=fake.sentence()[:30],
        categories=['FutureSystems'],
        keywords=['sqllite'],
        lead=[user],
        managers=[user],
        members=[user],
        alumnis=[fake.name()],
        contact=fake.name() + "\n" + fake.address(),
        orientation="Lot's of all make",
        primary_discipline="other",
        abstract=fake.paragraph(),
        intellectual_merit=fake.paragraph(),
        broader_impact=fake.paragraph(),
        url=fake.url(),
        results=fake.sentence(),
        agreement_use=True,
        agreement_slides=True,
        agreement_support=True,
        agreement_software=True,
        agreement_documentation=True,
        grant_organization=["NSF"],
        grant_id="1001",
        grant_url=fake.url(),
        resources_services=['Hadoop'],
        resources_software=['Other'],
        resources_clusters=['India'],
        resources_provision=['PaaS'],
        comment=fake.sentence(),
        use_of_fs=fake.paragraph(),
        scale_of_use=fake.paragraph(),
        comments=fake.sentence(),
        join_open=True,
        join_notification=True,
        loc_name=fake.country(),
        loc_street=fake.street_name(),
        loc_additional="None",
        loc_state=fake.state(),
        loc_country=fake.country(),
        active=False,
        project_id=uuid.uuid4(),
        status="pending"
    )
    return data


def generate_projects(n):
    """
    Generates n random projects in an array containing dicts for users

    :param n: number of projects
    :type n: integer
    :rtype: array of dicts
    """
    projects.clear()
    for i in range(0, n):
        data = random_project()
        projects.save(data)


def main():
    """
    Test function to create 10 users and 3 projects
    """

    # generate_users(10)
    generate_projects(3)

    print 70 * "="
    print users.find()
    print 70 * "="
    print 70 * "&"
    print users.find()[0]

    _projects = Project.objects()
    print _projects.count()
    pprint(_projects[0])


if __name__ == "__main__":
    main()
