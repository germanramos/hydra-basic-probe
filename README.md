App Manager Info Server
=======================

Monitors the system resources and the port our application is listening on and notifies.

# Deploy

## Prerequisites
* build tools (gcc 4.2+, build-essential)
  * yum groupinstall 'Development Tools'
* python 2.6+
* python-devel package
  * yum install python-devel
* pip python package manager 
  * wget https://bitbucket.org/pypa/setuptools/raw/0.7.4/ez_setup.py -O - | python
  * curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  * [sudo] python get-pip.py
* python psutil
  * pip install psutil 
* ssh
* git
* Increase max number of file descriptors - http://www.xenoclast.org/doc/benchmark/HTTP-benchmarking-HOWTO/node7.html


## Get source code

```
git clone https://github.com/innotech/hydra_basic_probe.git
```

# Launching

First start your application on the desired port. Then start the App Manager Info Server

```
python app_manager_info_server.py <host> <public_port> <network_interface> <infoserver_port> <pid>
```

* host - the host of the application, if the App Manager Info Server is in the same machine, you can use localhost.
* public_port - port used by your application (or one of them if many are used)
* network_interface - interface the server will be started (0.0.0.0 for any interface)
* infoserver_port - port used by the App Manager Info Server to receive requests from the App Manager.
* pid - pid of your application.
