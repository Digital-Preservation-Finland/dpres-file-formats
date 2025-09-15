"""Default values and controlled vocabularies."""
import enum

# Python module containing data files
DATA_MODULE_NAME = "dpres_file_formats.data"

# Name of the file formats json file
FILE_FORMATS_NAME = "file_formats.json"
# Name of the file formats json file
CONTAINERS_STREAMS_NAME = "av_container_grading.json"

# Allowed charsets
ALLOWED_CHARSETS = ["ISO-8859-15", "UTF-8", "UTF-16", "UTF-32"]


class UnknownValues(str, enum.Enum):
    """
    Controlled vocabulary for unknown values

    Enums UVNONE and UVNULL have a prefix UV (UnknownValues) to avoid confusion
    with other truly None or Null values which are Falsy values unlike UVNONE
    and UVNULL string literals.

    Values available on the digital preservation website:
    https://digitalpreservation.fi/support/vocabularies#Tuntemattomatarvot
    """
    UNAC = "(:unac)"  # Temporarily inaccessible
    UNAL = "(:unal)"  # Unallowed, suppressed intentionally
    UNAP = "(:unap)"  # Not applicable, makes no sense
    UNAS = "(:unas)"  # Value unassigned (e.g., Untitled)
    UNAV = "(:unav)"  # Value unavailable, possibly unknown
    UNKN = "(:unkn)"  # Known to be unknown (e.g., Anonymous, Inconnue)
    UVNONE = "(:none)"  # Never had a value, never will
    UVNULL = "(:null)"  # Explicitly and meaningfully empty
    TBA = "(:tba)"    # To be assigned or announced later
    ETAL = "(:etal)"  # Too numerous to list (et alia)


class ContentTypes(str, enum.Enum):
    """Controlled vocabulary for content types.

    Values taken from the DPS specification content types:
    https://urn.fi/urn:nbn:fi-fe2020100578096
    """
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "still image"
    WARC = "web archive"
    GEOSPATIAL = "geospatial data"
    DATABASE = "databases"
    RESEARCH = "research data"
    SCIENTIFIC = "scientific software"
    AUDIOCONTAINER = "audiocontainer"
    VIDEOCONTAINER = "videocontainer"


class TechMetadata(str, enum.Enum):
    """Controlled vocabulary for required technical metadata
    schema.
    """
    IMAGE = "MIX"
    AUDIO = "audioMD"
    VIDEO = "videoMD"
    CSV = "ADDML"


class RelationshipTypes(str, enum.Enum):
    """Controlled vocabulary for relationship types.

    Taken from PREMIS relationships:
    https://id.loc.gov/vocabulary/preservation/relationshipSubType.html
    """
    SUPERSEDED = "is superseded by"
    SUPERSEDES = "supersedes"


class Grades(str, enum.Enum):
    """Controlled vocabulary for digital preservation grading."""
    RECOMMENDED = "fi-dpres-recommended-file-format"
    ACCEPTABLE = "fi-dpres-acceptable-file-format"
    WITH_RECOMMENDED = "fi-dpres-bit-level-file-format-with-recommended"
    BIT_LEVEL = "fi-dpres-bit-level-file-format"
    UNACCEPTABLE = "fi-dpres-unacceptable-file-format"


class DpsSpecVersions(str, enum.Enum):
    """Controlled vocabulary for DPS File Format specification
    versions.
    """
    V3 = "1.3.0"
    V4 = "1.4.0"
    V5 = "1.5.0"
    V6 = "1.6.0"
    V7 = "1.7.0"
    V8 = "1.8.0"
    V9 = "1.9.0"
    V10 = "1.10.0"
    V11 = "1.11.0"
    V12 = "1.12.0"
    V13 = "1.13.0"
