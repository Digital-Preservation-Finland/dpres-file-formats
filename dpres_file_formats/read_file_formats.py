"""Functions that output the file formats list."""

from dpres_file_formats.defaults import FILE_FORMATS
from dpres_file_formats.json_handler import FileFormatsJson


def file_formats(deprecated=False,
                 unofficial=False,
                 versions_separately=True):
    """Return file formats as a list of dicts.

    :deprecated: Include deprecated (not active) formats and versions
        or not, defaults to False
    :unofficial: Include formats not offically in the DPS spec,
        such as bit level and unoffically supported file formats,
        defaults to False
    :versions_separately: If set to True, will output the list of each
        file format version as an independent flattened dict, defauls to
        False.
    :returns: A list of dicts
    """
    def _select_format_and_versions():
        """Selects a file format and its versions based on if deprecated
        or unoffical file format versions are to be included in the
        output or not. If a format dict is to be included, it is
        appended to the selected_formats list.
        """
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
            selected_formats.append(file_format)

    def _flatten_format_versions():
        """Split the file format to dicts for each file format version,
        merging file format keys to the version dicts. Each version
        dict is appended to the output_formats list.
        """
        format_dict = file_format.copy()
        # Exclude some file format keys from the output
        for key in ['versions', '_id']:
            try:
                del format_dict[key]
            except KeyError:
                pass

        # Merge file format and version dicts
        for version in file_format.get('versions', []):
            version_dict = version.copy()
            format_dict.update(version_dict)
            output_formats.append(format_dict.copy())

    file_formats_raw = FileFormatsJson().read_file_formats(
        path=FILE_FORMATS)

    selected_formats = []
    output_formats = []

    for file_format in file_formats_raw:
        _select_format_and_versions()

    if not versions_separately:
        output_formats = selected_formats
    else:
        for file_format in selected_formats:
            _flatten_format_versions()

    return output_formats
