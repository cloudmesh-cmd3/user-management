#!/usr/bin/env python

version = "1.0"


requirements = [
    'future',
    'sh',
    'docopt',
    'pyaml',
    'simplejson',
    'nose',
    'python-hostlist',
    'prettytable',
    'pytimeparse',
    'cloudmesh_base',
    'mongoengine',
    'cloudmesh_database',
    'tabulate',
    'cmd3',
    'fake-factory',
    'cloudmesh_database'
]

import os

from setuptools import setup, find_packages
from setuptools.command.install import install


try:
    from cloudmesh_base.util import banner
except:
    os.system("pip install cloudmesh_base")

from cloudmesh_base.util import banner
from cloudmesh_base.util import path_expand
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.util import auto_create_requirements

banner("Installing Cloudmesh Base")

home = os.path.expanduser("~")

auto_create_version("cloudmesh_management", version)
auto_create_requirements(requirements)


class SetupYaml(install):
    """Copies a management yaml file to ~/.cloudmesh."""

    description = __doc__

    def run(self):
        banner("Setup the cloudmesh management yaml files ")

        yamlfiles = ['country.yaml']

        for yamlfile in yamlfiles:
            
            filename = path_expand("~/.cloudmesh/{0}".format(yamlfile))

            if os.path.isfile(filename):
                print ("ERROR: the file {0} already exists".format(cmd3_yaml))
                print
                print ("If you like to reinstall it, please remove the file")
            else:
                print ("Copy file:  {0} -> {1} ".format(path_expand("etc/{0}".format(yamlfile), yamlfile)))
                Shell.mkdir("~/.cloudmesh")

            shutil.copy("etc/{0}".format(yamlfile, path_expand("~/.cloudmesh/{0}".format(yamlfile))))

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
    description='Usere management for cloudmesh',
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
        'Programming Language :: Python :: 2.7',
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
        },
)

