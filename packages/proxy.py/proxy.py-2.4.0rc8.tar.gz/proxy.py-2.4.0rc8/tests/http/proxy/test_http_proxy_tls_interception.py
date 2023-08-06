# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
import ssl
import uuid
import socket
import selectors
from typing import Any

import pytest
from unittest import mock

from pytest_mock import MockerFixture

from proxy.http import HttpProtocolHandler, HttpClientConnection, httpMethods
from proxy.http.proxy import HttpProxyPlugin
from proxy.common.flag import FlagParser
from proxy.common.utils import bytes_, build_http_request
from proxy.http.responses import PROXY_TUNNEL_ESTABLISHED_RESPONSE_PKT
from proxy.core.connection import TcpServerConnection
from proxy.common.constants import DEFAULT_CA_FILE
from ...test_assertions import Assertions


class TestHttpProxyTlsInterception(Assertions):

    @pytest.mark.asyncio    # type: ignore[misc]
    async def test_e2e(self, mocker: MockerFixture) -> None:
        host, port = uuid.uuid4().hex, 443
        netloc = '{0}:{1}'.format(host, port)

        self.mock_fromfd = mocker.patch('socket.fromfd')
        self.mock_selector = mocker.patch('selectors.DefaultSelector')
        self.mock_sign_csr = mocker.patch('proxy.http.proxy.server.sign_csr')
        self.mock_gen_csr = mocker.patch('proxy.http.proxy.server.gen_csr')
        self.mock_gen_public_key = mocker.patch(
            'proxy.http.proxy.server.gen_public_key',
        )
        self.mock_server_conn = mocker.patch(
            'proxy.http.proxy.server.TcpServerConnection',
        )
        self.mock_ssl_context = mocker.patch('ssl.create_default_context')
        self.mock_ssl_wrap = mocker.patch('ssl.wrap_socket')

        self.mock_sign_csr.return_value = True
        self.mock_gen_csr.return_value = True
        self.mock_gen_public_key.return_value = True

        ssl_connection = mock.MagicMock(spec=ssl.SSLSocket)
        self.mock_ssl_context.return_value.wrap_socket.return_value = ssl_connection
        self.mock_ssl_wrap.return_value = mock.MagicMock(spec=ssl.SSLSocket)
        plain_connection = mock.MagicMock(spec=socket.socket)

        def mock_connection() -> Any:
            if self.mock_ssl_context.return_value.wrap_socket.called:
                return ssl_connection
            return plain_connection

        # Do not mock the original wrap method
        self.mock_server_conn.return_value.wrap.side_effect = \
            lambda x, y: TcpServerConnection.wrap(
                self.mock_server_conn.return_value, x, y,
            )

        type(self.mock_server_conn.return_value).connection = \
            mock.PropertyMock(side_effect=mock_connection)

        self.fileno = 10
        self._addr = ('127.0.0.1', 54382)
        self.flags = FlagParser.initialize(
            ca_cert_file='ca-cert.pem',
            ca_key_file='ca-key.pem',
            ca_signing_key_file='ca-signing-key.pem',
            threaded=True,
        )
        self.plugin = mock.MagicMock()
        self.proxy_plugin = mock.MagicMock()
        self.flags.plugins = {
            b'HttpProtocolHandlerPlugin': [self.plugin, HttpProxyPlugin],
            b'HttpProxyBasePlugin': [self.proxy_plugin],
        }
        self._conn = self.mock_fromfd.return_value
        self.protocol_handler = HttpProtocolHandler(
            HttpClientConnection(self._conn, self._addr),
            flags=self.flags,
        )
        self.protocol_handler.initialize()

        self.plugin.assert_not_called()
        self.proxy_plugin.assert_not_called()

        connect_request = build_http_request(
            httpMethods.CONNECT, bytes_(netloc),
            headers={
                b'Host': bytes_(netloc),
            },
        )
        self._conn.recv.return_value = connect_request

        async def asyncReturnBool(val: bool) -> bool:
            return val

        # Prepare mocked HttpProtocolHandlerPlugin
        # self.plugin.return_value.get_descriptors.return_value = ([], [])
        # self.plugin.return_value.write_to_descriptors.return_value = asyncReturnBool(False)
        # self.plugin.return_value.read_from_descriptors.return_value = asyncReturnBool(False)
        # self.plugin.return_value.on_client_data.side_effect = lambda raw: raw
        # self.plugin.return_value.on_request_complete.return_value = False
        # self.plugin.return_value.on_response_chunk.side_effect = lambda chunk: chunk
        # self.plugin.return_value.on_client_connection_close.return_value = None

        # Prepare mocked HttpProxyBasePlugin
        self.proxy_plugin.return_value.write_to_descriptors.return_value = \
            asyncReturnBool(False)
        self.proxy_plugin.return_value.read_from_descriptors.return_value = \
            asyncReturnBool(False)
        self.proxy_plugin.return_value.before_upstream_connection.side_effect = lambda r: r
        self.proxy_plugin.return_value.handle_client_request.side_effect = lambda r: r
        self.proxy_plugin.return_value.resolve_dns.return_value = None, None

        self.mock_selector.return_value.select.side_effect = [
            [(
                selectors.SelectorKey(
                    fileobj=self._conn.fileno(),
                    fd=self._conn.fileno(),
                    events=selectors.EVENT_READ,
                    data=None,
                ),
                selectors.EVENT_READ,
            )],
        ]

        await self.protocol_handler._run_once()

        # Assert correct plugin was initialized
        self.plugin.assert_not_called()
        self.proxy_plugin.assert_called_once()
        self.assertEqual(self.proxy_plugin.call_args[0][1], self.flags)
        # Actual call arg must be `_conn` object
        # but because internally the reference is updated
        # we assert it against `mock_ssl_wrap` which is
        # called during proxy plugin initialization
        # for interception
        self.assertEqual(
            self.proxy_plugin.call_args[0][2].connection,
            self.mock_ssl_wrap.return_value,
        )

        # Assert our mocked plugins invocations
        # self.plugin.return_value.get_descriptors.assert_called()
        # self.plugin.return_value.write_to_descriptors.assert_called_with([])
        # # on_client_data is only called after initial request has completed
        # self.plugin.return_value.on_client_data.assert_not_called()
        # self.plugin.return_value.on_request_complete.assert_called()
        # self.plugin.return_value.read_from_descriptors.assert_called_with([
        #     self._conn.fileno(),
        # ])
        self.proxy_plugin.return_value.before_upstream_connection.assert_called()
        self.proxy_plugin.return_value.handle_client_request.assert_called()

        self.mock_server_conn.assert_called_with(host, port)
        self.mock_server_conn.return_value.connection.setblocking.assert_called_with(
            False,
        )

        self.mock_ssl_context.assert_called_with(
            ssl.Purpose.SERVER_AUTH, cafile=str(DEFAULT_CA_FILE),
        )
        # self.assertEqual(self.mock_ssl_context.return_value.options,
        #                  ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 |
        #                  ssl.OP_NO_TLSv1_1)
        self.assertEqual(plain_connection.setblocking.call_count, 2)
        self.mock_ssl_context.return_value.wrap_socket.assert_called_with(
            plain_connection, server_hostname=host,
        )
        self.assertEqual(self.mock_sign_csr.call_count, 1)
        self.assertEqual(self.mock_gen_csr.call_count, 1)
        self.assertEqual(self.mock_gen_public_key.call_count, 1)
        self.assertEqual(ssl_connection.setblocking.call_count, 1)
        self.assertEqual(
            self.mock_server_conn.return_value._conn,
            ssl_connection,
        )
        self._conn.send.assert_called_with(
            PROXY_TUNNEL_ESTABLISHED_RESPONSE_PKT,
        )
        assert self.flags.ca_cert_dir is not None
        self.mock_ssl_wrap.assert_called_with(
            self._conn,
            server_side=True,
            keyfile=self.flags.ca_signing_key_file,
            certfile=HttpProxyPlugin.generated_cert_file_path(
                self.flags.ca_cert_dir, host,
            ),
            ssl_version=ssl.PROTOCOL_TLS,
        )
        self.assertEqual(self._conn.setblocking.call_count, 2)
        self.assertEqual(
            self.protocol_handler.work.connection,
            self.mock_ssl_wrap.return_value,
        )

        # Assert connection references for all other plugins is updated
        # self.assertEqual(
        #     self.plugin.return_value.client._conn,
        #     self.mock_ssl_wrap.return_value,
        # )
        self.assertEqual(
            self.proxy_plugin.return_value.client._conn,
            self.mock_ssl_wrap.return_value,
        )
