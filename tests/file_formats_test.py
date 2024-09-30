"""Tests for file formats."""

from dpres_file_formats.file_formats import (
    supported_file_formats,
    supported_file_formats_versions,
    serialize_supported_file_formats,
    serialize_supported_file_formats_versions
)


def test_supported_file_formats():
    """Test supported_file_formats."""
    file_formats = supported_file_formats()
    assert file_formats
    assert file_formats[0]["mimetype"]
    assert file_formats[0]["versions"]
    assert file_formats[0]["versions"][0]["version"]


def test_supported_file_formats_versions():
    """test supported_file_formats_versions."""
    file_formats_versions = supported_file_formats_versions()
    assert file_formats_versions
    assert file_formats_versions[0]["mimetype"]
    assert file_formats_versions[0]["version"]


def test_serialize_supported_file_formats():
    """Test serialize_supported_file_formats."""
    assert isinstance(serialize_supported_file_formats(), str)


def test_serialize_supported_file_formats_versions():
    """test serialize_supported_file_formats_versions."""
    assert isinstance(serialize_supported_file_formats_versions(), str)
