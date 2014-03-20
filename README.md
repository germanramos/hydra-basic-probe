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
python hydra_basic_probe.py [-c config_file]
```

# Make rpm
http://tecadmin.net/create-rpm-of-your-own-script-in-centosredhat/#
http://blogdrake.net/blog/will/clase-de-empaquetado-rpm-parte-4

tree rpmbuild/
rpmbuild/
├── BUILD
│   ├── hydra_basic_probe-2
│   │   ├── debugfiles.list
│   │   ├── debuglinks.list
│   │   ├── debugsources.list
│   │   ├── elfbins.list
│   │   ├── hydra_basic_probe.cfg
│   │   ├── hydra_basic_probe.py
│   │   ├── nagios_parse_example.txt
│   │   ├── parseStatusDat.py
│   │   └── README.md
│   └── hydra_basic_probe-2.0
│       ├── hydra_basic_probe.cfg
│       ├── hydra_basic_probe.py
│       ├── nagios_parse_example.txt
│       ├── parseStatusDat.py
│       └── README.md
├── BUILDROOT
├── RPMS
│   └── noarch
│       └── hydra_basic_probe-2-0.noarch.rpm
├── SOURCES
│   ├── hydra_basic_probe-2
│   │   ├── hydra_basic_probe.cfg
│   │   ├── hydra_basic_probe.py
│   │   ├── nagios_parse_example.txt
│   │   ├── parseStatusDat.py
│   │   └── README.md
│   └── hydra_basic_probe-2.0.tar.gz
├── SPECS
│   └── hydra_basic_probe.spec
├── SRPMS
│   └── hydra_basic_probe-2-0.src.rpm
└── tmp
    ├── rpm-tmp.gmNrrF
    └── rpm-tmp.JcOP2r

11 directories, 25 files
[ec2-user@ip-172-31-10-20 ~]$ cat .rpmmacros 
%packager German Ramos
%_topdir /home/ec2-user/rpmbuild
%_tmppath /home/ec2-user/rpmbuild/tmp
