import configuration
 
import time
import sys
import os
import json
import logging  
import psutil
import socket
import threading
import urllib2

class stateEnum:
    READY = 0
    NOT_RUNNING = 1
    NOT_LISTENING = 2

def isPortOpen(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print s
        print s.connect((ip, int(port)))
        print s.shutdown(2)
        return stateEnum.READY
    except:
        return stateEnum.NOT_LISTENING

def checkProcessAndPortAndGetSystemInfo():
    config = configuration.getConfig()
    hydras = configuration.getHydras()
    data = {"state": stateEnum.NOT_RUNNING, "uri": config.get("MAIN", "uri")}
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
        #data["memLoad"] = psutil.virtual_memory().percent
        data["memLoad"] = psutil.phymem_usage().percent
        
        # Check port open (if option exists) 
        if config.get("MAIN", "check_enabled") == "true" and config.has_option("MAIN", "check_host") and config.has_option("MAIN", "check_port"):
            logging.debug("Checking Host and Port")
            data["state"] = isPortOpen(config.get("MAIN", "check_host"), int(config.get("MAIN", "check_port")))
        else:
            data["state"] = stateEnum.READY
             
    except Exception, e:
        logging.debug(str(e))
        data["state"] = stateEnum.NOT_RUNNING
              
    return data

def postDataToHydra(attributes):
    config = configuration.getConfig()
    hydras = configuration.getHydras()
    hostname = None
    try:
        hostname = config.get("MAIN", "hostname")
    except Exception:
        hostname = socket.gethostname()
    hydra_data = {hostname: attributes}
    answer = json.dumps(hydra_data)
    logging.debug("Data to post:")
    logging.debug(answer)
    
    for hydra in hydras:
        lines = hydra.split(":")
        post_url = lines[0] + ":" + lines[1] + ":" + config.get("MAIN", "hydra_admin_port") + "/apps/" + config.get("MAIN", "app_id") + "/Instances" 
        #post_url = hydra + "/apps/" + config.get("MAIN", "app_id") + "/Instances"
        logging.debug("Posting to " + post_url)                   
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        headers = {
                   'hydra_access_key':config.get("MAIN", "hydra_access_key"),
                   'hydra_secret_key':config.get("MAIN", "hydra_secret_key")
                   }
        try:
            request = urllib2.Request(post_url, answer, headers=headers)
            request.add_header("content-type", "application/json")
            url = opener.open(request, timeout=int(config.get("MAIN", "timeout")))
            if url.code != 200:
                logging.error("Error connecting with hydra {0}: Code: {1}".format(hydra,url.code))
            else:
                logging.debug("Posted OK")
                break
        except Exception, e:
            logging.error(str(e))
            logging.error("Exception connecting with hydra {0}".format(hydra))
            
def updateHydras():
    config = configuration.getConfig()
    hydras = configuration.getHydras()
    logging.debug("** Updating Hydras **")
    result = []
    for key,hydra in config.items("HYDRAS"):
        result += [hydra]
    
    for hydra in hydras:
        try:
            get_url = hydra + '/apps/hydra'
            headers = {'hydra_access_key':config.get("MAIN", "hydra_access_key")}
            request = urllib2.Request(get_url, headers=headers)
            response = urllib2.urlopen(request, timeout=int(config.get("MAIN", "timeout")))
            new_hydras = json.loads(response.read())
            if len(new_hydras)>0:                
                # Merge with no duplicates. Always config hydras first
                result = result + list(set(new_hydras) - set(result))
                break
            else:
                logging.error("Empty hydra list received from " + get_url)
        except Exception, e:
            logging.error("Exception updating hydras: " + str(e))
    
    logging.debug("Updated hydra servers list:")
    logging.debug(result)
    configuration.setHydras(result)    
    
    t = threading.Timer(int(config.get("MAIN","hydra_refresh_interval")), updateHydras)
    t.setDaemon(True)
    t.start()
            
def getNagios():
    config = configuration.getConfig()
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
