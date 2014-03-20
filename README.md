Hydra Basic Probe
=================

Monitors system resources of the system.
Monitors a proccess and port of our application and notifies to one or more hydra servers

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

## Get source code

```
git clone https://github.com/innotech/hydra_basic_probe.git
```

# Configuring

First tune config file. See example with documetation at nagios_basic_probe.cfg

# Launching
```
python app_manager_info_server.py [-c config_file]
```
