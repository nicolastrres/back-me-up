
class InaccessibleFileException(Exception):
    def __init__(self, file, error):
        super().__init__(
            'File %s does not exist or '
            'is inaccessible at the moment. Error raised: %s' % (
                file, error
            )
        )
