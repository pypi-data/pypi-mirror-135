from Scarf.Tip import FileDeliver
import yaml, os, multiprocessing


class Paramter:
    def __init__(self, configpath, config=None):
        if configpath:
            with open(configpath, "r+", encoding='utf8') as fd:
                self.__paramters = yaml.safe_load(fd.read())
        else:
            self.__paramters = config
        self.__release = self.__GetProperties(False, "server", "release")
        self.__http_port = self.__GetProperties(81, "server", "ports", "http")
        self.__https_port = self.__GetProperties(-1, "server", "ports", "https")
        self.__http2 = self.__GetProperties({"enable": False}, "server", "http2")
        self.__thread_pool_workers = self.__GetProperties(
            {"min": multiprocessing.cpu_count() * 2, "max": multiprocessing.cpu_count() * 2 + 3, "max_work_task": 10},
            "server", "workers")
        self.__server_ssl = {
            "crt": self.__GetProperties(None, "server", "ssl_options", "crt"),
            "key": self.__GetProperties(None, "server", "ssl_options", "key"),
            "pwd": self.__GetProperties('', "server", "ssl_options", "pwd"),
            "ssl_handshake_timeout": self.__GetProperties(15, "server", "ssl_options", "ssl_handshake_timeout")
        }
        self.__gzip = self.__GetProperties(tuple(), "server", "gzip")
        self.__static_options = [self.__GetProperties("", "server", "static", "visitpath").replace("\\", "/"),
                                 self.__GetProperties("index.html", "server", "static", "entryfile")]
        if os.path.exists(self.__static_options[0]):
            self.__static_options[0] = os.path.abspath(self.__static_options[0]).replace("\\", "/")
        self.__sql_options = []
        self.__keep_alive_timeout = (self.__GetProperties(15, "server", "keep_alive", "http_handshake_timeout"),
                                     self.__GetProperties(3, "server", "keep_alive", "http_data_readtimeout"),
                                     self.__GetProperties(3, "server", "keep_alive", "alive_timeout"))
        for item in self.__GetProperties([], "datasource"):
            self.__sql_options.append(item)
        cros_params = ("Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Access-Control-Max-Age",
                       "Access-Control-Allow-Credentials")
        self.__cros_params = {}
        self.__webcached = self.__GetProperties(
            {"expires": 0, "extername": tuple(), "range_size": 3145728}, "server",
            "webcached")
        self.__Pages = self.__GetProperties([], "server", "static", "map")
        for index, item in enumerate(self.__GetProperties([], "server", "cros")):
            if len(str(item)) > 0:
                self.__cros_params[cros_params[index]] = str(item).lower() if index == 3 else str(item)

    def __GetProperties(self, default_value, *keys):
        _item = self.__paramters
        for index, item in enumerate(keys):
            _item = _item.get(item, default_value) if index == len(keys) - 1 else _item.get(item, {})
        return _item

    def get_running_time_port(self):
        try:
            self.__http_port = int(self.__http_port)
            self.__https_port = int(self.__https_port)
            if self.__http_port > 65535 or self.__https_port > 65535:
                raise Exception("Error Port")
        except Exception as e:
            raise e
        """Get (HTTPPort,HTTPSPort,)"""
        return (self.__http_port, self.__https_port)

    def get_release(self):
        if not isinstance(self.__release, bool):
            raise ValueError("Value Error : release")
        return self.__release

    def get_thread_pool_worker_num(self):
        if not ((self.__thread_pool_workers.get("min") and self.__thread_pool_workers[
            "max"] and self.__thread_pool_workers.get("max_work_task")) or self.__thread_pool_workers.get("single")) :
            raise ValueError("Error TheadPool Options")
        return self.__thread_pool_workers

    def get_ssl_options(self):
        """Get SSLOptions crt,key,password,ssl_hand_shake_time"""
        return self.__server_ssl.copy()

    def get_sql_options(self):
        """Get SQL Options"""
        return self.__sql_options

    def get_static_path(self):
        return self.__static_options

    def get_keep_alive_timeout(self):
        return self.__keep_alive_timeout

    def get_gzip_file_types(self):
        return self.__gzip

    def get_cros_params(self):
        return self.__cros_params

    def get_web_cached(self):
        return self.__webcached

    def get_pages(self):
        return self.__Pages

    def get_http2(self):
        return self.__http2
