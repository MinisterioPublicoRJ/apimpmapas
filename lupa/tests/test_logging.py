from unittest import TestCase, mock

from lupa.logging import LogSuccess, LogError


class Log(TestCase):
    @mock.patch('lupa.logging.stdout')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_success_message(self, _output_wrapper, _stdout):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = LogSuccess()
        log.print('message')

        _output_wrapper.assert_called_once_with(_stdout)
        _wrapper_mock.write.assert_called_once_with('\x1b[92mmessage\x1b[0m')

    @mock.patch('lupa.logging.stderr')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_error_message(self, _output_wrapper, _stderr):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = LogError()
        log.print('message')

        _output_wrapper.assert_called_once_with(_stderr)
        _wrapper_mock.write.assert_called_once_with('\x1b[91mmessage\x1b[0m')
