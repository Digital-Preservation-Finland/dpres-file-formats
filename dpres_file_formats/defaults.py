"""Default values."""

CONTENT_TYPES = {
    "text": "text",
    "audio": "audio",
    "video": "video",
    "image": "still image",
    "warc": "web archive",
    "geospatial": "geospatial",
    "database": "database",
    "research": "research",
    "scientific": "scientific"
}

REQUIRED_METADATA = {
    "image": "MIX",
    "audio": "audioMD",
    "video": "videoMD",
    "csv": "ADDML"
}

# (:unap) = Not applicable, makes no sense
# (:unav) = Value unavailable, possibly unknown
# See: https://digitalpreservation.fi/support/vocabularies#Tuntemattomatarvot
UNAP = "(:unap)"
UNAV = "(:unav)"
UNKN = "(:unkn)"

# Digital preservation grading
RECOMMENDED = "fi-dpres-recommended-file-format"
ACCEPTABLE = "fi-dpres-acceptable-file-format"
BIT_LEVEL_WITH_RECOMMENDED \
    = "fi-dpres-bit-level-file-format-with-recommended"
BIT_LEVEL = "fi-dpres-bit-level-file-format"
UNACCEPTABLE = "fi-dpres-unacceptable-file-format"
