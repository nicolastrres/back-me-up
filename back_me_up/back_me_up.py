import os
from .exceptions import InaccessibleFileException


class Directory:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    @property
    def entries(self):
        entries = self.directory_handler.listdir(self.path)
        return [DirectoryEntry(entry) for entry in entries]


class DirectoryEntry:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    @property
    def last_modification_date(self):
        try:
            return self.directory_handler.path.getmtime(self.path)
        except FileNotFoundError as e:
            raise InaccessibleFileException(self.path, e)


class BackmeUp:
    pass
