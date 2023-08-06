# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
import random
import logging
from typing import Any, Dict, List, Tuple, Optional

from ..http import Url
from ..core.base import TcpUpstreamConnectionHandler
from ..http.parser import HttpParser
from ..http.server import HttpWebServerBasePlugin, httpProtocolTypes
from ..common.utils import text_
from ..http.exception import HttpProtocolException
from ..common.constants import DEFAULT_HTTP_PORT, DEFAULT_HTTPS_PORT


logger = logging.getLogger(__name__)


class ReverseProxyPlugin(TcpUpstreamConnectionHandler, HttpWebServerBasePlugin):
    """Extend in-built Web Server to add Reverse Proxy capabilities.

    This example plugin is equivalent to following Nginx configuration::

        ```text
        location /get {
            proxy_pass http://httpbin.org/get
        }
        ```

    Example::

        ```console
        $ curl http://localhost:9000/get
        {
          "args": {},
          "headers": {
            "Accept": "*/*",
            "Host": "localhost",
            "User-Agent": "curl/7.64.1"
          },
          "origin": "1.2.3.4, 5.6.7.8",
          "url": "http://localhost/get"
        }
        ```
    """

    # TODO: We must use nginx python parser and
    # make this plugin nginx.conf complaint.
    REVERSE_PROXY_LOCATION: str = r'/get$'
    # Randomly choose either http or https upstream endpoint.
    #
    # This is just to demonstrate that both http and https upstream
    # reverse proxy works.
    REVERSE_PROXY_PASS = [
        b'http://httpbin.org/get',
        b'https://httpbin.org/get',
    ]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.choice: Optional[Url] = None

    def handle_upstream_data(self, raw: memoryview) -> None:
        self.client.queue(raw)

    def routes(self) -> List[Tuple[int, str]]:
        return [
            (httpProtocolTypes.HTTP, ReverseProxyPlugin.REVERSE_PROXY_LOCATION),
            (httpProtocolTypes.HTTPS, ReverseProxyPlugin.REVERSE_PROXY_LOCATION),
        ]

    def handle_request(self, request: HttpParser) -> None:
        self.choice = Url.from_bytes(
            random.choice(ReverseProxyPlugin.REVERSE_PROXY_PASS),
        )
        assert self.choice.hostname
        port = self.choice.port or \
            DEFAULT_HTTP_PORT \
            if self.choice.scheme == b'http' \
            else DEFAULT_HTTPS_PORT

        self.initialize_upstream(text_(self.choice.hostname), port)
        assert self.upstream
        try:
            self.upstream.connect()
            if self.choice.scheme == b'https':
                self.upstream.wrap(
                    text_(
                        self.choice.hostname,
                    ), ca_file=str(self.flags.ca_file),
                )
            self.upstream.queue(memoryview(request.build()))
        except ConnectionRefusedError:
            raise HttpProtocolException(
                'Connection refused by upstream server {0}:{1}'.format(
                    text_(self.choice.hostname), port,
                ),
            )

    def on_client_connection_close(self) -> None:
        if self.upstream and not self.upstream.closed:
            logger.debug('Closing upstream server connection')
            self.upstream.close()
            self.upstream = None

    def on_access_log(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        log_format = '{client_addr} - {request_method} {request_path} -> {upstream_proxy_pass} - {connection_time_ms}ms'
        context.update({
            'upstream_proxy_pass': str(self.choice) if self.choice else None,
        })
        logger.info(log_format.format_map(context))
        return None
