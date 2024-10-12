from enum import Enum
import struct
from typing import IO, Any

# https://docs.micropython.org/en/latest/library/struct.html

debug = False

endian = ""

class IOOperation(Enum):
    READ=0
    WRITE=0

def io_short(io:IO, short_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(2)
        if debug:
            print(bytes_)
        val = int(struct.unpack(endian+'h', bytes_)[0])
        if debug:
            print(f"Read short {val}")
        return val
    else:
        if short_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write((short_value).to_bytes(2))
        return short_value
    
def io_int(io:IO, int_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        bytes_ = io.read(4)
        if debug:
            print(bytes_)
        val = struct.unpack(endian+'l', bytes_)[0]
        if debug:
            print(f"Read int {val}")
        return val
    else:
        if int_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write((int_value).to_bytes(4))
        return int_value

def io_float(io:IO, float_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        val = struct.unpack(endian+'f', io.read(4))[0]
        if debug:
            print(f"Read short {val}")
        return val
    else:
        if float_value is None:
            raise ValueError("Requested to write a None float.")
        io.write((float_value).to_bytes(4))
        return float_value

def io_str(io:IO, string_value:str, operation:IOOperation):
    if operation == IOOperation.READ:
        length = len(string_value)
        if debug:
            print(f"Reading string of length {length}")
        string_value = ""

        for _ in range(length*2):
            byt = io_bytes(io, None, 1, operation)[0]
            print(f"byt found {byt}")
            if not byt in [b"0xFD", b"0xFC"]:
                string_value += byt.decode()
        # for i = 1 to len do
        # (
        #     str0 = readByte file #unsigned
        #     if str0 != 0xFD AND str0 != 0xFC do str += bit.intAsChar str0
        # )

        # if debug:
        #     print(f"Reading string of length {length}")
        # val = io.read(length).decode('utf-8')
        if debug:
            print(f"Reading string \"{string_value}\"")
        return string_value
    else:
        if string_value is None:
            raise ValueError("Requested to write a None string.")
        io.write(string_value)
        return string_value
    
def io_bytes(io:IO, bytes_value:Any, bytes_count:int, operation:IOOperation):
    if operation == IOOperation.READ:
        if debug:
            print(f"Reading bytes of length {bytes_count}")
        val = io.read(bytes_count)
        if debug:
            print(f"Reading bytes {val}")
        return val, bytes_count
    else:
        if bytes_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(bytes_value)
        return bytes_value, bytes_count
    