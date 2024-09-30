"""A machine-readable list of supported file formats."""

from dpres_file_formats.defaults import (
    CONTENT_TYPES,
    REQUIRED_METADATA,
    RECOMMENDED,
    UNAP
)


FILE_FORMATS = [
    {
        "_id": "FI_DPRES_AAC_1",
        "mimetype": "audio/aac",
        "content_type": CONTENT_TYPES["audio"],
        "format_name_long": "Advanced Audio Coding",
        "format_name_short": "AAC",
        "typical_extensions": [".aac", ".m4a", ".mp4"],
        "required_metadata": REQUIRED_METADATA["audio"],
        "charsets": [],
        "versions": [
            {
                "_id": "FI_DPRES_AAC_1_NONE",
                "version": UNAP,
                "grade": RECOMMENDED,
                "format_registry_key": "fmt/199",
                "support_in_dps_ingest": True,
                "active": True,
                "added_in_dps_spec": "1.3",
                "removed_in_dps_spec": "",
                "format_spec_sources": [
                    {
                        "pid": "ISO_14496-3:2019",
                        "url": "",
                        "reference": ("International Organization for "
                                      "Standardization. Information "
                                      "technology — Coding of audio-visual "
                                      "objects — Part 3: Audio. "
                                      "ISO/IEC 14496-3:2019")
                    }
                ]
            }
        ]
    }
]
