from Scarf.Base.ThreadPool import ThreadPool

import queue, time, threading


class TaskParamter:
    def __init__(self, interval, times, callback, _this=None, user_arg=None):
        self.interval = interval
        self.cycle = interval
        self.times = times
        self.__callback = callback
        self.__user_arg = user_arg
        self.__this = _this
        self._last_time = 0

    def __call__(self, *args, **kwargs):
        return self.__callback(self.__this, *args, **kwargs)

    def call(self, *args, **kwargs):
        return self.__callback(self.__this, *args, self.__user_arg)


class TaskItem:
    def __init__(self, callback, arg, thread_pool: ThreadPool = None):
        self.callback = callback
        self.arg = arg
        self.__thread_pool = thread_pool

    def __call__(self, *args):
        if self.__thread_pool:
            self.__thread_pool.add_task(self.callback, tuple([self.arg] + [item for item in args]))
        else:
            self.callback(self.arg, *args)


class Timer:
    def __init__(self, _init_time, thread_pool: ThreadPool = None):
        self.__work_queue = [queue.Queue() for item in range(0, 0x3e9)]
        self.__wait_queue = []
        self.__last_time = _init_time
        self.__last_index = 0
        self.__time_instance = 0
        self.__instantaneous_time = 0
        self.__thread_pool = thread_pool
        self.__lock = threading.Lock()

    def __reslove(self, task_item, _time):
        flag = task_item.call(_time)
        if task_item.times > 1 and flag:
            task_item.times -= 1
        elif task_item.times == 1 or not flag:
            return
        task_item.interval += task_item.cycle
        self.add_task(task_item)

    def add_task(self, item: TaskParamter):
        if item.interval < 0x3e9:
            self.__work_queue[item.interval].put_nowait(TaskItem(self.__reslove, item))
        else:
            self.__wait_queue.append(item)

    def __update_wait(self, instance):
        for item in tuple(self.__wait_queue):
            item.interval -= instance
            if item.interval < 0x3e9:
                self.add_task(item)
                self.__wait_queue.remove(item)

    def __emit_queue(self, start, end, *args):
        """
        emit queue start to end
        """
        for _idx in range(start, end + 1):
            if not self.__work_queue[_idx].empty():
                self.__work_queue[_idx].get_nowait()(*args)

    def update(self, _time):
        _instance = _time - self.__last_time
        if _instance > 0x3e8:
            while _instance > 0x3e8:
                self.__emit_queue(self.__last_index, 0x3e8, _time)
                self.__emit_queue(0, self.__last_index, _time)
                self.__last_time = _time
                self.__update_wait(0x3e8)
                _instance -= 0x3e8
            start = 0
            end = _instance
        else:
            start = self.__last_index
            end = _instance

        self.__emit_queue(start, end, _time)
        self.__last_index = end
