ROOT=/
PREFIX=/usr
SHAREDIR=/usr/share/dpres-file-formats
PYTHON ?= python3


clean-rpm:
	rm -rf rpmbuild

install-json:
	# Install file formats JSON files
	mkdir -p "${SHAREDIR}"
	cp dpres_file_formats/data/file_formats.json "${SHAREDIR}"
	cp dpres_file_formats/data/av_container_grading.json "${SHAREDIR}"

	chmod -R 755 "${SHAREDIR}"
	chmod 644 "${SHAREDIR}/file_formats.json"
	chmod 644 "${SHAREDIR}/av_container_grading.json"

install: install-json
	#Cleanup temporary files
	rm -f INSTALLED_FILES

	# Use python setuptools
	${PYTHON} setup.py build ; ${PYTHON} ./setup.py install -O1 --prefix="${PREFIX}" --root="${ROOT}" --record=INSTALLED_FILES
