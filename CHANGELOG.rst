Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`__,
and this project adheres to `Semantic Versioning <(https://semver.org/spec/v2.0.0.html>`__.

1.1.1 - 2025-10-23
------------------

Added
^^^^^

- WARC 0.18
- StrEnum to controlled vocabularies

1.1.0 - 2025-09-25
------------------

Added
^^^^^

- Dolby Digital AC-3
- JavaScript Object Notation (JSON)
- Reference to DPS File Format specification V14
- Function to update the av_container_grading.json file

1.0.1 - 2025-08-27
------------------

Changed
^^^^^^^

- ``importlib`` is now used instead of deprecated ``pkg_resources`` library. ``setuptools`` is no longer a runtime dependency.

Fixed
^^^^^

- Update minimum Python version to 3.9; it was previously 3.6 which is not supported.

1.0.0 - 2025-07-22
------------------

- Initial release

Added
^^^^^

- Moved grading functionality from file-scraper to here
- Added file format data
