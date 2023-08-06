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
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from ...common.types import Readables, Writables, Descriptors
from ...core.connection import TcpServerConnection


logger = logging.getLogger(__name__)


class TcpUpstreamConnectionHandler(ABC):
    """:class:`~proxy.core.base.TcpUpstreamConnectionHandler` can
    be used to insert an upstream server connection lifecycle.

    Call `initialize_upstream` to initialize the upstream connection object.
    Then, directly use ``self.upstream`` object within your class.

    See :class:`~proxy.plugin.proxy_pool.ProxyPoolPlugin` for example usage.
    """

    def __init__(self, *args: Any,  **kwargs: Any) -> None:
        # This is currently a hack, see comments below for rationale,
        # will be fixed later.
        super().__init__(*args, **kwargs)   # type: ignore
        self.upstream: Optional[TcpServerConnection] = None
        # TODO: Currently, :class:`~proxy.core.base.TcpUpstreamConnectionHandler`
        # is used within :class:`~proxy.http.server.ReverseProxy` and
        # :class:`~proxy.plugin.ProxyPoolPlugin`.
        #
        # For both of which we expect a 4-tuple as arguments
        # containing (uuid, flags, client, event_queue).
        # We really don't need the rest of the args here.
        # May be uuid?  May be event_queue in the future.
        # But certainly we don't not client here.
        # A separate tunnel class must be created which handles
        # client connection too.
        #
        # Both :class:`~proxy.http.server.ReverseProxy` and
        # :class:`~proxy.plugin.ProxyPoolPlugin` are currently
        # calling client queue within `handle_upstream_data` callback.
        #
        # This can be abstracted out too.
        self.server_recvbuf_size = args[1].server_recvbuf_size
        self.total_size = 0

    @abstractmethod
    def handle_upstream_data(self, raw: memoryview) -> None:
        raise NotImplementedError()     # pragma: no cover

    def initialize_upstream(self, addr: str, port: int) -> None:
        self.upstream = TcpServerConnection(addr, port)

    async def get_descriptors(self) -> Descriptors:
        if not self.upstream:
            return [], []
        return [self.upstream.connection.fileno()], \
            [self.upstream.connection.fileno()] \
            if self.upstream.has_buffer() \
            else []

    async def read_from_descriptors(self, r: Readables) -> bool:
        if self.upstream and \
                self.upstream.connection.fileno() in r:
            try:
                raw = self.upstream.recv(self.server_recvbuf_size)
                if raw is not None:
                    self.total_size += len(raw)
                    self.handle_upstream_data(raw)
                else:
                    # Tear down because upstream proxy closed the connection
                    return True
            except TimeoutError:
                logger.info('Upstream recv timeout error')
                return True
            except ssl.SSLWantReadError:
                logger.info('Upstream SSLWantReadError, will retry')
                return False
            except ConnectionResetError:
                logger.debug('Connection reset by upstream')
                return True
        return False

    async def write_to_descriptors(self, w: Writables) -> bool:
        if self.upstream and \
                self.upstream.connection.fileno() in w and \
                self.upstream.has_buffer():
            try:
                self.upstream.flush()
            except ssl.SSLWantWriteError:
                logger.info('Upstream SSLWantWriteError, will retry')
                return False
            except BrokenPipeError:
                logger.debug('BrokenPipeError when flushing to upstream')
                return True
        return False
