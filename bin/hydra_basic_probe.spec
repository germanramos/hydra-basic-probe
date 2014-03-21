Name: hydra_basic_probe
Version: 2
Release: 0
Summary: Hydra Basic Probe rpm
Source0: hydra_basic_probe-2.0.tar.gz
License: MIT
Group: Applications
URL: https://github.com/innotech/hydra_basic_probe
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
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/hydra_basic_probe
install -m 0755 hydra_basic_probe.py $RPM_BUILD_ROOT/usr/local/hydra_basic_probe/hydra_basic_probe.py
install -m 0644 parseStatusDat.py $RPM_BUILD_ROOT/usr/local/hydra_basic_probe/parseStatusDat.py
install -m 0644 forever.sh $RPM_BUILD_ROOT/usr/local/hydra_basic_probe/forever.sh

install -m 0755 -d $RPM_BUILD_ROOT/etc/init.d
install -m 0755 hydra_basic_probe_init.d.sh $RPM_BUILD_ROOT/etc/init.d/hydra_basic_probe

install -m 0755 -d $RPM_BUILD_ROOT/etc/hydra_basic_probe
install -m 0644 hydra_basic_probe.cfg $RPM_BUILD_ROOT/etc/hydra_basic_probe/hydra_basic_probe.cfg
install -m 0644 nagios_parse_example.txt $RPM_BUILD_ROOT/etc/hydra_basic_probe/nagios_parse_example.txt
%clean
rm -rf $RPM_BUILD_ROOT
%post
echo   You should edit config file /etc/hydra_basic_probe/hydra_basic_probe.cfg
%files
%dir /etc/hydra_basic_probe
/usr/local/hydra_basic_probe/hydra_basic_probe.py
/usr/local/hydra_basic_probe/hydra_basic_probe.pyc
/usr/local/hydra_basic_probe/hydra_basic_probe.pyo
/usr/local/hydra_basic_probe/parseStatusDat.py
/usr/local/hydra_basic_probe/parseStatusDat.pyc
/usr/local/hydra_basic_probe/parseStatusDat.pyo
/usr/local/hydra_basic_probe/forever.sh
/etc/hydra_basic_probe/hydra_basic_probe.cfg
/etc/hydra_basic_probe/nagios_parse_example.txt
/etc/init.d/hydra_basic_probe
