class UploadFileError(Exception):
    def __init__(self, args):
        super().__init__(args)

        self.args = args
