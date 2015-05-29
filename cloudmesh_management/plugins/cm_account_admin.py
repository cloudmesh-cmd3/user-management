from __future__ import print_function

from cmd3.console import Console
from cmd3.shell import command

from cloudmesh_management.generate import generate_users, generate_projects
from cloudmesh_management.user import Users
from cloudmesh_management.project import Projects
from cloudmesh_management.committee import Committees
from cloudmesh_management.dbutil import DBUtil
from cloudmesh_management.util import get_current_user

import yaml


def implement():
    print("Yet to be implemented.")


def get_version():
    import cloudmesh_management
    return cloudmesh_management.version


class cm_account_admin:
    def activate_cm_account_admin(self):
        self.register_command_topic('mycommands', 'management')

    @command
    def do_management(self, args, arguments):
        """management: Command line for Administrators to manage users and projects

        Usage:
            management version
            management admin user generate [--count=N]
            management admin user list [USERNAME] [--format=FORMAT]
            management admin user add [YAMLFILE]
            management admin user delete [USERNAME]
            management admin user clear
            management admin user status USERNAME
            management admin user approve [USERNAME]
            management admin user activate [USERNAME]
            management admin user suspend [USERNAME]
            management admin user block [USERNAME]
            management admin user deny [USERNAME]
            management admin user assign [USERNAME] [ROLE]
            management admin user password USERNAME PASSWORD
            management admin user projects USERNAME
            management admin project generate [--count=N]
            management admin project list [PROJECTID] [--format=FORMAT]
            management admin project add [YAMLFILE]
            management admin project delete [PROJECTID]
            management admin project clear
            management admin project status [PROJECTID]
            management admin project activate [PROJECTID]
            management admin project deactivate [PROJECTID]
            management admin project close [PROJECTID]
            management admin project add [USERNAME] [PROJECTID] [ROLE]
            management admin project remove [USERNAME] [PROJECTID] [ROLE]
            management admin export [DATABASE] [COLLECTION] [--user=USERNAME] [--password=PASSWORD]
            management admin import [--file=FILENAME] [--dir=DIRNAME] [--db=DBNAME] [--collection=NAME]  [--user=USERNAME] [--password=PASSWORD]
            management committee setup [PROJECTID]
            management committee remove [PROJECTID]
            management committee reviewer add [PROJECTID] [USERNAME]
            management committee reviewer remove [PROJECTID] [USERNAME]
            management committee list
            management committee project list [PROJECTID] [--format=FORMAT]
            management committee project status
            management committee project approve [PROJECTID]
            management committee project deny [PROJECTID]
            management committee project block [PROJECTID]
            management committee project activate [PROJECTID]
            management committee project close [PROJECTID]
            management committee project open [PROJECTID]
            management user apply [--user=USERFILE|--project=PROJECTFILE]
            management user configure [USERNAME]
            management user password
            management user status
            management user add-sshkey [FILENAME]

        Options:
            --format=json   Show the user details in json format
        """

        # arguments = docopt(management_command.__doc__, args[1:])

        try:
            if arguments['version']:
                Console.info("Version: " + get_version())
            elif arguments['admin'] and arguments['user'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_users(count)
                else:
                    generate_users(10)
            elif arguments['admin'] and arguments['user'] and arguments['list']:
                user = Users()
                display_fmt = None
                user_name = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['USERNAME']:
                    user_name = arguments['USERNAME']
                user.list_users(display_fmt, user_name)
            elif arguments['admin'] and arguments['user'] and arguments['add']:
                user = Users()
                user.create_user_from_file(arguments['YAMLFILE'])
            elif arguments['admin'] and arguments['user'] and arguments['delete']:
                if arguments['USERNAME']:
                    user = Users()
                    user.delete_user(arguments['USERNAME'])
                else:
                    Console.error("Please specify a user to be removed")
            elif arguments['admin'] and arguments['user'] and arguments['clear']:
                user = Users()
                user.clear()
            elif arguments['admin'] and arguments['user'] and arguments['status']:
                user = Users()
                user_status = user.get_user_status(arguments['USERNAME'])
                if user_status:
                    Console.info(
                        "Status of user " + arguments['USERNAME'] + " - " + user.get_user_status(arguments['USERNAME']))
                else:
                    Console.info("User {0} not available in the database.".format(arguments['USERNAME']))
                return
            elif arguments['admin'] and arguments['user'] and arguments['approve']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='approved')
                    Console.info("User " + arguments['USERNAME'] + " approved.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['admin'] and arguments['user'] and arguments['activate']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='active')
                    Console.info("User " + arguments['USERNAME'] + " activated.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['admin'] and arguments['user'] and arguments['suspend']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='suspended')
                    Console.info("User " + arguments['USERNAME'] + " suspended.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['admin'] and arguments['user'] and arguments['block']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='blocked')
                    Console.info("User " + arguments['USERNAME'] + " blocked.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['admin'] and arguments['user'] and arguments['deny']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='denied')
                    Console.info("User " + arguments['USERNAME'] + " denied.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['admin'] and arguments['user'] and arguments['assign']:
                if arguments['USERNAME'] and arguments['ROLE']:
                    user = Users()
                    user.set_role(arguments['USERNAME'], arguments['ROLE'])
            elif arguments['admin'] and arguments['user'] and arguments['password']:
                user = Users()
                user.set_password(arguments['USERNAME'], arguments['PASSWORD'])
            elif arguments['admin'] and arguments['user'] and arguments['projects']:
                user = Users()
                user.list_projects(arguments['USERNAME'])
            #
            # Project part
            #
            elif arguments['admin'] and arguments['project'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_projects(count)
                    Console.info(str(count) + " projects generated.")
                else:
                    generate_projects(10)
                    Console.info("10 projects generated.")
            elif arguments['admin'] and arguments['project'] and arguments['list']:
                project = Projects()
                display_fmt = None
                project_id = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                project.list_projects(display_fmt, project_id)
            elif arguments['admin'] and arguments['project'] and arguments['add'] and arguments['YAMLFILE']:
                project = Projects()
                project.create_project_from_file(arguments['YAMLFILE'])
            elif arguments['admin'] and arguments['project'] and arguments['delete']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.delete_project(arguments['PROJECTID'])
                else:
                    Console.error("Please specify a project id to be removed")
            elif arguments['admin'] and arguments['project'] and arguments['clear']:
                project = Projects()
                project.clear()
                Console.info("Projects cleared from the database.")
            elif arguments['admin'] and arguments['project'] and arguments['status']:
                project = Projects()
                Console.info("Status of project is: " + project.get_project_status(arguments['PROJECTID']))
            elif arguments['admin'] and arguments['project'] and arguments['activate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'active')
                    Console.info("Project " + arguments['PROJECTID'] + " activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['admin'] and arguments['project'] and arguments['deactivate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'blocked')
                    Console.info("Project " + arguments['PROJECTID'] + " de-activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['admin'] and arguments['project'] and arguments['close']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'closed')
                    Console.info("Project " + arguments['PROJECTID'] + " closed.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['admin'] and arguments['project'] and arguments['add'] and arguments['USERNAME']:
                project = Projects()
                project.add_user(arguments['USERNAME'], arguments['PROJECTID'], arguments['ROLE'])
            elif arguments['admin'] and arguments['project'] and arguments['remove'] and arguments['USERNAME']:
                project = Projects()
                project.remove_user(arguments['USERNAME'], arguments['PROJECTID'], arguments['ROLE'])
            #
            # Database export/import part
            #
            elif arguments['admin'] and arguments['export']:
                database = None
                username = None
                password = None
                if arguments['DATABASE']:
                    database = arguments['DATABASE']
                else:
                    Console.info("Please specify the database..")
                #
                if arguments['COLLECTION']:
                    coll_name = arguments['COLLECTION']
                else:
                    coll_name = "*"
                #
                if arguments['--user']:
                    username = arguments['--user']

                if arguments['--password']:
                    password = arguments['--password']
                #
                DBUtil().serialize(db=database,
                                   collection=coll_name,
                                   user_name=username,
                                   pwd=password)
            elif arguments['admin'] and arguments['import']:
                database = None
                coll_name = None
                filename = None
                username = None
                password = None
                dir_name = None

                if arguments['--file']:
                    filename = arguments['--file']

                if arguments['--dir']:
                    dir_name = arguments['--dir']

                if arguments['--db']:
                    database = arguments['--db']

                if arguments['--collection']:
                    coll_name = arguments['--collection']

                if arguments['--user']:
                    username = arguments['--user']

                if arguments['--password']:
                    password = arguments['--password']
                #
                DBUtil().de_serialize(file=filename,
                                      dir=dir_name,
                                      db=database,
                                      collection=coll_name,
                                      user_name=username,
                                      pwd=password)
            #
            #
            # COMMITTEE SECTION
            #
            #
            elif arguments['committee'] and arguments['setup']:
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                    committee = Committees()
                    committee.setup_committee(project_id)
                else:
                    Console.error("Please specify a valid project ID.")
            elif arguments['committee'] and arguments['remove']:
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                    committee = Committees()
                    committee.remove_committee(project_id)
                else:
                    Console.error("Please specify a valid project ID.")
            elif arguments['committee'] and arguments['reviewer'] and arguments['add']:
                if arguments['USERNAME'] and arguments['PROJECTID']:
                    username = arguments['USERNAME']
                    project_id = arguments['PROJECTID']
                    committee = Committees()
                    committee.add_reviewers(project_id, username)
                    Console.info("User {0} added as a reviewer for the project with ID {1}".format(username, project_id))
                else:
                    Console.error("Please specify a project ID and user name.")
            elif arguments['committee'] and arguments['reviewer'] and arguments['remove']:
                if arguments['USERNAME'] and arguments['PROJECTID']:
                    username = arguments['USERNAME']
                    project_id = arguments['PROJECTID']
                    committee = Committees()
                    committee.remove_reviewers(project_id, username)
                    Console.info("User {0} added as a reviewer for the project with ID {1}".format(username, project_id))
                else:
                    Console.error("Please specify a project ID and user name.")
            elif arguments['committee'] and arguments['list']:
                committee = Committees()
                committee.list_committee()
            elif arguments['committee'] and arguments['project'] and arguments['status']:
                project = Projects()
                Console.info("Status of project is: " + project.get_project_status(arguments['PROJECTID']))
            elif arguments['committee'] and arguments['project'] and arguments['list']:
                project = Projects()
                display_fmt = None
                project_id = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                project.list_projects(display_fmt, project_id)
            elif arguments['committee'] and arguments['project'] and arguments['approve']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.amend_project_status(arguments['PROJECTID'], 'approved')
                    Console.info("Project " + arguments['PROJECTID'] + " approved.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['committee'] and arguments['project'] and arguments['deny']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.amend_project_status(arguments['PROJECTID'], 'denied')
                    Console.info("Project " + arguments['PROJECTID'] + " denied.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['committee'] and arguments['project'] and arguments['block']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.amend_project_status(arguments['PROJECTID'], 'blocked')
                    Console.info("Project " + arguments['PROJECTID'] + " blocked.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['committee'] and arguments['project'] and arguments['activate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'active')
                    Console.info("Project " + arguments['PROJECTID'] + " activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['committee'] and arguments['project'] and arguments['close']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.amend_project_status(arguments['PROJECTID'], 'closed')
                    Console.info("Project " + arguments['PROJECTID'] + " closed.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['committee'] and arguments['project'] and arguments['open']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.amend_project_status(arguments['PROJECTID'], 'opened')
                    Console.info("Project " + arguments['PROJECTID'] + " opened.")
                else:
                    Console.error("Please specify a project to be amended")
            #
            #
            # USER SECTION
            #
            #
            elif arguments['user'] and arguments['apply']:
                if arguments['--user']:
                    user = Users()
                    user.create_user_from_file(arguments['--user'])
                elif arguments['--project']:
                    project = Projects()
                    project.create_project_from_file(arguments['--project'])
                else:
                    Console.info("Submit a yaml file in the following format if you are applying for a user account:")
                    with open('etc/cloudmesh_user_info.yaml', 'r') as f:
                        doc = yaml.load(f)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(yaml.dump(doc, default_flow_style=False))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    Console.info("Submit a yaml file in the following format if you want to setup a project:")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    with open('etc/cloudmesh_project_info.yaml', 'r') as f:
                        doc = yaml.load(f)
                    print(yaml.dump(doc, default_flow_style=False))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            elif arguments['user'] and arguments['configure']:
                if arguments['USERNAME']:
                    user = Users()
                    user.create_config(arguments['USERNAME'])
                else:
                    Console.error("Please specify a username to configure.")
            elif arguments['user'] and arguments['password']:
                user = Users()
                current_user = get_current_user()
                if current_user:
                    if current_user == arguments['user']:
                        user.set_password(arguments['user'], arguments['password'])
                    else:
                        Console.error("Set the password for your username.")
                else:
                    Console.error("Local User configuration not found.")
                implement()
            elif arguments['user'] and arguments['status']:
                implement()
        except Exception, e:
            Console.error("Invalid arguments")
            print(e)

    pass


if __name__ == '__main__':
    cmd_object = cm_account_admin()
    cmd_object.do_management()
