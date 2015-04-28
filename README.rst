Command line User and Project Management
========================================

This module deals with management of users and projects using CMD3.

The code is located at:

* https://github.com/cloudmesh/management.git

Assumptions:

* Python 2.7.9 is installed
* virtual environment is installed and setup (for example, virtualenv ~/ENV -p <path to python version 2.7.9>)
* Cloudmesh is installed
* mongo server is running (fab server.start)

Clone the project with::

    git clone https://github.com/cloudmesh/management.git

Change to the cloned directory::

    cd management

Setup the requirements with::

    python setup.py requirements

Install the module::

    python setup.py install

If you are starting from scratch, the commands that needs to be run are listed below::

    pip install cloudmesh_base
    pip install cmd3
    pip install cloudmesh_database
    python setup.py requirements
    python setup.py install

If everything is setup correctly, run the following command::

    cm management -h

You should see the screen below::

    management - Command line option to manage users and projects

        Usage:
            management version
            management user generate [--count=N]
            management user list [USERNAME] [--format=FORMAT]
            management user add [YAMLFILE]
            management user delete [USERNAME]
            management user clear
            management user status USERNAME
            management user approve [USERNAME]
            management user activate [USERNAME]
            management user suspend [USERNAME]
            management user block [USERNAME]
            management user deny [USERNAME]
            management user password USERNAME PASSWORD
            management user projects USERNAME
            management project generate [--count=N]
            management project list [PROJECTID] [--format=FORMAT]
            management project add [YAMLFILE]
            management project delete [PROJECTID]
            management project clear
            management project status [PROJECTID]
            management project activate [PROJECTID]
            management project deactivate [PROJECTID]
            management project close [PROJECTID]
            management project add [USERNAME] [PROJECTID] [ROLE]
            management project remove [USERNAME] [PROJECTID] [ROLE]
            management export [DATABASE] [COLLECTION] [--user=USERNAME] [--password=PASSWORD]
            management import [--file=FILENAME] [--dir=DIRNAME] [--db=DBNAME] [--collection=NAME]  [--user=USERNAME] [--password=PASSWORD]

        Options:
            --help          Show this screen
            --format=json   Show the user details in json format


Manage Users
============

To generate a list of users run::

    cm management user generate

To generate "n" number of users run::

    cm management user generate --count=n

To clear all the users within the database::

    cm management user clear

To set a password for a user::

    cm management user password <USERNAME> <PASSWORD>

To get a list of users run::

    cm management user list

To get detail about a particular user::

    cm management user list USERNAME

To add a user using a YAML file::

    cm management user add <PATH TO YAML FILE>

.. note::

    A sample YAML file is available in etc directory within managament

To amend a status of the user::

* User will be in pending state by default
* The commands to change the user status are self explanatory

.. note::

The state changes for a user is listed in the figure below:

..  figure:: docs/management_states.png
:scale: 50%
    :align: center
        :alt: User states

Manage Projects
===============

To generate a list of projects run::

    cm management project generate

To generate "n" number of dummy projects::

    cm management project generate --count=n

To clear the projects within the database::

    cm management project clear

To add a member to a project::

    cm management project add member <USERID> <PROJECTID> <ROLE>


.. note::

    The user roles are member, lead, alumni. When adding a user as a member or lead, the USERID should be available
    within the database. If not an error message would be displayed. An alumni need not be a valid user within the
    system. No no check will be done against the alumni role. When you add a user as a lead or a member, user will be
    appended to the existing list accordingly.

To remove a member from a project::

    cm management project remove member <USERID> <PROJECTID>

To activate a project::

    cm management project activate <PROJECT ID>

To deactivate a project::

    cm management project deactivate <PROJECT ID>

To close a project::

    cm management project close <PROJECT ID>

Export/Import Collections
=========================

To export collection(s) from a database::

    cm management export <DATABASENAME> <COLLECTION NAME>

.. note::

    - To pass the username and password to access the database as parameters use --user=<USERNAME> and --password=<PASSWORD>. If the username and password is not passed, the system tried to get the details from the file, cloudmesh_server.yaml. If the details are not available in the yaml file, it tries to connect without them.

    - If <COLLECTION NAME> is not specified, the system tries to export all the non system collections to a json file
    names after the collection.


To import data from json file into a database::

    cm management import --file=<FILE NAME> --db=<DATABASE NAME>

                        or

    cm management import --dir=<DIR NAME> --db=<DATABASE NAME>

.. note::

    - To pass the username and password to access the database as parameters use --user=<USERNAME> and --password=<PASSWORD>. If the username and password is not passed, the system tried to get the details from the file, cloudmesh_server.yaml. If the details are not available in the yaml file, it tries to connect without them.

    - A file name or a directory name needs to be passed as source of the data.


Things partially completed
==========================

Create Mongo Class definition from yaml file
    The file class_generator.py has the code which reads the yaml file and depending on the contents of the files
    writes it to a python file named after the yaml file. The thing left out is to combine the definition with the
    methods that use the class definitions.

Start mongo if mongo is not running while using the "cm management" commands
    The file mongo.py has the code that is taken from mongo.py under fabfile directory in cloudmesh. This has three
    methods: "get_status", "start" and "stop". Need to understand the way cm works and where to hook these methods.