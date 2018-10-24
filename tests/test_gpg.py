import pytest

from pretty_bad_protocol import gnupg
from unittest.mock import Mock
from back_me_up.gpg import GPG


class TestGPG:

    @pytest.yield_fixture(autouse=True)
    def setup(self):
        self.gpg_lib_mocked = Mock(spec=gnupg)
        self.gpg_mock_instance = Mock(spec=gnupg.GPG)
        self.gpg_lib_mocked.GPG.return_value = self.gpg_mock_instance

        yield

    def test_should_pass_arguments_to_lib(self):
        GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')

        self.gpg_lib_mocked.GPG.assert_called_once_with(
            binary='binary path',
            homedir='homedir path'
        )

    def test_should_encrypt_file(self, tmp_path):
        fingerprint = 'some fingerprint'
        file_to_be_encrypted = tmp_path / 'some_file.txt'
        file_to_be_encrypted.write_text('some stuffs to encrypt')

        gpg = GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')
        gpg.encrypt_file(file_to_be_encrypted, fingerprint)

        self.gpg_mock_instance.encrypt.assert_called_once_with(
            b'some stuffs to encrypt',
            fingerprint,
            output=f'{file_to_be_encrypted}.gpg'
        )
