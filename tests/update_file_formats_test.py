"""Unit tests for the update file formats module."""

import json
import pytest
from dpres_file_formats import (
    add_av_container,
    add_format,
    add_version_to_format,
    replace_format
)


def _find_format(file_formats, mimetype):
    """Return mimetype from formats list"""
    with open(file_formats, encoding='utf-8') as json_file:
        file_formats = json.load(json_file)["file_formats"]

    for format_dict in file_formats:
        if format_dict['mimetype'] == mimetype:
            return format_dict
    return {}


def test_add_format(file_formats_path_fx):
    """Test add_format."""
    add_format(mimetype="yyy/zzz",
               content_type="TEXT",
               format_name_long="Test file format",
               format_name_short="XYZ",
               charsets=True)

    found_format = _find_format(file_formats_path_fx, "yyy/zzz")
    assert found_format["mimetype"]
    assert found_format["_id"] == "FI_DPRES_XYZ_1"
    assert "UTF-8" in found_format["charsets"]


def test_add_version_to_format(file_formats_path_fx):
    """Test add_version_to_format."""
    add_version_to_format(format_id="TEST_MIMETYPE_1",
                          version="4",
                          grade="RECOMMENDED",
                          support_in_dps_ingest=True,
                          active=True,
                          added_in_dps_spec="V10",
                          format_source_pid="abc")

    found_dict = None
    found_format = _find_format(file_formats_path_fx, "aaa/bbb")
    for version_dict in found_format["versions"]:
        if version_dict["version"] == "4":
            found_dict = version_dict
    assert found_dict["version"] == "4"
    assert found_dict["_id"] == "TEST_MIMETYPE_1_4"
    assert len(found_dict["format_sources"]) == 1
    assert isinstance(found_dict["format_sources"][0], dict)


def test_add_version_to_format_fail():
    """Test that add_version_to_format fails due to duplicate
    value.
    """
    with pytest.raises(ValueError):
        add_version_to_format(format_id="TEST_MIMETYPE_1",
                              version="1",
                              grade="RECOMMENDED",
                              support_in_dps_ingest=True,
                              active=True,
                              added_in_dps_spec="V10")


def test_replace_format(file_formats_path_fx):
    """Test replace_format."""
    replace_format(superseded_format="TEST_MIMETYPE_1",
                   superseding_format="TEST_MIMETYPE_2",
                   dps_spec_version="V11")

    deprecated_format = _find_format(file_formats_path_fx, "aaa/bbb")
    relation = deprecated_format["relations"][0]
    assert relation["type"] == "is superseded by"
    assert relation["_id"] == "TEST_MIMETYPE_2"
    assert relation["dps_spec_version"] == "1.11.0"
    assert relation["description"] == ("MIME type changed from aaa/bbb to "
                                       "bbb/ccc")
    for version in deprecated_format["versions"]:
        assert not version["active"]
        assert version["grade"] == "fi-dpres-unacceptable-file-format"

    relation = _find_format(file_formats_path_fx, "bbb/ccc")["relations"][0]
    assert relation["type"] == "supersedes"
    assert relation["_id"] == "TEST_MIMETYPE_1"
    assert relation["dps_spec_version"] == "1.11.0"
    assert relation["description"] == ("MIME type changed from aaa/bbb to "
                                       "bbb/ccc")


def test_add_av_container(av_container_grading_path_fx):
    """Test add_av_container."""
    add_av_container(version_id="TEST_MIMETYPE_3_1",
                     grade="RECOMMENDED",
                     video_streams=["TEST_MIMETYPE_4_1"],
                     audio_streams=["TEST_MIMETYPE_1_2"])

    found_container = _find_format(av_container_grading_path_fx, "fff/ggg")
    assert found_container["grade"] == "fi-dpres-recommended-file-format"


@pytest.mark.parametrize(
    ['version_id', 'video_streams', 'audio_streams'],
    [
        ('TEST_MIMETYPE_1_1', [], []),
        ('TEST_MIMETYPE_3_1', ['TEST_MIMETYPE_2_1'], []),
        ('TEST_MIMETYPE_3_1', [], ['TEST_MIMETYPE_2_2']),
        ('unknown', [], []),
        ('TEST_MIMETYPE_3_1', ['unknown'], [])
    ], ids=('Given container is not a container type',
            'Given video stream is not a video stream',
            'Given audio stream is not a audio stream',
            'Container does not exist',
            'Video stream does not exist')
)
def test_add_av_container_file(version_id,
                               video_streams,
                               audio_streams):
    """Test add_av_container with invalid input versions.."""
    with pytest.raises(ValueError):
        add_av_container(version_id=version_id,
                         grade="RECOMMENDED",
                         video_streams=video_streams,
                         audio_streams=audio_streams)
