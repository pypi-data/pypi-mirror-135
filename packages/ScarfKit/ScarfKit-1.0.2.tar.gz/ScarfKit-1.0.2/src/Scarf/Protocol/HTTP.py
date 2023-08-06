from asyncio import StreamWriter, StreamReader
from urllib.parse import unquote
from Scarf.Tip import FileDeliver
import json, types, gzip, asyncio, sys, os, mimetypes, time, hashlib, datetime, traceback


class HTTPConnectionState:
    HEADER = 0x0
    DATA = 0x1
    COMPLATE = 0x2
    INVAILD = 0x3


class HTTPRequest:
    def __init__(self, end_point, stream_id=-1):
        self.method = None
        self.path = None
        self.http_version = None
        self.stream_id = stream_id
        self.__remote_endpoint = end_point
        self.__querys = {}
        self.__headers = {}
        self.cookies = {}
        self.__data = b""
        self.__url_params = None
        self.gzip_flag = False
        self.keep_alive = True
        self.is_file = False
        self.is_websocket = False
        self.is_not_found = False
        self.state = HTTPConnectionState.HEADER
        self.__last_length = 0
        self.__cache_data = b""

    def __parse_cookie(self, cookie_str):
        cookie_str = cookie_str.strip()
        cookies = [item.strip().split('=') for item in cookie_str.split(";") if len(item) > 0]
        for item in cookies:
            self.cookies[item[0].strip()] = item[1].strip()

    def has_complate(self):
        return self.state == HTTPConnectionState.COMPLATE

    def parse_data(self, data):
        if self.state == HTTPConnectionState.HEADER:
            data = self.__cache_data + data
            if data.find(b"\r\n\r\n") == -1:
                self.state = HTTPConnectionState.INVAILD if len(self.__cache_data) > 65536 else self.state
                self.__cache_data += data
            else:
                self.__data = data[data.find(b"\r\n\r\n") + 4:]
                data = data[0:data.find(b"\r\n\r\n")].decode()
                data = data.split("\r\n")
                http_line = data[0].split(' ')
                self.method = http_line[0].upper()
                if http_line[1].find("?") > -1:
                    query_str = http_line[1][http_line[1].find("?") + 1:]
                    for item in query_str.split("&"):
                        name, value = item.split("=")
                        name = unquote(name)
                        value = unquote(value)
                        self.__querys[name] = value
                    self.path = unquote(http_line[1][0:http_line[1].find("?")])
                else:
                    self.path = unquote(http_line[1])
                self.http_version = float(http_line[2][http_line[2].find('/') + 1:])
                if self.http_version == 2.0 and self.stream_id == -1:
                    self.state = HTTPConnectionState.INVAILD
                    return
                for item in data[1:]:
                    item = item.split(':')
                    name = item[0].lower()
                    value = str.join(":", item[1:])
                    if name == 'cookie':
                        self.__parse_cookie(value)
                    self.__headers[name] = value.strip()
                if self.get_header("Connection", "").lower() == "close" or self.get_header(
                        "Connection", "").lower() != "keep-alive" and self.http_version < 1.1:
                    self.keep_alive = False
                encodings = self.get_header("Accept-Encoding", "")
                if encodings:
                    encodings = [item.strip() for item in encodings.split(",")]
                    if "gzip" in encodings:
                        self.gzip_flag = True
                self.__last_length = self.get_content_length() - len(self.__data)
                self.state = HTTPConnectionState.DATA if self.__last_length > 0 else HTTPConnectionState.COMPLATE
                if self.state == HTTPConnectionState.COMPLATE:
                    self.__cache_data = b""
        elif self.state == HTTPConnectionState.DATA:
            self.__data += data
            self.__last_length -= len(data)
            self.state = HTTPConnectionState.DATA if self.__last_length else HTTPConnectionState.COMPLATE

    def set_url_params(self, params):
        self.__url_params = params

    def get_content_length(self):
        return int(self.__headers.get("content-length", 0))

    def del_header(self, name):
        if self.__headers.get(name) is None:
            return
        del self.__headers[name]

    def get_header(self, name, default=None):
        return self.__headers.get(name.lower(), default)

    def set_header(self, name, value):
        self.__headers[name] = str(value)

    def get_data(self):
        return self.__data

    def headers(self):
        return self.__headers.copy()

    def query(self):
        return self.__querys.copy()

    def get_url_params(self):
        return self.__url_params.copy()

    def get_data_with_json(self):
        try:
            return json.loads(self.__data)
        except Exception:
            return {}

    def get_remote_endpoint(self):
        return self.__remote_endpoint._transport._sock.getpeername()

    def get_data_with_form_urlencoded(self):
        params = {}
        try:
            data = self.__data.decode()
            for item in data.split("&"):
                name, value = item.split("=")
                name = unquote(name)
                value = unquote(value)
                params[name] = value
            return params
        except:
            return params

    def get_data_with_form_data(self):
        if self.get_header("content-type", "").strip().lower().find("multipart/form-data") != 0:
            return None
        content_type = self.get_header("content-type", "").strip()
        index = content_type.index("boundary=")
        boundary = content_type[index + 9:]
        if boundary.find('"') > -1 or boundary.find('"') > -1:
            boundary = boundary[1:-1]
        contents = self.__data.split(boundary.encode())[1:-1]

        params = {}
        for item in contents:
            result = [val for val in item.split(b"\r\n") if val != b'--'][1:]
            if len(result) == 3:
                name, value = (result[0], bytes.join(b"\r\n", result[2:]))
            else:
                name, value = (result[0], bytes.join(b"\r\n", result[1:]))
            decode_str = name.decode().split(";")
            n, v = decode_str[1].strip().split("=")
            if n == "name":
                if v.find('"') > -1 and v.find('"') > -1:
                    v = v[1:-1]
                if len(decode_str) > 2:
                    filename_str = decode_str[2].strip().split("=")
                    if filename_str[0] == "filename":
                        file_content_split = value.split(b"\r\n")
                        if file_content_split[0].find(b"Content-Type:") > -1:
                            data = file_content_split[2:]
                            filetype = file_content_split[0].decode().split(":")[1].strip()
                        else:
                            data = file_content_split[1:]
                            filetype = None
                        params[v] = FileDeliver(None, bytes.join(b"\r\n", data),
                                                      filename_str[1][1:-1],
                                                      filetype)
                        continue

                params[v] = value.decode()
        return params


class HTTPResponse:
    static_http_code_plain = {
        "100": "Continue",
        "101": "Switching Protocol",
        "102": "Processing",
        "103": "Early Hints",
        "200": "OK",
        "201": "Created",
        "202": "Accepted",
        "203": "Non-Authoritative Information",
        "204": "No Content",
        "205": "Reset Content",
        "206": "Partial Content",
        "300": "Multiple Choice",
        "301": "Moved Permanently",
        "302": "Found",
        "303": "See Other",
        "304": "Not Modified",
        "307": "Temporary Redirect",
        "308": "Permanent Redirect",
        "400": "Bad Request",
        "401": "Unauthorized",
        "402": "Payment Required",
        "403": "Forbidden",
        "404": "Not Found",
        "405": "Method Not Allowed",
        "406": "Not Acceptable",
        "407": "Proxy Authentication Required",
        "408": "Request Timeout",
        "409": "Conflict",
        "410": "Gone",
        "411": "Length Required",
        "412": "Precondition Failed",
        "413": "Payload Too Large",
        "414": "URI Too Long",
        "415": "Unsupported Media Type",
        "416": "Range Not Satisfiable",
        "417": "Expectation Failed",
        "418": "I'm a teapot",
        "422": "Unprocessable Entity",
        "423": "Locked",
        "424": "Failed Dependency",
        "425": "Too Early",
        "426": "Upgrade Required",
        "428": "Precondition Required",
        "429": "Too Many Requests",
        "431": "Request Header Fields Too Large",
        "451": "Unavailable For Legal Reasons",
        "500": "Internal Server Error",
        "501": "Not Implemented",
        "502": "Bad Gateway",
        "503": "Service Unavailable",
        "505": "HTTP Version Not Supported",
        "506": "Variant Also Negotiates",
        "507": "Insufficient Storage",
        "508": "Loop Detected",
        "510": "Not Extended",
        "511": "Network Authentication Required"
    }

    @staticmethod
    def _guess_type(path):
        return mimetypes.types_map.get(os.path.splitext(path)[-1], "application/octet-stream")

    def __init__(self, loop, writer: StreamWriter, version, config, _gzip):
        mimetypes.types_map[".js"] = "application/javascript"
        self.__loop = loop
        self.__writer = writer
        self.__config = config
        self.__gzip_extern_name = self.__config.get_gzip_file_types()
        self.__static_path = sys.path[0] if len(self.__config.get_static_path()[0]) == 0 else \
            self.__config.get_static_path()[0]
        self.__gzip_flag = _gzip
        self.version = version
        self.__web_cached = self.__config.get_web_cached()
        self.__web_cached["range_size"] -= 1
        self.__code = 200
        self.__plain = "OK"
        self.__headers = {}
        self.__cookies = {}
        self.__start_read = 0
        self.__read_size = 0
        self._source_data = None
        self.__reinit()

    def set_data(self, data):
        self._source_data = data

    def __reinit(self):
        self.__chunked = False
        self.__sender = None
        self.__data = b""
        self.__path = ""
        self.__fd = None
        self.__cache_flag = False
        self.__range_flag = False
        self.__gzip_flag = False
        self.__source_data = None

    def set_code(self, code):
        self.__code = int(code)
        self.__plain = HTTPResponse.static_http_code_plain.get(str(code), "")

    def get_code(self):
        return self.__code

    def get_cookie_by_name(self, name, default_val=None):
        return self.__cookies.get(name, default_val)

    def get_cookie(self):
        cookie_str = []
        for item in self.__cookies.items():
            k, v = item
            if len(v.strip()) == 0:
                cookie_str.append(k)
            else:
                cookie_str.append(("%s=%s" % (str(k), str(v))))
        return str.join('; ', cookie_str)

    def set_cookie(self, val):
        if len(val) == 1:
            self.__cookies[val[0]] = ''
        else:
            k, v = val
            self.__cookies[k] = v

    code = property(get_code, set_code)

    cookies = property(get_cookie, set_cookie)

    def __type_outer(self, result):
        data = b""
        headers = {}
        code = 200
        plain = ""
        if result is None:
            code = 204
            data = b""
        elif isinstance(result, str):
            headers["Content-Type"] = "text/plain"
            data = result.encode()
        elif isinstance(result, dict) or isinstance(result, list):
            headers["Content-Type"] = "application/json"
            for key in (result.keys() if isinstance(result, dict) else range(0, len(result))):
                result[key] = self.__spread_type(result[key])
            data = json.dumps(result).encode()
        elif isinstance(result, tuple):
            for i, item in enumerate(result):
                if i == 0:
                    code = int(item)
                elif i == 1:
                    for _ in dict(result[1]).items():
                        key, value = _
                        headers[key] = value
                elif i == 2:
                    data = bytes(result[2], encoding='utf8') if isinstance(result[2], str) else bytes(result[2])
                elif i == 3:
                    plain = str(result[3])
        elif isinstance(result, types.GeneratorType):
            headers["Transfer-Encoding"] = "chunked"
            data = result
        elif isinstance(result, FileDeliver):
            path = result.test_exist(self.__static_path)
            if path is None:
                code = 404
                headers["Content-Type"] = 'text/plain'
                data = b"Not Found"
            else:
                data = path
        elif isinstance(result, Exception):
            code = 500
            headers["Content-Type"] = "text/plain"
            data = result
        else:
            return self.__type_outer(self.__spread_type(result))
        return (code, plain, headers, data)

    def __spread_type(self, cls):
        result = None
        if hasattr(cls, "__fields__"):
            result = {}
            fields = getattr(cls, "__fields__")
            for key in fields:
                if hasattr(cls, key):
                    val = getattr(cls, key)
                    result[key] = self.__spread_type(val)
        elif isinstance(cls, dict):
            result = {}
            for item in cls.items():
                k, v = item
                result[k] = self.__spread_type(v)

        elif isinstance(cls, int) or isinstance(cls, float) \
                or isinstance(cls, str) \
                or isinstance(cls, bool):
            result = cls
        elif isinstance(cls, datetime.datetime):
            result = str(cls)
        elif hasattr(cls, "__iter__"):
            result = []
            _iter = cls.__iter__()
            while _iter is not None:
                try:
                    result.append(self.__spread_type(next(_iter)))
                except StopIteration:
                    break
        return result

    def analysis_result(self, result):
        self.__reinit()
        self._source_data = result
        if isinstance(result, tuple):
            self.__gzip_flag = False
        code, plain, headers, data = self.__type_outer(result)
        self.code = code
        if len(plain) > 0:
            self.__plain = plain
        self.__headers.update(headers)
        self.__data = data
        if isinstance(data, types.GeneratorType):
            self.__chunked = True
            self.__sender = data
        elif isinstance(result, FileDeliver) and code == 200:
            self.__path = data
            self.__data = result

    def get_data(self):
        return self._source_data

    def result(self):
        if self.__fd:
            return (self.__path, self.__start_read, self.__read_size)
        elif self.__chunked:
            return self.__sender
        else:
            return self.__data

    def del_cookie(self, name):
        if self.cookies.get(name):
            del self.cookies[name]

    def push_response(self, req: HTTPRequest, single=False):
        tp = str

        if isinstance(self.__data, FileDeliver):
            exter_name = os.path.splitext(self.__path)[-1]
            _range = req.get_header("Range")

            self.__read_size = size = os.path.getsize(self.__path)

            self.__headers["Accept-Ranges"] = 'bytes'
            if _range:
                self.__fd = open(self.__path, "rb")
                _range = _range.split(",")[0].split("=")[1].split('-')
                self.__start_read = start = int(_range[0])
                end = int(_range[1]) if len(_range[1].strip()) > 0 else start + self.__web_cached["range_size"]
                end = size - 1 if end > size else end
                self.__headers["Content-Range"] = "bytes %i-%s/%i" % (
                    start, end, size)
                self.__read_size = size = int(_range[1]) - start if len(_range[1]) > 0 else end - start + 1
                self.__headers["Content-Length"] = str(size)
                self.__range_flag = True
                self.code = 206
                self.__data = b""

            if exter_name in self.__web_cached["extername"]:
                self.__headers["Cache-Control"] = "max-age=%i" % (self.__web_cached["expires"],)
                check_code = 200
                st_mtime = os.stat(self.__path).st_mtime
                lastfiletime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(st_mtime))
                md5 = '\"%s\"' % (hashlib.md5(FileDeliver.read_all(self.__path)).hexdigest(),)

                if req.get_header("If-Modified-Since"):
                    _since = req.get_header("If-Modified-Since").strip()
                    if int(st_mtime) == int(time.mktime(time.strptime(_since, "%a, %d %b %Y %H:%M:%S GMT"))):
                        check_code = 304
                    else:
                        check_code = 200
                elif req.get_header("If-Unmodified-Since"):
                    _since = req.get_header("If-Unmodified-Since").strip()
                    if int(st_mtime) != int(time.mktime(time.strptime(_since, "%a, %d %b %Y %H:%M:%S GMT"))):
                        check_code = 412
                    else:
                        check_code = 304

                if req.get_header("If-None-Match"):
                    _md5 = req.get_header("If-None-Match").strip()
                    if _md5 == md5:
                        check_code = 304
                    else:
                        check_code = 200 if check_code == 200 else check_code
                elif req.get_header("If-Match"):
                    _md5 = req.get_header("If-Match").strip()
                    if _md5 != md5:
                        check_code = 412
                    else:
                        check_code = 304

                if check_code == 304 or check_code == 412:
                    self.__data = b""
                    self.code = check_code if self.code == 200 else self.code
                    self.__chunked = False
                    self.__gzip_flag = False
                    self.__cache_flag = True

                self.__headers["Date"] = self.__headers["Expires"] = time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                                                                   time.localtime(
                                                                                       time.time() + self.__web_cached[
                                                                                           "expires"]))

                self.__headers["Last-Modified"] = lastfiletime
                self.__headers["Etag"] = md5

            self.__headers["Content-Type"] = HTTPResponse._guess_type(self.__path)

            if not self.__cache_flag and not self.__range_flag:
                if exter_name in self.__gzip_extern_name:
                    self.__data = FileDeliver.read_all(self.__path)
                else:
                    self.__fd = open(self.__path, "rb")
                    self.__data = b""
                    self.__headers["Content-Length"] = size
                    self.__gzip_flag = False
        elif isinstance(self.__data, Exception):
            self.__data = str.join('', traceback.format_exception(self.__data, value=self.__data,
                                                                  tb=self.__data.__traceback__)).encode()

        if len(self.__cookies.keys()):
            self.__headers["Set-Cookie"] = self.cookies

        if self.__chunked and not self.__cache_flag and not self.__range_flag and self.version < 2.0:
            tp = self.__sender.send(None)
            if tp is dict:
                self.__headers["Content-Type"] = "application/json"
            elif tp is str:
                self.__headers["Content-Type"] = "text/plain"
            elif tp is bytes:
                self.__headers["Content-Type"] = "application/octet-stream"
            else:
                self.__headers["Content-Type"] = tp
            self.__data = b""
            self.__gzip_flag = False

        if (self.__gzip_flag or self.__chunked) and (tp is str or tp is dict) and (not self.__range_flag):
            self.__headers["Content-Encoding"] = "gzip"
            if not self.__chunked:
                self.__data = gzip.compress(self.__data if isinstance(self.__data, bytes) else self.__data.encode())

        if self.__fd is None and not self.__cache_flag and not self.__range_flag and not self.__chunked:
            self.__headers["Content-Length"] = len(self.__data)

        if req.method == "HEAD":
            self.__data = b''
            self.__fd = None
            self.__chunked = False
            if self.__chunked:
                del self.__headers["Transfer-Encoding"]
            del self.__headers["Content-Length"]

        if self.version > 1.1:
            return

        header_ = "HTTP/%.1f %i %s\r\n" % (self.version, self.code, self.__plain)

        for item in self.__headers.items():
            key, value = item
            header_ += ("%s: %s\r\n" % (key, value))

        header_ += "\r\n"

        self.control_async(self.write_to_client(header_.encode() + self.__data), single)

        if self.__chunked:
            while True:
                data = self.__sender.send(None)
                if data is None:
                    data = b"0\r\n\r\n"
                    self.control_async(self.write_to_client(data), single)
                    self.__sender.send(None)
                    break
                if tp is dict or tp is str:
                    data = gzip.compress(data.encode())
                    data = hex(len(data))[2:].encode() + b"\r\n" + data + b"\r\n"
                else:
                    data = hex(len(data))[2:].encode() + b"\r\n" + data + b"\r\n"
                asyncio.run_coroutine_threadsafe(self.write_to_client(data), self.__loop)
        elif self.__fd:
            self.control_async(self.sendfile(self.__fd, self.__start_read, self.__read_size), single)

    def control_async(self, fn, single):
        waiter = asyncio.run_coroutine_threadsafe(fn, self.__loop)
        if single:
            return waiter
        else:
            return waiter.result()

    def set_header(self, name, value):
        self.__headers[name] = str(value)

    def del_header(self, name):
        if self.__headers.get(name) is None:
            return
        del self.__headers[name]

    def get_header(self, name, default=None):
        return self.__headers.get(name.lower(), default)

    def headers(self):
        return self.__headers.copy()

    async def sendfile(self, fd, start, count):
        """
        Zero Copy File
        :param fd: File fd
        :param start: start offset
        :param count: read count
        :return:
        """
        try:
            result = await self.__loop.sendfile(self.__writer.transport, fd, offset=start, count=count,
                                                fallback=False)
            fd.close()
            return result
        except PermissionError:
            pass
        except ValueError:
            pass
        except RuntimeError:
            fd.seek(start)
            data = fd.read(count)
            await self.write_to_client(data)
        finally:
            fd.close()

    async def write_to_client(self, data):
        try:
            self.__writer.write(data)
            await self.__writer.drain()
        except ConnectionResetError:
            return
