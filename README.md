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

Hydra Basic Probe check that one service is alive by checking two things:  
*  The PID exists
*  One TCP port is open (this is optional)

You have to specify the file that contains the 


In order to run hydra-basic-probe properly you shoud tune one configuration file `/etc/hydra-basic-probe/hydra-basic-probe.cfg`:

This file has 3 sections:

## MAIN section
This section contains all mandatory options that you should configure
TODO


See <a href="https://raw.githubusercontent.com/innotech/hydra-basic-probe/master/src/hydra-basic-probe.cfg">hydra-basic-probe.cfg</a> example file pre configured for sshd monitoring.  
See <a href="https://raw.githubusercontent.com/innotech/hydra-basic-probe/master/src/nagios-parse-example.txt">nagios-parse-example.txt</a> file for an example of how Hydra Basic Probe parse the NAGIOS file.

# Run
```
sudo /etc/init.d/hydra-basic-probe start
```

# License

(The MIT License)

Authors:  
Germán Ramos &lt;german.ramos@gmail.com&gt;  
Pascual de Juan &lt;pascual.dejuan@gmail.com&gt;  
Jonas da Cruz &lt;unlogic@gmail.com&gt;  
Luis Mesas &lt;luismesas@gmail.com&gt;  
Alejandro Penedo &lt;icedfiend@gmail.com&gt;  
Jose María San José &lt;josem.sanjose@gmail.com&gt;  
  
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
