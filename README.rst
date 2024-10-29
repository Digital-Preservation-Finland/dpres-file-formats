dpres / dpres-file-formats
==========================

This project contains a machine-readable registry in JSON about file
formats supported in the National Digital Preservation Services in Finland.

The project also contains python functions for reading information from the
JSON registry and for updating the registry.

Requirements
------------

Installation and usage requires Python 3.9 or newer.
The software is tested with Python 3.9 on AlmaLinux 9 release.

DPS Specifications Version
--------------------------

This file format list conforms to the following version of the DPS file
format specifications::

    1.12.0

See:

    * https://urn.fi/urn:nbn:fi-fe2020100578095 (in Finnish, official version)
    * https://urn.fi/urn:nbn:fi-fe2020100578096 (English translation)


Read the file formats
---------------------

Read and output the format registry in the following way::

    from dpres_file_formats.read_file_formats import file_formats
    file_formats(deprecated=False, unofficial=False, versions_separately=False)

The following arguments exist:
    * Include decprecated formats:  ``deprecated`` . When set to ``True``, the
      functions will also include deprecated, inactive file formats in the
      output.
    * Include unofficial formats: ``unofficial``. When set to ``True``, the
      functions will also include file formats not offically in the DPS spec in
      the output. This includes bit level file formats and formats with
      technical level support in the DPS ingest.
    * Output each version separately: ``versions_separately``. When set to
      ``True``, outputs a flattened list of each file format version displayed
      separately.

Output MIME types and their versions with a grading, which indicates their
level of support in the DPS::

     mimetype_grading()

Using the argument ``text_formats`` with the value "True" will output only text
based formats that require charset information.

Return AV containers with supported bit streams and the DPS grading for the
combination::

    containers_streams_grading(grade=None)

The argument ``grade`` is used for returning the container and streams with a
certain DPS grade.

Update file formats
-------------------

The file formats JSON can be updated using the following two functions, one
that adds a new format to the registry and another that adds a new file format
version to a format.

Adding a new format to the JSON registry::

    add_format(mimetype, content_type, format_name_long, format_name_short, **)

The following arguments exist:

    * MIME type: ``mimetype``
    * The content type (e.g. text, audio): ``content_type``
    * The full file format name: ``format_name_long``
    * A shorted file format name identifier: ``format_name_short``
    * A list of typical file format extensions: ``typical_extensions``
    * Required technical metadata: ``required_metadata``
    * A boolean of if character sets are mandatory (for text formats): ``charsets``

The ``format_name_short`` is used as a part of the file format identifier which is
created automatically when adding a file format. The arguments ``content_type``
and ``required_metadata`` require controlled vocabularies.

Adding a new file format version to a file format in the reigistry::

    add_version_to_format(format_id, grade, support_in_dps_ingest, active, added_in_dps_spec, **)

The following arguments exist:

    * The file format ID: ``format_id``
    * The file format version grade in the DPS: ``grade``
    * The current support in the DPS ingest as a boolean: ``support_in_dps_ingest``
    * The current status (active, inactive) in the DPS specifications as a boolean: ``active``
    * The DPS specifications version where the version was added: ``added_in_dps_spec``
    * The file format version: ``version``
    * An external file format registry key: ``format_registry_key``
    * The DPS specifications version where the version was removed: ``removed_in_dps_spec``
    * An ID for a file format source: ``format_source_pid``
    * A URL for a file format source: ``format_source_url``
    * A reference to a file format source: ``format_source_reference``

If the ``version`` is given as None, a value ``(:unap)`` will be set for the file
format version. The file format version identifier will be created automatically
based on the file format ID and the file format version. The arguments ``grade``,
``added_in_dps_spec`` and ``removed_in_dps_spec`` require controlled vocabularies.

A file format can replace another file format with the function::

    replace_format(superseded_format, superseding_format, dps_spec_version)

Where ``superseded_format`` is the ID of the replaced format and ``superseding_format``
is the ID of the format that replaces the previous format. The argument
``dps_spec_version`` denotes the DPS file format specification version where
the change occured.
