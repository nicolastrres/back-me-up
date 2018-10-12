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


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class BackmeUp:
    pass
