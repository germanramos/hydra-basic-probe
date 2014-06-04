import configuration
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import time
import json

PASSWORD = ""
LOCK_TIME = 1800
HALT_TIME = 90
STRESS_TIME = 45
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 9099
stress = 0;
halt = 0;
lock = 0


def demoServer():
    config = configuration.getConfig()
    global PASSWORD
    global LOCK_TIME
    global HALT_TIME
    global STRESS_TIME
    PASSWORD = config.get("MAIN", "demo_password")
    LOCK_TIME = int(config.get("MAIN", "demo_lock_time")) * 1000
    HALT_TIME = int(config.get("MAIN", "demo_halt_time")) * 1000
    STRESS_TIME = int(config.get("MAIN", "demo_stress_time")) * 1000
    server_class = ThreadedHTTPServer
    httpd = server_class((LISTEN_HOST, LISTEN_PORT), MyHandler)
    print time.asctime(), "Demo Server Starts - %s:%s" % (LISTEN_HOST, LISTEN_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Demo Server Stops - %s:%s" % (LISTEN_HOST, LISTEN_PORT)

def isHalted():
    return time.time() - halt < HALT_TIME

def isStressed():
    return time.time() - stress < STRESS_TIME

def isLocked():
    return time.time() - lock < LOCK_TIME
    
class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
        pass
 
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        print "Path: " + self.path
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        global stress
        global halt
        global lock
        splited = self.path.split("?")
        pwd = ""
        if len(splited) > 1:
            splited2 = splited[1].split("=")
            if len(splited2) > 1:
                pwd = splited2[1]
        self.path = splited[0];
        
        if isLocked() and pwd != PASSWORD and (self.path == "/stress" or self.path == "/halt" or self.path == "/ready"):
            data = "LOCKED"    
        elif self.path == "/lock":
            if pwd == PASSWORD:
                lock = time.time()
                data = "OK"
            else:
                data = "WRONG PASSWORD"
        elif self.path == "/unlock":
            if pwd == PASSWORD:
                lock = 0
                data = "OK"
            else:
                data = "WRONG PASSWORD"
        elif self.path == "/ready":
            stress = 0;
            halt = 0;
            data = "OK"
        elif self.path == "/stress":
            stress = time.time()
            data = "OK"
        elif self.path == "/halt":
            halt = time.time()
            data = "OK"
        elif self.path == "/status":
            data = {}
            data["halted"] = isHalted()
            data["stressed"] = isStressed()
            data["locked"] = isLocked()
        else:
            data = "UNKNOWN"
        self.wfile.write(json.dumps(data))
