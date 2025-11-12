"""Functions that output the file formats list."""
from __future__ import annotations

from dpres_file_formats.json_handler import (
    read_container_streams_json,
    read_file_formats_json,
)


def _select_format_and_versions(
    file_formats_raw: list[dict],
    include_deprecated: bool,
    include_unofficial: bool,
) -> list[dict]:
    """Selects a file format and its versions based on if deprecated
    or unofficial file format versions are to be included in the
    output or not. If a format dict is to be included, it is
    included in the returned list.

    :param file_formats_raw: List of file format dicts.
    :param deprecated: Should deprecated versions be included.
    :param unofficial: Should formats not officially in dps spec be included.
    :returns: List of file formats with filtered versions.
    """
    selected_formats = []

    for file_format in file_formats_raw:
        include_format = False
        included_versions = []
        # Set file format as active if any version is active or if
        # the format should be included in the output
        for version in file_format.get("versions", []):
            is_official_version = version.get("added_in_dps_spec", "")
            is_active_version = version.get("active", False)

            official_ok = include_unofficial or is_official_version
            status_ok = include_deprecated or is_active_version

            if official_ok and status_ok:
                include_format = True
                included_versions.append(version)

        if include_format:
            # Include only active versions in the output
            file_format["versions"] = included_versions
            selected_formats.append(file_format)

    return selected_formats


def _flatten_format_versions(selected_formats: list[dict]) -> list[dict]:
    """Split the file format to dicts for each file format version,
    merging file format keys to the version dicts.

    :param selected_formats: List of file foramts with filtered versions.
    :returns: List of flattened version dicts.
    """
    output_formats = []
    for file_format in selected_formats:
        format_dict = file_format.copy()
        # Exclude unwanted file format keys from the output
        for key in ["versions", "_id"]:
            try:
                del format_dict[key]
            except KeyError:
                pass

        # Merge file format and version dicts
        for version_dict in file_format.get("versions", []):
            merged_dict = {**format_dict, **version_dict}
            output_formats.append(merged_dict)

    return output_formats


def file_formats(
    deprecated: bool = False,
    unofficial: bool = False,
    versions_separately: bool = True,
    data: dict | None = None
) -> list[dict]:
    """Return file formats as a list of dicts with optional filtering and
        flattening.

    :param deprecated: Include deprecated (not active) formats and versions
        or not, defaults to False
    :param unofficial: Include formats not officially in the DPS spec,
        such as bit level and unofficially supported file formats,
        defaults to False
    :param versions_separately: If set to True, will output the list of each
        file format version as an independent flattened dict, defaults
        to False.
    :param data: Optional file format data dictionary. If not provided, the
        package's built-in file format data will be used instead.

    :returns: List of file format dicts.
    """
    if data:
        # Valid file format data has 'file_formats' as the root key
        data = data["file_formats"]
    else:
        data = read_file_formats_json()

    selected_formats = _select_format_and_versions(
        data, deprecated, unofficial
    )

    if not versions_separately:
        return selected_formats
    return _flatten_format_versions(selected_formats)


def av_container_grading() -> list[dict]:
    """Return information about supported av containers"""
    return read_container_streams_json()
