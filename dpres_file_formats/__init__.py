"""Dpres file formats."""

__version__ = '1.1.1'

from dpres_file_formats.read_file_formats import (
    file_formats,
    av_container_grading)
from dpres_file_formats.update_file_formats import (
    add_av_container,
    add_format,
    add_version_to_format,
    replace_format)
from dpres_file_formats.graders import grade

__all__ = ["file_formats",
           "av_container_grading",
           "add_av_container",
           "add_format",
           "add_version_to_format",
           "replace_format",
           "grade"]
