from cloudmesh_database.dbconn import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmeshobject import CloudmeshObject
from cloudmesh_management.user import User, Users
from cmd3.console import Console
from mongoengine import *
from tabulate import tabulate
import json
from bson.objectid import ObjectId
import uuid
import sys


def implement():
    print "IMPLEMENT ME"


STATUS = ('pending',
          'approved',
          'completed',
          'denied')

CATEGORY = ('Database', 'FutureGrid', 'other')

DISCIPLINE = ('other')
# see https://ncsesdata.nsf.gov/nsf/srs/webcasp/data/gradstud.htm
# put in discipline.txt and initialize from there through reading the file and codes
#

INSTITUTE_ROLE = ('graduate student',
                  'undergraduate student',
                  'staff',
                  'faculty',
                  'visitor',
                  'other')

CLUSTERS = ('india',
            'bravo',
            'echo',
            'delta',
            'other', 'None')

SERVICES = ('eucalyptus',
            'openstack',
            'mpi',
            'hadoop',
            'mapreduce',
            'docker',
            'other',
            'None')

SOFTWARE = ('HPC', 'other')

PROVISIONING = ('vm',
                'baremetal',
                'container',
                'iaas',
                'paas',
                'other', 'None')

GRANT_ORG = ('NSF',
             'DOE',
             'DoD',
             'NIH',
             'other', 'None')

REQUIRED = False


class Project(CloudmeshObject):
    # named connection (not 'default')
    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}

    '''
    The project object with its fields. The current fields include

    Attributes:

        title
        abstract
        intellectual_merit
        broader_impact
        use_of_fg
        scale_of_use
        categories
        keywords
        primary_discipline
        orientation
        contact
        url
        comment
        active
        projectid
        status
        lead
        managers
        members
        alumnis
        grant_orgnization
        grant_id
        grant_url
        results
        aggreement_use
        aggreement_slides
        aggreement_support
        aggreement_sotfware
        aggreement_documentation
        comments
        join_open
        join_notification
        resources_services
        resources_software
        resources_clusters
        resources_provision

    '''

    # -------------------------------------------------------------------
    # Project Information
    # -------------------------------------------------------------------
    title = StringField(max_length=30, required=REQUIRED)

    # -------------------------------------------------------------------
    # Project Vocabulary
    # -------------------------------------------------------------------

    categories = ListField(StringField(choices=CATEGORY), required=REQUIRED)
    keywords = ListField(StringField(), required=REQUIRED)

    # -------------------------------------------------------------------
    # Project Contact
    # -------------------------------------------------------------------

    # lead_institutional_role =  StringField(choices=INSTITUTE_ROLE, required=REQUIRED)
    lead = ReferenceField(User)
    managers = ListField(StringField())
    members = ListField(ReferenceField(User))
    alumnis = ListField(StringField())
    contact = StringField(required=REQUIRED)
    # active_members = lead u managers u members - alumnis
    # if not active : active_members = None

    # -------------------------------------------------------------------
    # Project Details
    # -------------------------------------------------------------------

    orientation = StringField(required=REQUIRED)
    primary_discipline = StringField(choices=DISCIPLINE, required=REQUIRED)
    abstract = StringField(required=REQUIRED)
    intellectual_merit = StringField(required=REQUIRED)
    broader_impact = StringField(required=REQUIRED)
    url = URLField(required=REQUIRED)
    results = StringField()

    # -------------------------------------------------------------------
    # Agreements
    # -------------------------------------------------------------------
    agreement_use = BooleanField()
    agreement_slides = BooleanField()
    agreement_support = BooleanField()
    agreement_software = BooleanField()
    agreement_documentation = BooleanField()

    # -------------------------------------------------------------------
    # Grant Information
    # -------------------------------------------------------------------
    grant_organization = StringField(choices=GRANT_ORG)
    grant_id = StringField()
    grant_url = URLField()

    # -------------------------------------------------------------------
    # Resources
    # -------------------------------------------------------------------
    resources_services = ListField(
        StringField(choices=SERVICES), required=REQUIRED)
    resources_software = ListField(
        StringField(choices=SOFTWARE), required=REQUIRED)
    resources_clusters = ListField(
        StringField(choices=CLUSTERS), required=REQUIRED)
    resources_provision = ListField(
        StringField(choices=PROVISIONING), required=REQUIRED)
    comment = StringField()
    use_of_fg = StringField(required=REQUIRED)
    scale_of_use = StringField(required=REQUIRED)

    # -------------------------------------------------------------------
    # Other
    # -------------------------------------------------------------------

    comments = StringField()

    # -------------------------------------------------------------------
    # Project Membership Management
    # -------------------------------------------------------------------
    join_open = BooleanField()
    join_notification = BooleanField()

    # -------------------------------------------------------------------
    # Location
    # -------------------------------------------------------------------

    loc_name = StringField()
    loc_street = StringField()
    loc_additional = StringField()
    loc_state = StringField()
    loc_country = StringField()

    # example search in a list field
    # Project.objects(categories__contains='education')

    active = BooleanField(required=REQUIRED)
    project_id = UUIDField()

    status = StringField(choices=STATUS, required=REQUIRED)
    # maybe we do not need active as this may be covered in status

    # -------------------------------------------------------------------
    # Project Committee: contains all the information about the projects committee
    # -------------------------------------------------------------------
    # comittee = ReferenceField(Committee)

    # BUG how can we add also arbitrary info in case of other, maybe omit
    # choices

    def to_json(self):
        """
        prints the project as a json object
        """

        d = {
            "title": self.title,
            "categories": self.categories,
            "keywords": self.keywords,
            "lead": self.lead,
            "managers": self.managers,
            "members": self.members,
            "alumnis": self.alumnis,
            "contact": self.contact,
            "orientation": self.orientation,
            "primary_discipline": self.primary_discipline,
            "abstract": self.abstract,
            "intellectual_merit": self.intellectual_merit,
            "broader_impact": self.broader_impact,
            "url": self.url,
            "results": self.results,
            "agreement_use": self.agreement_use,
            "agreement_slides": self.agreement_slides,
            "agreement_support": self.agreement_support,
            "agreement_software": self.agreement_software,
            "agreement_documentation": self.agreement_documentation,
            "grant_organization": self.grant_organization,
            "grant_id": self.grant_id,
            "grant_url": self.grant_url,
            "resources_services": self.resources_services,
            "resources_software": self.resources_software,
            "resources_clusters": self.resources_clusters,
            "resources_provision": self.resources_provision,
            "comment": self.comment,
            "use_of_fg": self.use_of_fg,
            "scale_of_use": self.scale_of_use,
            "comments": self.comments,
            "join_open": self.join_open,
            "join_notification": self.join_notification,
            "loc_name": self.loc_name,
            "loc_street": self.loc_street,
            "loc_additional": self.loc_additional,
            "loc_state": self.loc_state,
            "loc_country": self.loc_country,
            "active": self.active,
            "project_id": self.project_id,
            "status": self.status
        }
        return d

    def __str__(self):
        """
        Printing the object as a string
        """
        d = self.to_json()
        return str(d)


class Projects(object):
    """
    Convenience object to manage multiple projects
    """

    def __init__(self):
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        self.projects = Project.objects()
        self.users = User.objects()

    def __str__(self):
        """
        not implemented
        """
        implement()

    @classmethod
    def find(cls):
        return Project.objects()

    @classmethod
    def objects(cls):
        """
        Returns the projects
        """
        return Project.objects()

    @classmethod
    def save(cls, project):
        """
        Adds a project to the database but only after it has been verified

        :param project: the project id
        :type project: uuid
        """
        project.save()

    @classmethod
    def add_user(cls, user_name, project_id, role):
        """
        Adds a member to the project.

        :param role: the role of the user
        :type role: String
        :param user_name: the username
        :type user_name: String
        :param project: the project id
        :type project: uuid
        """
        """adds members to a particular project"""
        user = User.objects(username=user_name).first()
        if user and role != 'alumni':
            if role == "member":
                Project.objects(project_id=project_id).update_one(push__members=user)
                Console.info("User `{0}` added as Project member.".format(user_name))
            elif role == "lead":
                Project.objects(project_id=project_id).update_one(set__lead=user)
                Console.info("User `{0}` set as Lead.".format(user_name))
            else:
                Console.error("Role `{0}` cannot be amended".format(role))
        elif role == 'alumni':
            Project.objects(project_id=project_id).update_one(push__alumnis=user_name)
            Console.info("User `{0}` added as Alumni.".format(user_name))
        else:
            Console.error("The user `{0}` has not registered with Future Systems".format(user_name))

    @classmethod
    def find_users(cls, project, role):
        '''returns all the members of a particular project

        :param role: the role of the user
        :type role: String
        :param project: the project id
        :type project: uuid
        '''
        if role == "member":
            return project.members
        elif role == "lead":
            return project.leads
        elif role == "lead":
            return project.alumni

    @classmethod
    def find_by_id(cls, id):
        '''
        finds projects by if

        :param id: the project id
        :type id: uuid
        '''
        """Finds a project by the given id"""
        found = Project.objects(projectid=id)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None
            # User ID or project ID

    @classmethod
    def find_by_category(cls, category):
        '''
        find the project by category

        :param category: the category
        :type category: String
        '''
        """Finds and returns all project in that category"""
        found = Project.objects(categories=category)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    @classmethod
    def find_by_keyword(cls, keyword):
        '''
        finds a projects matching a keyword

        :param keyword: a keyword
        :type keyword: String
        '''
        """Finds and returns all projects with the entered keyword"""
        found = Project.objects(keyword=keyword)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    @classmethod
    def add(cls, project):
        """
        Adds a project

        :param project: the username
        :type project: String
        """

        if not project.status:
            project.status = 'pending'
        if (project.project_id is None) or (project.project_id == ""):
            found = False
            proposed_id = None
            project.project_id = proposed_id
        project.save()

    @classmethod
    def list_projects(cls, display_fmt=None, project_id=None):
        req_fields = ["title", "status", "lead", "managers", "members", "project_id"]
        try:
            if project_id is None:
                projects_json = Project.objects.only(*req_fields).to_json()
                projects_dict = json.loads(projects_json)
                if projects_dict:
                    if display_fmt != 'json':
                        cls.display(projects_dict, project_id)
                    else:
                        cls.display_json(projects_dict, project_id)
                else:
                    Console.error("No projects in the database.")
        except:
            Console.error("Oops.. Something went wrong in the list projects method "+sys.exc_info()[0])
        pass

    @classmethod
    def display(cls, project_dicts=None, project_id=None):
        if bool(project_dicts):
            values = []
            for entry in project_dicts:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    if key == "lead":
                        user = User.objects.get(id=ObjectId(value.get('$oid')))
                        lead_name = user.firstname+" "+user.lastname
                        items.append(lead_name)
                    elif key == "members":
                        entry=""
                        for item in value:
                            user = User.objects.get(id=ObjectId(item.get('$oid')))
                            entry += user.firstname+" "+user.lastname+","
                        entry = entry.strip(',')
                        items.append(entry)
                    elif key == "managers":
                        entry=""
                        for item in value:
                            entry += item.encode('ascii','ignore')
                        entry = entry.strip(', ')
                        items.append(entry)
                    elif key == "project_id":
                        items.append(value.get('$uuid').encode('ascii','ignore'))
                    else:
                        items.append(value)
                    headers.append(key.replace('_', ' ').title())
                values.append(items)
            table_fmt = "orgtbl"
            table = tabulate(values, headers, table_fmt)
            separator = ''
            try:
                seperator = table.split("\n")[1].replace("|", "+")
            except:
                separator = "-" * 50
            print separator
            print table
            print separator
        else:
            if project_id:
                Console.error("No project in the system with name '{0}'".format(project_id))

    @classmethod
    def display_json(cls, project_dict=None, project_id=None):
        if bool(project_dict):
            # pprint.pprint(user_json)
            print json.dumps(project_dict, indent=4)
        else:
            if project_id:
                Console.error("No project in the system with name '{0}'".format(project_id))


    @classmethod
    def clear(cls):
        """removes all projects from the database"""
        for project in Project.objects:
            project.delete()

    @classmethod
    def delete_project(cls, project_id=None):
        if project_id:
            try:
                project = Project.objects(project_id=project_id)
                if project:
                    project.delete()
                    Console.info("Project with id `{0}` removed from the database.".format(project_id))
                else:
                    Console.error("Project with id `{0}` does not exist.".format(project_id))
            except:
                Console.error("Oops! Something went wrong while trying to remove a project")
        else:
            Console.error("Please specify the project to be removed")

    @classmethod
    def amend_project_status(cls, project_id=None, new_status=None):
        current_status = ""
        if project_id:
            try:
                current_status = cls.get_project_status(project_id)
            except:
                Console.error("Oops! Something went wrong while trying to get project status")

            if new_status == "active":
                if current_status in ["pending", "blocked"]:
                    cls.set_project_status(project_id, new_status)
                else:
                    Console.error("Cannot activate project. Project is not in pending/blocked status.")
            elif new_status == "block":
                if current_status in ["active", "pending"]:
                    cls.set_project_status(project_id, new_status)
                else:
                    Console.error("Cannot block project. Project is not active or pending.")
            elif new_status == "close":
                if current_status in ["active", "pending", "blocked"]:
                    cls.set_project_status(project_id, new_status)
                else:
                    Console.error("Cannot close project. Project is not active/pending/blocked.")
        else:
            Console.error("Please specify the project to be amended")

    @classmethod
    def get_project_status(cls, project_id):
        if project_id:
            try:
                project = Project.objects(project_id=project_id).only('status')
                if project:
                    for entry in project:
                        return entry.status
            except:
                Console.error("Oops! Something went wrong while trying to get user status")
        else:
            Console.error("Please specify the user get status")


    @classmethod
    def set_project_status(cls, project_id, status):
        if project_id:
            try:
                Project.objects(project_id=project_id).update_one(set__status=status)
            except:
                Console.error("Oops! Something went wrong while trying to amend project status")
        else:
            Console.error("Please specify the project to be amended")
