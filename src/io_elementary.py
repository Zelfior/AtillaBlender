from enum import Enum
import struct
from typing import IO, Any

# https://docs.micropython.org/en/latest/library/struct.html

debug = False

endian = ""

class UnknownData(Exception):
    pass

class IOOperation(Enum):
    READ=0
    WRITE=1

def io_short(io:IO, short_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(2)
        val = int(struct.unpack(endian+'h', bytes_)[0])
        if debug:
            print(f"Read short {val}, at {io.tell()} : {hex(io.tell())}\n")
        return val
    else:
        if short_value is None:
            raise ValueError("Requested to write a None short integer.")
        io.write(struct.pack("h", short_value))
        return short_value
    
def io_int(io:IO, int_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(4)
        val = struct.unpack(endian+'l', bytes_)[0]
        if debug:
            print(f"Read int {val}, at {io.tell()} : {hex(io.tell())}\n")
        return val
    else:
        if int_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(struct.pack("l", int_value))
        return int_value

def io_float(io:IO, float_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(4)
        val = struct.unpack(endian+'f', bytes_)[0]
        if debug:
            print(f"Read short {val}, at {io.tell()} : {hex(io.tell())}\n")
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
            print(f"Reading string of length {length}, at {io.tell()} : {hex(io.tell())}\n")
        string_value = ""

        for _ in range(length*2):
            byt = io_bytes(io, None, 1, operation)[0]
            if debug:
                print(f"byt found {byt}\n")
            if not byt in [b"\x00"]:#[b"\xFD",b"\xfb", b"\xFC", b"\x00"]:
                string_value += byt.decode(encoding='cp437')
        if debug:
            print(f"Reading string \"{string_value}\"\n")
        return str(string_value)
    else:
        if string_value is None:
            raise ValueError("Requested to write a None string.")
        str_to_write = "".join([e+"\00" for e in string_value])
        io.write(str_to_write.encode())
        return str(string_value)
    
def io_bytes(io:IO, bytes_value:Any, bytes_count:int, operation:IOOperation):
    if operation == IOOperation.READ:
        if debug:
            print(f"Reading bytes of length {bytes_count}\n")
        val = io.read(bytes_count)
        if debug:
            print(f"Reading bytes {val}, at {io.tell()} : {hex(io.tell())}\n")
        return val, bytes_count
    else:
        if bytes_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(bytes_value)
        return bytes_value, bytes_count
    