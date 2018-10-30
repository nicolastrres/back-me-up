import os

from pretty_bad_protocol import gnupg
from back_me_up.exceptions import GPGKeyNotFound


class GPG:
    def __init__(self, gpg_lib, binary=None, homedir=None):
        self.gpg = gpg_lib.GPG(binary=binary, homedir=homedir)

    def encrypt_file(self, file_path, email):
        fingerprint = self.get_fingerprint(email)
        with open(file_path, 'rb') as file:
            data = file.read()
            self.gpg.encrypt(data, fingerprint, output=f'{file_path}.gpg')

    def get_fingerprint(self, email):
        key = self._get_key_by_email(email)
        if key is None:
            raise GPGKeyNotFound(email)
        return self._get_key_by_email(email)['fingerprint']

    def _get_key_by_email(self, email):
        return next((key for key in self.gpg.list_keys() if self._email_in_uids(email, key['uids'])), None)

    def _email_in_uids(self, email, uids):
        return any([uid for uid in uids if email in uid])


def create():
    binary = os.environ.get('GPG_BINARY')
    homedir = os.environ.get('GPG_HOMEDIR')
    return GPG(gnupg, binary=binary, homedir=homedir)
