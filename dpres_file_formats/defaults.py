"""Default values and controlled vocabularies."""
import enum

# Installed version under /usr/share, for accessing data
FILE_FORMATS_JSON = "/usr/share/dpres-file-formats/file_formats.json"
# Local version in project folder, for updating data
FILE_FORMATS_JSON_UPDATE = "dpres_file_formats/file_formats.json"

# Allowed charsets
ALLOWED_CHARSETS = ["ISO-8859-15", "UTF-8", "UTF-16", "UTF-32"]

# (:unap) = Not applicable, makes no sense
# See: https://digitalpreservation.fi/support/vocabularies#Tuntemattomatarvot
UNAP = "(:unap)"


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
    """Controllec vocabulary for DPS File Format specification
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
