ROOT=/
PREFIX=/usr
SHAREDIR=/usr/share/dpres-file-formats
PYTHON ?= python3


clean-rpm:
	rm -rf rpmbuild

install-json:
	# Install file formats JSON
	mkdir -p "${SHAREDIR}"
	cp dpres_file_formats/file_formats.json "${SHAREDIR}"

	chmod -R 755 "${SHAREDIR}"
	chmod 644 "${SHAREDIR}/file_formats.json"

install: install-json
	#Cleanup temporary files
	rm -f INSTALLED_FILES

	# Use python setuptools
	${PYTHON} setup.py build ; ${PYTHON} ./setup.py install -O1 --prefix="${PREFIX}" --root="${ROOT}" --record=INSTALLED_FILES
