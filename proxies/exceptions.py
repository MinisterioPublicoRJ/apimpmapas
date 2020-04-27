class DataDoesNotExistException(Exception):
    pass


class WaitDBException(Exception):
    pass


class DetranAPIClientError(Exception):
    def __init__(self, error):
        self.error = error
