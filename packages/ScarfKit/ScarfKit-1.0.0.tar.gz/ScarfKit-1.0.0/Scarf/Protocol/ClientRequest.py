from Scarf.paramter import Paramter
from Scarf.Protocol.HTTP2 import HTTP2Context, HTTP2ConnectionState
from Scarf.Protocol.HTTP import HTTPRequest, HTTPResponse, HTTPConnectionState
from Scarf.Protocol.WebSocket import WebSocket, WebSocketState
from Scarf.Context.RequestReslove import RequestReslove

from asyncio import StreamReader, StreamWriter

import asyncio, types


class ClientRequest:
    def __init__(self, context, reader: StreamReader, writer: StreamWriter, loop, config: Paramter,
                 request_reslove: RequestReslove,
                 http2, error: types.FunctionType):
        self.__config = config
        self.__single = config.get_thread_pool_worker_num().get("single", False)
        self.__http2 = http2
        self.__context = context
        self.reader = reader
        self.writer = writer
        self.__error = error
        self.__loop = loop
        self.__request_source = None
        self.__request_reslove = request_reslove
        self.__sql = config.get_sql_options()
        self.handshake_timeout = self.read_data_timeout = self.alive_timeout = 0
        self.__get_config()

    def __get_config(self):
        handshake_timeout, read_data_timeout, alive_timeout = self.__config.get_keep_alive_timeout()
        self.handshake_timeout = handshake_timeout
        self.read_data_timeout = read_data_timeout
        self.alive_timeout = alive_timeout

    def close(self, *args, **kwargs):
        if isinstance(self.__request_source, HTTP2Context):
            self.__request_source.close(*args, **kwargs)

    def read_data(self, data):
        try:
            if self.__request_source is None:
                self.__request_source = request = HTTPRequest(self.reader)
            else:
                request = self.__request_source

            if isinstance(self.__request_source, HTTPRequest):

                request.parse_data(data)

                if not request.has_complate():
                    if request.state == HTTPConnectionState.INVAILD:

                        if request.http_version == 2.0 and self.__http2["enable"]:
                            self.__request_source = HTTP2Context(self.__loop, self.writer, request,
                                                                 self.__request_reslove, self.__config, self.__http2,
                                                                 self.__error,
                                                                 self.__single)
                            if self.__request_source.state != HTTP2ConnectionState.INVAILD:
                                asyncio.run_coroutine_threadsafe(
                                    self.__context.post_read(self, self.reader, self.read_data_timeout),
                                    loop=self.__loop)
                            else:
                                raise ConnectionRefusedError("Close Invaild Connection")
                        return
                    timeout = self.handshake_timeout if request.state == HTTPConnectionState.HEADER else self.read_data_timeout
                    asyncio.run_coroutine_threadsafe(self.__context.post_read(self, self.reader, timeout),
                                                     loop=self.__loop)
                    return

                response = HTTPResponse(self.__loop, self.writer, request.http_version, self.__config,
                                        request.gzip_flag)
                result = next(self.__request_reslove.router_reslove(request, response))
                if isinstance(result, WebSocket):
                    if result.test_confirm():
                        result.bind(self.writer, self.__loop, self.__request_reslove._get_global_sql())
                        self.__request_source = result
                        asyncio.run_coroutine_threadsafe(
                            self.__context.post_read(self, self.reader, result._handshake_timeout),
                            loop=self.__loop)
                    else:
                        self.__request_source = None
                        self.writer.close()
                        raise ConnectionRefusedError("Close Invaild Connection")
                    return
                if request.keep_alive:
                    self.__context.client_context(self.reader, self.writer)
            elif isinstance(self.__request_source, WebSocket):
                self.__request_source(data)
                if self.__request_source.state == WebSocketState.INVAILD or self.__request_source.state == WebSocketState.CLOSE:
                    self.__request_source._close_sql_cons()
                    raise ConnectionRefusedError()
                asyncio.run_coroutine_threadsafe(
                    self.__context.post_read(self, self.reader, self.__request_source._data_timeout),
                    loop=self.__loop)
            elif isinstance(self.__request_source, HTTP2Context):
                self.__request_source.reslove_data(data)
                if self.__request_source.state == HTTP2ConnectionState.INVAILD:
                    raise ConnectionError("HTTP2 Request Invaild")
                else:
                    asyncio.run_coroutine_threadsafe(
                        self.__context.post_read(self, self.reader, self.read_data_timeout),
                        loop=self.__loop)
        except ConnectionError:
            self.writer.close()
        except ConnectionRefusedError:
            self.writer.close()
        except ConnectionResetError:
            self.writer.close()
