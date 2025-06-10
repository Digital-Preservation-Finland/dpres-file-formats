"""Digital preservation grading."""
from typing import Any

from dpres_file_formats.defaults import Grades
from dpres_file_formats.read_file_formats import file_formats, \
    av_container_grading


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

    formats = file_formats()

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype in map(lambda f: f["mimetype"], cls.formats)

    def grade(self):
        """Return digital preservation grade."""
        try:
            grade = list(
                filter(
                    lambda f: f["mimetype"] == self.mimetype and
                              f["version"] == self.version,
                    self.formats
                )
            )[0]["grade"]
        except IndexError:
            grade = Grades.UNACCEPTABLE

        return grade


class TextGrader(BaseGrader):
    """Grade file based on mimetype, version and charset."""

    formats = file_formats()

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        # TextGrader accepts mimetypes which are in formats and have allowed
        # charsets list non-empty.
        return bool([file_format for file_format in cls.formats if
                     file_format["mimetype"] == mimetype and
                     bool(file_format["charsets"])])

    def grade(self):
        """Return digital preservation grade."""
        try:
            grade = list(
                filter(
                    lambda f: f["mimetype"] == self.mimetype and
                              f["version"] == self.version and
                              any(
                                  map(lambda s: s["charset"] in f["charsets"],
                                      self.streams.values()
                                      )
                              ),
                    self.formats
                )
            )[0]["grade"]
        except IndexError:
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

    av_container_grades = av_container_grading()

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype in map(
            lambda container: container["mimetype"] and container["version"],
            cls.av_container_grades)

    def grade(self):
        """Return digital preservation grade."""
        # First stream should be the container
        container = self.streams[0]
        container_mimetype = container["mimetype"]
        container_version = container["version"]

        # Create a set of (mime_type, version) tuples
        # This makes it trivial to check which grade should be assigned
        # using set operations.
        contained_formats = {
            (stream["mimetype"].lower(), stream["version"])
            for index, stream in self.streams.items()
            if index != 0
        }

        relevant_grades = list(
            filter(
                lambda x: (
                        x["mimetype"].lower() == container_mimetype.lower() and
                        x["version"] == container_version
                ),
                self.av_container_grades)
        )

        transform_streams = lambda obj: list(
            map(
                lambda s: (s["mimetype"].lower(), s["version"]),
                obj["audio_streams"] + obj["video_streams"])
        )

        grading_criteria = list(
            map(
                lambda old: {
                    "grade": old["grade"],
                    "streams": transform_streams(old)
                },
                relevant_grades
            )
        )

        matching = [y for y in grading_criteria if
                    all(map(lambda s: s in y["streams"], contained_formats))]

        if len(matching) == 0:
            return Grades.UNACCEPTABLE

        return matching[0]["grade"]
