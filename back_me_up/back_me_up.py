import os
from .logs import get_logger
from .s3_gateway import create as create_s3_gateway
from .gpg import create as create_gpg
from .directory import Directory, Entry
from .md5 import calculate_md5


class BackmeUp:
    def __init__(self, directory_handler, remote_storage_gateway, gpg_wrapper):
        self.directory_handler = directory_handler
        self.remote_storage_gateway = remote_storage_gateway
        self.gpg_wrapper = gpg_wrapper
        self.logger = get_logger('back_me_up.back_me_up.BackmeUp')

    def sync(self, remote_folder, local_path, email=None):
        entries = self._get_entries(local_path)

        for entry in entries:
            local_hash = calculate_md5(entry.path)
            remote_hash = self._get_remote_md5_hash(remote_folder, entry.path, email)

            if remote_hash != local_hash:
                self._upload_file(remote_folder, entry, local_hash, email)
            else:
                self.logger.info(f'File {entry.path} not changed since last update. Not re-uploading file. \n')

    def _get_remote_md5_hash(self, remote_folder, path, email=None):
        remote_path = f'{path}.gpg' if email else path
        self.logger.debug(f'Getting md5 hash metadata from {remote_folder} for file {remote_path}')

        return self.remote_storage_gateway.get_md5_metadata(remote_folder, remote_path)

    def _upload_file(self, remote_folder, entry, hash, email):
        self.logger.info(f'Uploading {entry.path}')
        self.logger.info(f'Hash md5: ${hash} \n')
        if email:
            self.gpg_wrapper.encrypt_file(entry.path, email)
            entry.path = f'{entry.path}.gpg'
        self.remote_storage_gateway.upload(remote_folder, entry.path, metadata={'md5': hash})

    def _get_entries(self, path):
        if self.directory_handler.path.isdir(path):
            return Directory(path, self.directory_handler).entries
        return [Entry(path, self.directory_handler)]


def create():
    s3_gateway = create_s3_gateway()
    gpg_wrapper = create_gpg()
    return BackmeUp(os, s3_gateway, gpg_wrapper)
