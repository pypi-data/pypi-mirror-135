import asyncio, ssl, sys


class TCPServer:
    def __init__(self, ports, callback, http2, ssloptions={}):
        (http_port, https_port) = ports
        self.__http_port = http_port
        self.__https_port = https_port
        self.__http2 = http2
        self.__ssl_options = ssloptions
        self.__ssl_context = None
        self.__HTTP_Server = None
        self.__HTTPS_Server = None
        self.__callback = callback
        self.__event_loop = self.__GetEventLoop()
        self.__event_loop.run_until_complete(self.__CreateTcpServer())

    def start_loop(self):
        if self.__HTTPS_Server:
            self.__event_loop.run_until_complete(self.__HTTPS_Server.start_serving())
        if self.__HTTP_Server:
            self.__event_loop.run_until_complete(self.__HTTP_Server.start_serving())
        while True:
            try:
                self.__event_loop.run_forever()
            except asyncio.InvalidStateError as e:
                continue

    def get_event_loop(self):
        return self.__event_loop

    def stop_loop(self):
        self.__event_loop.stop()

    async def __CreateTcpServer(self):
        if self.__http_port > -1:
            self.__HTTP_Server = await asyncio.start_server(self.__callback, start_serving=False, host='0.0.0.0',
                                                            port=self.__http_port, loop=self.__event_loop)
        if self.__https_port > -1:
            self.__ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            if self.__http2 and ssl.HAS_ALPN:
                self.__ssl_context.set_alpn_protocols(["h2"])
            self.__ssl_context.load_cert_chain(self.__ssl_options["crt"], self.__ssl_options["key"],
                                               self.__ssl_options["pwd"])
            self.__HTTPS_Server = await asyncio.start_server(self.__callback, start_serving=False, host='0.0.0.0',
                                                             port=self.__https_port, loop=self.__event_loop,
                                                             ssl_handshake_timeout=self.__ssl_options[
                                                                 "ssl_handshake_timeout"],
                                                             ssl=self.__ssl_context)

    def __GetEventLoop(self):
        """Get The Best Event Loop At This Platform"""
        loop = None
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.SelectorEventLoop(selector=None)
        return loop
