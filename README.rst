CMD3 Commandline definition example
===================================

In this example we will teach you how simple it is to create separate python modules and add them to cmd3 via the
plugin mechanism. We will use the simple system command ping in this example to ping a machine and to notify the user
 if it is available or not.

The code is located at:

* https://github.com/cloudmesh/cmd3_example.git

  First, please check it out with::

    git clone https://github.com/cloudmesh/cmd3_example.git

 Next enter the directory with::

   cd cmd3_example

You may want to explore two files. One is the code that contains a simple wrapper class to ping. Naturally we could
have omitted that cass, but it shows you how to organize your code as we want to keep the code in the command shell
very limited. This will also simplify testing of the cmd3 extensions more easily.

The code in HostStatus.py contains the the class method HOSTSTATUS.status(hostname) tht we use in the creation of a
shell command next. The shell command is located in the plugin directory in the file:

* cmd3_example/plugins/cm_shell_hoststatus.py

  Edit this file and review with the cmd3 documentation at hand what is happening.

  first we define a class that is later on is used by cmd3. The class contains to methods. An activation method and a do
  method. The activation method must be followed by the classname. The do method is the actual command that we define.

  In the activation method you should not define any big program but only setting variables. Do not use the activation
  method to start databases or other code. This is all to be set in the do method. However you can avoid the repeated
  execution of code in the do method through a boolean variable. In our case we do not such complicated things, but
  just add a "command type" my commands. This is useful in case you have many commands and you like to distinguish them
  in the::

    cm help

command.

To install this command you must have cmd3 installed. you can do this simply with::

  pip install cmd3
  
next you execute (while standing in the cmd3_example directory)::

  python setup.py requirements
  python setup.py install

Now you have installed the example into your environment. However you need to still register this new package with
cmd3. This is easy as you can place the following filr into the directory

  ~/.cloudmesh/cmd3.yaml

::
    meta:
	yaml_version: 2.1
	kind: cmd3
	filename: ${HOME}/.cloudmesh/cmd3.yaml
	location: ${HOME}/.cloudmesh/cmd3.yaml
	prefix: cmd3
    cmd3:
	modules:
	- cloudmesh_cmd3.plugins
	- cloudmesh_docker.plugins
	- cloudmesh_slurm.plugins
	- cloudmesh_deploy.plugins
	- cmd3_example.plugins

Make sure the file does not have any tabs in it.

Now you can start cmd3 with::

  cm

and issue the command

  help

You should be able to see the new command. Or you can just say 

To start it you simply say::

 cm>  hoststatus iu.edu
 
to run it directly from commandline you can use::

  cm hoststatus iu.edu

If you have written extensions with cmd3 let us know we could discuss the creation ofa user contributed space in the
cmd3 git reporsitory.


  








  
 
