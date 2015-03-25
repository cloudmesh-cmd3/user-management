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
            management version

        Options:
            -h --help       Show this screen

Manage Users
============

To generate a list of users run::

    cm management user generate

To get a list of users run::

    cm management user list

To get detail about a particular user::

    cm management user list USERNAME

To add a user using a YAML file::

    cm management user add <PATH TO YAML FILE>

    Note: A sample YAML file is available in etc directory within managament

To amend a status of the user::

* The state changes for a user is listed in the figure below:

    ..  figure:: docs/management_states.png
        :scale: 50%
        :alt: User states