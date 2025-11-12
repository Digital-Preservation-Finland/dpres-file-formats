"""Install dpres-file-formats"""
import re

from setuptools import find_packages, setup

with open('README.rst', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='dpres_file_formats',
    description='File formats supported by the DPS in Finland',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    package_data={'': ['*.json']},
    python_requires='>=3.9',
    setup_requires=['setuptools_scm'],
    use_scm_version={
        "write_to": "dpres_file_formats/_version.py"
    },
    tests_require=['pytest'],
    test_suite='tests'
)
