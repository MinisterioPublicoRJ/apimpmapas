class DataDoesNotExistException(Exception):
    pass


class WaitDBException(Exception):
    pass


class DetranCustonError(Exception):
    def __init__(self, error):
        self.error = error