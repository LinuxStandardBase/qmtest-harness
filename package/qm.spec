%define name qm
%define version 2.2
%define release 4

Summary: QMTest is an automated software test execution tool.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
#Prefix: %{_prefix}
Vendor: Mark Mitchell <mark@codesourcery.com>
Packager: LSB Test Team <lsb-test@freestandards.org>
Url: http://www.codesourcery.com/qm/test
Requires: lsb-python
BuildRequires: lsb-python
AutoReqProv: no


%description
QMTest is a cost-effective general purpose testing solution that can be
used to implement a robust, easy-to-use testing process.

%prep
%setup

%build
./configure --exec_prefix=/opt/lsb/test --with-python=/opt/lsb/appbat/bin/python
env CFLAGS="$RPM_OPT_FLAGS" /opt/lsb/appbat/bin/python setup.py build

%install
/opt/lsb/appbat/bin/python setup.py install --root=$RPM_BUILD_ROOT --install-data=/opt/lsb/test --record=INSTALLED_FILES

%clean
# uncomment later. leave in now for speed
if [ -e "${RPM_BUILD_ROOT}"  -a "${RPM_BUILD_ROOT}" != "/" ]; then 
    rm -rf ${RPM_BUILD_ROOT}
fi


%files -f INSTALLED_FILES
%defattr(-,root,root)
