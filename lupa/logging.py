from sys import stdout

from django.core.management.base import OutputWrapper


class LogSuccess:
    def __init__(self):
        self._output = OutputWrapper(stdout)

    def print(self, msg):
        color_prefix = '\033[92m'
        color_suffix = '\033[0m'
        self._output.write(f'{color_prefix}{msg}{color_suffix}')
