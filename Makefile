ROOT=/
PREFIX=/usr
PYTHON ?= python3


clean-rpm:
	rm -rf rpmbuild

install:
	#Cleanup temporary files
	rm -f INSTALLED_FILES

	# Use python setuptools
	${PYTHON} setup.py build ; ${PYTHON} ./setup.py install -O1 --prefix="${PREFIX}" --root="${ROOT}" --record=INSTALLED_FILES
