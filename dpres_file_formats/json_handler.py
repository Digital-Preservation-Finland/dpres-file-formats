"""Module for the class that handles the file format JSON."""
import json


class FileFormatsJson:
    """Class for reading and writing the file formats JSON."""
    def __init__(self):
        self._file_formats = []
        self._path = None

    def _read(self):
        """Read file formats from JSON file."""
        with open(self._path, "r", encoding="UTF-8") as json_file:
            self._file_formats = json.load(json_file)["file_formats"]

    def _write(self):
        """Write _file_formats to JSON file."""
        file_formats = {"file_formats": self._file_formats}
        with open(self._path, "w", encoding="UTF-8") as json_file:
            json.dump(file_formats,
                      json_file,
                      indent=4,
                      ensure_ascii=False)

    def read_file_formats(self, path):
        """Return self._file_formats."""
        self._path = path
        self._read()
        return self._file_formats

    def update_file_formats(self, path, file_formats):
        """Updates the file format JSON file."""
        self._path = path
        self._file_formats = file_formats
        self._write()
