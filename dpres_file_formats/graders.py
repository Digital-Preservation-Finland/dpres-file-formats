"""Digital preservation grading."""
import functools
from typing import Union

from dpres_file_formats.defaults import Grades, UNAV
from dpres_file_formats.read_file_formats import file_formats, \
    av_container_grading

NUMERIC_QUALITY_TO_GRADE = [Grades.UNACCEPTABLE, Grades.BIT_LEVEL,
                            Grades.WITH_RECOMMENDED, Grades.ACCEPTABLE,
                            Grades.RECOMMENDED]

GRADE_TO_NUMERIC_QUALITY = {
    Grades.RECOMMENDED: 4,
    Grades.ACCEPTABLE: 3,
    Grades.WITH_RECOMMENDED: 2,
    Grades.BIT_LEVEL: 1,
    Grades.UNACCEPTABLE: 0
}


class BaseGrader:
    """Base class for graders."""

    def __init__(self, mimetype: str, version: str, streams: dict[int, dict]):
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

    formats = file_formats(unofficial=True)

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype.lower() in map(lambda f: f["mimetype"].lower(),
                                       cls.formats)

    def grade(self):
        """Return digital preservation grade."""
        grades = list(filter(
            lambda f:
            f["mimetype"].lower() == self.mimetype.lower() and
            f["version"] == self.version,
            self.formats
        ))

        if len(grades) == 0:
            return Grades.UNACCEPTABLE

        return grades[0]["grade"]


class TextGrader(BaseGrader):
    """Grade file based on mimetype, version and charset."""

    formats = file_formats(unofficial=True)

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        # TextGrader accepts mimetypes which are in formats and have allowed
        # charsets list non-empty.
        return bool(list(filter(
            lambda file_format:
            file_format["mimetype"].lower() == mimetype.lower() and
            file_format["charsets"], cls.formats)))

    def grade(self):
        """Return digital preservation grade."""

        def does_match(file_format):
            # Given a file format object, checks if it has a relevant mime
            def in_file_format_charsets(stream_info):
                # Given a stream object, checks if it has acceptable charset
                return stream_info["charset"] in file_format["charsets"]

            return (
                    file_format["mimetype"].lower() ==
                    self.mimetype.lower() and
                    file_format["version"] == self.version and
                    any(map(in_file_format_charsets, self.streams.values())))

        # Find the matching grades (assumed to have only 1 element) from the
        # formats
        grades = list(filter(does_match, self.formats))

        if len(grades) == 0:
            return Grades.UNACCEPTABLE
        return grades[0]["grade"]


def weakest_grade(grades: list[Union[Grades, str]]):
    return NUMERIC_QUALITY_TO_GRADE[
        min(map(lambda x: GRADE_TO_NUMERIC_QUALITY[x], grades))]


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
        return mimetype.lower() in map(
            lambda container: container["mimetype"].lower(),
            cls.av_container_grades)

    def grade(self):
        """Return digital preservation grade."""
        # First stream should be the container
        container = self.streams[0]
        container_mimetype = container["mimetype"].lower()
        container_version = container["version"]

        # Create a set of (mime_type, version) tuples
        # This makes it trivial to check which grade should be assigned.
        contained_formats = {
            (stream["mimetype"].lower(), stream["version"])
            for index, stream in self.streams.items()
            if index != 0
        }

        # When the container has no streams, return RECOMMENDED.
        if len(contained_formats) == 0:
            return Grades.RECOMMENDED

        grading_criteria = self._grading_criteria(container_mimetype.lower(),
                                                  container_version)

        # Find the correct grade for each stream
        grades: list[str] = [
            criterion["grade"]
            for contained_format in contained_formats
            for criterion in grading_criteria if
            contained_format in criterion["streams"]
        ]

        # Return UNACCEPTABLE if some grade was not found.
        if len(grades) != len(contained_formats):
            return Grades.UNACCEPTABLE

        # Select the weakest grade using tables
        return weakest_grade(grades)

    @classmethod
    @functools.cache
    def _grading_criteria(cls, container_mimetype: str,
                          container_version: str) \
            -> list[dict[str, Union[list[tuple[str, str]], str]]]:
        """
        Given container mimetype and version, returns a list in a useful
        form based on av_container_grades.
        :return: List of grades, where each grade is a dict with keys
            ``grade`` and ``streams``.
            Streams are tuples in the form of ``(mimetype, version)``
            and grade is the name of the grade.
        :rtype: list[dict[str, Union[list[tuple[str, str]], str]]]

        """
        # We only care about the entries which have the correct mimetype and
        # version.
        relevant_grades = list(
            filter(
                lambda av_container_grade: (
                        av_container_grade["mimetype"].lower()
                        == container_mimetype and
                        av_container_grade["version"] == container_version
                ),
                cls.av_container_grades)
        )

        def transform_streams(format_object) -> list[tuple[str, str]]:
            return list(
                map(
                    lambda stream: (stream["mimetype"].lower(),
                                    stream["version"]),
                    format_object["audio_streams"] +
                    format_object["video_streams"])
            )

        # Transform grades to a format which is easier to work with
        grading_criteria = list(
            map(
                lambda format_object: {
                    "grade": format_object["grade"],
                    "streams": transform_streams(format_object)
                },
                relevant_grades
            )
        )
        return grading_criteria


class NotContainerStreamsGrader(BaseGrader):
    """
    Gives grades to non-container files based on the amount of their streams.
    """

    # File formats, which contain only a single metadata stream. Excludes AV
    # file formats and gif/tiff formats, because they can contain multiple
    # metadata streams.
    non_container_grades = ((set(map(lambda f: f["mimetype"].lower(),
                                     file_formats(unofficial=True))) -
                             set(map(lambda f: f["mimetype"].lower(),
                                     av_container_grading()))) -
                            {"image/gif", "image/tiff"})

    @classmethod
    def is_supported(cls, mimetype):
        """Check whether grader is supported with given mimetype."""
        return mimetype.lower() in cls.non_container_grades

    def grade(self):
        """Return digital preservation grade."""

        if (len(self.streams)) > 1:
            return Grades.UNACCEPTABLE

        # This grader is only considering the amount of streams. Some other
        # grader might give worse grade, which overrides this.
        return Grades.RECOMMENDED


GRADERS = [MIMEGrader, TextGrader, ContainerStreamsGrader,
           NotContainerStreamsGrader]


def grade(mimetype: str, version: str, streams: dict[int, dict]):
    """Return digital preservation grade."""
    if not mimetype or mimetype == UNAV:
        grade = UNAV
    else:
        grades = [grader(mimetype, version, streams).grade()
                  for grader in GRADERS
                  if grader.is_supported(mimetype)]
        # If no graders support the MIME type, we don't know anything
        # about the MIME type and therefore can not accept it
        if not grades:
            return Grades.UNACCEPTABLE
        # Multiple grades might be returned. For example, Grader (which
        # only performs a quick MIME type check) might grade the main file
        # format as RECOMMENDED, while ContainerStreamsGrader might give it
        # a lower grade because the contained streams do not fulfill the
        # additional requirements.
        #
        # In such cases, pick the lowest assigned grade.
        grade = weakest_grade(grades)
    return grade
