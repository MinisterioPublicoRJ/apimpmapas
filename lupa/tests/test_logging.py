from unittest import TestCase, mock

from lupa.logging import LogSuccess, LogError, LogInfo, Log


class Logging(TestCase):
    @mock.patch('lupa.logging.stdout')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_success_message(self, _output_wrapper, _stdout):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = LogSuccess()
        log.print('message', ending='')

        _output_wrapper.assert_called_once_with(_stdout)
        _wrapper_mock.write.assert_called_once_with(
            '\x1b[92mmessage\x1b[0m',
            ending=''
        )

    @mock.patch('lupa.logging.stderr')
    @mock.patch('lupa.logging.OutputWrapper')
    def test_error_message(self, _output_wrapper, _stderr):
        _wrapper_mock = mock.MagicMock()
        _output_wrapper.return_value = _wrapper_mock
        log = LogError()
        log.print('message', ending='')

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
        log = LogInfo()
        log.print('message', ending='')

        _output_wrapper.assert_called_once_with(_stdout)
        _wrapper_mock.write.assert_called_once_with(
            'message\x1b[0m',
            ending=''
        )

    @mock.patch('lupa.logging.LogSuccess')
    @mock.patch('lupa.logging.LogError')
    def test_log_class(self, _LogError, _LogSuccess):
        _log_error = mock.MagicMock()
        _log_success = mock.MagicMock()
        _LogError.return_value = _log_error
        _LogSuccess.return_value = _log_success

        log = Log()

        log.printok('message ok')
        log.printerr('message err')

        _log_error.print.assert_called()
        _log_success.print.assert_called()
