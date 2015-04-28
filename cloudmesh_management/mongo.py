import os
import sys
import subprocess

from fabric.api import local, hide, settings
from cloudmesh_base.locations import config_file
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand, banner

#####################################################
#   The code has been taken from mongo.py under
#   "cloudmesh/fabfile"
#####################################################

def get_status(app):
    with hide('output', 'running', 'warnings'):
        output = local("ps -ef | grep {0}".format(app), capture=True).split("\n")
    pid = None
    for item in output:
        if "grep" not in item:
            item = item.lstrip(" ")
            item = item.rstrip(" ")
            pid = item.split(" ")[0]
            break
    return pid is None


def is_yes(value):
    check = str(value).lower()
    if check in ['true', 'false', 'y', 'n', 'yes', 'no']:
        return check in ['true', 'y', 'yes']
    else:
        print "parameter not in", ['true', 'false', 'y', 'n', 'yes', 'no']
        print "found", value, check
        sys.exit()


def start(auth=False):
    """
    Start the mongod service in the location as specified in "cloudmesh_server.yaml"
    """
    banner("Starting mongod")
    config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
    mongo_config = config['cloudmesh']['server']['mongo']
    path = path_expand(mongo_config["path"])
    port = mongo_config["port"]

    if not os.path.exists(path):
        print "Creating mongodb directory in", path
        local("mkdir -p {0}".format(path))

    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            lines = local(
                "ps -ax |grep '[m]ongod.*port {0}'".format(port), capture=True)\
                .split("\n")

    if lines != ['']:
        pid = lines[0].split(" ")[0]
        print "NO ACTION: mongo already running in pid {0} for port {1}"\
            .format(pid, port)
    else:
        print "ACTION: Starting mongod ... Please wait ..."
        print

        with_auth = ""
        if is_yes(auth):
            with_auth = "--auth"

        local(
            'mongod {2} --bind_ip 127.0.0.1 '
            '--fork --dbpath {0} '
            '--logpath {0}/mongodb.log '
            '--port {1}'
            .format(path, port, with_auth))
    pass


def stop():
    """
    Stops the currently running mongod
    """
    # for some reason shutdown does not work
    # local("mongod --shutdown")
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("killall -15 mongod")

    # Added to make sure the mongodb server is shutdown.
    # - killall does not work if the server is running on root or mongodb
    try:
        # this throw error messages in some cases
        # local("echo \"use admin\ndb.shutdownServer()\" | mongo")
        # this ignore the error message in case it occurs
        subprocess.check_output('echo "use admin\ndb.shutdownServer()" | mongo', shell=True)
    except:
        pass


print get_status("mongod")
start(False)