import os

from back_me_up.exceptions import InaccessibleFileException


class StatusFile:
    def __init__(self, path):
        self.path = path

    def store_file_last_modification_data(
            self,
            backup_file_name,
            last_modification_date
    ):
        with open(self.path, 'w') as status_file:
            status_file.write(
                '%s,%s' % (backup_file_name, last_modification_date)
            )

    @property
    def lines(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()
        return lines

    def get_last_modification_date(self, file_to_backup):
        return self._parse_lines()[file_to_backup]

    def _parse_lines(self):
        parsed_lines = {}
        for line in self.lines:
            file_name, last_modification_date = line.split(',')
            parsed_lines[file_name] = last_modification_date

        return parsed_lines


class BackupFolder:
    def __init__(self, path):
        self.path = path

    @property
    def files(self):
        return [BackupFile(file_path) for file_path in os.listdir(self.path)]


class BackupFile:
    def __init__(self, path):
        self.path = path

    @property
    def last_modification_date(self):
        try:
            return os.path.getmtime(self.path)
        except FileNotFoundError as e:
            raise InaccessibleFileException(self.path, e)
