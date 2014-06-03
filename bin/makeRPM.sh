#!/bin/bash

### http://tecadmin.net/create-rpm-of-your-own-script-in-centosredhat/#

sudo yum install rpm-build rpmdevtools
rm -rf ~/rpmbuild
rpmdev-setuptree

mkdir ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/hydra-basic-probe.py  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/parseStatusDat.py  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/configuration.py  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/probeLib.py  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/demoServer.py  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/hydra-basic-probe.cfg  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp ../src/nagios-parse-example.txt  ~/rpmbuild/SOURCES/hydra-basic-probe-2
cp hydra-basic-probe-init.d.sh ~/rpmbuild/SOURCES/hydra-basic-probe-2


cp hydra-basic-probe.spec ~/rpmbuild/SPECS

pushd ~/rpmbuild/SOURCES/
tar czf hydra-basic-probe-2.0.tar.gz hydra-basic-probe-2/
cd ~/rpmbuild 
rpmbuild -ba SPECS/hydra-basic-probe.spec

popd
cp ~/rpmbuild/RPMS/noarch/hydra-basic-probe-2-0.noarch.rpm .
