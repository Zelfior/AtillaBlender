from enum import Enum
import struct
from typing import IO, Any

# https://docs.micropython.org/en/latest/library/struct.html

debug = False

endian = ""

class IOOperation(Enum):
    READ=0
    WRITE=1

def io_short(io:IO, short_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(2)
        if debug:
            print(bytes_)
        val = int(struct.unpack(endian+'h', bytes_)[0])
        if debug:
            print(f"Read short {val}, at {io.tell()} : {hex(io.tell())}")
        return val
    else:
        if short_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(struct.pack("h", short_value))
        return short_value
    
def io_int(io:IO, int_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(4)
        if debug:
            print(bytes_)
        val = struct.unpack(endian+'l', bytes_)[0]
        if debug:
            print(f"Read int {val}, at {io.tell()} : {hex(io.tell())}")
        return val
    else:
        if int_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(struct.pack("l", int_value))
        return int_value

def io_float(io:IO, float_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        # print(hex(io.tell()))
        bytes_ = io.read(4)
        val = struct.unpack(endian+'f', bytes_)[0]
        if debug:
            print(f"Read short {val}, at {io.tell()} : {hex(io.tell())}")
        return val
    else:
        if float_value is None:
            raise ValueError("Requested to write a None float.")
        io.write(struct.pack("f", float_value))
        return float_value

def io_str(io:IO, string_value:str, operation:IOOperation):
    if operation == IOOperation.READ:
        length = len(string_value)
        if debug:
            print(f"Reading string of length {length}, at {io.tell()} : {hex(io.tell())}")
        string_value = ""

        for _ in range(length*2):
            byt = io_bytes(io, None, 1, operation)[0]
            if debug:
                print(f"byt found {byt}")
            if not byt in [b"\xFD",b"\xfb", b"\xFC"]:
                string_value += byt.decode(encoding='cp437')
        if debug:
            print(f"Reading string \"{string_value}\"")
        return string_value
    else:
        if string_value is None:
            raise ValueError("Requested to write a None string.")
        io.write(string_value.encode())
        return string_value
    
def io_bytes(io:IO, bytes_value:Any, bytes_count:int, operation:IOOperation):
    debug = True
    if operation == IOOperation.READ:
        if debug:
            print(f"Reading bytes of length {bytes_count}")
        val = io.read(bytes_count)
        if debug:
            print(f"Reading bytes {val}, at {io.tell()} : {hex(io.tell())}")
        return val, bytes_count
    else:
        if bytes_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(bytes_value)
        return bytes_value, bytes_count
    