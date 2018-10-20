import os
import hashlib
from .logs import get_logger
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
                entries.extend(
                    Directory(entry.path, self.directory_handler).entries
                )
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
        self.logger = get_logger('back_me_up.back_me_up.BackmeUp')

    def sync(self, remote_folder, local_path):
        entries = self._get_entries(local_path)

        for entry in entries:
            local_hash = calculate_md5(entry.path)
            remote_hash = self._get_remote_md5_hash(remote_folder, entry.path)
            if remote_hash != local_hash:
                self._upload_file(remote_folder, entry, local_hash)
            else:
                self.logger.info(f'File {entry.path} not changed since last update. Not re-uploading file. \n')

    def _get_remote_md5_hash(self, remote_folder, path):
        self.logger.debug(f'Getting md5 hash metadata from {remote_folder} for file {path}')
        return self.remote_storage_gateway.get_md5_metadata(remote_folder, path)

    def _upload_file(self, remote_folder, entry, hash):
        self.logger.info(f'Uploading {entry.path}')
        self.logger.info(f'Hash md5: ${hash} \n')
        self.remote_storage_gateway.upload(remote_folder, entry.path, metadata={'md5': hash})

    def _get_entries(self, path):
        if self.directory_handler.path.isdir(path):
            return Directory(path, self.directory_handler).entries
        return [Entry(path, self.directory_handler)]


def create():
    s3_gateway = create_s3_gateway()
    return BackmeUp(os, s3_gateway)


def calculate_md5(path):
    hash = ''
    with open(path, 'rb') as file:
        hash = hashlib.md5(file.read()).hexdigest()

    return hash
