from __future__ import print_function

from cloudmesh_management.generate import generate_users, generate_projects
from cloudmesh_management.user import Users
from cloudmesh_management.project import Projects

from cmd3.console import Console
from cmd3.shell import command


class cm_account_admin:

    def activate_cm_account_admin (self):
        self.register_command_topic('admin', 'management')

    @command
    def do_management(self, args, arguments):
        """management - Command line option to manage users and projects

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
            management version

        Options:
            -h --help       Show this screen
            --version       Show version
            --format=FORMAT Output format: table, json
            --all           Displays all users
        """

        # arguments = docopt(management_command.__doc__, args[1:])

        try:
            if arguments['user'] and arguments['list']:
                user = Users()
                display_fmt = None
                user_name = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['USERNAME']:
                    user_name = arguments['USERNAME']
                user.list_users(display_fmt, user_name)
            elif arguments['user'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_users(count)
                    Console.info(str(count)+" users generated.")
                else:
                    generate_users(10)
                    Console.info("10 users generated.")
            elif arguments['user'] and arguments['clear']:
                user = Users()
                user.clear()
                Console.info("Users cleared from the database.")
            elif arguments['user'] and arguments['delete']:
                if arguments['USERNAME']:
                    user = Users()
                    user.delete_user(arguments['USERNAME'])
                    Console.info("User "+arguments['USERNAME']+" removed from the database.")
                else:
                    Console.error("Please specify a user to be removed")
            elif arguments['user'] and arguments['approve']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='approved')
                    Console.info("User "+arguments['USERNAME']+" approved.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['activate']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='active')
                    Console.info("User "+arguments['USERNAME']+" activated.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['suspend']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='suspended')
                    Console.info("User "+arguments['USERNAME']+" suspended.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['block']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='blocked')
                    Console.info("User "+arguments['USERNAME']+" blocked.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['deny']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='denied')
                    Console.info("User "+arguments['USERNAME']+" denied.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['status']:
                user = Users()
                Console.info("Status of user "+arguments['USERNAME']+" "+user.get_user_status(arguments['USERNAME']))
            elif arguments['user'] and arguments['add']:
                user = Users()
                user.create_user_from_file(arguments['YAMLFILE'])
            elif arguments['user'] and arguments['password']:
                user = Users()
                user.set_password(arguments['USERNAME'], arguments['PASSWORD'])
            #
            # Project part
            #
            elif arguments['project'] and arguments['generate']:
                if arguments['--count']:
                    count = int(arguments['--count'])
                    generate_projects(count)
                    Console.info(str(count)+" projects generated.")
                else:
                    generate_users(10)
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
        except Exception, e:
            Console.error("Invalid arguments")
            print(e)

    pass

if __name__ == '__main__':
    cmd_object = cm_account_admin()
    cmd_object.do_management()