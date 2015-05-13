#!/usr/bin/env python

import os
import shutil

from setuptools import setup, find_packages
from setuptools.command.install import install
from cmd3.console import Console


try:
    from cloudmesh_base.util import banner
except:
    os.system("pip install cloudmesh_base")

from cloudmesh_base.util import banner
from cloudmesh_base.util import path_expand
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.util import auto_create_requirements
from cloudmesh_management.class_generator import SourceCode

version = "1.1"


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

requirements = parse_requirements('requirements.txt')

banner("Installing Cloudmesh Base")

home = os.path.expanduser("~")

auto_create_version("cloudmesh_management", version)
auto_create_requirements(requirements)


class SetupYaml(install):
    """Copies a management yaml file to ~/.cloudmesh."""

    description = __doc__

    def run(self):
        banner("Setup the cloudmesh management yaml files ")

        yamlfiles = ['cloudmesh_user.yaml', 'cloudmesh_project.yaml']
        dir_path = path_expand("~/.cloudmesh/{0}".format("accounts"))

        if not os.path.exists(dir_path):
            Shell.mkdir(dir_path)

        for yamlfile in yamlfiles:

            filename = path_expand("~/.cloudmesh/{0}/{1}".format("accounts", yamlfile))

            if os.path.isfile(filename):
                Console.error("File {0} already exists. If you like to reinstall it, please remove the file".format(yamlfile))
            else:
                Console.info("Copying file:  {0} -> {1} ".format(path_expand("etc/{0}/{1}".format("accounts", yamlfile)), filename))
                shutil.copy("etc/{0}/{1}".format("accounts", yamlfile), path_expand("~/.cloudmesh/{0}/{1}".format("accounts", yamlfile)))


class ResetYaml(install):
    """Copies a management yaml file to ~/.cloudmesh."""

    description = __doc__

    def run(self):
        banner("Reset the cloudmesh management yaml files ")

        yaml_files = ['cloudmesh_user.yaml', 'cloudmesh_project.yaml']
        dir_path = path_expand("~/.cloudmesh/{0}".format("accounts"))

        if not os.path.exists(dir_path):
            Shell.mkdir(dir_path)

        for yaml_file in yaml_files:
            filename = path_expand("~/.cloudmesh/{0}/{1}".format("accounts", yaml_file))
            if os.path.isfile(filename):
                Console.info("Removing file:  {0}".format(filename))
                Shell.rm(filename)
                Console.info("Copying file:  {0} -> {1} ".format(path_expand("etc/{0}/{1}".format("accounts", yaml_file)), filename))
                shutil.copy("etc/{0}/{1}".format("accounts", yaml_file), path_expand("~/.cloudmesh/{0}/{1}".format("accounts", yaml_file)))
            else:
                Console.info("Copying file:  {0} -> {1} ".format(path_expand("etc/{0}/{1}".format("accounts", yaml_file)), filename))
                shutil.copy("etc/{0}/{1}".format("accounts", yaml_file), path_expand("~/.cloudmesh/{0}/{1}".format("accounts", yaml_file)))


class ReGenFile(install):
    def run(self):
        banner("Regenerate the python code ")

        python_files = ['user', 'project']

        for item in python_files:
            SourceCode.parse(class_type=item)



# class SetupYaml(install):
#     """Copies a management yaml file to ~/.cloudmesh."""
#
#     description = __doc__
#
#     def run(self):
#         banner("Setup the cloudmesh management yaml files ")
#
#         yamlfiles = ['country.yaml']
#
#         for yamlfile in yamlfiles:
#
#             filename = path_expand("~/.cloudmesh/{0}".format(yamlfile))
#
#             if os.path.isfile(filename):
#                 print ("ERROR: the file {0} already exists".format(yamlfile))
#                 print
#                 print ("If you like to reinstall it, please remove the file")
#             else:
#                 print ("Copy file:  {0} -> {1} ".format(path_expand("etc/{0}".format(yamlfile)), yamlfile))
#                 Shell.mkdir("~/.cloudmesh")
#                 shutil.copy("etc/{0}".format(yamlfile), path_expand("~/.cloudmesh/{0}".format(yamlfile)))


class UploadToPypi(install):
    """Upload the package to pypi."""
    def run(self):
        os.system("Make clean Install")
        os.system("python setup.py install")                
        banner("Build Distribution")
        os.system("python setup.py sdist --format=bztar,zip upload")        


class RegisterWithPypi(install):
    """Upload the package to pypi."""
    def run(self):
        banner("Register with Pypi")
        os.system("python setup.py register")        

        
class InstallBase(install):
    """Install the package."""
    def run(self):
        banner("Install Cloudmesh Base")
        install.run(self)


class InstallRequirements(install):
    """Install the requirements."""
    def run(self):
        banner("Install Cloudmesh Base Requirements")
        os.system("pip install -r requirements.txt")
        

class InstallAll(install):
    """Install requirements and the package."""
    def run(self):
        banner("Install Cloudmesh Base Requirements")
        os.system("pip install -r requirements.txt")
        banner("Install Cloudmesh Base")        
        install.run(self)
        
setup(
    name='cloudmesh_management',
    version=version,
    description='User management for cloudmesh',
    # description-file =
    #    README.rst
    author='The Cloudmesh Team',
    author_email='laszewski@gmail.com',
    url='http://github.org/cloudmesh/management',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7.9',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Boot',
        'Topic :: System :: Systems Administration',
        'Framework :: Flask',
        'Environment :: OpenStack',
    ],
    packages=find_packages(),
    install_requires=requirements,
    cmdclass={
        'install': InstallBase,
        'requirements': InstallRequirements,
        'all': InstallAll,
        'pypi': UploadToPypi,
        'pypiregister': RegisterWithPypi,
        'yaml': SetupYaml,
        'resetyaml': ResetYaml,
        'regenfile': ReGenFile,
        },
)

