import os, types, mimetypes


class RequestsState:
    NEXT = 0x0
    PUSHNOW = 0x1
    CLOSE = 0x2


class Methods:
    GET = "GET"
    HEAD = 'HEAD'
    POST = "POST"
    PUT = 'PUT'
    DELETE = 'DELETE'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = "TRACE"


class ClassSource:
    FORM_URLENCODE = 0x01
    JSON = 0x02
    FORM_DATA = 0x04


class FileDeliver:
    @staticmethod
    def read_all(path):
        fd = open(path, mode="rb+")
        _data = fd.read()
        fd.close()
        return _data

    @staticmethod
    def write_all(path, data):
        fd = open(path, mode="wb+")
        _data = fd.write(data)
        fd.close()

    def __init__(self, path=None, data=None, filename=None, filetype=None):
        self.data = None
        self.__path = None
        self.filename = ""
        self.filtype = ""
        if path is None:
            self.data = data
            self.filename = filename
            self.filtype = filetype
            self.ext_name = os.path.splitext(self.filename)[-1] if self.filename else ""
        elif isinstance(path, FileDeliver):
            self.data = path.data
            self.filename = path.filename
            self.filtype = path.filtype
            self.__path = path.__path
            self.ext_name = path.ext_name
        else:
            self.__path = path.replace("\\", "/")
            self.filename = os.path.split(self.__path)[-1]
            _types = mimetypes.guess_type(self.__path)
            self.filtype = _types[0] if len(_types) > 0 else None
            self.ext_name = os.path.splitext(self.__path)[-1]

    def invaild(self):
        return self.__path is None and self.data is None

    def test_exist(self, static_path):
        if os.path.exists(self.__path):
            return self.__path
        elif os.path.exists(static_path + "/" + self.__path):
            return static_path + self.__path
        return None

    def save(self, path):
        FileDeliver.write_all(path, self.data)


class Vector:
    def __init__(self, tp):
        self.type = tp

    def __call__(self):
        return None


class LogHandle:
    def __init__(self, name):
        self.name = name

    def add_handle(self):
        pass

    def info(self):
        pass

    def warn(self):
        pass

    def critical(self):
        pass

    def error(self):
        pass

    def debug(self):
        pass

def async_taker(method, *args):
    pass


class SQLModel:
    @staticmethod
    def model_factory(parent):
        def create_model(cls):
            cache_fields = {}
            __fields__ = []
            for item in cls.__dict__.items():
                key, value = item
                if not ((str(key).startswith("__") and str(key).endswith("__")) or isinstance(value,
                                                                                              types.FunctionType)):
                    __fields__.append(key)
                cache_fields[key] = value
            cache_fields["__fields__"] = __fields__
            return type(cls.__name__, (parent,), cache_fields)

        return create_model

    class DataBaseConnection:
        def __init__(self, id):
            self.id = str(id)

    def get_con(self, *args):
        raise ModuleNotFoundError("Connect Method Not Defined")

    def destory_con(self, *args):
        raise ModuleNotFoundError("Close Method Not Defined")


class WebSocketHOOK:
    HANDSHAKE = 0x0
    MESSAGE = 0x1
    CLOSE = 0x2
    PING = 0x3
