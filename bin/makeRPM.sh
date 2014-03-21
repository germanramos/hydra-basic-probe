#!/bin/bash
sudo yum install rpm-build rpmdevtools
rpmdev-setuptree
mkdir ~/rpmbuild/SOURCES/hydra_basic_probe-2

cp ../src/*  ~/rpmbuild/SOURCES/hydra_basic_probe-2
cp hydra_basic_probe_init.d.sh ~/rpmbuild/SOURCES/hydra_basic_probe-2
cp forever.sh ~/rpmbuild/SOURCES/hydra_basic_probe-2
cp hydra_basic_probe.spec ~/rpmbuild/SPECS

pushd ~/rpmbuild/SOURCES/
tar czf hydra_basic_probe-2.0.tar.gz hydra_basic_probe-2/
cd ~/rpmbuild 
rpmbuild -ba SPECS/hydra_basic_probe.spec

popd
cp ~/rpmbuild/RPMS/noarch/hydra_basic_probe-2-0.noarch.rpm .
