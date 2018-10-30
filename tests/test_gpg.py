import pytest

from pretty_bad_protocol import gnupg
from unittest.mock import Mock
from back_me_up.gpg import GPG
from hamcrest import assert_that, equal_to
from back_me_up.exceptions import GPGKeyNotFound


class TestGPG:
    @pytest.yield_fixture(autouse=True)
    def setup(self):
        self.gpg_lib_mocked = Mock(spec=gnupg)
        self.gpg_mock_instance = Mock(spec=gnupg.GPG)
        self.gpg_lib_mocked.GPG.return_value = self.gpg_mock_instance
        self.gpg_mock_instance.list_keys.return_value = [
            {
                'uids': ['Nicolas Agustin <nicolastrres@gmail.com>'],
                'fingerprint': 'some fingerprint'
            }
        ]

        yield

    def test_should_pass_arguments_to_lib(self):
        GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')

        self.gpg_lib_mocked.GPG.assert_called_once_with(
            binary='binary path',
            homedir='homedir path'
        )

    def test_should_encrypt_file(self, tmp_path):
        file_to_be_encrypted = tmp_path / 'some_file.txt'
        file_to_be_encrypted.write_text('some stuffs to encrypt')

        gpg = GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')
        gpg.encrypt_file(file_to_be_encrypted, email='nicolastrres@gmail.com')

        self.gpg_mock_instance.encrypt.assert_called_once_with(
            b'some stuffs to encrypt',
            'some fingerprint',
            output=f'{file_to_be_encrypted}.gpg'
        )

    def test_get_fingerprint_by_email(self):
        self.gpg_mock_instance.list_keys.return_value = [
            {
                'uids': ['Nicolas Agustin <nicolastrres@gmail.com>'],
                'fingerprint': 'some fingerprint'
            }
        ]

        gpg = GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')

        assert_that(gpg.get_fingerprint('nicolastrres'), equal_to('some fingerprint'))

    def test_should_raise_an_error_if_no_gpg_key_found(self):
        self.gpg_mock_instance.list_keys.return_value = []

        gpg = GPG(self.gpg_lib_mocked, binary='binary path', homedir='homedir path')

        with pytest.raises(GPGKeyNotFound) as error_raised:
            gpg.get_fingerprint('someemail@gmail.com')

        assert_that(
            error_raised.value.message,
            equal_to(('GPG key associated with email someemail@gmail.com was not found'))
        )
