from unittest import TestCase, mock

from lupa.logging import Log


class Logging(TestCase):
    @mock.patch('lupa.logging.stdout')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_success_message(self, _output_wrapper, _stdout):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = Log()
        log.printok('message', ending='')

        _output_wrapper.assert_called_once_with(_stdout)
        _wrapper_mock.write.assert_called_once_with(
            '\x1b[92mmessage\x1b[0m',
            ending=''
        )

    @mock.patch('lupa.logging.stdout')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_error_message(self, _output_wrapper, _stderr):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = Log()
        log.printerr('message', ending='')

        _output_wrapper.assert_called_once_with(_stderr)
        _wrapper_mock.write.assert_called_once_with(
            '\x1b[91mmessage\x1b[0m',
            ending=''
        )

    @mock.patch('lupa.logging.stdout')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_info_message(self, _output_wrapper, _stdout):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = Log()
        log.print('message', ending='')

        _output_wrapper.assert_called_once_with(_stdout)
        _wrapper_mock.write.assert_called_once_with(
            'message\x1b[0m',
            ending=''
        )
