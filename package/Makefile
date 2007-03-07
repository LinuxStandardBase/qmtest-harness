# XXX We should play the usual tricks defining stuff here and building
# XXX a specfile from this info, but not yet: for now keep in sync
PACKAGE=qm
VERSION=2.2
LSBSpec=3.1
LSBRelease=3
RELEASE=5
#
# Derive date string for daily snapshots
ISO_DATE=$(shell date +"%Y%m%d")
PWD=$(shell pwd)

FULL_PACKAGE_NAME=$(PACKAGE)-$(VERSION)
TARBALL=$(FULL_PACKAGE_NAME).tar.gz
RPM_BINARY_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).lsb$(LSBRelease).$(RPM_BUILD_ARCH).rpm
RPM_SOURCE_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).lsb$(LSBRelease).src.rpm


# Temporary build directory
TMP_BUILD_DIR=/tmp/$(FULL_PACKAGE_NAME)

# Handle different version generation for snapshots than for official builds
# OFFICIAL_RELEASE should be set to the tag to extract from CVS
ifdef OFFICIAL_RELEASE
VERSION_SUFFIX=
# EXPORT_TAG should be set to the cvs tag to use
EXPORT_TAG=--revision=otag:$(OFFICIAL_RELEASE)
else
VERSION_SUFFIX=.$(ISO_DATE)
EXPORT_TAG=
endif

# Determine whether to use rpm or rpmbuild to build the packages
ifeq ($(wildcard /usr/bin/rpmbuild),)
	RPM_BUILD_CMD=rpm
else
	RPM_BUILD_CMD=rpmbuild 
endif

# Get RPM configuration information
# NOTE THAT RPM_TMP_BUILD_DIR IS DELETED AFTER THE RPM BUILD IS COMPLETED
# The rpmrc file translates targets where there are multiple choices per
# architecture. On build, the derived RPM_BUILD_ARCH is given as the target
RCFILELIST="/usr/lib/rpm/rpmrc:./rpmrc"
RPM_TMP_BUILD_DIR=/var/tmp/rpm-build
RPM_BUILD_ARCH=$(shell rpm --rcfile ${RCFILELIST} --eval=%{_target_cpu})
RPM_BINARY_DIR=$(RPM_TMP_BUILD_DIR)/RPMS/$(RPM_BUILD_ARCH)
RPM_SRPM_DIR=$(RPM_TMP_BUILD_DIR)/SRPMS

# Override this on the command line to use a different repo
BZRTREES?=http://bzr.freestandards.org/lsb/3.1
BZR_MODULE=qmtest-harness

# Default target
all: rpm_package

tarball: $(TARBALL) 

rpm_package: $(RPM_BINARY_NAME) $(RPM_SOURCE_NAME) 

$(RPM_BINARY_NAME) $(RPM_SOURCE_NAME): $(PACKAGE).spec $(TARBALL) 
	@mkdir -p $(RPM_TMP_BUILD_DIR)/BUILD
	@mkdir -p $(RPM_TMP_BUILD_DIR)/RPMS
	@mkdir -p $(RPM_TMP_BUILD_DIR)/SRPMS
ifdef SIGN_PACKAGES
	@expect -c 'set timeout -1' -c 'spawn $(RPM_BUILD_CMD) --sign --rcfile ${RCFILELIST} --define=_sourcedir\ $(PWD) --define=_topdir\ $(RPM_TMP_BUILD_DIR) --define=_target_cpu\ $(RPM_BUILD_ARCH) --define=rel\ $(RELEASE) -ba $(PACKAGE).spec' -c 'expect -ex "Enter pass phrase:"' -c 'send "\n"' -c 'expect "Executing(%clean)"' -c 'expect "exit 0"' -c 'send "\n"'
else
	@$(RPM_BUILD_CMD) --rcfile ${RCFILELIST} --define="_sourcedir $(PWD)" --define="_topdir $(RPM_TMP_BUILD_DIR)" --define="_target_cpu $(RPM_BUILD_ARCH)" --define="rel $(RELEASE)" -ba $(PACKAGE).spec
endif
	@mv $(RPM_SRPM_DIR)/$(RPM_SOURCE_NAME) .
	@mv $(RPM_BINARY_DIR)/$(RPM_BINARY_NAME) .
	@rm -rf $(RPM_TMP_BUILD_DIR)

$(TARBALL):
	bzr export $(EXPORT_TAG) $(TARBALL) $(BZRTREES)/$(BZR_MODULE)

.PHONY : tarball rpm_package
