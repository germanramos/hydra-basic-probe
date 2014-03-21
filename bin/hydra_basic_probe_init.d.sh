#!/bin/bash

# Hydra Basic Probe - Startup script for Hydra Basic Probe

# chkconfig: 35 85 15
# description: App for monitoring process to report status to Hydra 
# processname: python
# config: 
# pidfile: /var/run/hydra_basic_probe.pid

DISTRO_INFO=$(cat /proc/version)

if [[ $(echo $DISTRO_INFO | grep 'Debian\|Ubuntu') == "" ]]; then
	. /etc/rc.d/init.d/functions
fi

APP_NAME=hydra_basic_probe
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/hydra_basic_probe/forever.sh
RUNDIR=/usr/local/hydra_basic_probe
USER=root
GROUP=root
PID_DIR=/var/run
PID_NAME=$APP_NAME.pid
PID_FILE=$PID_DIR/$PID_NAME
LOCK_FILE=/var/lock/subsys/${APP_NAME}

case "$1" in
start)
  if [ -f $PID_FILE ]
  then
    echo Already running with PID `cat $PID_FILE`
  else
    if [[ $(echo $DISTRO_INFO | grep 'Debian\|Ubuntu') != "" ]]; then
      if start-stop-daemon --start --pidfile $PID_FILE --chdir $RUNDIR --background --make-pidfile --chuid $USER:$GROUP --exec $DAEMON
      then
        echo ok
      else
        echo start failed
      fi
    else
      if [ ! -d /var/log/${APP_NAME} ]; then
        sudo mkdir /var/log/${APP_NAME}
      fi
      sudo chown -R $USER:$GROUP /var/log/${APP_NAME}
      cd $RUNDIR
      sudo -u "$USER" $DAEMON $DAEMON_ARGS &
      RETVAL=$?
      if [ $RETVAL -eq 0 ]
      then
        echo [OK]
        PID=$!
        touch $LOCK_FILE
        echo $PID > $PID_FILE
      else
        echo [ERROR]
      fi
    fi
  fi
  ;;
stop)
  if [ -f $PID_FILE ]
  then
	PID=`cat $PID_FILE`
	PIDS="$PID `ps -ef| awk '$3 == '$PID' { print $2 }'`"
      for i in $PIDS
	  do
	    echo killing $i
	    kill -9 $i
	  done
	  rm -f $PID_FILE
  else
    echo $PID_FILE not found
  fi
  ;;
restart)
  ${0} stop
  ${0} start
  ;;
*)
  echo "Usage: /etc/init.d/$NAME {start|stop|restart}"
  exit 1
  ;;
esac

exit 0
