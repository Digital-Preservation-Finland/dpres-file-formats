"""Module for the class that handles the file format JSON."""

from __future__ import annotations

import json
from os import PathLike

from dpres_file_formats.defaults import CONTAINERS_STREAMS, FILE_FORMATS


def _read(path: str | PathLike) -> list[dict]:
    with open(path, "r", encoding="UTF-8") as json_file:
        return json.load(json_file)["file_formats"]


def _write(path: str | PathLike, file_formats: list[dict]) -> None:
    data = {"file_formats": file_formats}
    with open(path, "w", encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def read_file_formats_json() -> list[dict]:
    """Read file formats from JSON file."""
    return _read(FILE_FORMATS)


def update_file_formats_json(file_formats: list[dict]) -> None:
    """Write file formats to JSON file."""
    _write(FILE_FORMATS, file_formats)


def read_container_streams_json() -> list[dict]:
    """Read container streams from JSON file."""
    return _read(CONTAINERS_STREAMS)


def write_container_streams_json(container_streams: list[dict]) -> None:
    """Write container streams from JSON file."""
    _write(CONTAINERS_STREAMS, container_streams)
