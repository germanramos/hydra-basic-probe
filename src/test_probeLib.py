import pytest
import probeLib
from probeLib import *
from mock import MagicMock

def test_isPortOpen_should_return_False_when_exception_on_connect():
    # Fixture
    mock = MagicMock()
    mock.connect = MagicMock(side_effect=Exception('Boom!'))
    mock.socket.return_value = mock
    probeLib.socket = mock
      
    # Test
    assert isPortOpen("127.0.0.1", "22") == 2
    
def test_isPortOpen_should_return_True_when_connect_ok():
    # Fixture
    probeLib.socket = MagicMock()
      
    # Test
    assert isPortOpen("127.0.0.1", "22") == 0
