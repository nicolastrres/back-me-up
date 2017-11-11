import tempfile

import os
from unittest.mock import Mock

from hamcrest import assert_that, equal_to

from back_me_up import back_me_up


def test_should_return_empty_list_when_no_files():
    with tempfile.TemporaryDirectory() as directory:
        actual_files = back_me_up.list_files(directory)

    assert_that([], equal_to(actual_files))


def test_should_return_all_files():
    with tempfile.TemporaryDirectory() as directory:
        with tempfile.NamedTemporaryFile(dir=directory) as file:
            expected_file_name = os.path.basename(file.name)
            actual_files = back_me_up.list_files(directory)

    assert_that([expected_file_name], equal_to(actual_files))


def test_should_return_last_modified_date():
    expected_last_modification_date = 1510431915.0
    os.path.getmtime = Mock(return_value=expected_last_modification_date)

    with tempfile.NamedTemporaryFile() as file:
        last_modified_date = back_me_up.get_last_modification_date(file.name)

    assert_that(expected_last_modification_date, equal_to(last_modified_date))
