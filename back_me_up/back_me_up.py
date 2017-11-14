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
        with open(self.path, 'a') as status_file:
            status_file.write(
                '%s,%s\n' % (backup_file_name, last_modification_date)
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


class BackmeUp:
    def __init__(self, status_file, file_storage_service):
        self.file_storage_service = file_storage_service
        self.status_file = status_file

    def backup_folder(self, path):
        for file in BackupFolder(path=path).files:
            self._store_file_status(file.path, file.last_modification_date)
            self.file_storage_service.backup_file(file.path)

    def _store_file_status(self, file_path, file_modification_date):
        self.status_file.store_file_last_modification_data(
            file_path,
            file_modification_date
        )
