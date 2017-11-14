import os
import tempfile
from unittest import mock

import pytest
from hamcrest import assert_that, equal_to

from back_me_up import back_me_up
from back_me_up.exceptions import InaccessibleFileException


class TestBackupFolder:

    def test_should_return_empty_list_when_no_files(self):
        with tempfile.TemporaryDirectory() as directory:
            backup_folder = back_me_up.BackupFolder(directory)
            actual_files = backup_folder.files

        assert_that([], equal_to(actual_files))

    def test_should_return_all_files(self):
        with tempfile.TemporaryDirectory() as directory:
            with tempfile.NamedTemporaryFile(dir=directory) as file:
                expected_file_path = os.path.basename(file.name)
                backup_folder = back_me_up.BackupFolder(directory)
                actual_file_paths = [file.path for file in backup_folder.files]

        assert_that([expected_file_path], equal_to(actual_file_paths))


class TestBackupFile:
    @mock.patch('os.path.getmtime')
    def test_should_return_last_modified_date(self, getmtime_mocked):
        expected_last_modification_date = 1510431915.0
        getmtime_mocked.return_value = expected_last_modification_date

        with tempfile.NamedTemporaryFile() as file:
            backup_file = back_me_up.BackupFile(file.name)
            last_modified_date = backup_file.last_modification_date

        assert_that(
            expected_last_modification_date, equal_to(last_modified_date)
        )

    def test_should_raise_inaccessible_file_exception_when_file_not_exist(
            self
    ):
        with pytest.raises(InaccessibleFileException) as excinfo:
            __ = back_me_up.BackupFile(  # NOQA
                'non-existent-file.txt'
            ).last_modification_date

        assert_that(
            "File non-existent-file.txt does not exist or "
            "is inaccessible at the moment. Error raised: [Errno 2] No "
            "such file or directory: 'non-existent-file.txt'",
            equal_to(str(excinfo.value))
        )


class TestStatusFile:
    def test_should_store_file_data(self):
        with tempfile.NamedTemporaryFile() as file:
            status_file = back_me_up.StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )

            actual_line = file.read()

        assert_that(b'my_file.txt,1510431915.0', equal_to(actual_line))

    def test_read_last_modification_date(self):
        with tempfile.NamedTemporaryFile(delete=False) as file:
            status_file = back_me_up.StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )

            last_modification_date = status_file.get_last_modification_date(
                file_to_backup='my_file.txt'
            )

            assert_that('1510431915.0', equal_to(last_modification_date))
