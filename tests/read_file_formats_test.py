"""Unit tests for the read file formats module."""

import pytest
from dpres_file_formats.read_file_formats import (
    containers_streams_grading,
    mimetypes_grading,
    file_formats,
)


@pytest.mark.parametrize(
    ("deprecated",
     "unofficial",
     "versions_separately",
     "found_formats",
     "found_versions"),
    [
        (False, False, False, 3, 1),
        (True, False, False, 4, 2),
        (False, True, False, 3, 2),
        (True, True, False, 4, 3),
        (False, False, True, 3, None),
        (True, False, True, 5, None),
        (False, True, True, 4, None),
        (True, True, True, 6, None)
    ],
    ids=[
        'Active and offical file formats',
        'Include deprecated file formats',
        'Include unoffical file formats',
        'Include both deprecated and unoffical file formats',
        'Active and offical file formats, output versions',
        'Include deprecated file formats, output versions',
        'Include unoffical file formats, output versions',
        'Include both deprecated and unoffical file formats, output versions'

    ]
)
def test_file_formats(
        deprecated,
        unofficial,
        versions_separately,
        found_formats,
        found_versions):
    """Test file_formats."""
    dps_formats = file_formats(
        deprecated, unofficial, versions_separately)

    assert len(dps_formats) == found_formats
    assert dps_formats[0]["mimetype"]
    if not versions_separately:
        assert len(dps_formats[0]["versions"]) == found_versions
        assert dps_formats[0]["versions"][0]["version"]
    else:
        assert dps_formats[0]["version"]


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
