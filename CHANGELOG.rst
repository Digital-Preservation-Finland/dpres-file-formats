Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`__,
and this project adheres to `Semantic Versioning <(https://semver.org/spec/v2.0.0.html>`__.

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
