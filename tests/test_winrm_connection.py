import mock
import unittest
import winrm

from lib.winrm_connection import WinRmConnection


class TestWinRmConnection(unittest.TestCase):

    def setUp(self):
        super(TestWinRmConnection, self).setUp()

    def test_init_defaults(self):
        hostname = 'localhost'
        username = 'username'
        password = 'password'
        expected_url = 'https://{}:5986/wsman'.format(hostname)
        connection = WinRmConnection(hostname, username=username, password=password)
        self.assertIsInstance(connection.session, winrm.Session)
        self.assertEqual(connection.session.url, expected_url)
        self.assertEqual(connection.session.protocol.username, username)
        self.assertEqual(connection.session.protocol.password, password)
        self.assertEqual(connection.session.protocol.server_cert_validation,
                         'ignore')
        self.assertEqual(connection.session.protocol.transport.endpoint, expected_url)
        self.assertEqual(connection.session.protocol.transport.auth_method, 'ntlm')
        self.assertEqual(connection.session.protocol.transport.username, username)
        self.assertEqual(connection.session.protocol.transport.password, password)
        self.assertEqual(connection.session.protocol.transport.server_cert_validation,
                         'ignore')

    def test_init_params(self):
        hostname = 'hostname'
        port = 1234
        scheme = 'https'
        transport = 'tport'
        username = 'username'
        password = 'password'
        url = '{}://{}:{}/wsman'.format(scheme, hostname, port)
        server_cert_validation = 'ignore'
        connection = WinRmConnection(hostname, port=port, transport=transport,
                                     username=username, password=password)
        self.assertIsInstance(connection.session, winrm.Session)
        self.assertEqual(connection.session.url, url)
        self.assertEqual(connection.session.protocol.username, username)
        self.assertEqual(connection.session.protocol.password, password)
        self.assertEqual(connection.session.protocol.server_cert_validation,
                         server_cert_validation)
        self.assertEqual(connection.session.protocol.transport.endpoint, url)
        self.assertEqual(connection.session.protocol.transport.auth_method, transport)
        self.assertEqual(connection.session.protocol.transport.username, username)
        self.assertEqual(connection.session.protocol.transport.password, password)
        self.assertEqual(connection.session.protocol.transport.server_cert_validation,
                         server_cert_validation)

    def test_init_http(self):
        hostname = 'hostname'
        port = 5985
        scheme = 'http'
        transport = 'tport'
        username = 'username'
        password = 'password'
        url = '{}://{}:{}/wsman'.format(scheme, hostname, port)
        server_cert_validation = 'ignore'
        connection = WinRmConnection(hostname, port=port, transport=transport,
                                     username=username, password=password)
        self.assertIsInstance(connection.session, winrm.Session)
        self.assertEqual(connection.session.url, url)
        self.assertEqual(connection.session.protocol.username, username)
        self.assertEqual(connection.session.protocol.password, password)
        self.assertEqual(connection.session.protocol.server_cert_validation,
                         server_cert_validation)
        self.assertEqual(connection.session.protocol.transport.endpoint, url)
        self.assertEqual(connection.session.protocol.transport.auth_method, transport)
        self.assertEqual(connection.session.protocol.transport.username, username)
        self.assertEqual(connection.session.protocol.transport.password, password)
        self.assertEqual(connection.session.protocol.transport.server_cert_validation,
                         server_cert_validation)

    def test_run_ps(self):
        connection = WinRmConnection('localhost', username='u', password='p')

        mock_session = mock.MagicMock()
        mock_session.run_ps.return_value = "expected result"
        connection.session = mock_session

        result = connection.run_ps("powershell command")

        self.assertEquals(result, "expected result")
        mock_session.run_ps.assert_called_with("powershell command")

    def test_run_cmd(self):
        connection = WinRmConnection('localhost', username='u', password='p')

        mock_session = mock.MagicMock()
        mock_session.run_cmd.return_value = "expected result"
        connection.session = mock_session

        result = connection.run_cmd("cmd command")

        self.assertEquals(result, "expected result")
        mock_session.run_cmd.assert_called_with("cmd command")
