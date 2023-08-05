from Scarf.Protocol.HTTP import HTTPRequest, HTTPResponse
from asyncio import StreamWriter

import asyncio, types, math, random, gzip, sys

sys.setrecursionlimit(0xffff)


class HTTP2ConnectionState:
    OPEN = 0x0
    CONTINUE = 0x1
    RESLOVE_REQUEST = 0x2
    INVAILD = 0x3


class NodeItem:
    def __init__(self, prev, next, value):
        self.prev = prev
        self.next = next
        self.value = value


class Stream:
    def __init__(self, _id, window_size):
        self.state = None
        self.id = _id
        self.cache_data = b""
        self.weight = 0xff
        self.window_size = window_size
        self.frame_size = 0x4000
        self.monopoly = False
        self.http_request: HTTPRequest = None
        self.deep_id = 0
        self.open_stream = True
        self.result_frames = []


class HPACK:
    huffman_table = None
    static_table = [{
        ":authority": ""
    }, {
        ":method": "GET"
    }, {
        ":method": "POST"
    }, {
        ":path": "/"
    }, {
        ":path": "/index.html"
    }, {
        ":scheme": "http"
    }, {
        ":scheme": "https"
    }, {
        ":status": "200"
    }, {
        ":status": "204"
    }, {
        ":status": "206"
    }, {
        ":status": "304"
    }, {
        ":status": "400"
    }, {
        ":status": "404"
    }, {
        ":status": "500"
    }, {
        "accept-charset": ""
    }, {
        "accept-encoding": "gzip, deflate"
    }, {
        "accept-language": ""
    }, {
        "accept-ranges": ""
    }, {
        "accept": ""
    }, {
        "access-control-allow-origin": ""
    }, {
        "age": ""
    }, {
        "allow": ""
    }, {
        "authorization": ""
    }, {
        "cache-control": ""
    }, {
        "content-disposition": ""
    }, {
        "content-encoding": ""
    }, {
        "content-language": ""
    }, {
        "content-length": ""
    }, {
        "content-location": ""
    }, {
        "content-range": ""
    }, {
        "content-type": ""
    }, {
        "cookie": ""
    }, {
        "date": ""
    }, {
        "etag": ""
    }, {
        "expect": ""
    }, {
        "expires": ""
    }, {
        "from": ""
    }, {
        "host": ""
    }, {
        "if-match": ""
    }, {
        "if-modified-since": ""
    }, {
        "if-none-match": ""
    }, {
        "if-range": ""
    }, {
        "if-unmodified-since": ""
    }, {
        "last-modified": ""
    }, {
        "link": ""
    }, {
        "location": ""
    }, {
        "max-forwards": ""
    }, {
        "proxy-authenticate": ""
    }, {
        "proxy-authorization": ""
    }, {
        "range": ""
    }, {
        "referer": ""
    }, {
        "refresh": ""
    }, {
        "retry-after": ""
    }, {
        "server": ""
    }, {
        "set-cookie": ""
    }, {
        "strict-transport-security": ""
    }, {
        "transfer-encoding": ""
    }, {
        "user-agent": ""
    }, {
        "vary": ""
    }, {
        "via": ""
    }, {
        "www-authenticate": ""
    }]
    static_huffman_table = {
        "1111111111000": 0,
        "11111111111111111011000": 1,
        "1111111111111111111111100010": 2,
        "1111111111111111111111100011": 3,
        "1111111111111111111111100100": 4,
        "1111111111111111111111100101": 5,
        "1111111111111111111111100110": 6,
        "1111111111111111111111100111": 7,
        "1111111111111111111111101000": 8,
        "111111111111111111101010": 9,
        "111111111111111111111111111100": 10,
        "1111111111111111111111101001": 11,
        "1111111111111111111111101010": 12,
        "111111111111111111111111111101": 13,
        "1111111111111111111111101011": 14,
        "1111111111111111111111101100": 15,
        "1111111111111111111111101101": 16,
        "1111111111111111111111101110": 17,
        "1111111111111111111111101111": 18,
        "1111111111111111111111110000": 19,
        "1111111111111111111111110001": 20,
        "1111111111111111111111110010": 21,
        "111111111111111111111111111110": 22,
        "1111111111111111111111110011": 23,
        "1111111111111111111111110100": 24,
        "1111111111111111111111110101": 25,
        "1111111111111111111111110110": 26,
        "1111111111111111111111110111": 27,
        "1111111111111111111111111000": 28,
        "1111111111111111111111111001": 29,
        "1111111111111111111111111010": 30,
        "1111111111111111111111111011": 31,
        "010100": 32,
        "1111111000": 33,
        "1111111001": 34,
        "111111111010": 35,
        "1111111111001": 36,
        "010101": 37,
        "11111000": 38,
        "11111111010": 39,
        "1111111010": 40,
        "1111111011": 41,
        "11111001": 42,
        "11111111011": 43,
        "11111010": 44,
        "010110": 45,
        "010111": 46,
        "011000": 47,
        "00000": 48,
        "00001": 49,
        "00010": 50,
        "011001": 51,
        "011010": 52,
        "011011": 53,
        "011100": 54,
        "011101": 55,
        "011110": 56,
        "011111": 57,
        "1011100": 58,
        "11111011": 59,
        "111111111111100": 60,
        "100000": 61,
        "111111111011": 62,
        "1111111100": 63,
        "1111111111010": 64,
        "100001": 65,
        "1011101": 66,
        "1011110": 67,
        "1011111": 68,
        "1100000": 69,
        "1100001": 70,
        "1100010": 71,
        "1100011": 72,
        "1100100": 73,
        "1100101": 74,
        "1100110": 75,
        "1100111": 76,
        "1101000": 77,
        "1101001": 78,
        "1101010": 79,
        "1101011": 80,
        "1101100": 81,
        "1101101": 82,
        "1101110": 83,
        "1101111": 84,
        "1110000": 85,
        "1110001": 86,
        "1110010": 87,
        "11111100": 88,
        "1110011": 89,
        "11111101": 90,
        "1111111111011": 91,
        "1111111111111110000": 92,
        "1111111111100": 93,
        "11111111111100": 94,
        "100010": 95,
        "111111111111101": 96,
        "00011": 97,
        "100011": 98,
        "00100": 99,
        "100100": 100,
        "00101": 101,
        "100101": 102,
        "100110": 103,
        "100111": 104,
        "00110": 105,
        "1110100": 106,
        "1110101": 107,
        "101000": 108,
        "101001": 109,
        "101010": 110,
        "00111": 111,
        "101011": 112,
        "1110110": 113,
        "101100": 114,
        "01000": 115,
        "01001": 116,
        "101101": 117,
        "1110111": 118,
        "1111000": 119,
        "1111001": 120,
        "1111010": 121,
        "1111011": 122,
        "111111111111110": 123,
        "11111111100": 124,
        "11111111111101": 125,
        "1111111111101": 126,
        "1111111111111111111111111100": 127,
        "11111111111111100110": 128,
        "1111111111111111010010": 129,
        "11111111111111100111": 130,
        "11111111111111101000": 131,
        "1111111111111111010011": 132,
        "1111111111111111010100": 133,
        "1111111111111111010101": 134,
        "1011001": 135,
        "1111111111111111010110": 136,
        "11111111111111111011010": 137,
        "11111111111111111011011": 138,
        "11111111111111111011100": 139,
        "11111111111111111011101": 140,
        "11111111111111111011110": 141,
        "111111111111111111101011": 142,
        "11111111111111111011111": 143,
        "111111111111111111101100": 144,
        "111111111111111111101101": 145,
        "1111111111111111010111": 146,
        "11111111111111111100000": 147,
        "111111111111111111101110": 148,
        "11111111111111111100001": 149,
        "11111111111111111100010": 150,
        "11111111111111111100011": 151,
        "11111111111111111100100": 152,
        "111111111111111111100": 153,
        "1111111111111111011000": 154,
        "11111111111111111100101": 155,
        "1111111111111111011001": 156,
        "11111111111111111100110": 157,
        "11111111111111111100111": 158,
        "111111111111111111101111": 159,
        "1111111111111111011010": 160,
        "111111111111111111101": 161,
        "11111111111111111001": 162,
        "1111111111111111011011": 163,
        "1111111111111111011100": 164,
        "11111111111111111101000": 165,
        "11111111111111111101001": 166,
        "111111111111111111110": 167,
        "11111111111111111101010": 168,
        "1111111111111111011101": 169,
        "1111111111111111011110": 170,
        "111111111111111111110000": 171,
        "111111111111111111111": 172,
        "1111111111111111011111": 173,
        "11111111111111111101011": 174,
        "11111111111111111101100": 175,
        "111111111111111100000": 176,
        "111111111111111100001": 177,
        "1111111111111111100000": 178,
        "111111111111111100010": 179,
        "11111111111111111101101": 180,
        "1111111111111111100001": 181,
        "11111111111111111101110": 182,
        "11111111111111111101111": 183,
        "11111111111111111010": 184,
        "1111111111111111100010": 185,
        "1111111111111111100011": 186,
        "1111111111111111100100": 187,
        "11111111111111111110000": 188,
        "1111111111111111100101": 189,
        "1111111111111111100110": 190,
        "11111111111111111110001": 191,
        "11111111111111111111100000": 192,
        "11111111111111111111100001": 193,
        "11111111111111101011": 194,
        "1111111111111110001": 195,
        "1111111111111111100111": 196,
        "11111111111111111110010": 197,
        "1111111111111111101000": 198,
        "1111111111111111111101100": 199,
        "11111111111111111111100010": 200,
        "11111111111111111111100011": 201,
        "11111111111111111111100100": 202,
        "111111111111111111111011110": 203,
        "111111111111111111111011111": 204,
        "11111111111111111111100101": 205,
        "111111111111111111110001": 206,
        "1111111111111111111101101": 207,
        "1111111111111110010": 208,
        "111111111111111100011": 209,
        "11111111111111111111100110": 210,
        "111111111111111111111100000": 211,
        "111111111111111111111100001": 212,
        "11111111111111111111100111": 213,
        "111111111111111111111100010": 214,
        "111111111111111111110010": 215,
        "111111111111111100100": 216,
        "111111111111111100101": 217,
        "11111111111111111111101000": 218,
        "11111111111111111111101001": 219,
        "1111111111111111111111111101": 220,
        "111111111111111111111100011": 221,
        "111111111111111111111100100": 222,
        "111111111111111111111100101": 223,
        "11111111111111101100": 224,
        "111111111111111111110011": 225,
        "11111111111111101101": 226,
        "111111111111111100110": 227,
        "1111111111111111101001": 228,
        "111111111111111100111": 229,
        "111111111111111101000": 230,
        "11111111111111111110011": 231,
        "1111111111111111101010": 232,
        "1111111111111111101011": 233,
        "1111111111111111111101110": 234,
        "1111111111111111111101111": 235,
        "111111111111111111110100": 236,
        "111111111111111111110101": 237,
        "11111111111111111111101010": 238,
        "11111111111111111110100": 239,
        "11111111111111111111101011": 240,
        "111111111111111111111100110": 241,
        "11111111111111111111101100": 242,
        "11111111111111111111101101": 243,
        "111111111111111111111100111": 244,
        "111111111111111111111101000": 245,
        "111111111111111111111101001": 246,
        "111111111111111111111101010": 247,
        "111111111111111111111101011": 248,
        "1111111111111111111111111110": 249,
        "111111111111111111111101100": 250,
        "111111111111111111111101101": 251,
        "111111111111111111111101110": 252,
        "111111111111111111111101111": 253,
        "111111111111111111111110000": 254,
        "11111111111111111111101110": 255,
        "111111111111111111111111111111": 256
    }

    @staticmethod
    def init():
        init_node = NodeItem(None, [None, None], None)
        for item in HPACK.static_huffman_table.items():
            k, v = item
            _init_node = init_node
            for idx, num in enumerate(k):
                num = int(num)
                if num and not _init_node.next[1]:
                    _init_node.next[1] = NodeItem(_init_node, [None, None], None)
                elif num == 0 and not _init_node.next[0]:
                    _init_node.next[0] = NodeItem(_init_node, [None, None], None)
                _init_node = _init_node.next[num]
                if idx == len(k) - 1:
                    _init_node.value = v
        HPACK.huffman_table = init_node

    def __init__(self, size):
        if HPACK.huffman_table is None:
            HPACK.init()
        self.huffman_table = HPACK.huffman_table
        self.static_table = HPACK.static_table.copy()
        self.dynamic_table = []
        self.__dynamic_size = size
        self.dynamic_client_table = []
        self.__dynamic_client_size = size
        self.computed_dynamic(self.dynamic_client_table, size)

    def get_dynamic_size(self):
        return self.__dynamic_size

    def set_dynamic_size(self, val):
        self.__dynamic_size = val
        self.computed_dynamic(self.dynamic_table, val)

    dynamic_size = property(get_dynamic_size, set_dynamic_size)

    def computed_dynamic(self, table, size):
        length = 0
        idx = len(table) - 1
        while idx > -1:
            item = table[idx]
            key = tuple(item.keys())[0]
            if length + len(key) + len(item[key]) + 0x20 > size:
                while idx > -1:
                    table.pop()
                    idx -= 1
                return
            length += len(key) + len(item[key]) + 0x20
            idx -= 1

    def parse_headers(self, data):
        result = {}
        i = 0
        while i < len(data):
            if data[i] >> 5 == 1:
                size = data[i] & 0x1f
                if size == 0x1f:
                    size, i = self.more_repeat(i, data, 0x1f)
                else:
                    self.dynamic_size = size
            elif data[i] >> 7 == 1:
                _index = data[i] & 0x7f
                if _index == 0x7f:
                    _index, i = self.more_repeat(i, data, 0x7f)
                if _index - 1 < len(self.static_table):
                    result.update(self.static_table[_index - 1])
                else:
                    result.update(self.dynamic_table[_index - 1 - len(self.static_table)])
            elif data[i] >> 6 == 1 or data[i] >> 4 == 0 or data[i] >> 4 == 1:
                mode = data[i] >> 6 == 1
                _index = data[i] & (0x3f if mode else 0xf)
                if _index == 0:
                    key_len = data[i + 1] & 0x7f
                    key_huffman = data[i + 1] & 0x80
                    val_len = data[i + 2 + key_len] & 0x7f
                    val_huffman = data[i + 2 + key_len] & 0x80
                    if val_len == 0x7f:
                        val_len, i = self.more_repeat(i + 1, data, 0x7f)
                        i -= 1
                    key = str.join('', [chr(item) for item in (
                        self.huffman_match_str(data[i + 2: i + 2 + key_len]) if key_huffman else data[
                                                                                                 i + 2: i + 2 + key_len])])

                    value = str.join('', [chr(item) for item in (self.huffman_match_str(
                        data[i + 3 + key_len: i + 3 + key_len + val_len]) if val_huffman else data[
                                                                                              i + 3 + key_len: i + 3 + key_len + val_len])])

                    result[key] = value
                    i += (key_len + val_len + 2)
                else:
                    if _index == 0xf:
                        _index, i = self.more_repeat(i, data, 0xf)
                    elif _index == 0x3f:
                        _index, i = self.more_repeat(i, data, 0x3f)
                    if _index - 1 < len(self.static_table):
                        key = tuple(self.static_table[_index - 1].keys())[0]
                    else:
                        key = tuple(self.dynamic_table[_index - 1 - len(self.static_table)].keys())[0]

                    val_len = data[i + 1] & 0x7f
                    huffman = data[i + 1] & 0x80
                    if val_len == 0x7f:
                        val_len, i = self.more_repeat(i + 1, data, 0x7f)
                        i -= 1
                    result[key] = str.join('', [chr(item) for item in (
                        self.huffman_match_str(data[i + 2:i + 2 + val_len], key) if huffman else data[
                                                                                                 i + 2:i + 2 + val_len])])
                    i += (val_len + 1)
                if mode:
                    self.dynamic_table.insert(0, {str(key): str(result[key])})
            i += 1
        self.computed_dynamic(self.dynamic_table, self.dynamic_size)
        return result

    def header_translate(self, headers, table=None, basic=0):
        data = b""
        table = table if table else self.static_table
        for item in headers.items():
            k, v = item
            k = k.lower()
            v = str(v)
            value = 0
            _index = 0
            for i, _ in enumerate(table):
                _k = tuple(_.keys())[0]
                if k == _k and v == _[_k]:
                    value = 0x80
                    i += 1
                    if i < 0x7f:
                        value += (i + basic)
                        data += value.to_bytes(length=1, byteorder='big', signed=False)
                    else:
                        data += self.more_computed(value, (i + basic), 0x7f)
                    break
                elif k == _k and len(_[_k]) == 0:
                    i += 1
                    if i < 0x3f:
                        value = (0x40 + i + basic).to_bytes(length=1, byteorder='big', signed=False)
                    else:
                        value = self.more_computed(0x40, (i + basic), 0x3f)
                    if table is self.static_table:
                        self.dynamic_client_table.append({str(k): str(v)})
                    value += self.huffman_encode(v)
                    data += value
                    break
                if i == len(table) - 1 and table is self.static_table:
                    value = self.header_translate({k: v}, self.dynamic_client_table, len(self.static_table))
                    if len(value) == 0:
                        value = 0x10.to_bytes(length=1, byteorder='big', signed=False)
                        value += self.huffman_encode(k)
                        value += self.huffman_encode(v)
                    data += value
        self.computed_dynamic(self.dynamic_client_table, self.__dynamic_client_size)
        return data

    def more_computed(self, value, idx, basic_num):
        result = b""
        value += basic_num
        result += value.to_bytes(length=1, byteorder='big', signed=False)
        idx -= basic_num
        while idx >= 0x80:
            result += ((idx % 0x80) | 0x80).to_bytes(length=1, byteorder='big', signed=False)
            idx /= 0x80
        result += idx.to_bytes(length=1, byteorder='big', signed=False)
        return result

    def huffman_encode(self, _str):
        result = b''
        data = ""
        for item in _str:
            for huffman in self.static_huffman_table:
                if self.static_huffman_table[huffman] == ord(item):
                    data += huffman
        for _ in range(0, 8 - (len(data) % 8) if len(data) % 8 > 0 else 0):
            data += "1"
        for _idx in range(0, len(data) // 8 + 1 if len(data) % 8 > 0 else len(data) // 8):
            _data = data[_idx * 8:(_idx + 1) * 8]
            _idx = -1
            sum = 0
            while _idx >= -len(_data):
                sum += int(_data[_idx]) * pow(2, _idx * -1 - 1)
                _idx -= 1
            result += sum.to_bytes(length=1, byteorder='big', signed=False)
        result = (0x80 + len(result)).to_bytes(length=1, byteorder='big', signed=False) + result
        return result

    def huffman_match_str(self, data, k=None):
        result_str = []
        cache_node: NodeItem = self.huffman_table
        for item in data:
            _bin_list = []
            while item > 1:
                _bin_list.insert(0, item % 2)
                item = int(item / 2)
            _bin_list.insert(0, item)
            for _ in range(0, 8 - len(_bin_list)):
                _bin_list.insert(0, 0)
            for n, i in enumerate(_bin_list):
                cache_node = cache_node.next[i]
                if cache_node.value:
                    result_str.append(cache_node.value)
                    cache_node = self.huffman_table
        return result_str

    def more_repeat(self, i, data, basic_num):
        cache_data = []
        i += 1
        while data[i] & 0x80 > 0:
            cache_data.insert(0, data[i] & 0x7f)
            i += 1
        _sum = data[i] & 0x7f
        for item in cache_data:
            _sum = _sum * 0x80 + item
        _sum += basic_num
        return (_sum, i)


class HTTP2Context:
    class ErrorCodes:
        NO_ERROR = 0x0
        PROTOCOL_ERROR = 0x1
        INTERNAL_ERROR = 0x2
        FLOW_CONTROL_ERROR = 0x3
        SETTINGS_TIMEOUT = 0x4
        STREAM_CLOSED = 0x5
        FRAME_SIZE_ERROR = 0x6
        REFUSED_STREAM = 0x7
        CANCEL = 0x8
        COMPRESSION_ERROR = 0x9
        CONNECT_ERROR = 0xa
        ENHANCE_YOUR_CALM = 0xb
        INADEQUATE_SECURITY = 0xc
        HTTP_1_1_REQUIRED = 0xd
        error_table = {
            "0": "NO_ERROR",
            "1": "PROTOCOL_ERROR",
            "2": "INTERNAL_ERROR",
            "3": "FLOW_CONTROL_ERROR",
            "4": "SETTINGS_TIMEOUT",
            "5": "STREAM_CLOSED",
            "6": "FRAME_SIZE_ERROR",
            "7": "REFUSED_STREAM",
            "8": "CANCEL",
            "9": "COMPRESSION_ERROR",
            "10": "CONNECT_ERROR",
            "11": "ENHANCE_YOUR_CALM",
            "12": "INADEQUATE_SECURITY",
            "13": "HTTP_1_1_REQUIRED",
        }

    class FrameTypes:
        DATA = 0x0
        HEADERS = 0x1
        PRIORITY = 0x2
        RST_STREAM = 0x3
        SETTINGS = 0x4
        PUSH_PROMISE = 0x5
        PING = 0x6
        GOAWAY = 0x7
        WINDOW_UPDATE = 0x8
        CONTINUATION = 0x9

    settings_params = {
        "SETTINGS_HEADER_TABLE_SIZE": 0x1,
        "SETTINGS_ENABLE_PUSH": 0x2,
        "SETTINGS_MAX_CONCURRENT_STREAMS": 0x3,
        "SETTINGS_INITIAL_WINDOW_SIZE": 0x4,
        "SETTINGS_MAX_FRAME_SIZE": 0x5,
        "SETTINGS_MAX_HEADER_LIST_SIZE": 0x6,
    }

    user_setting_params = {
        "header_size": "SETTINGS_HEADER_TABLE_SIZE",
        "allow_push": "SETTINGS_ENABLE_PUSH",
        "max_stream": "SETTINGS_MAX_CONCURRENT_STREAMS",
        "init_window_size": "SETTINGS_INITIAL_WINDOW_SIZE",
        "max_frame_size": "SETTINGS_MAX_FRAME_SIZE",
        "header_list_size": "SETTINGS_MAX_HEADER_LIST_SIZE"
    }

    def __init__(self, loop, writer: StreamWriter, req: HTTPRequest, request_reslove,
                 project_config, config, error,
                 single: bool):
        self.__single = single
        self.__loop = loop
        self.__writer = writer
        self.__request_reslove = request_reslove
        self.__http_req = req
        self.__error = error
        self.__cache_data = b''
        self.__project_config = project_config
        self.__config = config
        self.__global_settings = [4096, 0, 100, 65535, 0x4000, None]
        self.__activate_frame = {}
        for item in self.__config.get("settings", {}).items():
            k, v = item
            k = HTTP2Context.user_setting_params.get(k)
            if k is None:
                continue
            k = HTTP2Context.settings_params[k]
            # "SETTINGS_HEADER_TABLE_SIZE": 0,
            # "SETTINGS_ENABLE_PUSH": 1,
            # "SETTINGS_MAX_CONCURRENT_STREAMS": 2,
            # "SETTINGS_INITIAL_WINDOW_SIZE": 3,
            # "SETTINGS_MAX_FRAME_SIZE": 4,
            # "SETTINGS_MAX_HEADER_LIST_SIZE": 5,
            self.__global_settings[k - 1] = v
        self.__streams = NodeItem(None, [], Stream(0, self.__global_settings[4]))
        self.__hpack = HPACK(4096)
        self.state = HTTP2ConnectionState.OPEN
        data = req.get_data()
        if data[0: data.find(b"\r\n\r\n")] == b"SM":
            data = data[data.find(b"\r\n\r\n") + 4:]
        else:
            self.state = HTTP2ConnectionState.INVAILD
        # frame format
        self.__length = 0
        self.__type = 0
        self.__flags = 0
        self.__r = 0
        self.__stream_identifier = 0
        self.__extern_data = b""
        self.reslove_data(data)

    def reslove_data(self, data):
        if len(self.__cache_data) > 0:
            data = self.__cache_data + data
            self.__cache_data = b""
        if len(data) < 9:
            self.state = HTTP2ConnectionState.CONTINUE
            self.__cache_data = data
            return
        self.__length = int.from_bytes(data[0:3], byteorder='big', signed=False)
        self.__type = data[3]
        self.__flags = data[4]
        self.__r = data[5] >> 7
        self.__stream_identifier = int.from_bytes(data[5:9], byteorder='big', signed=False) & 0x7fffffff
        stream = self.get_stream(self.__stream_identifier)
        if stream:
            stream = stream.value
            if not stream.open_stream:
                self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR,
                           "RST Stream Can Not Reslove Any Message Except PRIORITY")
                return
        elif self.__type != HTTP2Context.FrameTypes.HEADERS:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "Not Create Stream")
            return
        if len(data) < self.__length:
            self.__cache_data = data
            self.state = HTTP2ConnectionState.CONTINUE
            return
        if self.__length > 0:
            self.__extern_data = data[9: 9 + self.__length]

        if self.__type == HTTP2Context.FrameTypes.SETTINGS:
            self.parse_settings(self.__extern_data, self.__flags, self.__length, stream)
            self.__hpack.dynamic_size = self.__global_settings[0]
        elif self.__type == HTTP2Context.FrameTypes.WINDOW_UPDATE:
            self.parse_window_update(self.__extern_data, self.__length, stream)
        elif self.__type == HTTP2Context.FrameTypes.HEADERS:
            self.parse_headers(self.__extern_data, self.__flags, self.__stream_identifier, self.__length)
        elif self.__type == HTTP2Context.FrameTypes.DATA:
            self.parse_data(self.__extern_data, self.__flags, stream, self.__length)
        elif self.__type == HTTP2Context.FrameTypes.CONTINUATION:
            self.parse_continuation(self.__extern_data, self.__flags, stream)
        elif self.__type == HTTP2Context.FrameTypes.PING:
            self.control_async(self.write_data(self.ping(self.__extern_data, self.__stream_identifier)))
        elif self.__type == HTTP2Context.FrameTypes.GOAWAY:
            self.parse_goaway(self.__extern_data, self.__length)
        elif self.__type == HTTP2Context.FrameTypes.RST_STREAM:
            self.parse_rst_stream(self.__extern_data, stream)
        elif self.__type == HTTP2Context.FrameTypes.PRIORITY:
            self.parse_priority(self.__extern_data, stream)

        data = data[9 + self.__length:]
        if len(data) > 0 and self.state != HTTP2ConnectionState.INVAILD:
            self.reslove_data(data)
        else:
            self.flush()

    def flush(self):
        if self.__activate_frame.get("0"):
            stream = self.__activate_frame["0"]
            self.push_data(stream.result_frames, stream.window_size)
            self.__activate_frame["0"].result_frames.clear()
            del self.__activate_frame["0"]
        if len(self.__activate_frame.keys()):
            weight_pool = {}
            activate_pool = []
            _sum = 0
            for item in self.__activate_frame.values():
                weight_pool[str(item.id)] = []
                if not self.get_node_path(item.id, weight_pool[str(item.id)]):
                    continue
                weight = 0xff + 1
                if len(weight_pool[str(item.id)]) > 1:
                    for index, _ in enumerate(weight_pool[str(item.id)]):
                        sum_weight = sum((_.value.weight for _ in weight_pool[str(item.id)][index - 1].next))
                        weight *= int(_.value.weight / sum_weight) if sum_weight else 1
                        if weight < 5:
                            weight = 5
                            break
                        elif index < len(weight_pool[str(item.id)]) - 1:
                            weight -= 10
                activate_pool.append((weight, item))
                _sum += weight
            result = b""
            while len(activate_pool) > 0:
                verifity_sum = 0
                ran_num = random.randint(0, _sum)
                for idx, item in enumerate(activate_pool):
                    if ran_num < item[0] + verifity_sum:
                        if len(result) + len(item[1].result_frames) >= self.__global_settings[3]:
                            self.control_async(self.write_data(result))
                            result = b""
                        if len(item[1].result_frames) > 0:
                            result += item[1].result_frames.pop(0)
                        if len(item[1].result_frames) == 0:
                            _sum -= item[0]
                            activate_pool.pop(idx)
                            del self.__activate_frame[str(item[1].id)]
                        break
                    verifity_sum += item[0]
            if len(result) > 0:
                self.control_async(self.write_data(result))

    def get_node_path(self, _id, result, start_stream=None):
        start_stream = start_stream if start_stream else self.__streams.next
        for item in start_stream:
            if item.value.id == _id:
                result.append(item)
                return True
            elif len(item.next) > 0:
                if self.get_node_path(_id, result, item.next):
                    result.append(item)
                    return True
        return len(result) > 0

    def parse_priority(self, data, stream):
        if stream.id == 0:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "PRIORITY Frame StreamIdentifier Must > 0")
            return
        elif len(data) != 5:
            self.close(HTTP2Context.ErrorCodes.FRAME_SIZE_ERROR, "PRIORITY Frame Data Must Have Five Bits")
            return
        node = self.get_stream(stream.id)
        stream: Stream = node.value
        if stream:
            deep_id = int.from_bytes(data[0:4], byteorder='big', signed=False)
            e = deep_id & 0x80000000
            deep_id &= 0x7fffffff
            stream.monopoly = e
            if stream.deep_id != deep_id:
                node.prev.next.remove(node)
                self.get_stream(deep_id).next.append(node)
                stream.deep_id = deep_id
            stream.weight = data[4]

    def parse_goaway(self, data, length):
        # stream_id = int.from_bytes(data[0:3], byteorder='big', signed=False)
        error_code = int.from_bytes(data[3:7], byteorder='big', signed=False)
        plain = data[8: length].decode()
        self.__error(RuntimeError("HTTP2 Error Summary: %s , Error Plain: %s" % (
            HTTP2Context.ErrorCodes.error_table.get(str(error_code), ""), plain)))
        self.__writer.close()

    def parse_continuation(self, data, flags, stream):
        if not stream and (
                stream.state == HTTP2Context.FrameTypes.CONTINUATION or stream.state == HTTP2Context.FrameTypes.HEADERS or stream.state == HTTP2Context.FrameTypes.PUSH_PROMISE):
            self.close(HTTP2Context.ErrorCodes.INTERNAL_ERROR, "HTTP Request Is Not Vaild")
            return
        END_HEADERS = flags & 0x4
        if END_HEADERS and stream.state == HTTP2Context.FrameTypes.HEADERS:
            data = stream.cache_data + data
            try:
                headers = self.__hpack.parse_headers(data)
            except Exception as e:
                self.__error(e)
                self.close(HTTP2Context.ErrorCodes.COMPRESSION_ERROR, str(e))
                return
            self.__create_request(stream, headers)
            stream.state = None
            stream.cache_data = b""
        else:
            stream.cache_data += data

    def parse_data(self, data, flags, stream, length):
        if not stream:
            return
        elif length > self.__global_settings[4]:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "Frame Size Overflow Settings")
            return
        END_STREAM = flags & 0x1
        PADDED = flags & 0x8
        padded_length = 0
        start = 0

        if PADDED:
            padded_length = data[0]
            start += 1

        _data = data[start: length - padded_length]
        stream.http_request.parse_data(_data)

        if END_STREAM and stream.http_request.has_complate():
            self.__activate_frame[str(stream.id)] = stream
            self.__request_context(stream)
        else:
            self.close(HTTP2Context.ErrorCodes.INTERNAL_ERROR, "HTTP Request Is Not Vaild")

    def parse_headers(self, data, flags, stream_id, length):
        if stream_id > self.__global_settings[2]:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "Stream Quantity exceeds limit")
            return
        # END_STREAM = flags & 0x1
        END_HEADERS = flags & 0x4
        PADDED = flags & 0x8
        PRIORITY = flags & 0x20
        padded_length = 0
        start = 0

        if PADDED:
            padded_length = data[0]
            start += 1

        if PRIORITY:
            e = data[start] & 128
            deep_stream = int.from_bytes(data[0:4], byteorder='big', signed=False) & 0x7fffffff
            weight = data[start + 4] + 1
            stream: Stream = self.get_stream(stream_id, deep_stream).value
            stream.monopoly = bool(e)
            stream.deep_id = deep_stream
            stream.weight = weight
            stream.frame_size = self.__global_settings[4]
            start += 5
        else:
            stream: Stream = self.get_stream(stream_id, 0).value

        if END_HEADERS:
            header_fragment = stream.cache_data + data[start:length - padded_length]
            headers = self.__hpack.parse_headers(header_fragment)
            self.__create_request(stream, headers)
        else:
            stream.state = HTTP2Context.FrameTypes.HEADERS
            stream.cache_data += data[start:length - padded_length]

    def rst_stream(self, error: int, stream):
        self.control_async(self.write_data(self.http2_outer_(HTTP2Context.FrameTypes.RST_STREAM, 0, stream.id,
                                                             error.to_bytes(length=4, byteorder='big', signed=False))))

    def parse_rst_stream(self, data, stream: Stream):
        if len(data) < 4:
            self.close(HTTP2Context.ErrorCodes.FRAME_SIZE_ERROR, "RST_STREAM Has No Error Code")
            return
        elif stream.id == 0:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "RST_STREAM Stream Id Must > 0")
            return
        error = int.from_bytes(data[0:4], byteorder='big', signed=False)
        error = HTTP2Context.ErrorCodes.error_table.get(str(error), "")
        self.__error(RuntimeWarning("Stream ID: %i Error, Error summary: %s" % (stream.id, error)))
        stream.result_frames.clear()
        stream.open_stream = False

    def parse_window_update(self, data, length, stream: Stream):
        if length < 4:
            self.close(HTTP2Context.ErrorCodes.FRAME_SIZE_ERROR, "INVAILD Window Size")
            return

        window_size = int.from_bytes(data[0:4], byteorder='big', signed=False) & 0x7fffffff

        if window_size == 0:
            self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "WINDOW_UPDATE Frame Size Must > 0")
            return
        elif window_size > 0x7fffffff:
            if stream.id == 0:
                self.close(HTTP2Context.ErrorCodes.FLOW_CONTROL_ERROR, "WINDOW UPDATE Exceed Max Size")
            else:
                self.rst_stream(HTTP2Context.ErrorCodes.FLOW_CONTROL_ERROR, stream)
            return

        if self.__stream_identifier == 0:
            if self.__global_settings[0x3] is None:
                self.__global_settings[0x3] = window_size
            else:
                stream.result_frames.append(
                    self.http2_outer_(HTTP2Context.FrameTypes.WINDOW_UPDATE, 0, 0, self.window_update,
                                      self.__global_settings[0x3]))
                self.__activate_frame[str(stream.id)] = stream

        else:
            value: Stream = self.get_stream(self.__stream_identifier).value
            if value:
                value.window_size = window_size

    def parse_settings(self, data, flags, length, stream):
        if flags & 0x1:
            if length > 0:
                self.close(HTTP2Context.ErrorCodes.FRAME_SIZE_ERROR, "Settings ACK Frame Payload Length Must 0")
            return
        for item in range(0, length // 6):
            _data = data[item * 6: (item + 1) * 6]
            identfier = int.from_bytes(_data[0:2], byteorder='big', signed=False) - 1
            value = int.from_bytes(_data[2:6], byteorder='big', signed=False)
            if self.__global_settings[identfier] is None:
                if identfier == 1 and not (value == 0 or value == 1):
                    self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "SETTINGS_ENABLE_PUSH Must '0' Or '1'")
                    return
                elif identfier == 3 and value > 0x7fffffff:
                    self.close(HTTP2Context.ErrorCodes.FLOW_CONTROL_ERROR, "Flow Control Setting Error")
                    return
                elif identfier == 4 and (value > 0x7fffffff or value < 0xffffff):
                    self.close(HTTP2Context.ErrorCodes.PROTOCOL_ERROR, "Frame Size Setting Error")
                    return
                self.__global_settings[identfier] = value
        stream.result_frames.append(self.http2_outer_(HTTP2Context.FrameTypes.SETTINGS, 0, 0, self.settings))
        stream.result_frames.append(self.http2_outer_(HTTP2Context.FrameTypes.SETTINGS, 1, 0, self.settings, 1))
        self.__activate_frame[str(stream.id)] = stream

    def window_update(self, window_size: int):
        return (window_size & 0x7fffffff).to_bytes(length=4, byteorder='big', signed=False)

    def http2_outer_(self, tp, flags, stream_id, child_fn=None, *args):
        data = tp.to_bytes(length=1, byteorder='big', signed=False)
        data += flags.to_bytes(length=1, byteorder='big', signed=False)
        data += stream_id.to_bytes(length=4, byteorder='big', signed=False)
        if tp == HTTP2Context.FrameTypes.CONTINUATION:
            _data = data
            length = len(_data)
        elif tp == HTTP2Context.FrameTypes.DATA or tp == HTTP2Context.FrameTypes.GOAWAY or tp == HTTP2Context.FrameTypes.RST_STREAM:
            if isinstance(child_fn, int):
                length = child_fn
                _data = b""
            else:
                _data = child_fn
                length = len(_data)
        else:
            _data = child_fn(*args)
            length = len(_data)
        return length.to_bytes(length=3, byteorder='big', signed=False) + data + _data

    def data(self, data, stream: Stream, set_end_stream=True):
        result = b""
        times = math.ceil(len(data) / stream.frame_size)
        for num in range(0, times):
            _data = self.http2_outer_(HTTP2Context.FrameTypes.DATA, int(num == times - 1) and set_end_stream, stream.id,
                                      data[num * stream.frame_size: (num + 1) * stream.frame_size])
            if len(result) + len(_data) > stream.window_size:
                stream.result_frames.append(result)
                result = b""
            result += _data
        if len(result) > 0:
            stream.result_frames.append(result)

    def close(self, error, reason):
        data = self.__stream_identifier.to_bytes(length=4, byteorder='big', signed=False)
        data += error.to_bytes(length=4, byteorder='big', signed=False)
        data += reason.encode()
        self.control_async(self.write_data(self.http2_outer_(HTTP2Context.FrameTypes.GOAWAY, 0, 0, data)))
        self.state = HTTP2ConnectionState.INVAILD
        self.__writer.close()

    def ping(self, data, stream_id, ack=0x1):
        return self.http2_outer_(HTTP2Context.FrameTypes.PING, ack, stream_id, data)

    def headers(self, header_data, pri=False, e=0, deep_stream=0, weight=0):
        data = b""
        if pri:
            data += (deep_stream | (0x80000000 if e else 0)).to_bytes(length=4, byteorder='big', signed=False)
            data += (weight - 1).to_bytes(length=1, byteorder='big', signed=False)
        data += header_data
        return data

    def settings(self, ack=0):
        _data = b""
        if ack == 0:
            for index, item in enumerate(self.__global_settings):
                if item is None:
                    continue
                _data += (index + 1).to_bytes(length=2, byteorder='big', signed=False)
                _data += item.to_bytes(length=4, byteorder='big', signed=False)
        return _data

    def __create_request(self, stream, headers):
        stream.http_request = HTTPRequest(self.__writer, stream.id)
        path = headers.get(":path")
        method = headers.get(":method")
        if path and method:
            request_ = "%s %s HTTP/2.0\r\n" % (method.upper(), path)
            del headers[":path"]
            del headers[":method"]
            for k in headers:
                request_ += "%s: %s\r\n" % (k, headers[k])
            request_ += "\r\n"
            stream.http_request.parse_data(request_.encode())
            if stream.http_request.has_complate():
                self.__activate_frame[str(stream.id)] = stream
                self.__request_context(stream)
        else:
            self.state = HTTP2ConnectionState.INVAILD

    def send_header(self, header_data, stream, end_stream):
        fixed_length = 9
        flags = 0
        pri = False
        if stream.monopoly or stream.weight:
            fixed_length += 5
            flags |= 0x20
            pri = True

        if len(header_data) + fixed_length < stream.window_size:
            flags |= 0x4
            flags |= end_stream
            return [self.http2_outer_(HTTP2Context.FrameTypes.HEADERS, flags, stream.id, self.headers, header_data, pri,
                                      stream.monopoly, stream.deep_id, stream.weight)]
        else:
            result = []
            times = len(header_data) // (stream.window_size - fixed_length) + int(
                bool(len(header_data) % (stream.window_size - fixed_length)))
            for item in range(0, times):
                data = header_data[
                       item * (stream.window_size - fixed_length): (item + 1) * (stream.window_size - fixed_length)]
                if item == 0:
                    data = self.http2_outer_(HTTP2Context.FrameTypes.HEADERS, flags, stream.id, self.headers, data, pri,
                                             stream.monopoly, stream.deep_id, stream.weight)
                elif item == times - 1:
                    flags |= 0x4
                    flags |= end_stream

                data = self.http2_outer_(HTTP2Context.FrameTypes.CONTINUATION, flags, stream.id, data)
                result.append(data)
            return result

    def __request_context(self, stream):
        request = stream.http_request
        response = HTTPResponse(None, None, 2.0, self.__project_config, request.gzip_flag)
        reter = self.__request_reslove.router_reslove(request, response)
        next(reter)
        response_headers = {}
        response_headers[":status"] = str(response.code)
        response_headers.update(response.headers())
        result = response.result()
        tp = None
        if isinstance(result, types.GeneratorType):
            del response_headers["Transfer-Encoding"]
            tp = next(result)
            if tp is dict:
                response_headers["Content-Type"] = "application/json"
            elif tp is str:
                response_headers["Content-Type"] = "text/plain"
            elif tp is bytes:
                del response_headers["Content-Encoding"]
                response_headers["Content-Type"] = "application/octet-stream"
            else:
                response_headers["Content-Type"] = tp
        for source in self.send_header(self.__hpack.header_translate(response_headers), stream,
                                       0 if isinstance(result, types.GeneratorType) or len(result) > 0 else 1):
            stream.result_frames.append(source)
        if isinstance(result, tuple):
            path, start, size = result
            fd = open(path, "rb")
            times = math.ceil(size / stream.frame_size)
            for num in range(0, times):
                _size = size - num * stream.frame_size if num == times - 1 else stream.frame_size
                data = self.http2_outer_(HTTP2Context.FrameTypes.DATA, int(bool(num == times - 1)), stream.id, _size)
                fd.seek(start + num * stream.frame_size)
                data += fd.read(_size)
                stream.result_frames.append(data)
            fd.close()
        elif isinstance(result, types.GeneratorType):
            data = next(result)
            while True:
                end = next(result)
                if tp is dict or tp is str:
                    data = gzip.compress(data.encode())
                self.__activate_frame[str(stream.id)] = stream
                if end is None:
                    self.data(data, stream)
                    self.flush()
                    next(result)
                    break
                self.data(data, stream, False)
                self.flush()
                data = end
        else:
            self.data(result, stream)

        next(reter)
        stream.http_request = None

    def get_stream(self, _id, deep_stream_id=-1, start_stream=None) -> NodeItem:
        """
        Get Stream
        @param _id: Stream Id
        @deep_stream_id: Deep Stream Id - 0: most | >0: deep stream id | <0: No Create(Only Find)
        @weight: Stream Priority
        """
        if _id == 0:
            return self.__streams
        start_stream = start_stream if start_stream else self.__streams.next
        for item in start_stream:
            if item.value.id == _id:
                return item
            elif len(item.next) > 0:
                node_item = self.get_stream(_id, -1, item.next)
                if node_item:
                    return node_item
        node = None
        if deep_stream_id > 0:
            deep_stream = self.get_stream(deep_stream_id, -1, self.__streams.next)
            if deep_stream.value:
                node = NodeItem(deep_stream, [], Stream(_id, self.__global_settings[3]))
                deep_stream.next.append(node)
        elif deep_stream_id == 0:
            node = NodeItem(self.__streams, [], Stream(_id, self.__global_settings[3]))
            self.__streams.next.append(node)
        return node

    def push_data(self, data, window_size):
        result = b""
        for item in data:
            if len(result) + len(item) > window_size:
                self.control_async(self.write_data(result))
                result = b""
            result += item
        if len(result) > 0:
            self.control_async(self.write_data(result))

    def control_async(self, fn):
        waiter = asyncio.run_coroutine_threadsafe(fn, self.__loop)
        if self.__single:
            return waiter
        else:
            return waiter.result()

    async def write_data(self, data):
        try:
            self.__writer.write(data)
            await self.__writer.drain()
        except ConnectionResetError:
            return
