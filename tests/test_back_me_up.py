import os
from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to, has_length

from back_me_up import Directory, DirectoryEntry
from back_me_up.exceptions import InaccessibleFileException


@pytest.fixture
def directory_handler():
    return Mock(spec=os)


class TestDirectory:
    def test_should_return_empty_list_when_no_entries(
            self, directory_handler
    ):
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
    def test_should_return_last_modification_date(self, directory_handler):
        directory_handler.path.getmtime.return_value = 1510431915.0

        backup_file = DirectoryEntry('/file1', directory_handler)

        assert_that(
            backup_file.last_modification_date,
            equal_to(1510431915.0)
        )

    def test_should_raise_inaccessible_file_exception_when_file_not_exist(
            self, directory_handler
    ):
        directory_handler.path.getmtime.side_effect = FileNotFoundError(
            "[Errno 2] No such file or directory: 'non-existent-file.txt'"
        )

        with pytest.raises(InaccessibleFileException) as excinfo:
            _ = DirectoryEntry(  # NOQA
                'non-existent-file.txt',
                directory_handler
            ).last_modification_date

        assert_that(
            "File non-existent-file.txt does not exist or "
            "is inaccessible at the moment. Error raised: [Errno 2] No "
            "such file or directory: 'non-existent-file.txt'",
            equal_to(str(excinfo.value))
        )


class TestBackmeUp:
    pass
