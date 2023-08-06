from Scarf.paramter import Paramter
from Scarf.Base.ThreadPool import ThreadPool
from Scarf.Protocol.ClientRequest import ClientRequest
from Scarf.Context.RequestReslove import RequestReslove
from Scarf.Context.Timer import Timer
from Scarf.Context.Log import LogDeeper

import traceback, sys, asyncio, time


class ClientContext:
    def __init__(self, config: Paramter, routers, timer_tasks, filters, sql, extend, loggers,
                 main_logger):
        self.__config = config
        self.__filters = filters
        self.__event_loop = None
        self.__thread_pool = None
        self.__timer = None
        self.__main_logger = main_logger
        self.__http2 = self.__config.get_http2()
        self.__request_reslove = RequestReslove(routers, self.__error_cache, self.__config, self.__filters, sql, extend,
                                                loggers)
        thread_opts = self.__config.get_thread_pool_worker_num()
        if not thread_opts.get("single"):
            self.__thread_pool = ThreadPool(thread_opts["min"], thread_opts["max"], thread_opts["max_work_task"],
                                            self.__error_cache)
            if len(timer_tasks) > 0:
                self.__timer = Timer(int(time.time() * 1000), self.__thread_pool)
                for item in timer_tasks:
                    self.__timer.add_task(item)
                self.__thread_pool.add_task(self.__update_timer, ())
            self.__thread_pool.begin_work()

    def stop_work(self):
        self.__thread_pool.finish_work()

    def __update_timer(self):
        self.__timer.update(int(time.time() * 1000))
        self.__thread_pool.add_task(self.__update_timer, ())

    def set_loop(self, loop):
        self.__event_loop = loop

    def client_context(self, reader, writer):
        crt = ClientRequest(self, reader, writer, self.__event_loop, self.__config, self.__request_reslove,
                            self.__http2,
                            self.__error_cache)
        asyncio.run_coroutine_threadsafe(self.post_read(crt, reader, crt.alive_timeout), loop=self.__event_loop)

    async def post_read(self, crt, reader, timeout):
        try:
            data = (await reader.read(65536)) if timeout == -1 else (
                await asyncio.wait_for(reader.read(65536), loop=self.__event_loop, timeout=timeout))
            if len(data) == 0:
                raise asyncio.TimeoutError
            if self.__thread_pool:
                self.__thread_pool.add_task(crt.read_data, (data,))
            else:
                crt.read_data(data)
        except BrokenPipeError:
            crt.writer.close()
        except asyncio.exceptions.IncompleteReadError:
            crt.writer.close()
        except asyncio.TimeoutError:
            crt.writer.close()
        except ConnectionResetError:
            crt.writer.close()
        except Exception as e:
            self.__error_cache(e)

    def async_taker(self, method, *args):
        self.__thread_pool.add_task(method, args)

    def __error_cache(self, ex):
        if self.__main_logger:
            self.__main_logger.error(str.join("", traceback.format_exception(ex, value=ex, tb=ex.__traceback__)))
        else:
            traceback.print_exception(ex, value=ex, tb=ex.__traceback__)
