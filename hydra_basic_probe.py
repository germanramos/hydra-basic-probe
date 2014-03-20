#!/usr/bin/env python
# encoding: utf-8
'''
hydra basic probe -- Simple probe for hydra. Proactive version

The hydra basic probe is in charge of check and monitor one server and update the status information at one or several Hydra Servers using the restful server API.

The basic functionality is to notify to one Hydra Server when an application is Started, Stopping, or Removed. In addition, it will provide information about the server health status like CPU and memory usage and any useful information like the size of the server or the prefered balance strategy.

All these information should be updated periodically. If not, the Hydra server will assume that the servers are shutted down.

@author:     German Ramos Garcia
'''

import time
import sys
import os
import json
import logging
from logging.config import fileConfig   
from optparse import OptionParser
import urllib2
import ConfigParser
import psutil
import socket
import parseStatusDat

__all__ = []
__version__ = 2.0
__date__ = '2014-03-20'
__updated__ = '2014-03-20'

TESTRUN = 0
PROFILE = 0
config = 0

class stateEnum:
    READY = 0
    NOT_RUNNING = 1
    NOT_LISTENING = 2

def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return stateEnum.READY
    except:
        return stateEnum.NOT_LISTENING

def check():
    data = {"state": stateEnum.NOT_RUNNING}
    try:
        # Check process
        f = open(config.get("MAIN", "pid_file"), 'r+')
        PID = f.read()
        f.close()
        logging.debug("Checking PID " + PID.strip())
        connections = len(psutil.Process(int(PID)).get_connections(kind='inet'))
        data["connections"] = connections
        
        # Check CPU and Memory
        logging.debug("Checking CPU and Memory")
        data["cpuLoad"] = psutil.cpu_percent(interval=0.1, percpu=False)
        data["memLoad"] = psutil.virtual_memory().percent
        
        # Check port open (if option exists) 
        if config.get("MAIN", "check_enabled") == "true" and config.has_option("MAIN", "check_host") and config.has_option("MAIN", "check_port"):
            logging.debug("Checking Host and Port")
            data["state"] = isOpen(config.get("MAIN", "check_host"), int(config.get("MAIN", "check_port")))
        else:
            data["state"] = stateEnum.READY
             
    except Exception, e:
        data["state"] = stateEnum.NOT_RUNNING
              
    return data

def send(data):
    answer = json.dumps(data)
    logging.debug("Data to post:")
    logging.debug(answer)
    #POST
    for key,hydra in config.items("HYDRAS"):
        logging.debug("Posting to " + hydra)                   
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(hydra + "/app/" + config.get("MAIN", "app_id"), answer)
        request.add_header("content-type", "application/json")
        #request.get_method = lambda: 'POST'
        url = opener.open(request)
        if url.code != 200:
            logging.error("Error connecting with hydra {0}: Code: {1}".format(hydra,url.code))
        else:
            logging.debug("Posted OK")
            
def getNagios():
    result = {}
    try:
        if config.has_section("NAGIOS"):
            nagios = parseStatusDat.parseFile(config.get("NAGIOS","nagios_dat_file"))             
            for key,path in config.items("NAGIOS")[1:]:
                splitted = path.split(":")
                value = nagios
                for i in range(len(splitted)):
                    value = value[splitted[i]]
                result[key] = value
    except Exception, e:
        logging.error("Exception in getNagios: " + str(e))
    return result

def main(argv=None):
    '''Command line options.'''
    
    program_name = os.path.basename(sys.argv[0])
    program_version = "v2.0"
    program_build_date = "%s" % __updated__
 
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "MIT License"
 
    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-c", "--config", default="hydra_basic_probe.cfg", dest="configFile", action="store", help="set configuration file [default: %default]")
      
        # process options
        (opts, _args) = parser.parse_args(argv)
        
        global config
        config = ConfigParser.ConfigParser()
        #config.read(['app_manager.cfg', os.path.expanduser('~/app_manager.cfg'), '/etc/app_manager.cfg'])
        print "Using config file " + opts.configFile;
        config.read([opts.configFile])
        
        #Conf logging
        logging.getLogger().setLevel(logging.DEBUG);
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        fileHandler = logging.handlers.RotatingFileHandler(config.get("MAIN", "log_file"), mode='a', maxBytes=1048576, backupCount=3)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(fileHandler)
        print "Logging to " + config.get("MAIN", "log_file");
        
        # MAIN BODY #
        while True:
            try:
                logging.debug("*** BEGIN ITERATION ***")
                data = check()
                
                for key,value in config.items("ATTRIBUTES"):
                    data[key] = value
                
                data = dict(data.items() + getNagios().items())
                
                send(data)
                
            except Exception, e:
                logging.error("Exception: " + str(e))
                
            time.sleep(config.getint("MAIN", "sleep_time"));
        
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'app_manager_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())