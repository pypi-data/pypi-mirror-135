from Scarf.Context.RequestReslove import RouterRegister, FilterRegister, EventHandler, WebSocketParamter
from Scarf.paramter import Paramter
from Scarf.Base.TCPServer import TCPServer
from Scarf.Context.Timer import TaskParamter
from Scarf.Context.Context import ClientContext
from Scarf.Protocol.HTTP import HTTPRequest
from Scarf.Tip import *
from Scarf.Context.Log import LogDeeper

import types, os, yaml, json, sys


class Scarf:
    def __init__(self):
        """transport server"""
        self.__transport_server = None
        self.__config: Paramter = None
        self.__context: ClientContext = None
        self.__routers = []
        self.__req_intercept = []
        self.__res_filter = []
        self.__events_ = []
        self.__tasks = []
        self.__sql_opts = {}
        self.__websocket_map = {}
        self.__extend = {}
        self.__module_config = {}
        self.__modules = {}
        self.__loggers = {}
        self.__server_log: LogDeeper = None

    def __scan_config(self):
        if os.path.exists("./config"):
            for item in os.walk("./config"):
                for file in item[2]:
                    module, exter_name = os.path.splitext(file)
                    with open("./config/" + file, "r+", encoding='utf8') as fd:
                        if exter_name == ".yml":
                            self.__module_config[module] = yaml.safe_load(fd.read())
                        elif exter_name == ".json":
                            self.__module_config[module] = json.loads(fd.read())
                        else:
                            self.__server_log.warn("ignore '%s' module config ,file type not support" % (module,))
                        fd.close()

    def load_config_from_file(self, config_path: str):
        self.__config = Paramter(config_path)
        self.__server_log = LogDeeper("Scarf", "WebServer", self.__config.get_release())

    def load_config(self, config: dict):
        self.__config = Paramter(None, config)
        self.__server_log = LogDeeper("Scarf", "WebServer", self.__config.get_release())

    def scan_module(self, md):
        for item in dir(md):
            value = getattr(md, item)
            if isinstance(value, types.MethodType):
                ret_type = value.__annotations__.get("return")
                if ret_type is RouterRegister:
                    self.__routers.append(value(item))
                elif ret_type is TaskParamter:
                    self.__tasks.append(value(item))
                elif ret_type is WebSocketParamter:
                    value = value(item)
                    if not self.__websocket_map.get(value.path):
                        self.__websocket_map[value.path] = []
                    self.__websocket_map[value.path].append(value)
            self.__modules[md.__module__ + "." + md.__class__.__name__] = md

        if not hasattr(md, '_emit'):
            setattr(md, '_emit', self.__emit)

    def __emit(self, event_, *params, **kwargs):
        sources = []
        event_obj = None
        for i, e in enumerate(self.__events_):
            result = e.test_event(event_)
            if isinstance(result, bool):
                if result:
                    event_obj = e
                    break
            elif isinstance(result, int) and result > 0:
                sources.append([result, i])

        if len(sources) > 0 and event_obj is None:
            sources.sort(key=lambda a: a[0], reverse=True)
            event_obj = self.__events_[sources[0][1]]

        if event_obj is None:
            return None

        return event_obj(*params, **kwargs)

    def register_hook(self, module):
        if isinstance(module, FilterRegister):
            _req_flag, _res_flag = module.get_reg_opt()
            if _req_flag:
                self.__req_intercept.append(module)
            if _res_flag:
                self.__res_filter.append(module)
            setattr(module, '_emit', self.__emit)
        else:
            raise TypeError("Class Not 'FilterRegister' ")

    def register_events(self, md):
        for item in dir(md):
            value = getattr(md, item)
            if isinstance(value, types.MethodType):
                ret_type = value.__annotations__.get("return")
                if ret_type is EventHandler:
                    self.__events_.append(value(item))
        if not hasattr(md, '_emit'):
            setattr(md, '_emit', self.__emit)

    def register_global(self, name, module):
        self.__extend[name] = module

    def register_sql_model(self, name, model):
        for item in self.__config.get_sql_options():
            if name == str(item["name"]):
                item = item.copy()
                del item["name"]
                value = model(**item)
                if isinstance(value, SQLModel):
                    self.__sql_opts[name] = value
                    return
                else:
                    raise ValueError("Invaild SQL Factory Class")

        raise ValueError("No The Same DataSource ('%s')" % (name,))

    def __router_map(self, router, path, static_path, entry_file):
        router = str.join('', [item for item in router.split("/*") if len(item.strip()) > 0])

        def static_factory(_this, req: HTTPRequest):
            file_path = req.path[req.path.index(router) + len(router):]
            not_found_404 = (404, {"Content-Type": "text/plain"}, "Not Found")
            if len(file_path.strip()) == 0:
                file_path = static_path + path + "/" + entry_file
                if os.path.exists(file_path):
                    return FileDeliver(file_path)
                else:
                    return not_found_404
            else:
                file_path = static_path + path + file_path
                if not os.path.exists(file_path):
                    req.is_not_found = True
                    return not_found_404
                elif os.path.isfile(file_path):
                    return FileDeliver(file_path)
                else:
                    file_path += ('/' + entry_file)
                    if os.path.exists(file_path):
                        return FileDeliver(file_path)
                    else:
                        return not_found_404

        return static_factory

    def start_server(self):
        if not self.__config:
            self.__config = Paramter(configpath=None, config={})
        self.__scan_config()
        static_path, entry_file = self.__config.get_static_path()
        static_path = static_path.replace("\\", "/")
        for page in self.__config.get_pages():
            path = FileDeliver(page["path"]).test_exist(static_path)
            result = None
            if path:
                if os.path.isfile(path):
                    result = lambda _: FileDeliver(page["path"])
                else:
                    result = self.__router_map(page["router"], page["path"], static_path, entry_file)
            self.__routers.append(
                RouterRegister(page["router"], (Methods.GET,), ((), (), (), ()), result,
                               None, True))
        for item in self.__modules.items():
            name, module = item
            filename = sys.modules[module.__module__].__file__.replace('/', "\\").split(
                os.path.split(sys.path[0])[0].replace('/', "\\") + "\\")[1]
            module_name = module.__module__ + "." + module.__class__.__name__
            logger = LogDeeper(filename, module_name, self.__config.get_release(),
                               self.__module_config.get(module_name, {}).get("log_format",
                                                                             f"%(asctime)s - $filename[line:%(lineno)d | %(funcName)s] - %(levelname)s: %(message)s"))
            self.__loggers[module_name] = logger

        if len(self.__websocket_map.keys()) > 0:
            handshake_timeout = -1
            data_timeout = -1
            for item in self.__websocket_map.items():
                k, v = item
                hooks = [None, None, None, None]
                for _ in v:
                    if _.hook == WebSocketHOOK.HANDSHAKE:
                        handshake_timeout = _.kwargs.get("handshake_timeout", 10)
                        hooks[0] = _
                    elif _.hook == WebSocketHOOK.MESSAGE:
                        handshake_timeout = _.kwargs.get("data_timeout", 10)
                        hooks[1] = _
                    elif _.hook == WebSocketHOOK.CLOSE:
                        hooks[2] = _
                    elif _.hook == WebSocketHOOK.PING:
                        hooks[3] = _
                try:
                    if hooks.index(None) < 3 and hooks.index(None) > -1:
                        _idx = hooks.index(None)
                        raise Exception("Websocket Hook Not Implementation '%s'" % (
                            'HANDSHAKE' if _idx == 0 else "MESSAGE" if _idx == 1 else "CLOSE" if _idx == 2 else ''))
                except ValueError:
                    pass
                self.__routers.append(
                    WebSocketParamter(k, tuple(hooks), None, handshake_timeout=handshake_timeout,
                                      data_timeout=data_timeout))

        self.__context = ClientContext(self.__config, self.__routers, self.__tasks,
                                       (self.__req_intercept, self.__res_filter),
                                       self.__sql_opts, self.__extend, self.__loggers, self.__server_log)

        for item in self.__module_config.items():
            module_, config = item
            module = self.__modules.get(module_)
            if module:
                name = "init_handle"
                if hasattr(module, config[name]):
                    init_handle = getattr(module, config[name])
                    result = {}
                    for item in init_handle.__annotations__.items():
                        arg_name, tp = item
                        if tp is LogHandle:
                            result[arg_name] = self.__loggers[module.__module__ + "." + module.__class__.__name__]
                        elif isinstance(tp, LogHandle):
                            if tp.name == "WebServer":
                                result[arg_name] = self.__server_log
                            else:
                                result[arg_name] = self.__loggers.get(tp.name)
                        elif tp is SQLModel.DataBaseConnection:
                            if len(self.__sql_opts.values()) > 0:
                                result[arg_name] = tuple(self.__sql_opts.values())[0].get_con()
                            else:
                                result[arg_name] = None
                        elif tp is async_taker:
                            result[arg_name] = self.__context.async_taker
                        elif isinstance(tp, SQLModel.DataBaseConnection):
                            for item in self.__sql_opts.items():
                                name, value = item
                                if name == tp.id:
                                    result[arg_name] = value.get_con()
                                    break
                            else:
                                result[arg_name] = None
                        elif tp is dict or tp is list:
                            result[arg_name] = config.get("config")
                        else:
                            for _ in self.__extend.items():
                                k, v = _
                                if isinstance(tp, str):
                                    if k == tp:
                                        result[arg_name] = v
                                        break
                                elif isinstance(tp, v) or tp is v:
                                    result[arg_name] = tp
                                    break
                    init_handle(**result)
                else:
                    self.__server_log.warn("module '%s' not has init_handle" % (module_,))

        self.__transport_server = TCPServer(self.__config.get_running_time_port(), self.__context.client_context,
                                            self.__config.get_http2()["enable"],
                                            self.__config.get_ssl_options())
        self.__context.set_loop(self.__transport_server.get_event_loop())
        self.__transport_server.start_loop()

    def stop_work(self):
        self.__transport_server.stop_loop()
        self.__context.stop_work()
