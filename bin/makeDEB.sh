#!/bin/bash

### http://linuxconfig.org/easy-way-to-create-a-debian-package-and-local-package-repository

rm -rf ~/debbuild
mkdir -p ~/debbuild/DEBIAN
cp control ~/debbuild/DEBIAN

mkdir -p ~/debbuild/etc/hydra-basic-probe
cp ../src/hydra-basic-probe.cfg ~/debbuild/etc/hydra-basic-probe
cp ../src/nagios-parse-example.txt ~/debbuild/etc/hydra-basic-probe

mkdir -p ~/debbuild/etc/init.d
cp hydra-basic-probe-init.d.sh ~/debbuild/etc/init.d/hydra-basic-probe

mkdir -p ~/debbuild/usr/local/hydra-basic-probe
cp ../src/hydra-basic-probe.py  ~/debbuild/usr/local/hydra-basic-probe
cp ../src/parseStatusDat.py  ~/debbuild/usr/local/hydra-basic-probe
cp ../src/configuration.py  ~/debbuild/usr/local/hydra-basic-probe
cp ../src/probeLib.py  ~/debbuild/usr/local/hydra-basic-probe
cp ../src/demoServer.py  ~/debbuild/usr/local/hydra-basic-probe

chmod -R 644 ~/debbuild/usr/local/hydra-basic-probe/* ~/debbuild/etc/hydra-basic-probe/*
chmod 755 ~/debbuild/etc/init.d/hydra-basic-probe
chmod 755 ~/debbuild/usr/local/hydra-basic-probe/hydra-basic-probe.py
sudo chown -R root:root ~/debbuild/*

pushd ~
sudo dpkg-deb --build debbuild

popd
sudo mv ~/debbuild.deb hydra-basic-probe-2-0.noarch.deb
