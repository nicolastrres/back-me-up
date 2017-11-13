import os

from back_me_up.exceptions import InaccessibleFileException


def list_files(folder):
    return os.listdir(folder)


def get_last_modification_date(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError as e:
        raise InaccessibleFileException(file_path, e)


def store_file_last_modification_data(
        status_file_path,
        backup_file_name,
        last_modification_date
):
    with open(status_file_path, 'w') as status_file:
        status_file.write(
            '%s,%s' % (backup_file_name, last_modification_date)
        )


def read_file(file_to_read):
    with open(file_to_read, 'r') as file:
        lines = file.readlines()
    return parse_lines(lines)


def parse_lines(lines):
    parsed_lines = {}
    for line in lines:
        file_name, last_modification_date = line.split(',')
        parsed_lines[file_name] = last_modification_date

    return parsed_lines


def read_last_modifcation_date(status_file_path, file_to_backup):
    lines = read_file(status_file_path)
    return lines[file_to_backup]
