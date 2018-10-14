import os
from unittest.mock import Mock, call

import pytest
from hamcrest import assert_that, equal_to, has_length

from back_me_up.back_me_up import Directory, BackmeUp
from back_me_up.s3_gateway.s3_gateway import S3Gateway

@pytest.fixture
def directory_handler():
    return Mock(spec=os)


class TestDirectory:
    def test_should_return_empty_list_when_no_entries(
            self, directory_handler
    ):
        directory_handler.listdir.return_value = []

        directory = Directory('/', directory_handler)

        assert_that(directory.entries, equal_to([]))

    def test_should_return_all_entries(self, directory_handler):
        directory_handler.listdir.return_value = ['file1', 'file2']
        directory_handler.path.isdir.return_value = False

        directory = Directory('/', directory_handler)

        assert_that(directory.entries, has_length(2))
        assert_that(directory.entries[0].path, equal_to('//file1'))
        assert_that(directory.entries[1].path, equal_to('//file2'))

    def test_should_return_all_entries_including_subdirs(self, directory_handler):
        directory_handler.path.isdir.side_effect = is_dir_side_effect
        directory_handler.listdir.side_effect = list_dir_side_effect

        directory = Directory('dir', directory_handler)

        assert_that(directory.entries, has_length(5))
        assert_that(directory.entries[0].path, equal_to('dir/file1'))
        assert_that(directory.entries[1].path, equal_to('dir/file2'))
        assert_that(directory.entries[2].path, equal_to('dir/subdir/file3'))
        assert_that(directory.entries[3].path, equal_to('dir/subdir/file4'))
        assert_that(directory.entries[4].path, equal_to('dir/subdir/file5'))



class TestBackmeUp:
    def test_should_upload_file_to_bucket(self, directory_handler):
        directory_handler.path.isdir.return_value = False
        s3_gateway = Mock(spec=S3Gateway)

        back_me_up = BackmeUp(directory_handler, s3_gateway)
        back_me_up.sync('my bucket', 'some file')

        s3_gateway.upload.assert_called_once_with('my bucket', 'some file')

    def test_should_upload_directory_with_subdirectories_to_bucket(self, directory_handler):
        directory_handler.path.isdir.side_effect = is_dir_side_effect
        directory_handler.listdir.side_effect = list_dir_side_effect
        s3_gateway = Mock(spec=S3Gateway)

        back_me_up = BackmeUp(directory_handler, s3_gateway)
        back_me_up.sync('my bucket', 'dir')

        expected_calls = [call('my bucket', 'dir/file1'), call('my bucket', 'dir/file2'), call('my bucket', 'dir/subdir/file3'), call('my bucket', 'dir/subdir/file4'), call('my bucket', 'dir/subdir/file5')]
        s3_gateway.upload.assert_has_calls(expected_calls)


def is_dir_side_effect(*args, **kwargs):
    if args[0] == 'dir' or args[0] == 'dir/subdir':
        return True
    return False

def list_dir_side_effect(*args, **kwargs):
    if args[0] == 'dir':
        return ['file1', 'file2', 'subdir']

    if args[0] == 'dir/subdir':
        return ['file3', 'file4', 'file5']

    return []
