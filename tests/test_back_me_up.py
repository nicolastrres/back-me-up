import tempfile

import os
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
