"""Functions that add and modify the file formats list."""

from dpres_file_formats.defaults import (
    ALLOWED_CHARSETS,
    ContentTypes,
    FILE_FORMATS_UPDATE,
    DpsSpecVersions,
    Grades,
    RelationshipTypes,
    TechMetadata,
    UNAP
)
from dpres_file_formats.json_handler import FileFormatsJson

FORMAT_ID = 'FI_DPRES_{format_name_short}_{name_count}'
VERSION_ID = '{format_id}_{version_name}'


# pylint: disable=too-many-arguments, too-many-positional-arguments
def add_format(
        mimetype,
        content_type,
        format_name_long,
        format_name_short,
        typical_extensions=None,
        required_metadata='',
        charsets=False):
    """Adds a new file format.

    :mimetype: The MIME type of the file format
    :content_type: The content type, from a controlled vocabulary
    :format_name_long: The full human readable file format name
    :format_name_short: A short file format name (e.g. AAC, MP3)
    :typical_extensions: A list of typical file format extensions
    :required_metadata: Required technical metadata, from a
        controlled vocabulary
    :charsets: A boolean value of whether charset are required

    :returns: The file format ID
    """

    if required_metadata:
        required_metadata = TechMetadata[required_metadata].value

    if charsets:
        charsets = ALLOWED_CHARSETS
    else:
        charsets = []

    if not typical_extensions:
        typical_extensions = []

    file_formats_json = FileFormatsJson()
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS_UPDATE)

    # Count format_name_short for the format_id
    name_count = 1

    for file_format in file_formats:
        if file_format.get('format_name_short', '') == format_name_short:
            name_count += 1

    # Use format_name_short and a running number as base for format_id
    format_id = FORMAT_ID.format(format_name_short=format_name_short,
                                 name_count=name_count)

    format_dict = {
        '_id': format_id,
        'mimetype': mimetype,
        'content_type': ContentTypes[content_type].value,
        'format_name_long': format_name_long,
        'format_name_short': format_name_short,
        'typical_extensions': typical_extensions,
        'required_metadata': required_metadata,
        'charsets': charsets,
        'relations': [],
        'versions': []
    }
    file_formats.append(format_dict)

    file_formats_json.update_file_formats(
        path=FILE_FORMATS_UPDATE,
        file_formats=file_formats)

    return format_id


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
def add_version_to_format(
        format_id,
        grade,
        support_in_dps_ingest,
        active,
        version=None,
        format_registry_key='',
        added_in_dps_spec='',
        removed_in_dps_spec='',
        format_source_pid='',
        format_source_url='',
        format_source_reference=''):
    """Adds a new file format version to to an existing file format. The
    file format must exist and the version cannot be a duplicate of an
    existing version.

    :format_id: The ID of the file format as a string
    :grade: The file format grade in the DPS (e.g. recommended file
        format), from a controlled vocabulary
    :support_in_dps_ingest: The support of the file format version in
        the DPS ingest, as a boolean value
    :active: The status of the file format in the DPS, i.e. is the
        file format version in the latest version of the specifications,
        as a boolean value
    :version: The file format version as a string
    :format_registry_key: The PRONOM format registry key as a string
    :added_in_dps_spec: The DPS specification version, where the file
        format version was added, from a controlled vocabulary
    :removed_in_dps_spec: The DPS specification version, where the file
        format version was removed, from a controlled vocabulary
    :format_source_pid: The file format source ID
    :format_source_url: The file format source URL, requires
        format_source_pid
    :format_source_reference: Bibliographic reference to the file format
        source, requires format_source_pid

    :raises ValueError: if file format is missing, or an existing
        file format version is detected
    """

    version_name = version
    if not version:
        version = UNAP
        version_name = 'UNAP'

    if added_in_dps_spec:
        added_in_dps_spec = DpsSpecVersions[added_in_dps_spec].value

    if removed_in_dps_spec:
        removed_in_dps_spec = DpsSpecVersions[removed_in_dps_spec].value

    format_sources = []
    if format_source_pid:
        format_source = {
            'pid': format_source_pid,
            'url': format_source_url,
            'reference': format_source_reference
        }
        format_sources.append(format_source)

    file_formats_json = FileFormatsJson()
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS_UPDATE)
    format_dict = None
    for file_format in file_formats:
        if file_format['_id'] == format_id:
            format_dict = file_format

    if not format_dict:
        raise ValueError(f"File format {format_id} doesn't exist")

    for versions_dict in format_dict.get('versions', []):
        if version in versions_dict['version']:
            raise ValueError(
                f"Version {version} for file format {format_id} "
                "already exists")

    version_id = VERSION_ID.format(format_id=format_dict['_id'],
                                   version_name=version_name)

    version_dict = {
        '_id': version_id,
        'version': version,
        'grade': Grades[grade].value,
        'format_registry_key': format_registry_key,
        'support_in_dps_ingest': support_in_dps_ingest,
        'active': active,
        'added_in_dps_spec': added_in_dps_spec,
        'removed_in_dps_spec': removed_in_dps_spec,
        'format_sources': format_sources
    }
    try:
        format_dict['versions'].append(version_dict)
    except KeyError:
        format_dict['versions'] = [version_dict]

    file_formats_json.update_file_formats(
        path=FILE_FORMATS_UPDATE,
        file_formats=file_formats)


def replace_format(superseded_format,
                   superseding_format,
                   dps_spec_version):
    """Replaces a format by adding a relationship between two formats,
    where one format supersedes another format. The superseded format
    is deprecated and its versions are marked no longer active and
    unacceptable for digital preservation.

    :superseded_format: ID of the file format that is deprecated
    :superseding_format: ID of the file format that replaces
        the deprecated format
    dps_spec_version: The DPS specification version, where the change
        was published, from a controlled vocabulary
    """

    file_formats_json = FileFormatsJson()
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS_UPDATE)

    superseded_format_id = ''
    superseded_format_mimetype = ''
    superseding_format_id = ''
    superseding_format_mimetype = ''

    dps_spec = DpsSpecVersions[dps_spec_version].value

    for format_dict in file_formats:
        if format_dict['_id'] == superseded_format:
            superseded_format_id = format_dict['_id']
            superseded_format_mimetype = format_dict['mimetype']
        if format_dict['_id'] == superseding_format:
            superseding_format_id = format_dict['_id']
            superseding_format_mimetype = format_dict['mimetype']

    relation = {
        '_id': '',
        'type': '',
        'dps_spec_version': dps_spec,
        'description': (f"MIME type changed from {superseded_format_mimetype} "
                        f"to {superseding_format_mimetype}")
    }

    for format_dict in file_formats:
        if format_dict['_id'] == superseded_format:
            superseded_relation = relation.copy()
            superseded_relation['_id'] = superseding_format_id
            superseded_relation['type'] = RelationshipTypes.SUPERSEDED
            try:
                format_dict['relations'].append(superseded_relation)
            except KeyError:
                format_dict['relations'] = [superseded_relation]

            # Set all versions as inactive and unacceptable for digital
            # preservation for the deprecated format
            for version in format_dict['versions']:
                version['active'] = False
                version['support_in_dps_ingest'] = False
                version['grade'] = Grades['UNACCEPTABLE'].value
                version['removed_in_dps_spec'] = dps_spec

        if format_dict['_id'] == superseding_format:
            superseding_relation = relation.copy()
            superseding_relation['_id'] = superseded_format_id
            superseding_relation['type'] = RelationshipTypes.SUPERSEDES
            try:
                format_dict['relations'].append(superseding_relation)
            except KeyError:
                format_dict['relations'] = [superseding_relation]

    file_formats_json.update_file_formats(
        path=FILE_FORMATS_UPDATE,
        file_formats=file_formats)


def add_source_to_format(version_id,
                         format_source_pid,
                         format_source_url='',
                         format_source_reference=''):
    """Adds a file format version source to a given version.

    :version_id: The ID of the version
    :format_source_pid: The file format source ID
    :format_source_url: The file format source URL, requires
        format_source_pid
    :format_source_reference: Bibliographic reference to the file format
        source, requires format_source_pid
    """
    file_formats_json = FileFormatsJson()
    file_formats = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS_UPDATE)

    format_source = {
        'pid': format_source_pid,
        'url': format_source_url,
        'reference': format_source_reference
    }

    for format_dict in file_formats:
        for version_dict in format_dict.get('versions', []):
            if version_dict['_id'] == version_id:
                try:
                    version_dict['format_sources'].append(format_source)
                except KeyError:
                    version_dict['format_sources'] = [format_source]
                break

    file_formats_json.update_file_formats(
        path=FILE_FORMATS_UPDATE,
        file_formats=file_formats)
