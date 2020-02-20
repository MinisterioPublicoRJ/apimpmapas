from sys import stdout

from django.core.management.base import OutputWrapper


class Log:
    def __init__(self):
        self._output = OutputWrapper(stdout)

    def print(self, msg, ending='\n', color_prefix=''):
        self._output.write(f'{color_prefix}{msg}\033[0m', ending=ending)

    def printerr(self, msg, ending='\n'):
        self.print(msg, ending, color_prefix='\033[91m')

    def printok(self,  msg, ending='\n'):
        self.print(msg, ending, color_prefix='\033[92m')
