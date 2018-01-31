import StringIO

import mock
import pytest

from onioff import nowPrint


@pytest.fixture
def mocked_stdout():
    return mock.patch('sys.stdout', new=StringIO.StringIO())


def test_nowPrint_green(mocked_stdout):
    message = 'testing'
    green_format = '\x1b[32m{}\x1b[0m'.format(message)

    with mocked_stdout as stdout:
        nowPrint(message)
        assert stdout.getvalue() == green_format


def test_nowPrint_error(mocked_stdout):
    message = 'testing'
    error_format = '\x1b[31m{}\x1b[0m'.format(message)

    with mocked_stdout as stdout:
        nowPrint(message, error=True)
        assert stdout.getvalue() == error_format


def test_nowPrint_heavy(mocked_stdout):
    message = 'testing'
    heavy_format = '\x1b[33m{}\x1b[0m'.format(message)

    with mocked_stdout as stdout:
        nowPrint(message, heavy=True)
        assert stdout.getvalue() == heavy_format


def test_nowPrint_with_ext(mocked_stdout):
    sep_sign = '-->'
    message = 'testing'.format(sep_sign)
    msg_e = 'ext message'
    message_ext = '{} {} {}'.format(message, sep_sign, msg_e)
    expected = '\x1b[32m{} {} \x1b[0m\x1b[1m\x1b[32m{}\x1b[0m'.format(
        message, sep_sign, msg_e)

    with mocked_stdout as stdout:
        nowPrint(message_ext, ext=True)
        assert stdout.getvalue() == expected
