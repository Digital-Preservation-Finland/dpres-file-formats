"""Functions to output file formats list."""

import json
from dpres_file_formats.file_formats_list import FILE_FORMATS


def supported_file_formats():
    """Return supported file formats as a list of dicts."""
    return FILE_FORMATS


def supported_file_formats_versions():
    """Return a list of flattened dicts of supported file format
    with each version separately.
    """
    format_versions = []
    for file_format in FILE_FORMATS:
        for version in file_format["versions"]:
            version["mimetype"] = file_format["mimetype"]
            version["content_type"] = file_format["content_type"]
            version["format_name_long"] = file_format["format_name_long"]
            version["format_name_short"] = file_format["format_name_short"]
            version["typical_extensions"] = file_format["typical_extensions"]
            version["required_metadata"] = file_format["required_metadata"]
            version["charsets"] = file_format["charsets"]
        format_versions.append(version)
    return format_versions


def serialize_supported_file_formats():
    """Serialize supported file formats to a string."""
    file_formats = {"file_formats": supported_file_formats()}
    return json.dumps(file_formats, indent=4)


def serialize_supported_file_formats_versions():
    """Print supported file format versions as a string"""
    file_formats = {"file_formats": supported_file_formats_versions()}
    return json.dumps(file_formats, indent=4)
