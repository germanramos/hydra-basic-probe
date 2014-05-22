Name: hydra-basic-probe
Version: 2
Release: 0
Summary: Hydra Basic Probe
Source0: hydra-basic-probe-2.0.tar.gz
License: MIT
Group: custom
URL: https://github.com/innotech/hydra-basic-probe
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: python-psutil
%description
Monitors system resources of the system.
Monitors a proccess and port of our application and notifies to one or more hydra servers
%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/hydra-basic-probe
install -m 0755 hydra-basic-probe.py $RPM_BUILD_ROOT/usr/local/hydra-basic-probe/hydra-basic-probe.py
install -m 0644 parseStatusDat.py $RPM_BUILD_ROOT/usr/local/hydra-basic-probe/parseStatusDat.py
install -m 0644 configuration.py $RPM_BUILD_ROOT/usr/local/hydra-basic-probe/configuration.py
install -m 0644 probeLib.py $RPM_BUILD_ROOT/usr/local/hydra-basic-probe/probeLib.py

install -m 0755 -d $RPM_BUILD_ROOT/etc/init.d
install -m 0755 hydra-basic-probe-init.d.sh $RPM_BUILD_ROOT/etc/init.d/hydra-basic-probe

install -m 0755 -d $RPM_BUILD_ROOT/etc/hydra-basic-probe
install -m 0644 hydra-basic-probe.cfg $RPM_BUILD_ROOT/etc/hydra-basic-probe/hydra-basic-probe.cfg
install -m 0644 nagios-parse-example.txt $RPM_BUILD_ROOT/etc/hydra-basic-probe/nagios-parse-example.txt
%clean
rm -rf $RPM_BUILD_ROOT
%post
echo   You should edit config file /etc/hydra-basic-probe/hydra-basic-probe.cfg
echo   When finished, you may want to run \"update-rc.d hydra-basic-probe defaults\"
%files
%dir /etc/hydra-basic-probe
/usr/local/hydra-basic-probe/hydra-basic-probe.py
/usr/local/hydra-basic-probe/hydra-basic-probe.pyc
/usr/local/hydra-basic-probe/hydra-basic-probe.pyo
/usr/local/hydra-basic-probe/parseStatusDat.py
/usr/local/hydra-basic-probe/parseStatusDat.pyc
/usr/local/hydra-basic-probe/parseStatusDat.pyo
/usr/local/hydra-basic-probe/configuration.py
/usr/local/hydra-basic-probe/configuration.pyc
/usr/local/hydra-basic-probe/configuration.pyo
/usr/local/hydra-basic-probe/probeLib.py
/usr/local/hydra-basic-probe/probeLib.pyc
/usr/local/hydra-basic-probe/probeLib.pyo
/etc/hydra-basic-probe/hydra-basic-probe.cfg
/etc/hydra-basic-probe/nagios-parse-example.txt
/etc/init.d/hydra-basic-probe
