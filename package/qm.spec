%define name qm
%define version 2.2
%define release 1

Summary: QMTest is an automated software test execution tool.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Copyright: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Vendor: Mark Mitchell <mark@codesourcery.com>
Packager: LSB Test Team <lsb-test@freestandards.org>
Url: http://www.codesourcery.com/qm/test
Requires: lsb-python
BuildRequires: lsb-python
AutoReqProv: no


%description
UNKNOWN

%prep
%setup

%build
./configure --exec_prefix=/opt/lsb/test --with-python=/opt/lsb/appbat/bin/python
env CFLAGS="$RPM_OPT_FLAGS" /opt/lsb/appbat/bin/python setup.py build

%install
/opt/lsb/appbat/bin/python setup.py install --root=$RPM_BUILD_ROOT --install-data=/opt/lsb/test --record=INSTALLED_FILES

%clean
#rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
