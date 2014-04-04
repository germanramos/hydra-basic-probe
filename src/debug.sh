sudo python hydra-basic-probe.py -c /etc/hydra/hydra-basic-probe.cfg &
PID = $!
tail -f /tmp/hydra-basic-probe.log
sudo kill $PID

