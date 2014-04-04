Hydra Basic Probe
=================

[![Build Status](https://travis-ci.org/innotech/hydra-basic-probe.png)](https://travis-ci.org/innotech/hydra-basic-probe)

Monitors system resources of the system.  
Monitors a proccess and port of our application and notifies to one or more hydra servers

# Installation

## Ubuntu/Debian
```
dpkg -i hydra-basic-probe-2-0.noarch.deb
apt-get install -f
```
## CentOS/RedHat/Fedora
```
yum install python-psutil-0.6.1-1.el6.x86_64.rpm hydra-basic-probe-2-0.noarch.rpm 
```

# Configuration

First, tune configuration at /etc/hydra-basic-probe.  
See hydra-basic-probe.cfg file pre configured for sshd monitoring.  
See NAGIOS example parsed file nagios-parse-example.txt

# Run
```
sudo /etc/init.d/hydra-basic-probe start
```
