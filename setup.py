"""Install dpres-file-formats"""
import re

from setuptools import find_packages, setup

with open('README.rst', encoding='utf-8') as fh:
    long_description = fh.read()

with open('dpres_file_formats/__init__.py', encoding='utf-8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='dpres_file_formats',
    version=version,
    description='File formats supported by the DPS in Finland',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    package_data={'': ['*.json']},
    install_requires=['setuptools'],
    python_requires='>=3.6',
    tests_require=['pytest'],
    test_suite='tests'
)
