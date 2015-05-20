from __future__ import print_function

from cmd3.console import Console
from cmd3.shell import command

from cloudmesh_management.user import Users
from cloudmesh_management.project import Projects


def IMPLEMENT():
    print("Yet to be implemented.")


def get_version():
    import cloudmesh_management
    return cloudmesh_management.version


class cm_committee_admin:

    def activate_cm_committee_admin(self):
        self.register_command_topic('admin', 'committee')

    @command
    def do_committee(self, args, arguments):
        """management - Command line option to manage users and projects

        Usage:
            committee version
            committee user list [USERNAME]
            committee user status
            committee user details [PROJECTID] [--format=FORMAT]
            committee user approve [PROJECTID]
            committee user deny [PROJECTID]
            committee project list [PROJECTID]
            committee project status
            committee project details [PROJECTID] [--format=FORMAT]
            committee project approve [PROJECTID]
            committee project deny [PROJECTID]
            committee project suspend [PROJECTID]
            committee project activate [PROJECTID]
            committee project close [PROJECTID]
            committee project open [PROJECTID]

        Options:
            --format=json   Show the project details in json format
        """

        # arguments = docopt(management_command.__doc__, args[1:])

        try:
            if arguments['version']:
                Console.info("Version: " + get_version())
            elif arguments['user'] and arguments['list']:
                user = Users()
                display_fmt = None
                user_name = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['USERNAME']:
                    user_name = arguments['USERNAME']
                user.list_users(display_fmt, user_name)
            elif arguments['user'] and arguments['status']:
                user = Users()
                Console.info("Status of user "+arguments['USERNAME']+" "+user.get_user_status(arguments['USERNAME']))
            elif arguments['user'] and arguments['status']:
                IMPLEMENT()
            elif arguments['user'] and arguments['approve']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='approved')
                    Console.info("User "+arguments['USERNAME']+" approved.")
                else:
                    Console.error("Please specify a user to be amended")
            elif arguments['user'] and arguments['deny']:
                if arguments['USERNAME']:
                    user = Users()
                    user.amend_user_status(arguments['USERNAME'], new_status='denied')
                    Console.info("User "+arguments['USERNAME']+" denied.")
                else:
                    Console.error("Please specify a user to be amended")
            #
            # Project part
            #
            elif arguments['project'] and arguments['status']:
                project = Projects()
                Console.info("Status of project is: "+project.get_project_status(arguments['PROJECTID']))
            elif arguments['project'] and arguments['list']:
                project = Projects()
                display_fmt = None
                project_id = None
                if arguments['--format']:
                    display_fmt = arguments['--format']
                if arguments['PROJECTID']:
                    project_id = arguments['PROJECTID']
                project.list_projects(display_fmt, project_id)
            elif arguments['project'] and arguments['details']:
                IMPLEMENT()
            elif arguments['project'] and arguments['approve']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'approved')
                    Console.info("Project "+arguments['PROJECTID']+" approved.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['deny']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'denied')
                    Console.info("Project "+arguments['PROJECTID']+" denied.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['suspend']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'suspended')
                    Console.info("Project "+arguments['PROJECTID']+" suspended.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['activate']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'active')
                    Console.info("Project "+arguments['PROJECTID']+" activated.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['close']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'closed')
                    Console.info("Project "+arguments['PROJECTID']+" closed.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['close']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'closed')
                    Console.info("Project "+arguments['PROJECTID']+" closed.")
                else:
                    Console.error("Please specify a project to be amended")
            elif arguments['project'] and arguments['open']:
                if arguments['PROJECTID']:
                    project = Projects()
                    project.set_project_status(arguments['PROJECTID'], 'opened')
                    Console.info("Project "+arguments['PROJECTID']+" opened.")
                else:
                    Console.error("Please specify a project to be amended")
        except Exception, e:
            Console.error("Invalid arguments")
            print(e)

    pass

if __name__ == '__main__':
    cmd_object = cm_committee_admin()
    cmd_object.do_management()
