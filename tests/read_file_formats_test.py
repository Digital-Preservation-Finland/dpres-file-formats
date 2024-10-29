"""Unit tests for the read file formats module."""

import pytest
from dpres_file_formats.read_file_formats import (
    containers_streams_grading,
    mimetypes_grading,
    supported_file_formats,
    supported_file_formats_versions
)


@pytest.mark.parametrize(
    ("deprecated", "unofficial", "found_formats", "found_versions"),
    [
        (False, False, 3, 1),
        (True, False, 4, 2),
        (False, True, 3, 2),
        (True, True, 4, 3)
    ]
)
def test_supported_file_formats(
        deprecated, unofficial, found_formats, found_versions):
    """Test supported_file_formats."""
    file_formats = supported_file_formats(deprecated, unofficial)

    assert len(file_formats) == found_formats
    assert file_formats[0]["mimetype"]
    assert len(file_formats[0]["versions"]) == found_versions
    assert file_formats[0]["versions"][0]["version"]


@pytest.mark.parametrize(
    ("deprecated", "unofficial", "found_formats"),
    [
        (False, False, 3),
        (True, False, 5),
        (False, True, 4),
        (True, True, 6)
    ]
)
def test_supported_file_formats_versions(
        deprecated, unofficial, found_formats):
    """Test supported_file_formats_versions."""
    file_formats_versions = supported_file_formats_versions(
            deprecated=deprecated,
            unofficial=unofficial)

    assert len(file_formats_versions) == found_formats
    assert file_formats_versions[0]["mimetype"]
    assert file_formats_versions[0]["version"]


@pytest.mark.parametrize(("text_formats", "found_mimetypes"), [
    (False, 2),
    (True, 1)
])
def test_mimetypes_grading(text_formats, found_mimetypes):
    """Test mimetypes_grading."""
    mimetypes = mimetypes_grading(text_formats)
    assert len(mimetypes) == found_mimetypes
    assert "bbb/ccc" in mimetypes
    if not text_formats:
        assert "aaa/bbb" in mimetypes
        assert mimetypes["aaa/bbb"]["2"] == (
                "fi-dpres-recommended-file-format")
        # Check that two formats with same mimetype have merged and
        # that inactive versions have been excluded
        assert len(mimetypes["aaa/bbb"]) == 3
        assert ["2", "3", "5"] == list(mimetypes["aaa/bbb"].keys())
        assert "1" not in mimetypes["aaa/bbb"]


@pytest.mark.parametrize(("grade", "expected_mimetype", "found_count"), [
    ("RECOMMENDED", "aaa/bbb", 1),
    ("ACCEPTABLE", "bbb/ccc", 1),
    (None, "aaa/bbb", 2)
])
def test_containers_streams_grading(grade, expected_mimetype, found_count):
    """Test containers_streams_grading."""
    containers = containers_streams_grading(grade=grade)
    assert len(containers) == found_count
    assert containers[expected_mimetype]
