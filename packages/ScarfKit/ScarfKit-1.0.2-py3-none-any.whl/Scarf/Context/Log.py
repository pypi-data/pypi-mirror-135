from string import Template
import logging, sys, os, traceback

if sys.platform == "win32":
    import ctypes, sys

    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    FOREGROUND_BLACK = 0x00  # black.
    FOREGROUND_DARKBLUE = 0x01  # dark blue.
    FOREGROUND_DARKGREEN = 0x02  # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
    FOREGROUND_DARKRED = 0x04  # dark red.
    FOREGROUND_DARKPINK = 0x05  # dark pink.
    FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
    FOREGROUND_DARKWHITE = 0x07  # dark white.
    FOREGROUND_DARKGRAY = 0x08  # dark gray.
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    FOREGROUND_SKYBLUE = 0x0b  # skyblue.
    FOREGROUND_RED = 0x0c  # red.
    FOREGROUND_PINK = 0x0d  # pink.
    FOREGROUND_YELLOW = 0x0e  # yellow.
    FOREGROUND_WHITE = 0x0f  # white.

    # Windows CMD命令行 背景颜色定义 background colors
    BACKGROUND_BLUE = 0x10  # dark blue.
    BACKGROUND_GREEN = 0x20  # dark green.
    BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
    BACKGROUND_DARKRED = 0x40  # dark red.
    BACKGROUND_DARKPINK = 0x50  # dark pink.
    BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
    BACKGROUND_DARKWHITE = 0x70  # dark white.
    BACKGROUND_DARKGRAY = 0x80  # dark gray.
    BACKGROUND_BLUE = 0x90  # blue.
    BACKGROUND_GREEN = 0xa0  # green.
    BACKGROUND_SKYBLUE = 0xb0  # skyblue.
    BACKGROUND_RED = 0xc0  # red.
    BACKGROUND_PINK = 0xd0  # pink.
    BACKGROUND_YELLOW = 0xe0  # yellow.
    BACKGROUND_WHITE = 0xf0  # white.

    # get handle
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool


    def printWhite(mess):
        set_cmd_text_color(FOREGROUND_WHITE)
        sys.stdout.write(mess)
        resetColor()


    def printSkyBlue(mess):
        set_cmd_text_color(FOREGROUND_SKYBLUE)
        sys.stdout.write(mess)
        resetColor()


    def printRed(mess):
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess)
        resetColor()


    def printYellow(mess):
        set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess)
        resetColor()


    def printPink(mess):
        set_cmd_text_color(FOREGROUND_PINK)
        sys.stdout.write(mess)
        resetColor()


    # reset white
    def resetColor():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


class LogDeeper(logging.Handler):
    def __init__(self, filename, module_name, released,
                 format=f"%(asctime)s - $filename[line:%(lineno)d | %(funcName)s] - %(levelname)s: %(message)s"):
        super().__init__()
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        if not os.path.exists("./logs/" + module_name + ".log"):
            open("./logs/" + module_name + ".log", "w+").close()
        self.__released = released
        self.__module_name = module_name
        self.__file = filename
        self.__logger_handle = []
        self.__logger = logging.getLogger(module_name)
        self.__logger.setLevel(logging.DEBUG)
        self.__file_log_handle = logging.FileHandler("./logs/" + module_name + ".log", mode="a+", encoding='utf8')
        self.__file_log_handle.setLevel(logging.NOTSET)
        format = Template(format).substitute(filename=filename)
        self.__logger_format = logging.Formatter(format)
        self.__file_log_handle.setFormatter(logging.Formatter(format))
        self.__logger.addHandler(self.__file_log_handle)
        self.__logger.addHandler(self)
        self.warn = self.__logger.warning
        self.critical = self.__logger.critical
        self.error = self.__logger.error
        if self.__released:
            self.__logger.debug = lambda _: _
        else:
            self.debug = self.__logger.debug
        self.info = self.__logger.info

    def handle(self, record):
        if sys.platform == "win32":
            print_func = None
            if record.levelname == "INFO":
                print_func = printWhite
            elif record.levelname == "DEBUG":
                print_func = printSkyBlue
            elif record.levelname == "WARNING":
                print_func = printYellow
            elif record.levelname == "ERROR":
                print_func = printRed
            elif record.levelname == "CRITICAL":
                print_func = printPink
            else:
                print_func = print

            print_func(self.__logger_format.format(record) + "\n")
        else:
            levelColor = 37
            if record.levelname == "INFO":
                levelColor = 37
            elif record.levelname == "DEBUG":
                levelColor = 44
            elif record.levelname == "WARNING":
                levelColor = 33
            elif record.levelname == "ERROR":
                levelColor = 31
            elif record.levelname == "CRITICAL":
                levelColor = 35
            print("\033[%im %s \033[0m" % (levelColor, self.__logger_format.format(record),))
        for item in self.__logger_handle:
            item(record)

    def add_handle(self, handle):
        self.__logger_handle.append(handle)
