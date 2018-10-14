import os
import logging
from .exceptions import InaccessibleFileException
from .s3_gateway import create as create_s3_gateway


class Directory:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    @property
    def entries(self):
        paths = self.directory_handler.listdir(self.path)
        entries = [Entry(f'{self.path}/{path}') for path in paths]

        for entry in entries:
            if self.directory_handler.path.isdir(entry.path):
                entries.extend(Directory(entry.path, self.directory_handler).entries)
                entries = self._get_entries_without_path(entries, entry.path)

        return entries

    def _get_entries_without_path(self, entries, path):
        return list(filter(lambda x: x.path != path, entries))

class Entry:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    def __str__(self):
        return self.path


class BackmeUp:
    def __init__(self, directory_handler, remote_storage_gateway):
        self.directory_handler = directory_handler
        self.remote_storage_gateway = remote_storage_gateway
        self.logger = logging.getLogger('back_me_up.back_me_up.BackmeUp')
        self.logger.setLevel(logging.INFO)

    def sync(self, remote_folder, local_path):
        entries = self._get_entries(local_path)
        for entry in entries:
            self.logger.info(f'Uploading {entry.path}')
            self.remote_storage_gateway.upload(remote_folder, entry.path)

    def _get_entries(self, path):
        if self.directory_handler.path.isdir(path):

            return Directory(path, self.directory_handler).entries

        return [Entry(path, self.directory_handler)]


def create():
    s3_gateway = create_s3_gateway()
    return BackmeUp(os, s3_gateway)
