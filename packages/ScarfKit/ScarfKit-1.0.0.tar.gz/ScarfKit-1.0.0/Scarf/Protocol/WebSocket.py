from Scarf.Protocol.HTTP import HTTPRequest
from Scarf.Tip import SQLModel
from asyncio import StreamWriter

import hashlib, base64, asyncio, socket, traceback


class WebSocketState:
    HANDSHAKE = 0x1,
    READLENGTH = 0x2,
    READDATA = 0x3,
    CLOSE = 0x4,
    INVAILD = 0x5


class WebSocketParamter:
    def __init__(self, path, hook, _this, callback=None, **kwargs):
        self.path = path
        self.hook = hook
        self.__this = _this
        self.methods = ("GET",)
        self.callback = callback
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.callback(self.__this, *args, **kwargs)

    def get_logger(self, loggers):
        return loggers.get(self.__this.__module__ + "." + self.__this.__class__.__name__)

class WebSocket:
    class MessageType:
        CONTINUE = 0x0
        TEXT = 0x1
        BINARY = 0x2
        CLOSE = 0x8
        PING = 0x9
        PONG = 0xA

    def __init__(self, path, hooks, logger, **kwargs):
        self.path = path
        enter_hook, message_hook, close_hook, ping_hook = hooks
        self.__enter_callback = enter_hook
        self.__message_hook = message_hook
        self.__close_hook = close_hook
        self.__ping_hook = ping_hook
        self.__logger = logger
        self._handshake_timeout = kwargs.get("handshake_timeout", 10)
        self._data_timeout = kwargs.get("data_timeout", 10)
        self.state = WebSocketState.HANDSHAKE
        self.__writer: StreamWriter = None
        self.__loop = None
        self.__confim_handshake = False
        self.__run_single = kwargs.get("single", False)
        self.__random = ""
        self.__const_random = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        self.__sql = {}
        self.__sql_used = {}
        self.user_arg = None

        self.__cache_data = b""
        self.__close_flag = False
        self.__cache_message = []

        self.__fin = 0
        self.__rsvs = [0, 0, 0]
        self.__opcode = 0
        self.__mask_flag = 0
        self.__payload_len = 0
        self.__mask_keys = None
        self.__data = None

    def bind(self, writer, loop, sql):
        self.__writer = writer
        self.__loop = loop
        self.__sql = sql
        for args in self.__cache_message:
            self.__push_data(*args)

    def _handshake(self):
        sha1 = hashlib.sha1()
        sha1.update((self.__random + self.__const_random).encode())
        magic_num = base64.b64encode(sha1.digest()).decode()
        return (101, {"Connection": "Upgrade", "Upgrade": "websocket", "Sec-Websocket-Accept": magic_num}, b"")

    def __get_sql_use(self, fn, sqls):
        for i in fn.__annotations__.items():
            k, v = i
            if isinstance(v, SQLModel.DataBaseConnection):
                sql = sqls.get(v.id)
                if sql:
                    return (k, v.id)
                else:
                    return (k, None)
            elif v is SQLModel.DataBaseConnection:
                v = tuple(sqls.items())
                if len(v) > 0:
                    return (k, v[0][0])
                else:
                    return (k, None)
        return (None, None)

    def _close_sql_cons(self):
        for item in self.__sql_used.items():
            n, s = item
            self.__sql[n].destory_con(s)

    def __close_sql_cons(self, sql_params, cache_params):
        for key in sql_params:
            cache_params[key].destory_con(sql_params[key])

    def __call__(self, data: HTTPRequest, key=None, sql=None, sql_use=None):
        sql_params = {}
        try:
            if self.state == WebSocketState.HANDSHAKE:
                self.__random = key
                arg_name, id = self.__get_sql_use(self.__enter_callback.callback, sql)
                if arg_name:
                    if sql_use.get(id):
                        sql_params[arg_name] = sql_use[id]
                    else:
                        sql_params[arg_name] = sql_use[id] = sql[id].get_con()
                _flag = self.__enter_callback(data, self, **sql_params)
                self.__confim_handshake = True if isinstance(_flag, bool) and _flag else False
                if self.__confim_handshake:
                    self.state = WebSocketState.READLENGTH
                return _flag
            elif self.state == WebSocketState.READLENGTH or self.state == WebSocketState.READDATA:
                self.__reslove_data(data)

        except Exception as e:
            self.__logger.error(str.join('', traceback.format_exception(e, value=e, tb=e.__traceback__)))

    def __call_hook(self, name, *args, **kwargs):
        result = None
        if name == "enter":
            hook = self.__enter_callback
        elif name == "message":
            hook = self.__message_hook
        elif name == "close":
            hook = self.__close_hook
        else:
            hook = self.__ping_hook
        if hook:
            sql_params = {}
            arg_name, id = self.__get_sql_use(hook.callback, self.__sql)
            if arg_name:
                if self.__sql_used.get(id):
                    sql_params[arg_name] = self.__sql_used[id]
                else:
                    sql_params[arg_name] = self.__sql_used[id] = self.__sql[id].get_con()
            kwargs.update(sql_params)
            try:
                result = hook(*args, **kwargs)
            except Exception as e:
                self.__logger.error(str.join('', traceback.format_exception(e, value=e, tb=e.__traceback__)))
        return result

    def __reslove_data(self, data):
        if len(self.__cache_data) > 0:
            data = self.__cache_data + data
            self.__cache_data = b""
        if len(data) < 2:
            self.__cache_data += data
            self.state = WebSocketState.READLENGTH
            return
        else:
            header_size = 2
            if self.state == WebSocketState.READDATA:
                if self.__payload_len < 126:
                    header_size = 6
                elif self.__payload_len <= 65536:
                    header_size = 8
                else:
                    header_size = 14
                if self.__payload_len + header_size > len(data):
                    self.state = WebSocketState.READDATA
                    self.__cache_data = data
                    return
            else:
                self.__fin = (data[0] & 0x80) >> 7
                self.__rsvs[0] = (data[0] & 0x40) >> 6
                self.__rsvs[1] = (data[0] & 0x20) >> 5
                self.__rsvs[2] = (data[0] & 0x10) >> 4
                self.__opcode = (data[0]) & 0xf
                self.__mask_flag = (data[1] & 0x80) >> 7
                if not self.__mask_flag:
                    self.state = WebSocketState.INVAILD
                    return
                payload_len = data[1] & 0x7f
                if payload_len == 126:
                    if len(data) < 4:
                        self.state = WebSocketState.READLENGTH
                        self.__cache_data = data
                        return
                    header_size += 2
                    payload_len = int.from_bytes(data[2:4], byteorder='big', signed=False)
                elif payload_len == 127:
                    if len(data) < 10:
                        self.state = WebSocketState.READLENGTH
                        self.__cache_data = data
                        return
                    header_size += 8
                    payload_len = int.from_bytes(data[2:10], byteorder='big', signed=False)
                self.__payload_len = payload_len
                if len(data) < header_size + 4:
                    self.state = WebSocketState.READLENGTH
                    self.__cache_data = data
                    return
                self.__mask_keys = [int(item) for item in data[header_size:header_size + 4]]
                header_size += 4
                if len(data) < header_size + self.__payload_len:
                    self.state = WebSocketState.READDATA
                    self.__cache_data = data
                    return

            payload_data = bytearray(data[header_size:header_size + self.__payload_len])
            for index, _ in enumerate(payload_data):
                payload_data[index] = self.__mask_keys[index % 4] ^ _
            if self.__opcode == WebSocket.MessageType.TEXT:
                self.__data = payload_data.decode()
            elif self.__opcode == WebSocket.MessageType.BINARY:
                self.__data = bytes(payload_data)
            if self.__opcode == WebSocket.MessageType.CLOSE:
                self.__data = bytes(payload_data)
                code = -1
                reason = ""
                if len(self.__data) > 0:
                    code = int.from_bytes(self.__data[0:2], byteorder='big', signed=False)
                    reason = self.__data[2:].decode()
                self.__close_flag = True
                self.__call_hook("close", self, code, reason)
            elif self.__opcode == WebSocket.MessageType.PONG:
                self.__call_hook("ping", self)
            else:
                self.__call_hook("message", self, self.__data, self.__fin)
            self.state = WebSocketState.READLENGTH
            if len(data[header_size + self.__payload_len:]) > 0:
                self.__reslove_data(data[header_size + self.__payload_len:])

    def test_confirm(self):
        return self.__confim_handshake

    def ping(self):
        self.__push_data(b"", WebSocket.MessageType.PING)

    def send(self, data):
        if isinstance(data, str):
            self.__push_data(data, WebSocket.MessageType.TEXT)
        else:
            self.__push_data(data, WebSocket.MessageType.BINARY)

    def close(self, code, reason):
        self.__push_data(int(code).to_bytes(length=2, byteorder='big', signed=False) + str(reason).encode(),
                         WebSocket.MessageType.CLOSE)

    def __push_data(self, data, msg_type):
        if self.__writer is None:
            self.__cache_message.append((data, msg_type))
            return
        if msg_type == WebSocket.MessageType.TEXT:
            data = data.encode()

        if len(data) < 126:
            _data = bytearray(b"")
            _data.append(0x80 | msg_type)
            _data.append(0x7f & len(data))
            _data = bytes(_data) + data
            self.__sync_write(_data)
        elif len(data) < 0xffff:
            _data = bytearray(b"")
            _data.append(0x80 | msg_type)
            _data.append(126)
            _data = bytes(_data) + len(data).to_bytes(length=2, byteorder='big', signed=False)
            _data += data
            self.__sync_write(_data)
        else:
            _count = len(data) // 131000 + 1 if len(data) % 131000 > 0 else len(data) / 131000
            for _ in range(0, _count):
                _data = bytearray(b"")
                slice_data = data[131000 * _: 131000 * (_ + 1)]
                if _ == 0:
                    _data.append(msg_type)
                elif _ == _count - 1:
                    if len(slice_data) < 0xffff:
                        self.__push_data(slice_data, WebSocket.MessageType.CONTINUE)
                        break
                    _data.append(0x80 | msg_type)
                else:
                    _data.append(WebSocket.MessageType.CONTINUE)
                _data.append(127)
                _data = bytes(_data) + len(slice_data).to_bytes(length=8, byteorder='big', signed=False)
                _data += slice_data
                self.__sync_write(_data)

        if msg_type == WebSocket.MessageType.CLOSE:
            self.state = WebSocketState.CLOSE
            self.__writer.transport.get_extra_info("socket").shutdown(socket.SHUT_WR)

    def __sync_write(self, data):
        waiter = asyncio.run_coroutine_threadsafe(self.__write_data(data), self.__loop)
        if self.__run_single:
            return waiter
        else:
            return waiter.result()

    async def __write_data(self, data):
        self.__writer.write(data)
        await self.__writer.drain()
