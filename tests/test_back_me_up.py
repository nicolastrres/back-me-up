import os
import tempfile
import pytest

from unittest.mock import Mock, call, patch
from hamcrest import assert_that, equal_to, has_length

from back_me_up.back_me_up import Directory, BackmeUp, calculate_md5
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
    @patch('back_me_up.back_me_up.calculate_md5')
    def test_should_upload_file_to_bucket(self, calculate_md5_mocked, directory_handler):
        calculate_md5_mocked.return_value = 'some md5 hash'
        directory_handler.path.isdir.return_value = False
        s3_gateway = Mock(spec=S3Gateway)

        back_me_up = BackmeUp(directory_handler, s3_gateway)
        back_me_up.sync('my bucket', 'some file')

        s3_gateway.upload.assert_called_once_with(
            'my bucket',
            'some file',
            metadata={'md5': 'some md5 hash'}
        )

    @patch('back_me_up.back_me_up.calculate_md5')
    def test_should_upload_directory_with_subdirectories_to_bucket(self, calculate_md5_mocked, directory_handler):
        calculate_md5_mocked.return_value = 'some md5 hash'
        directory_handler.path.isdir.side_effect = is_dir_side_effect
        directory_handler.listdir.side_effect = list_dir_side_effect
        s3_gateway = Mock(spec=S3Gateway)

        back_me_up = BackmeUp(directory_handler, s3_gateway)
        back_me_up.sync('my bucket', 'dir')

        expected_calls = [
            call('my bucket', 'dir/file1', metadata={'md5': 'some md5 hash'}),
            call('my bucket', 'dir/file2', metadata={'md5': 'some md5 hash'}),
            call('my bucket', 'dir/subdir/file3', metadata={'md5': 'some md5 hash'}),
            call('my bucket', 'dir/subdir/file4', metadata={'md5': 'some md5 hash'}),
            call('my bucket', 'dir/subdir/file5', metadata={'md5': 'some md5 hash'})
        ]
        s3_gateway.upload.assert_has_calls(expected_calls)


def test_should_calculate_md5_hash_for_file():
    fd, path = tempfile.mkstemp()
    expected_hash = 'd41d8cd98f00b204e9800998ecf8427e'

    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write('some stuffs')
            assert_that(calculate_md5(path), equal_to(expected_hash))
    finally:
        os.remove(path)


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
