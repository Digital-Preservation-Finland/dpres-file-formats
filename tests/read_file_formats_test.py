"""Unit tests for the read file formats module."""

import pytest
from dpres_file_formats.read_file_formats import (
    containers_streams_grading,
    find_mimetypes,
    mimetypes_format_registry_keys,
    mimetypes_grading,
    supported_file_formats,
    supported_file_formats_versions
)


@pytest.mark.parametrize(
    ("active", "dps_spec_formats", "found_formats", "found_versions"),
    [
        (True, True, 3, 1),
        (False, True, 4, 2),
        (True, False, 3, 2),
        (False, False, 4, 3)
    ]
)
def test_supported_file_formats(
        active, dps_spec_formats, found_formats, found_versions):
    """Test supported_file_formats."""
    file_formats = supported_file_formats(active, dps_spec_formats)

    assert len(file_formats) == found_formats
    assert file_formats[0]["mimetype"]
    assert len(file_formats[0]["versions"]) == found_versions
    assert file_formats[0]["versions"][0]["version"]


@pytest.mark.parametrize(
    ("active", "dps_spec_formats", "basic_info", "found_formats"),
    [
        (True, True, False, 3),
        (False, True, False, 5),
        (True, False, False, 4),
        (False, False, False, 6),
        (True, True, True, 3)
    ]
)
def test_supported_file_formats_versions(
        active, dps_spec_formats, basic_info, found_formats):
    """test supported_file_formats_versions."""
    file_formats_versions = supported_file_formats_versions(
            active=active,
            dps_spec_formats=dps_spec_formats,
            basic_info=basic_info)

    assert len(file_formats_versions) == found_formats
    assert file_formats_versions[0]["mimetype"]
    assert file_formats_versions[0]["version"]
    if basic_info:
        assert len(file_formats_versions[0]) == 2


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


@pytest.mark.parametrize(("mimetype", "found"), [
    ("aaa/bbb", 2),
    ("unknown", 0)
])
def test_find_mimetypes(mimetype, found):
    """Test find_mimetypes."""
    formats = find_mimetypes(mimetype)
    assert len(formats) == found


def test_mimetypes_format_registry_keys():
    """Test mimetypes_format_registry_keys."""
    mimetypes = mimetypes_format_registry_keys()

    # Two formats with the same mimetypes should have been combined
    # and only the active versions' registry keys should have been added
    assert len(mimetypes) == 2
    assert len(mimetypes["aaa/bbb"]) == 2
    for registry_keys in mimetypes["aaa/bbb"]:
        assert registry_keys in ['key_002', 'key_004']

    # Empty format registry keys should have been added
    assert len(mimetypes["bbb/ccc"]) == 1
    assert next(iter(mimetypes["bbb/ccc"])) == ''


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
