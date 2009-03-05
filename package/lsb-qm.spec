%define name lsb-qm
%define rname qm

Summary: QMTest is an automated software test execution tool.
Name: %{name}
# rel, ver, LSBRelease is passed in from Makefile so we only have 
# to set the buildno one place
Version: %{ver}
Release: %{rel}.lsb%{LSBRelease}
Source0: %{rname}_%{version}.orig.tar.gz
Source1: configure
Source2: configure.in
Source3: GNUmakefile.in

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
%setup -q -n %{rname}-%{version}.orig

%build
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

# tarball we got from Debian uses whrandom, which is 
# deprecated, replace with random
sed -i 's|whrandom|random|g' qm/web.py 
sed -i 's|whrandom|random|g' qm/test/web/web.py 
sed -i 's|whrandom|random|g' qm/external/DocumentTemplate/DT_Util.py 

./configure --exec_prefix=/opt/lsb/test --with-python=/opt/lsb/appbat/bin/python
env CFLAGS="$RPM_OPT_FLAGS" /opt/lsb/appbat/bin/python setup.py build

%install
/opt/lsb/appbat/bin/python setup.py install --root=$RPM_BUILD_ROOT --install-data=/opt/lsb/test --record=INSTALLED_FILES

# this file is still holding the buildroot path
sed -i "s|${RPM_BUILD_ROOT}|/opt/lsb/test|g" ${RPM_BUILD_ROOT}/opt/lsb/appbat/lib/python2.4/site-packages/qm/config.py
rm -f ${RPM_BUILD_ROOT}/opt/lsb/appbat/lib/python2.4/site-packages/qm/config.pyc
sed -i 's|/opt/lsb/appbat/lib/python2.4/site-packages/qm/config.pyc||g' INSTALLED_FILES

# bug 2509 - drop all .pyc/.pyo files
find ${RPM_BUILD_ROOT}/opt/lsb -name '*.pyc' | xargs rm -f
find ${RPM_BUILD_ROOT}/opt/lsb -name '*.pyo' | xargs rm -f
cp INSTALLED_FILES INSTALLED_FILES.pyc
grep -v '\.pyc' INSTALLED_FILES.pyc > INSTALLED_FILES

%clean
# uncomment later. leave in now for speed
if [ -e "${RPM_BUILD_ROOT}"  -a "${RPM_BUILD_ROOT}" != "/" ]; then 
    rm -rf ${RPM_BUILD_ROOT}
fi


%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Wed Sep 03 2008 Stew Benedict <stewb@linux-foundation.org>
- use upstream tarball (bug 711)


