from sys import stdout, stderr

from django.core.management.base import OutputWrapper


class BaseLog:
    def __init__(self, output):
        self._output = OutputWrapper(output)
        self._color_prefix = ''
        self._color_suffix = '\033[0m'

    def print(self, msg):
        self._output.write(f'{self._color_prefix}{msg}{self._color_suffix}')


class LogSuccess(BaseLog):
    def __init__(self):
        super().__init__(stdout)
        self._color_prefix = '\033[92m'


class LogError(BaseLog):
    def __init__(self):
        super().__init__(stderr)
        self._color_prefix = '\033[91m'
