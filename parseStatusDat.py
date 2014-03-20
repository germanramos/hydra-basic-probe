# encoding: utf-8

import sys
import re
 
def parseFile( path ):
  result = {}
  record = {}
  mode   = ""
  parse_enabled = False

  f = open( path, 'r' )
 
  for line in f.readlines():
    line = line.rstrip()
    if re.match( "^(\w+) \{$", line ):
      if line.find( "host" ) >= 0:
        mode = "host"
      elif line.find( "service" ) >= 0:
        mode = "service"
      elif line.find( "info" ) >= 0:
        mode = "info"
      elif line.find( "program" ) >= 0:
        mode = "program"
      else:
        continue
      record   = {}
      parse_enabled = True
      continue
    elif parse_enabled and re.match( "^\t\}$", line ):
      if mode == "host":
        if result.get( mode, None ) is None:
          result[ mode ] = {}
        result[ mode ][ record[ "host_name" ] ] = record.copy()
      elif mode == "service":
        if result.get( mode, None ) is None:
          result[ mode ] = {}
        if result[ mode ].get( record[ "host_name" ], None ) is None:
          result[ mode ][ record[ "host_name" ] ] = {}
        result[ mode ][ record[ "host_name" ] ][ record[ "service_description" ] ] = record.copy()
      else:
        result[ mode ] = record.copy()
      parse_enabled = False
      continue
    elif not parse_enabled:
      continue
    elif re.match( "^(\s*)#", line ):
      continue
    elif re.match( "^\t\w", line ):
      pass
    else:
      continue
    
    line = line.strip()
    data = line.split( "=", 1 )
    record[ data[0] ] = data[1]
    
  f.close()
  return result
  