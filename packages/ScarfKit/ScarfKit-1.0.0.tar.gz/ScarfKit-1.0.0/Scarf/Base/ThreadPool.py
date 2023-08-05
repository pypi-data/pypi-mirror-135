import threading, types, queue


class Actuator:
    """
    Thread Reslove Object
    """

    def __init__(self, function: types.FunctionType, arguments: tuple):
        self.arguments = arguments
        self.function = function

    def __call__(self, *args):
        self.function(*args)


class ThreadContext:
    def __init__(self, _id: int, revicer_: types.FunctionType, _queue: queue.Queue, error_: types.FunctionType):
        self.sync_flag = True
        self.__id = _id
        """ Sync Work Support """
        self.__revicer = revicer_
        """ Async Work Support """
        self.__queue = _queue
        self.__event = threading.Event()
        self.__error = error_
        self.__th = threading.Thread(target=self.__revicer, args=(_id,))
        self.__finish_flag = False
        self.__event.set()

    def reslove_context(self, destory_notify):
        timeout = -1 if destory_notify is None else 0.5
        alive_times = 6
        while not self.__finish_flag:
            self.__event.wait()
            if self.sync_flag:
                context = yield None
                if context is None:
                    continue
                result = context.function(*context.arguments)
                yield result
            try:
                context = self.__queue.get(block=timeout > -1, timeout=timeout)
                context(*context.arguments)
            except queue.Empty:
                if destory_notify is None:
                    self.__event.clear()
                    continue
                else:
                    alive_times -= 1
                    if alive_times == 0:
                        destory_notify(self.__id)
                        return
            except Exception as e:
                self.__error(e)

    def start_work(self):
        self.__th.start()

    def destroy(self):
        self.__finish_flag = True
        self.active()

    def active(self):
        self.__event.set()

    def sleep(self):
        self.__event.clear()


class ThreadPool:
    def __init__(self, min_size: int, max_size: int, max_work_num: int, error_: types.FunctionType):
        """
        Thread Pool Constructor
        :param min_size: Thread Pool Max Thread Size
        :param max_size: Thread Pool Min Thread Size
        :param error_: Thread Pool Reslove Error Callback
        """
        self.__min_size = int(min_size)
        self.__max_size = int(max_size)
        self.__max_work_num = int(max_work_num)
        self.__error_callback = error_
        self.__all_queue_work = False
        self.__operator_lock = threading.Lock()
        self.__recivers = [_id for _id in range(0, max_size)]
        self.__Queues = [{'source': queue.Queue(), 'id': _} for _ in range(0, min_size)]
        self.__threads = [
            (ThreadContext(_id, self.__get_revicer, self.__Queues[_id]["source"], error_) if _id < min_size else None)
            for _id in
            range(0, max_size)]

    def __get_revicer(self, _id: int):
        try:
            self.__recivers[_id] = self.__threads[_id].reslove_context(
                None if _id < self.__min_size else self.__destory_notify)
            self.__threads[_id].sync_flag = False
            self.__recivers[_id].send(None)
            self.__threads[_id].sleep()
        except StopIteration:
            return
        except Exception as e:
            print(str(e))

    def __comput_better(self):
        _queue = self.__Queues.copy()
        _queue.sort(key=lambda el: el["source"].qsize())
        return _queue[0]["id"]

    def __destory_notify(self,_id):
        self.__operator_lock.acquire()
        self.__Queues.remove(self.__Queues[_id])
        self.__threads[_id].destroy()
        self.__threads.remove(self.__threads[_id])
        self.__all_queue_work = False
        self.__operator_lock.release()

    def add_task(self, fn, args):
        index = self.__comput_better()
        if self.__Queues[index]["source"].qsize() >= self.__max_work_num and not self.__all_queue_work:
            self.__operator_lock.acquire()
            for _id, _th in enumerate(self.__threads):
                if _th is None:
                    self.__Queues.append({'source': queue.Queue(), 'id': _id})
                    self.__threads[_id] = ThreadContext(_id, self.__get_revicer, self.__Queues[_id]["source"],
                                                        self.__error_callback)
                    self.__threads[_id].start_work()
                    if _id == self.__max_size - 1:
                        self.__all_queue_work = True
                    break
            self.__operator_lock.release()
        self.__Queues[index]['source'].put(Actuator(fn, args))
        self.__threads[index].active()

    def add_task_sync_reslove(self, fn: types.MethodType, args: tuple):
        index = self.__comput_better()
        self.__threads[index].sync_flag = True
        self.__threads[index].active()
        result = self.__recivers[index].send(Actuator(fn, args))
        self.__recivers[index].send(None)
        self.__threads[index].sync_flag = False
        return result

    def begin_work(self):
        for _th in self.__threads:
            if _th is None:
                continue
            _th.start_work()

    def finish_work(self):
        for _th in self.__threads:
            if _th is None:
                continue
            _th.destroy()