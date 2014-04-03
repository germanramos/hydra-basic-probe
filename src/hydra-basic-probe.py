#!/usr/bin/env python
# encoding: utf-8
'''
hydra basic probe -- Simple probe for hydra. Proactive version

The hydra basic probe is in charge of checkProcessAndPortAndGetSystemInfo and monitor one server and update the status information at one or several Hydra Servers using the restful server API.

The basic functionality is to notify to one Hydra Server when an application is Started, Stopping, or Removed. In addition, it will provide information about the server health status like CPU and memory usage and any useful information like the size of the server or the prefered balance strategy.

All these information should be updated periodically. If not, the Hydra server will assume that the servers are shutted down.

@author:     German Ramos Garcia
'''
from optparse import OptionParser
import ConfigParser
from logging.config import fileConfig 

import configuration
import parseStatusDat
from probeLib import * 

__all__ = []
__version__ = 2.0
__date__ = '2014-03-20'
__updated__ = '2014-03-20'

TESTRUN = 0
PROFILE = 0
hydras = []

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
        parser.add_option("-c", "--config", default="hydra-basic-probe.cfg", dest="configFile", action="store", help="set configuration file [default: %default]")
      
        # process options
        (opts, _args) = parser.parse_args(argv)
        config = ConfigParser.ConfigParser()
        #config.read(['app_manager.cfg', os.path.expanduser('~/app_manager.cfg'), '/etc/app_manager.cfg'])
        print "Using config file " + opts.configFile;
        config.read([opts.configFile])
        configuration.setConfig(config)
        
        #Conf logging
        logging.getLogger().setLevel(logging.DEBUG);
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        fileHandler = logging.handlers.RotatingFileHandler(config.get("MAIN", "log_file"), mode='a', maxBytes=1048576, backupCount=3)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(fileHandler)
        print "Logging to " + config.get("MAIN", "log_file");
        
        # Launch update hydra proccess
        global hydras
        for key,hydra in config.items("HYDRAS"):
            hydras += [hydra]
        configuration.setHydras(hydras)
        updateHydras()
        
        # MAIN BODY #
        while True:
            try:
                logging.debug("*** BEGIN ITERATION ***")
                data = checkProcessAndPortAndGetSystemInfo()
                
                for key,value in config.items("ATTRIBUTES"):
                    data[key] = value
                
                data = dict(data.items() + getNagios().items())
                
                postDataToHydra(data)
                
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