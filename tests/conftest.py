"""Configure py.test default values and functionality"""
import contextlib
import json

import pytest


@pytest.fixture(scope='function')
def file_formats_path_fx(tmp_path):
    """Fixture to return tmp path to file format json."""
    return tmp_path / "file_formats.json"


@pytest.fixture(scope='function')
def av_container_grading_path_fx(tmp_path):
    """Fixture to return tmp path to file format json."""
    return tmp_path / "av_container_grading.json"


# pylint: disable=redefined-outer-name
@pytest.fixture(scope='function', autouse=True)
def file_format_json_mock(
        file_formats_path_fx, av_container_grading_path_fx, monkeypatch):
    """Fixture to use test data for file formats JSON."""

    data = {
        "file_formats": [
            {
                "_id": "TEST_MIMETYPE_1",
                "mimetype": "aaa/bbb",
                "content_type": "audio",
                "format_name_short": "ABC",
                "relations": [],
                "charsets": [],
                "versions": [
                    {
                        "_id": "TEST_MIMETYPE_1_1",
                        "active": False,
                        "grade": "fi-dpres-recommended-file-format",
                        "format_registry_key": "key_001",
                        "version": "1",
                        "added_in_dps_spec": "1",
                        "format_sources": []
                    },
                    {
                        "_id": "TEST_MIMETYPE_1_2",
                        "active": True,
                        "grade": "fi-dpres-recommended-file-format",
                        "format_registry_key": "key_002",
                        "version": "2",
                        "added_in_dps_spec": "1",
                        "format_sources": []
                    },
                    {
                        "_id": "TEST_MIMETYPE_1_3",
                        "active": True,
                        "grade": "fi-dpres-bit-level-file-format",
                        "format_registry_key": "key_002",
                        "version": "3",
                        "added_in_dps_spec": "",
                        "format_sources": []
                    }
                ]
            },
            {
                "_id": "TEST_MIMETYPE_2",
                "mimetype": "bbb/ccc",
                "content_type": "image",
                "format_name_short": "ABC",
                "charsets": ["ISO-8859-15", "UTF-8", "UTF-16", "UTF-32"],
                "relations": [],
                "versions": [
                    {
                        "_id": "TEST_MIMETYPE_2_1",
                        "active": True,
                        "grade": "fi-dpres-recommended-file-format",
                        "format_registry_key": "",
                        "version": "1",
                        "added_in_dps_spec": "1",
                        "format_sources": []
                    }
                ]
            },
            {
                "_id": "TEST_MIMETYPE_3",
                "mimetype": "fff/ggg",
                "content_type": "videocontainer",
                "format_name_short": "GHI",
                "charsets": [],
                "relations": [],
                "versions": [
                    {
                        "_id": "TEST_MIMETYPE_3_1",
                        "active": False,
                        "grade": "fi-dpres-recommended-file-format",
                        "format_registry_key": "key_003",
                        "version": "1",
                        "added_in_dps_spec": "1",
                        "format_sources": []
                    }
                ]
            },
            {
                "_id": "TEST_MIMETYPE_4",
                "mimetype": "aaa/bbb",
                "content_type": "video",
                "format_name_short": "ABC-D",
                "charsets": [],
                "relations": [],
                "versions": [
                    {
                        "_id": "TEST_MIMETYPE_4_1",
                        "active": True,
                        "grade": "fi-dpres-recommended-file-format",
                        "format_registry_key": "key_004",
                        "version": "5",
                        "added_in_dps_spec": "1",
                        "format_sources": []
                    }
                ]
            }
        ]
    }

    with open(file_formats_path_fx, "w", encoding="UTF-8") as outfile:
        json.dump(data, outfile)
    with open(av_container_grading_path_fx, "w", encoding="UTF-8") as outfile:
        json.dump({"file_formats": []}, outfile)

    @contextlib.contextmanager
    def mock_resource_path(module, resource_name):
        if module == "dpres_file_formats.data":
            if resource_name == "file_formats.json":
                yield file_formats_path_fx
                return
            if resource_name == "av_container_grading.json":
                yield av_container_grading_path_fx
                return

        raise ValueError(
            f"Module {module} resource {resource_name} not detected"
        )

    # pylint: disable=import-outside-toplevel
    import dpres_file_formats.json_handler
    monkeypatch.setattr(
        dpres_file_formats.json_handler,
        'resource_path',
        mock_resource_path)
