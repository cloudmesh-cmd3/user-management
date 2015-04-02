from __future__ import print_function
from cloudmesh_management.generate import generate_users, generate_projects
from cloudmesh_management.user import Users
from cloudmesh_management.project import Projects
from cmd3.console import Console
from cmd3.shell import command


def get_version():
    import cloudmesh_management
    return cloudmesh_management.version


class cm_account_admin:

    def __init__(self):
        pass

    def activate_cm_account_admin(self):
        self.register_command_topic('admin', 'management')

    @command
    def do_management(self, args, arguments):
        """management - Command line option to manage users and projects

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

        Options:
            --help          Show this screen
            --format=json   Show the user details in json format
        """

        # arguments = docopt(management_command.__doc__, args[1:])

        try:
            if arguments['version']:
                Console.info("Version: " + get_version())
            elif arguments['user'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_users(count)
                else:
                    generate_users(10)
            elif arguments['user'] and arguments['list']:
                user = Users()
                display_fmt = None
                user_name = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['USERNAME']:
                    user_name = arguments['USERNAME']
                user.list_users(display_fmt, user_name)
            elif arguments['user'] and arguments['add']:
                user = Users()
                user.create_user_from_file(arguments['YAMLFILE'])
            elif arguments['user'] and arguments['delete']:
                if arguments['USERNAME']:
                    user = Users()
                    user.delete_user(arguments['USERNAME'])
                else:
                    Console.error("Please specify a user to be removed")
            elif arguments['user'] and arguments['clear']:
                user = Users()
                user.clear()
            elif arguments['user'] and arguments['status']:
                user = Users()
                Console.info("Status of user "+arguments['USERNAME']+" "+user.get_user_status(arguments['USERNAME']))
            elif arguments['user'] and arguments['approve']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='approved')
                    Console.info("User "+arguments['USERNAME']+" approved.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['activate']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='active')
                    Console.info("User "+arguments['USERNAME']+" activated.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['suspend']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='suspended')
                    Console.info("User "+arguments['USERNAME']+" suspended.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['block']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='blocked')
                    Console.info("User "+arguments['USERNAME']+" blocked.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['deny']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='denied')
                    Console.info("User "+arguments['USERNAME']+" denied.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['password']:
                user = Users()
                user.set_password(arguments['USERNAME'], arguments['PASSWORD'])
            elif arguments['user'] and arguments['projects']:
                user = Users()
                user.list_projects(arguments['USERNAME'])
            #
            # Project part
            #
            elif arguments['project'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_projects(count)
                    Console.info(str(count)+" projects generated.")
                else:
                    generate_projects(10)
                    Console.info("10 projects generated.")
            elif arguments['project'] and arguments['list']:
                project = Projects()
                display_fmt = None
                project_id = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                project.list_projects(display_fmt, project_id)
            elif arguments['project'] and arguments['add'] and arguments['YAMLFILE']:
                project = Projects()
                project.create_project_from_file(arguments['YAMLFILE'])
            elif arguments['project'] and arguments['delete']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.delete_project(arguments['PROJECTID'])
                else:
                    Console.error("Please specify a project id to be removed")
            elif arguments['project'] and arguments['clear']:
                project = Projects()
                project.clear()
                Console.info("Projects cleared from the database.")
            elif arguments['project'] and arguments['status']:
                project = Projects()
                Console.info("Status of project is: "+project.get_project_status(arguments['PROJECTID']))
            elif arguments['project'] and arguments['activate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'active')
                    Console.info("Project "+arguments['PROJECTID']+" activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['deactivate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'blocked')
                    Console.info("Project "+arguments['PROJECTID']+" de-activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['close']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'closed')
                    Console.info("Project "+arguments['PROJECTID']+" closed.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['add'] and arguments['USERNAME']:
                project = Projects()
                project.add_user(arguments['USERNAME'], arguments['PROJECTID'], arguments['ROLE'])
            elif arguments['project'] and arguments['remove'] and arguments['USERNAME']:
                project = Projects()
                project.remove_user(arguments['USERNAME'], arguments['PROJECTID'], arguments['ROLE'])
        except Exception, e:
            Console.error("Invalid arguments")
            print(e)

    pass

if __name__ == '__main__':
    cmd_object = cm_account_admin()
    cmd_object.do_management()