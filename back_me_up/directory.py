import os


class Directory:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    @property
    def entries(self):
        paths = self.directory_handler.listdir(self.path)
        entries = [Entry(f'{self.path}/{path}') for path in paths]

        for entry in entries:
            if self.directory_handler.path.isdir(entry.path):
                entries.extend(
                    Directory(entry.path, self.directory_handler).entries
                )
                entries = self._get_entries_without_path(entries, entry.path)

        return entries

    def _get_entries_without_path(self, entries, path):
        return list(filter(lambda x: x.path != path, entries))


class Entry:
    def __init__(self, path, directory_handler=os):
        self.path = path
        self.directory_handler = directory_handler

    def __str__(self):
        return self.path
