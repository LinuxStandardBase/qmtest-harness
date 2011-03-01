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

%clean
# uncomment later. leave in now for speed
if [ -e "${RPM_BUILD_ROOT}"  -a "${RPM_BUILD_ROOT}" != "/" ]; then 
    rm -rf ${RPM_BUILD_ROOT}
fi


%files -f INSTALLED_FILES
%defattr(-,root,root)
# directories not called out in INSTALLED_FILES
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm/external
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm/external/DocumentTemplate
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm/test
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm/test/classes
%dir /opt/lsb/appbat/lib/python2.4/site-packages/qm/test/web
%dir /opt/lsb/test/qm
%dir /opt/lsb/test/qm/diagnostics
%dir /opt/lsb/test/qm/doc
%dir /opt/lsb/test/qm/doc/test
%dir /opt/lsb/test/qm/doc/test/html
%dir /opt/lsb/test/qm/doc/test/print
%dir /opt/lsb/test/qm/dtml
%dir /opt/lsb/test/qm/dtml/test
%dir /opt/lsb/test/qm/messages
%dir /opt/lsb/test/qm/messages/test
%dir /opt/lsb/test/qm/tutorial
%dir /opt/lsb/test/qm/tutorial/test
%dir /opt/lsb/test/qm/tutorial/test/tdb
%dir /opt/lsb/test/qm/tutorial/test/tdb/QMTest
%dir /opt/lsb/test/qm/web
%dir /opt/lsb/test/qm/web/images
%dir /opt/lsb/test/qm/web/stylesheets
%dir /opt/lsb/test/qm/xml

%changelog
* Thu Feb 24 2011 Stew Benedict <stewb@linux-foundation.org>
- own the directories we populate (bug 3195)

* Wed Sep 03 2008 Stew Benedict <stewb@linux-foundation.org>
- use upstream tarball (bug 711)


