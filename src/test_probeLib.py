import pytest
import probeLib
from probeLib import *
from mock import MagicMock

def test_isPortOpen_should_return_True_when_connect_ok():
    # Fixture
    probeLib.socket = MagicMock()
      
    # Test and check
    assert isPortOpen("127.0.0.1", "22") == 0
    
def test_isPortOpen_should_return_False_when_exception_on_connect():
    # Fixture
    mock = MagicMock()
    mock.connect = MagicMock(side_effect=Exception('Boom!'))
    mock.socket.return_value = mock
    probeLib.socket = mock

    # Test
    assert isPortOpen("127.0.0.1", "22") == 2

def test_checkProcessAndPortAndGetSystemInfo_should_return_status_0_when_process_exists():
    #Fixture
    probeLib.configuration = MagicMock()
    probeLib.configuration.config.get("MAIN","uri").return_value = "https://localhost:22"
    probeLib.configuration.config.get("MAIN", "pid_file").return_value = "/var/run/ssh.pid"
    probeLib.configuration.getHydras().return_value = []
    
    probeLib.open = MagicMock()
    probeLib.open.read().return_value = "22"
    
    probeLib.psutil = MagicMock()
    process = MagicMock()
    process.get_connections.return_value = [1,2]
    probeLib.psutil.Process.return_value = process
    
    # Test
    data = probeLib.checkProcessAndPortAndGetSystemInfo()
    
    # Check
    print data
    assert data["state"] == 0
    
    # ORIGINAL
    #assert data["connections"] == 2
    
    # ALTERNATIVE 1
    assert data["connections"] == 1
    
    
    
    