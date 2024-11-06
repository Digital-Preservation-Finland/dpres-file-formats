"""Unit tests for the read file formats module."""

import pytest
from dpres_file_formats.read_file_formats import file_formats


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
        'Active and official file formats',
        'Include deprecated file formats',
        'Include unofficial file formats',
        'Include both deprecated and unofficial file formats',
        'Active and official file formats, output versions',
        'Include deprecated file formats, output versions',
        'Include unofficial file formats, output versions',
        'Include both deprecated and unofficial file formats, output versions'

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
