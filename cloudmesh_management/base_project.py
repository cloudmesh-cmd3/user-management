from cloudmesh_database.dbconn import get_mongo_dbname_from_collection
from cloudmesh_management.cloudmeshobject import CloudmeshObject
from mongoengine import *

GRANT_ORGANIZATION = ('NSF', 'DOE', 'DoD', 'NIH', 'other', 'None')
RESOURCES_SERVICES = ('Eucalyptus', 'Openstack', 'MPI', 'Hadoop', 'Mapreduce', 'Docker', 'Other', 'None')
RESOURCES_SOFTWARE = ('HPC', 'Other')
RESOURCES_CLUSTERS = ('India', 'Bravo', 'Echo', 'Delta', 'Other', 'None')
RESOURCES_PROVISION = ('VM', 'Baremetal', 'Container', 'IaaS', 'PaaS', 'Other', 'None')


class Project(CloudmeshObject):
    db_name = get_mongo_dbname_from_collection("manage")
    if db_name:
        meta = {'db_alias': db_name}

    """
    Hidden Fields
    """
    status = StringField(required=True, default='pending')
    project_id = UUIDField()
    
    """
    Project Fields
    """
    title = StringField(required=True)
    categories = ListField(required=True)
    keywords = ListField(required=True)
    lead = ListField(ReferenceField('User'))
    managers = ListField(ReferenceField('User'))
    members = ListField(ReferenceField('User'))
    alumnis = ListField(required=True)
    contact = StringField(required=True)
    orientation = StringField(required=True)
    primary_discipline = StringField(required=True)
    abstract = StringField(required=True)
    intellectual_merit = StringField(required=True)
    broader_impact = StringField(required=True)
    url = StringField(required=True)
    results = StringField(required=True)
    agreement_use = BooleanField(required=True)
    agreement_slides = BooleanField(required=True)
    agreement_support = BooleanField(required=True)
    agreement_software = BooleanField(required=True)
    agreement_documentation = BooleanField(required=True)
    grant_organization = ListField(StringField(choices=GRANT_ORGANIZATION), required=True)
    grant_id = StringField()
    grant_url = URLField()
    resources_services = ListField(StringField(choices=RESOURCES_SERVICES), required=True)
    resources_software = ListField(StringField(choices=RESOURCES_SOFTWARE), required=True)
    resources_clusters = ListField(StringField(choices=RESOURCES_CLUSTERS), required=True)
    resources_provision = ListField(StringField(choices=RESOURCES_PROVISION), required=True)
    comment = StringField(required=True)
    use_of_fs = StringField(required=True)
    scale_of_use = StringField(required=True)
    comments = StringField(required=True)
    join_open = BooleanField(required=True)
    join_notification = BooleanField(required=True)
    loc_name = StringField(required=True)
    loc_street = StringField(required=True)
    loc_additional = StringField(required=True)
    loc_state = StringField(required=True)
    loc_country = StringField(required=True)
