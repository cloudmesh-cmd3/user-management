from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_management.cloudmeshobject import CloudmeshObject
from mongoengine import *
import datetime


class User(CloudmeshObject):
    """
    This class is used to represent a Cloudmesh User
    """

    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}
    #
    # defer the connection to where the object is instantiated
    # get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    """
    User fields
    """

    username = StringField(required=True)
    email = EmailField(required=True)
    password = StringField()
    confirm = StringField()
    title = StringField(required=True)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    phone = StringField(required=True)
    url = StringField(required=True)
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    institution = StringField(required=True)
    institutionrole = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    advisor = StringField(required=True)
    country = StringField(required=True)

    """
    Hidden fields
    """

    status = StringField(required=True, default='pending')
    userid = UUIDField()
    # projects = ListField(ReferenceField(Project))

    """
    Message received from either reviewers,
    committee or other users. It is a list because
    there might be more than one message
    """

    message = ListField(StringField())

    @classmethod
    def order(cls):
        """
        Order the attributes to be printed in the display
        method
        """
        try:
            return [
                ("username", cls.username),
                ("status", cls.status),
                ("title", cls.title),
                ("firstname", cls.firstname),
                ("lastname", cls.lastname),
                ("email", cls.email),
                ("url", cls.url),
                ("citizenship", cls.citizenship),
                ("bio", cls.bio),
                ("password", cls.password),
                ("phone", cls.phone),
                ("projects", cls.projects),
                ("institution", cls.institution),
                ("department", cls.department),
                ("address", cls.address),
                ("country", cls.country),
                ("advisor", cls.advisor),
                ("date_modified", cls.date_modified),
                ("date_created", cls.date_created),
                ("date_approved", cls.date_approved),
                ("date_deactivated", cls.date_deactivated),
            ]
        except:
            return None

    @classmethod
    def hidden(cls):
        """
        Hidden attributes
        """
        return [
            "userid",
            "active",
            "message",
        ]


    def is_active(self):
        """
        Check if the user is active
        """
        d1 = datetime.datetime.now()
        return (self.active == True) and (datetime.datetime.now() < self.date_deactivate)

    @classmethod
    def set_password(cls, password):
        """
        Not implemented

        :param password:
        :type password:
        """
        #self.password_hash = generate_password_hash(password)
        pass

    @classmethod
    def check_password(cls, password):
        """
        Not implemented

        :param password:
        :type password:
        """
        # return check_password_hash(self.password_hash, password)
        pass

    @classmethod
    def json(cls):
        """
        Returns a json representation of the object
        """
        d = {}
        for (field, value) in cls.order():
            try:
                d[field] = value
            except:
                pass
        return d

    @classmethod
    def yaml(cls):
        """
        Returns the yaml object of the object.
        """
        return cls.__str__(fields=True, all=True)

    """
    def __str__(self, fields=False, all=False):
        content = ""
        for (field, value)  in self.order():
            try:
                if not (value is None or value == "") or all:
                    if fields:
                        content = content + field + ": "
                    content = content + value + "\n"
            except:
                pass
        return content
    """

###########

STATUS = ('pending', 'approved', 'completed', 'denied')

CATEGORY = ('Database', 'FutureSystems', 'other')

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
    managers = ListField(ReferenceField(User))
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


class SubUser(User):
    projects = ListField(ReferenceField(Project))
