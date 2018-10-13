import os
from .exceptions import InaccessibleFileException
from .s3_gateway import create as create_s3_gateway

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


class BackmeUp:
    def __init__(self, remote_storage_gateway):
        self.remote_storage_gateway = remote_storage_gateway

    def sync(self, remote_folder, local_path):
        self.remote_storage_gateway.upload(remote_folder, local_path)


def create():
    s3_gateway = create_s3_gateway()
    return BackmeUp(s3_gateway)
