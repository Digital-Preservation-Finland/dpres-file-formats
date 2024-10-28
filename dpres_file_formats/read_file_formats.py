"""Functions that output the file formats list."""

from dpres_file_formats.defaults import (CONTAINERS_STREAMS,
                                         FILE_FORMATS,
                                         Grades)
from dpres_file_formats.json_handler import FileFormatsJson


def supported_file_formats(deprecated=False, unofficial=False):
    """Return supported file formats as a list of dicts.

    :deprecated: Include deprecated (not active) formats and versions
        or not, defaults to False
    :unofficial: Include formats not offically in the DPS spec,
        such as bit level and unoffically supported file formats,
        defaults to False
    :returns: A list of dicts
    """
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)

    formats = []

    if not deprecated or not unofficial:
        for file_format in file_formats:

            include_format = False
            included_versions = []

            # Set file format as active if any version is active or if
            # the format should be included in the output
            for version in file_format.get('versions', []):
                official = any((
                    not unofficial and version.get('added_in_dps_spec', ''),
                    unofficial))
                active = any((not deprecated and version.get('active', False),
                              deprecated))
                if active and official:
                    include_format = True
                    included_versions.append(version)

            # Include only active versions in the output
            file_format['versions'] = included_versions
            if include_format:
                formats.append(file_format)

    else:
        formats = file_formats

    return formats


def supported_file_formats_versions(deprecated=False,
                                    unofficial=False,
                                    basic_info=False):
    """Return a list of flattened dicts of supported file format
    with each version separately.

    :deprecated: Include deprecated (not active) formats and versions
        or not, defaults to False
    :unofficial: Include formats not offically in the DPS spec,
        such as bit level and unoffically supported file formats,
        defaults to False
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
            # the format should be included in the output
            official = any((
                not unofficial and version.get('added_in_dps_spec', ''),
                unofficial))
            active = any((not deprecated and version.get('active', False),
                          deprecated))

            # Add only active format to the output when active is True
            if active and official:
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
