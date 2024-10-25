"""Functions that output the file formats list."""

import json
from dpres_file_formats.defaults import (CONTAINERS_STREAMS,
                                         FILE_FORMATS,
                                         Grades)
from dpres_file_formats.json_handler import FileFormatsJson


def supported_file_formats(active=True, dps_spec_formats=True):
    """Return supported file formats as a list of dicts.

    :active: Returns only active formats and versions or not,
        defaults to True
    :dps_spec_formats: Returns only formats offically in the DPS
        spec, discarding bit level and unoffically supported file
        formats, defaults to True
    :returns: A list of dicts
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)

    formats = []

    if active or dps_spec_formats:
        for file_format in file_formats:

            format_active = False
            active_versions = []

            # Set file format as active if any version is active or if
            # the format is a DPS format
            for version in file_format.get('versions', []):
                dps_format = any((
                    dps_spec_formats and version.get('added_in_dps_spec', ''),
                    not dps_spec_formats))
                version_active = any((active and version.get('active', False),
                                      not active))
                if version_active and dps_format:
                    format_active = True
                    active_versions.append(version)

            # Include only active versions in the output
            file_format['versions'] = active_versions
            if format_active:
                formats.append(file_format)

    else:
        formats = file_formats

    return formats


def supported_file_formats_versions(active=True,
                                    dps_spec_formats=True,
                                    basic_info=False):
    """Return a list of flattened dicts of supported file format
    with each version separately.

    :active: Returns only active formats and versions or not,
        defaults to True
    :dps_spec_formats: Returns only formats offically in the DPS
        spec, discarding bit level and unoffically supported file
        formats, defaults to True
    :basic_info: Returns only the mimetype and the version keys
    :returns: A list of dicts
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)

    format_versions = []

    for file_format in file_formats:

        if not basic_info:
            format_dict = file_format.copy()
            # Exclude some file format keys from the output
            for key in ['versions', '_id']:
                try:
                    del format_dict[key]
                except KeyError:
                    pass
        else:
            format_dict = {'mimetype': file_format['mimetype']}

        # Merge file format and version dicts
        for version in file_format.get('versions', []):
            version_dict = version.copy()
            if basic_info:
                version_dict = {'version': version['version']}
            format_dict.update(version_dict)

            # Set file format version as active if it is active or if
            # it is a DPS format
            dps_format = any((
                dps_spec_formats and version.get('added_in_dps_spec', ''),
                not dps_spec_formats))
            version_active = any((active and version.get('active', False),
                                  not active))

            # Add only active format to the output when active is True
            if version_active and dps_format:
                format_versions.append(format_dict)

    return format_versions


def mimetypes_grading(text_formats=False):
    """Return a dictionary of file format gradings for active
    file format versions.

    The grading dictionary is based on mimetypes and their versions.
    Each active file format with the same mimetype have their
    active versions merged in the output.

    :text_files: Return only text formats that require charset
        information, defaults to false
    :return: A dictionary of mimetypes with their graded versions
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)
    mimetypes = {}

    for file_format in file_formats:
        format_versions = {}

        # Populate mimetype dict with active versions only
        for version in file_format.get('versions', []):
            if version.get('active', False):
                format_versions[version['version']] = version.get('grade', '')

        # Add format only if it has active versions
        if format_versions:

            # Add only formats with charsets if text_formats is True
            if any((not text_formats,
                    text_formats and file_format.get('charsets', []))):

                # If mimetype has been added, just add the new versions
                # to the previously added mimetyoe
                if file_format['mimetype'] in mimetypes:
                    mimetypes[file_format['mimetype']].update(format_versions)
                else:
                    mimetypes[file_format['mimetype']] = format_versions

    return mimetypes


def serialize_supported_file_formats(active=True, dps_spec_formats=True):
    """Serialize supported file formats to a string.

    :active: Returns only active formats and versions or not,
        defaults to True
    :dps_spec_formats: Returns only formats offically in the DPS
        spec, discarding bit level and unoffically supported file
        formats, defaults to True
    :returns: A string of serialized JSON data with indentations
    """
    file_formats = {'file_formats': supported_file_formats(
        active=active, dps_spec_formats=dps_spec_formats)}
    return json.dumps(file_formats, indent=4, ensure_ascii=False)


def serialize_supported_file_formats_versions(active=True,
                                              dps_spec_formats=True,
                                              basic_info=False):
    """Serialize supported file format versions to a string.

    :active: Returns only active formats and versions or not,
        defaults to True
    :dps_spec_formats: Returns only formats offically in the DPS
        spec, discarding bit level and unoffically supported file
        formats, defaults to True
    :basic_info: Returns only the mimetype and the version keys
    :returns: A string of serialized JSON data with indentations
    """
    file_formats = {
        'file_formats': supported_file_formats_versions(
            active=active,
            dps_spec_formats=dps_spec_formats,
            basic_info=basic_info)}
    return json.dumps(file_formats, indent=4, ensure_ascii=False)


def find_mimetypes(mimetype):
    """Returns file formats from the file formats list based on
    a given MIME type.

    :mimetype: The MIME type as a string
    :returns: The file formats as a list
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)
    formats = []
    for format_dict in file_formats:
        if format_dict['mimetype'] == mimetype:
            formats.append(format_dict)
    return formats


def mimetypes_format_registry_keys():
    """Returns a dictionary of active mimetypes and their
    corresponding format registry keys.

    :returns: A dictionary of mimetypes with their format registry keys
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)
    mimetypes = {}

    for file_format in file_formats:
        active = False
        format_reg_keys = set()

        # Populate format registry keys dict with data from active
        # versions only
        for version in file_format.get('versions', []):
            if version.get('active', False):
                active = True
                format_reg_keys.add(version.get('format_registry_key', ''))

        # Add format only if it has active versions
        if active:

            # If mimetype has been added, just add the new format
            # registry keys to the previously added mimetyoe
            mimetype = file_format['mimetype']
            if mimetype in mimetypes:
                mimetypes[mimetype].update(format_reg_keys)
            else:
                mimetypes[mimetype] = format_reg_keys

    return mimetypes


def containers_streams_grading(grade=None):
    """Returns a dictionary of AV containers with a grading and
    supported bit streams as tuples.

    :grade: The DPS grade for returning only a certain grade
    :returns: A dictionary of AV containers
    """
    if grade:
        grade = Grades[grade].value

    containers = FileFormatsJson().read_file_formats(
        path=CONTAINERS_STREAMS)

    selected_containers = {}

    for container_dict in containers:

        # Construct stream tuples
        streams = set()
        for stream in container_dict.get('audio_streams', []):
            streams.add((stream['mimetype'], stream['version']))
        for stream in container_dict.get('video_streams', []):
            streams.add((stream['mimetype'], stream['version']))

        if any((grade and container_dict.get('grade', '') == grade,
                not grade)):

            # The mimetype is not a unique key when returning all
            # containers regardless of grade
            mimetype = container_dict['mimetype']
            if mimetype in selected_containers:
                containers[mimetype].update(streams)
            else:
                selected_containers[mimetype] = streams

    return selected_containers
