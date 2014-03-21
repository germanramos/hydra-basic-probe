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
cp ../src/*  ~/debbuild/usr/local/hydra-basic-probe

pushd ~
dpkg-deb --build debbuild

popd
mv ~/debbuild.deb hydra-basic-probe-2.0.deb
	