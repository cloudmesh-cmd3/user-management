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
                management user generate [--count=N]
                management user list [USERNAME] [--format=FORMAT]
                management user add [YAMLFILE]
                management user approve [USERNAME]
                management user activate [USERNAME]
                management user suspend [USERNAME]
                management user block [USERNAME]
                management user deny [USERNAME]
                management user delete [USERNAME]
                management user clear
                management user status USERNAME
                management user password USERNAME PASSWORD
                management project generate [--count=N]
                management project list [PROJECTID] [--format=FORMAT]
                management project clear
                management project delete [PROJECTID]
                management project status [PROJECTID]
                management project activate [PROJECTID]
                management project deactivate [PROJECTID]
                management project close [PROJECTID]
                management project add member [USERNAME] [PROJECTID] [ROLE]
                management project remove member [USERNAME] [PROJECTID]
                management version

            Options:
                -h --help       Show this screen
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

    THe user roles are member, lead, alumni. When adding a user as a member or lead, the USERID should be available
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

