import os
import tempfile
from unittest import mock
from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to, has_length

from back_me_up import Directory, DirectoryEntry, BackmeUp, StatusFile
from back_me_up.exceptions import InaccessibleFileException


class TestDirectory:

    @pytest.fixture
    def directory_handler(self):
        return Mock(spec=os)

    def test_should_return_empty_list_when_no_entries(self, directory_handler):
        directory_handler.listdir.return_value = []

        backup_folder = Directory('/', directory_handler)

        assert_that(backup_folder.entries, equal_to([]))

    def test_should_return_all_entries(self, directory_handler):
        directory_handler.listdir.return_value = ['file1', 'file2']

        backup_folder = Directory('/', directory_handler)

        assert_that(backup_folder.entries, has_length(2))
        assert_that(backup_folder.entries[0].path, equal_to('file1'))
        assert_that(backup_folder.entries[1].path, equal_to('file2'))


class TestDirectoryEntry:
    @mock.patch('os.path.getmtime')
    def test_should_return_last_modified_date(self, getmtime_mocked):
        expected_last_modification_date = 1510431915.0
        getmtime_mocked.return_value = expected_last_modification_date

        with tempfile.NamedTemporaryFile() as file:
            backup_file = DirectoryEntry(file.name)
            last_modified_date = backup_file.last_modification_date

        assert_that(
            expected_last_modification_date, equal_to(last_modified_date)
        )

    def test_should_raise_inaccessible_file_exception_when_file_not_exist(
            self
    ):
        with pytest.raises(InaccessibleFileException) as excinfo:
            __ = DirectoryEntry(  # NOQA
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
            status_file = StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )

            actual_line = file.read()

        assert_that(equal_to(actual_line), b'my_file.txt,1510431915.0\n')

    def test_should_store_file_status_without_overriding_other_files_statuses(
            self
    ):
        with tempfile.NamedTemporaryFile() as file:
            status_file = StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )
            status_file.store_file_last_modification_data(
                'another_file.txt', 1231.11010
            )

            actual_lines = file.readlines()

        assert_that(actual_lines, has_length(2))
        assert_that(b'my_file.txt,1510431915.0\n', equal_to(actual_lines[0]))
        assert_that(b'another_file.txt,1231.1101\n', equal_to(actual_lines[1]))

    def test_read_last_modification_date(self):
        with tempfile.NamedTemporaryFile(delete=False) as file:
            status_file = StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )

            last_modification_date = status_file.get_last_modification_date(
                file_to_backup='my_file.txt'
            )

            assert_that('1510431915.0', equal_to(last_modification_date))

    def test_update_modification_date_of_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as file:
            status_file = StatusFile(file.name)
            status_file.store_file_last_modification_data(
                'my_file.txt', 1510431915.0
            )

            print(status_file.lines)

            status_file.update_last_modification_date(
                'my_file.txt', 222222222.0
            )

            print(status_file.lines)

            assert_that(
                status_file.get_last_modification_date('my_file.txt'),
                equal_to('222222222.0')
            )


class TestBackmeUp:

    @mock.patch('os.path.getmtime')
    def test_should_backup_new_file(self, getmtime_mocked):
        getmtime_mocked.return_value = 12345
        file_storage_service = mock.Mock()
        status_file = mock.Mock()

        with tempfile.TemporaryDirectory() as directory:
            with tempfile.NamedTemporaryFile(dir=directory) as file:
                back_me_up = BackmeUp(
                    status_file=status_file,
                    file_storage_service=file_storage_service
                )

                back_me_up.backup_folder(directory)

        status_file.store_file_last_modification_data.assert_called_once_with(
            os.path.basename(file.name), 12345
        )
        file_storage_service.backup_file(file.name)
