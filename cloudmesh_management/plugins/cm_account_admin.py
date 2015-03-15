from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command

from cloudmesh_management.generate_classes import project_fields, user_fields
from cloudmesh_management.generate import generate_users
from cloudmesh_management.user import Users
from docopt import docopt
import sys


class cm_account_admin:

    def activate_cm_account_admin (self):
        self.register_command_topic('admin', 'management')

    @command
    def do_management(self, args, arguments):
        """cm-management - Command line option to manage users and projects

        Usage:
            management user generate [--count=N]
            management user list [USERNAME] [--format=FORMAT]
            management user clear
            management user add [YAMLFILE]
            management user delete [USERNAME]
            management user activate [USERNAME]
            management user deactivate [USERNAME]
            management user approve [USERNAME]
            management user deny [USERNAME]
            management project generate
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
                else:
                    generate_users(10)
            elif arguments['user'] and arguments['clear']:
                user = Users()
                user.clear()
            elif arguments['user'] and arguments['delete']:
                if arguments['USERNAME']:
                    user = Users()
                    user.delete_user(arguments['USERNAME'])
                else:
                    Console.info("Error: Please specify a user to be removed")
            elif arguments['user'] and arguments['approve']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='approved')
            elif arguments['user'] and arguments['deny']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], status='denied')
            elif arguments['project']:
                Console.info("Dummy Projects")
            elif arguments['list']:
                print("Listing Users")
        except Exception, e:
            Console.error("Invalid arguments")
            print(e)

    pass

if __name__ == '__main__':
    cmd_object = cm_account_admin()
    cmd_object.do_management()