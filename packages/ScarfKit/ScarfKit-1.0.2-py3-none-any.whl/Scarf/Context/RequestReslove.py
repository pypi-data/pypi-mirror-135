from Scarf.Protocol.HTTP import HTTPRequest, HTTPResponse
from Scarf.Protocol.WebSocket import WebSocketParamter, WebSocket
from Scarf.Context.Timer import TaskParamter
from Scarf.paramter import Paramter
from Scarf.Tip import *

import os, types, traceback


class EventHandler:
    def __init__(self, callback, event, _this):
        self.__callback = callback
        self.__event = event
        self.__source = _this

    def test_event(self, name):
        if name == self.__event:
            return True
        event_ = self.__event.split(".")
        name = name.split(".")
        if len(name) > len(event_):
            return False

        index = -1
        source = 0

        while index >= -len(name):
            if event_[index] == name[index]:
                source += 1
            else:
                break
            index -= 1

        return source

    def set_source(self, _this):
        self.__source = _this

    def __call__(self, *args, **kwargs):
        return self.__callback(self.__source, *args, **kwargs)


class FilterRegister:
    def __init__(self, req, res):
        self.__req_flag_____ = bool(req)
        self.__res_flag_____ = bool(res)
        self.__self_____ = self

    def enter_intercept(self, req: HTTPRequest, res: HTTPResponse):
        if self.__req_flag_____:
            raise RuntimeError("Request Interceptor not implemented")
        else:
            pass

    def outer_filter(self, req: HTTPRequest, res: HTTPResponse):
        if self.__res_flag_____:
            raise RuntimeError("Request Filter not implemented")
        else:
            pass

    def get_reg_opt(self):
        return (self.__req_flag_____, self.__res_flag_____)

    def set_source(self, _this):
        self.__self_____ = _this


class RouterRegister:
    def __init__(self, path, methods, args_source, callback, this, is_file=False):
        self.path = path
        self.methods = methods
        self.is_file = is_file
        self.__args_source = args_source
        self.__this = this
        self.__callback = callback

    def __call__(self, *args, **kwargs):
        return self(self.__this, *args, **kwargs)

    def _get_logger(self, loggers):
        return loggers.get(self.__this.__module__ + "." + self.__this.__class__.__name__)

    def call(self, req: HTTPRequest, res: HTTPResponse, error, sql_use, sqls, extend):
        querys = req.query()
        url_params = req.get_url_params()
        data = None
        ctp = req.get_header("content-type", "")
        if ctp.find("application/x-www-form-urlencoded") > -1:
            data = req.get_data_with_form_urlencoded()
            ctp = ClassSource.FORM_URLENCODE
        elif ctp.find("application/json") > -1:
            data = req.get_data_with_json()
            ctp = ClassSource.JSON
        elif ctp.find("multipart/form-data") > -1:
            data = req.get_data_with_form_data()
            ctp = ClassSource.FORM_DATA
        else:
            ctp = 0
        types_values = self.__callback.__annotations__
        call_params = [self.__this]
        for arg in types_values.items():
            arg_name, tp = arg
            _flag = False
            if isinstance(tp, type) or isinstance(tp, str):
                for _ in extend.items():
                    k, v = _
                    if isinstance(v, type(tp)) or v is tp:
                        _flag = True
                        call_params.append(v)
                        break
                    elif isinstance(tp, str):
                        if k == tp:
                            _flag = True
                            call_params.append(v)
                            break
                if _flag:
                    continue
            if isinstance(tp, HTTPRequest) or tp is HTTPRequest:
                call_params.append(req)
                continue
            elif isinstance(tp, HTTPResponse) or tp is HTTPResponse:
                call_params.append(res)
                continue
            elif tp is bytes:
                call_params.append(req.get_data())
                continue
            elif isinstance(tp, SQLModel.DataBaseConnection):
                if sqls.get(tp.id):
                    if sql_use.get(tp.id):
                        sql_con = sql_use[tp.id]
                    else:
                        sql_con = sql_use[tp.id] = sqls[tp.id].get_con()
                else:
                    sql_con = None
                call_params.append(sql_con)
                continue
            elif tp is SQLModel.DataBaseConnection:
                v = tuple(sqls.items())
                if len(v) > 0:
                    if sql_use.get(v[0][0]):
                        sql_con = sql_use[v[0][0]]
                    else:
                        sql_con = sql_use[v[0][0]] = sqls[v[0][0]].get_con()
                    call_params.append(sql_con)
                else:
                    call_params.append(None)
                continue
            for index, item in enumerate(self.__args_source):
                try:
                    if arg_name in item:
                        if index == 0:
                            call_params.append(tp(querys.get(arg_name, tp())))
                        elif index == 1:
                            if ctp & item[0] == 0:
                                call_params.append(tp())
                                continue
                            if arg_name[0] == "_":
                                _value = data
                            else:
                                _value = data.get(arg_name, tp())
                            if isinstance(tp, Vector):
                                if not isinstance(_value, list):
                                    call_params.append([])
                                    continue
                                try:
                                    call_params.append(self.__arrary_push((data if arg_name[0] == "_" else _value), tp))
                                except:
                                    call_params.append([])
                                continue
                            elif tp is FileDeliver and isinstance(_value, FileDeliver):
                                call_params.append(_value)
                                continue
                            elif tp is dict and isinstance(_value, dict):
                                call_params.append(_value)
                                continue
                            elif isinstance(_value, dict):
                                _new_tp = tp()
                                for _ in _value.items():
                                    key, value = _
                                    if hasattr(_new_tp, key):
                                        if hasattr(_new_tp, "__annotations__"):
                                            cls_type = _new_tp.__annotations__.get(key, type(value))
                                        else:
                                            cls_type = type(value)
                                        try:
                                            value = cls_type(value)
                                        except:
                                            value = tp()
                                        setattr(_new_tp, key, value)
                                call_params.append(_new_tp)
                                continue
                            call_params.append(tp(_value))
                        elif index == 2:
                            call_params.append(tp(req.get_header(arg_name, tp())))
                        elif index == 3:
                            call_params.append(tp(url_params.get(arg_name, tp())))
                except Exception as e:
                    call_params.append(tp())
                    error(e)
                    break
        return self.__callback(*call_params)

    def __arrary_push(self, data, tp):
        params = []
        for item in data:
            if isinstance(tp.type, Vector):
                params.append(self.__arrary_push(item, tp.type))
            elif tp.type is dict:
                params.append(item)
            else:
                _new_type = tp.type()
                for _ in item.items():
                    key, value = _
                    if hasattr(_new_type, key):
                        setattr(_new_type, key, value)
                params.append(_new_type)
        return params


class RequestReslove:
    @staticmethod
    def route(path, methods=(Methods.GET,), args_source=((), (), (), ())):
        def factory(callback=lambda _: _):
            def set_self(self, name) -> RouterRegister:
                router = RouterRegister(path, methods, args_source, callback, self)
                setattr(self, name, router)
                return router

            return set_self

        return factory

    @staticmethod
    def websocket(path, hook, **kwargs):
        def factory(callback=lambda _: _):
            def set_self(self, name) -> WebSocketParamter:
                router = WebSocketParamter(path, hook, self, callback, **kwargs)
                setattr(self, name, router)
                return router

            return set_self

        return factory

    @staticmethod
    def event(*args, **externs):
        def factory(fn=lambda _: _):

            def set_self(self, name) -> EventHandler:
                router = EventHandler(fn, args[0], self)
                setattr(self, name, router)
                return router

            if isinstance(fn, types.FunctionType) or isinstance(fn, types.MethodType):
                return set_self
            else:
                module_rename = externs.get("modules", False)
                if len(args) % 2 == 0 and len(args) > 0:
                    index = 0
                    while index < len(args):
                        event_name = args[index]
                        if module_rename:
                            event_name = fn.__module__ + "." + fn.__name__ + "." + event_name
                            fn_ = getattr(fn, args[index + 1])
                            setattr(fn, args[index + 1], RequestReslove.event(event_name)(fn_))
                        index += 2
                return fn

        return factory

    @staticmethod
    def timer(cycle, times=0, user_arg=None):
        def factory(callback=lambda _: _):
            def set_self(self, name) -> TaskParamter:
                if isinstance(cycle, int):
                    task = TaskParamter(cycle, times, callback, self, user_arg)
                else:
                    raise TypeError("Unknow Type In Timer")
                setattr(self, name, task)
                return task

            return set_self

        return factory

    def __init__(self, routers, error_, config: Paramter, filters, sql, extend, loggers):
        self.__routers = routers
        self.__loggers = loggers
        self.__sql = sql
        self.__enter_intercept = []
        self.__outer_filters = []
        self.__extend = extend
        enter_intercept, outer_filters = filters
        self.__enter_intercept = enter_intercept
        self.__outer_filters = outer_filters
        self.__config = config
        self.__single_reslove = self.__config.get_thread_pool_worker_num().get("single", False)
        self.__cros_config = self.__config.get_cros_params()
        static_path, entry_file = self.__config.get_static_path()
        self.__static_path = static_path
        self.__static_entryfile = entry_file
        self.__error = error_

    def _get_global_sql(self):
        return self.__sql

    def __get_deep_from_method(self, fn):
        result = []
        extends = {}
        for i in fn.__annotations__.items():
            k, v = i
            if isinstance(v, SQLModel.DataBaseConnection):
                sql = self.__sql.get(v.id)
                if sql:
                    result = (k, v.id)
                else:
                    result = (k, None)
            elif v is SQLModel.DataBaseConnection:
                v = tuple(self.__sql.items())
                if len(v) > 0:
                    result = (k, v[0][0])
                else:
                    result = (k, None)
            else:
                for _ in self.__extend.items():
                    _k, _v = _
                    if isinstance(v, str):
                        if _k == v:
                            extends[k] = _v
                            break
                    elif isinstance(_v, type(v)) or v is _v:
                        extends[k] = _v
                        break
        return (result, extends)

    def __close_cons(self, sql_use):
        for item in sql_use.items():
            n, s = item
            self.__sql[n].destory_con(s)

    def router_reslove(self, req: HTTPRequest, res: HTTPResponse):
        sql_use = {}

        router = self._router_match(req)

        req.is_file = isinstance(router, str) or (isinstance(router, RouterRegister) and router.is_file)
        req.is_websocket = isinstance(router, WebSocketParamter)
        req.is_not_found = router is None

        for intercept in self.__enter_intercept:
            sql_params = {}
            result = self.__get_deep_from_method(intercept.enter_intercept)
            if len(result[0]) > 1:
                arg_name, id = result[0]
                if arg_name and id:
                    if sql_use.get(id):
                        sql_params[arg_name] = sql_use[id]
                    else:
                        sql_params[arg_name] = sql_use[id] = self.__sql[id].get_con()
                else:
                    sql_params[arg_name] = None
            result = intercept.enter_intercept(req, res, **sql_params, **result[1])
            if result == 0 or result is None:
                continue
            elif result == 1:
                res.analysis_result(res._source_data)
                res.push_response(req, self.__single_reslove)
                if req.http_version > 1.1:
                    yield None
                self.__close_cons(sql_use)
                yield None
            elif result == 2:
                self.__close_cons(sql_use)
                raise ConnectionRefusedError()

        if router is None:
            res.set_data((404, {"Content-Type": "text/plain"}, "Not Found"))
        elif isinstance(router, str):
            res.set_data(FileDeliver(router))
        elif req.method.upper() == "OPTIONS":
            for _ in self.__cros_config.items():
                key, value = _
                res.set_header(key, value)
            res.set_header("Access-Control-Allow-Methods", str.join(', ', router.methods))
        elif req.method.upper() not in str.join(', ', router.methods):
            res.analysis_result((405, {"Content-Type": "text/plain"}, "Method Not Allowed"))
        elif isinstance(router, RouterRegister):
            try:
                res.set_data(router.call(req, res, self.__error, sql_use, self.__sql, self.__extend))
            except Exception as e:
                logger = router._get_logger(self.__loggers)
                if logger:
                    logger.error(str.join('', traceback.format_exception(e, value=e, tb=e.__traceback__)))
                res.set_data(e)

        elif isinstance(router, WebSocketParamter):
            key = req.get_header("Sec-WebSocket-Key")
            if req.get_header("Connection") and key:
                router = WebSocket(router.path, router.hook, router.hook[0].get_logger(self.__loggers), **router.kwargs,
                                   single=self.__single_reslove)
                result = router(req, key, sql=self.__sql, sql_use=sql_use)
                if isinstance(result, tuple):
                    res.analysis_result(result)
                else:
                    res.analysis_result(router._handshake())
                res.push_response(req, self.__single_reslove)
                yield router
                yield None
            else:
                res.set_data((400, {"Content-Type": "text/plain"}, b"Invaild WebSocket Request"))

        for outer in self.__outer_filters:
            sql_params = {}
            result = self.__get_deep_from_method(outer.outer_filter)
            if len(result[0]) > 1:
                arg_name, id = result[0]
                if arg_name and id:
                    if sql_use.get(id):
                        sql_params[arg_name] = sql_use[id]
                    else:
                        sql_params[arg_name] = sql_use[id] = self.__sql[id].get_con()
                else:
                    sql_params[arg_name] = None
            result = outer.outer_filter(req, res, **sql_params, **result[1])
            if result == 0 or result is None:
                continue
            elif result == 1:
                break
            elif result == 2:
                self.__close_cons(sql_use)
                raise ConnectionRefusedError()

        res.analysis_result(res._source_data)
        res.push_response(req, self.__single_reslove)
        if req.http_version > 1.1:
            yield None
        self.__close_cons(sql_use)
        yield None

    def _router_match(self, req):
        _path = req.path
        path = self.__static_path + _path.replace("\\", "/")
        if os.path.exists(path):
            if os.path.isfile(path):
                return path
            else:
                if os.path.exists(path + "/" + self.__static_entryfile):
                    return path + "/" + self.__static_entryfile

        for item in self.__routers:
            url_params = {}

            _item = [_.strip() for _ in item.path.split("/") if len(_.strip()) > 0]
            path = [_.strip() for _ in _path.split("/") if len(_.strip()) > 0]

            if len(path) > len(_item) and _item[-1] != "*":
                continue
            elif len(path) < len(_item):
                for n in range(0, len(_item) - len(path)):
                    path.append(None)

            for i, _ in enumerate(_item):
                if _[0] == ":":
                    url_params[_item[i][1:]] = path[i]
                elif _ != "*" and path[i] != _:
                    break
                if i == len(_item) - 1:
                    req.set_url_params(url_params)
                    return item
        return None
