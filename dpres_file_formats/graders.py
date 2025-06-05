"""Digital preservation grading."""
from typing import Any

from dpres_file_formats.defaults import Grades, UNKN, UNAP


class BaseGrader:
    """Base class for graders."""

    def __init__(self, mimetype: str, version: str, streams: iter(Any)):
        """Initialize grader."""
        self._mimetype = mimetype
        self._version = version
        self._streams = streams

    @property
    def mimetype(self):
        """MIME type of the file to grade"""
        return self._mimetype

    @property
    def version(self):
        """MIME version of the file to grade"""
        return self._version

    @property
    def streams(self):
        """List of streams of the file to grade"""
        return self._streams

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        raise NotImplementedError

    def grade(self):
        """Determine and return digital preservation grade for the file."""
        raise NotImplementedError


class MIMEGrader(BaseGrader):
    """Grade file based on mimetype and version."""

    formats = {
        "application/epub+zip": {
            "2.0.1": Grades.RECOMMENDED,
            "3": Grades.RECOMMENDED
        },
        "application/pdf": {
            "A-1a": Grades.RECOMMENDED,
            "A-1b": Grades.RECOMMENDED,
            "A-2a": Grades.RECOMMENDED,
            "A-2b": Grades.RECOMMENDED,
            "A-2u": Grades.RECOMMENDED,
            "A-3a": Grades.RECOMMENDED,
            "A-3b": Grades.RECOMMENDED,
            "A-3u": Grades.RECOMMENDED,
            "1.2": Grades.ACCEPTABLE,
            "1.3": Grades.ACCEPTABLE,
            "1.4": Grades.ACCEPTABLE,
            "1.5": Grades.ACCEPTABLE,
            "1.6": Grades.ACCEPTABLE,
            "1.7": Grades.ACCEPTABLE
        },
        "application/geopackage+sqlite3": {
            "1.3.0": Grades.RECOMMENDED,
            "1.3.1": Grades.RECOMMENDED
        },
        "application/matlab": {
            "7": Grades.RECOMMENDED,
            "7.3": Grades.RECOMMENDED
        },
        "application/msword": {
            "97-2003": Grades.ACCEPTABLE
        },
        "application/mxf": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "application/postscript": {
            "3.0": Grades.ACCEPTABLE
        },
        "application/vnd.ms-excel": {
            "8": Grades.ACCEPTABLE,
            "8X": Grades.ACCEPTABLE
        },
        "application/vnd.ms-powerpoint": {
            "97-2003": Grades.ACCEPTABLE
        },
        "application/vnd.oasis.opendocument.formula": {
            "1.0": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED
        },
        "application/vnd.oasis.opendocument.graphics": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED
        },
        "application/vnd.oasis.opendocument.presentation": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED
        },
        "application/vnd.oasis.opendocument.spreadsheet": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED
        },
        "application/vnd.oasis.opendocument.text": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED
        },
        "application/vnd.openxmlformats-officedocument.presentationml."
        "presentation": {
            "2007 onwards": Grades.ACCEPTABLE
        },
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
            "2007 onwards": Grades.ACCEPTABLE
        },
        "application/vnd.openxmlformats-officedocument.wordprocessingml."
        "document": {
            "2007 onwards": Grades.ACCEPTABLE
        },
        "application/warc": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED
        },
        "application/x.fi-dpres.atlproj": {
            "(:unap)": Grades.WITH_RECOMMENDED
        },
        "application/x.fi-dpres.segy": {
            "1.0": Grades.BIT_LEVEL,
            "2.0": Grades.BIT_LEVEL,
            UNKN: Grades.BIT_LEVEL
        },
        "application/x-hdf5": {
            "1.10": Grades.RECOMMENDED
        },
        "application/x-siard": {
            "2.1.1": Grades.RECOMMENDED,
            "2.2": Grades.RECOMMENDED
        },
        "application/x-spss-por": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/aac": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/flac": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/l8": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/l16": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/l20": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/l24": {
            UNAP: Grades.RECOMMENDED
        },
        "audio/mp4": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "audio/mpeg": {
            "1": Grades.ACCEPTABLE,
            "2": Grades.ACCEPTABLE
        },
        "audio/x-aiff": {
            UNAP: Grades.ACCEPTABLE,  # AIFF-C
            "1.3": Grades.RECOMMENDED  # AIFF
        },
        "audio/x-ms-wma": {
            "9": Grades.ACCEPTABLE
        },
        "audio/x-wav": {
            UNAP: Grades.RECOMMENDED,  # WAV
            "2": Grades.RECOMMENDED  # BWF
        },
        "image/gif": {
            "1987a": Grades.ACCEPTABLE,
            "1989a": Grades.ACCEPTABLE
        },
        "image/jp2": {
            UNAP: Grades.RECOMMENDED
        },
        "image/jpeg": {
            "1.00": Grades.RECOMMENDED,
            "1.01": Grades.RECOMMENDED,
            "1.02": Grades.RECOMMENDED,
            "2.0": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.1": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.2": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.2.1": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.3": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.3.1": Grades.RECOMMENDED,  # JPEG/EXIF
            "2.3.2": Grades.RECOMMENDED,  # JPEG/EXIF
        },
        "image/png": {
            "1.2": Grades.RECOMMENDED
        },
        "image/svg+xml": {
            "1.1": Grades.RECOMMENDED
        },
        "image/tiff": {
            "6.0": Grades.RECOMMENDED,  # TIFF
            "1.0": Grades.RECOMMENDED,  # GeoTiff
        },
        "image/webp": {
            UNAP: Grades.RECOMMENDED
        },
        "image/x-adobe-dng": {
            "1.1": Grades.RECOMMENDED,
            "1.2": Grades.RECOMMENDED,
            "1.3": Grades.RECOMMENDED,
            "1.4": Grades.RECOMMENDED,
            "1.5": Grades.RECOMMENDED
        },
        "image/x-dpx": {
            "1.0": Grades.ACCEPTABLE,  # Allowed for special case
            "2.0": Grades.RECOMMENDED
        },
        "model/step": {
            "4.0.2.1": Grades.RECOMMENDED,
            "4.3.2.0": Grades.RECOMMENDED
        },
        "video/avi": {  # Container
            UNAP: Grades.ACCEPTABLE
        },
        "video/dv": {
            UNAP: Grades.ACCEPTABLE
        },
        "video/h264": {
            UNAP: Grades.RECOMMENDED
        },
        "video/h265": {
            UNAP: Grades.RECOMMENDED
        },
        "video/jpeg2000": {
            UNAP: Grades.RECOMMENDED
        },
        "video/mj2": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "video/mp1s": {  # Container
            UNAP: Grades.ACCEPTABLE
        },
        "video/mp2p": {  # Container
            UNAP: Grades.ACCEPTABLE
        },
        "video/mp2t": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "video/mp4": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "video/mpeg": {
            "1": Grades.ACCEPTABLE,
            "2": Grades.ACCEPTABLE
        },
        "video/quicktime": {  # Container
            UNAP: Grades.RECOMMENDED
        },
        "video/x.fi-dpres.prores": {
            UNAP: Grades.WITH_RECOMMENDED
        },
        "video/x-ffv": {
            "3": Grades.RECOMMENDED
        },
        "video/x-matroska": {  # Container
            "4": Grades.RECOMMENDED
        },
        "video/x-ms-asf": {  # Container
            UNAP: Grades.ACCEPTABLE
        },
        "video/x-ms-wmv": {
            "9": Grades.ACCEPTABLE
        },
    }

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype in cls.formats

    def grade(self):
        """Return digital preservation grade."""
        try:
            grade = self.formats[self.mimetype][self.version]
        except KeyError:
            grade = Grades.UNACCEPTABLE

        return grade


class TextGrader(BaseGrader):
    """Grade file based on mimetype, version and charset."""

    formats = {
        "application/xhtml+xml": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED,
            "5": Grades.RECOMMENDED
        },
        "application/gml+xml": {
            "3.2.2": Grades.RECOMMENDED,
        },
        "application/vnd.google-earth.kml+xml": {
            "2.3": Grades.RECOMMENDED,
        },
        "text/csv": {
            UNAP: Grades.RECOMMENDED
        },
        "text/html": {
            "4.01": Grades.RECOMMENDED,
            "5": Grades.RECOMMENDED
        },
        "text/plain": {
            UNAP: Grades.RECOMMENDED
        },
        "text/xml": {
            "1.0": Grades.RECOMMENDED,
            "1.1": Grades.RECOMMENDED
        },
    }

    allowed_charsets = ['ISO-8859-15', 'UTF-8', 'UTF-16', 'UTF-32']

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype in cls.formats

    def grade(self):
        """Return digital preservation grade."""
        try:
            grade = self.formats[self.mimetype][self.version]
        except KeyError:
            grade = Grades.UNACCEPTABLE

        for stream in self.streams.values():
            if stream['charset'] not in self.allowed_charsets:
                grade = Grades.UNACCEPTABLE

        return grade


class ContainerStreamsGrader(BaseGrader):
    """
    Grade file based on what certain containers are allowed to contain.
    This grader does not check the grade of the container itself, the grade
    of the container should be evaluated by MIMEGrader.

    Requirements based on DPRES File Formats specification 1.11.0, section 6,
    tables 2 and 3.
    """
    recommended_formats = {
        # Recommended
        "application/mxf": {
            # Audio
            ("audio/aac", UNAP),
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/h264", UNAP),
            ("video/jpeg2000", UNAP),
        },
        "audio/mp4": {
            ("audio/aac", UNAP)
        },
        "video/mj2": {
            # Audio
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/jpeg2000", UNAP),
        },
        "video/mp2t": {
            # Audio
            ("audio/aac", UNAP),

            # Video
            ("video/h264", UNAP),
            ("video/h265", UNAP)
        },
        "video/mp4": {
            # Audio
            ("audio/aac", UNAP),

            # Video
            ("video/h264", UNAP),
            ("video/h265", UNAP)
        },
        "video/quicktime": {
            # Audio
            ("audio/aac", UNAP),
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/h264", UNAP),
            ("video/h265", UNAP),
            ("video/jpeg2000", UNAP),
        },
        "video/x-matroska": {
            # Audio
            ("audio/flac", UNAP),
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/h265", UNAP),
            ("video/x-ffv", "3")
        },
    }
    acceptable_formats = {
        # Acceptable
        "application/mxf": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/dv", UNAP),
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/avi": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/dv", UNAP),
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/dv": {
            # Audio
            ("audio/l8", UNAP),
            ("audio/l16", UNAP),
            ("audio/l20", UNAP),
            ("audio/l24", UNAP),

            # Video
            ("video/dv", UNAP)
        },
        "video/mp1s": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/mp2p": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/mp2t": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/mp4": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/quicktime": {
            # Audio
            ("audio/mpeg", "1"),
            ("audio/mpeg", "2"),

            # Video
            ("video/dv", UNAP),
            ("video/mpeg", "1"),
            ("video/mpeg", "2"),
        },
        "video/x-ms-asf": {
            # Audio
            ("audio/x-ms-wma", "9"),

            # Video
            ("video/x-ms-wmv", "9"),
        },
    }
    bit_level_recommended_formats = {
        "video/quicktime": {
            # Video
            ("video/x.fi-dpres.prores", UNAP),
        }
    }

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return (
                mimetype in cls.recommended_formats
                or mimetype in cls.acceptable_formats
        )

    def grade(self):
        """Return digital preservation grade."""
        # First stream should be the container
        container = self.streams[0]
        container_mimetype = container["mimetype"]

        # Create a set of (mime_type, version) tuples
        # This makes it trivial to check which grade should be assigned
        # using set operations.
        contained_formats = {
            (stream["mimetype"], stream["version"])
            for index, stream in self.streams.items()
            if index != 0
        }

        recommended = self.recommended_formats.get(container_mimetype, set())
        acceptable = self.acceptable_formats.get(container_mimetype, set())
        bit_level_recommended = self.bit_level_recommended_formats.get(
            container_mimetype, set()
        )

        formats_left_after_recommended = contained_formats - recommended
        formats_left_after_acceptable = (
                formats_left_after_recommended - acceptable
        )
        formats_left_after_bit_level_recommended = (
                formats_left_after_acceptable - bit_level_recommended
        )

        if not formats_left_after_recommended:
            # Only contains recommended formats or contains nothing at all
            grade = Grades.RECOMMENDED
        elif not formats_left_after_acceptable:
            # Contains at least one acceptable format
            grade = Grades.ACCEPTABLE
        elif not formats_left_after_bit_level_recommended:
            # Contains at least one bit_level_with_recommended format
            grade = Grades.WITH_RECOMMENDED
        else:
            # Contains at least one unacceptable format
            grade = Grades.UNACCEPTABLE

        return grade
