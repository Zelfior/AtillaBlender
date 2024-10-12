from enum import Enum
import struct
from typing import IO, Any

class IOOperation(Enum):
    READ=0
    WRITE=0

def io_short(io:IO, short_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return struct.unpack('i', io.read(2))
    else:
        if short_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write((short_value).to_bytes(2))
        return short_value
    
def io_int(io:IO, int_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return struct.unpack('i', io.read(4))
    else:
        if int_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write((int_value).to_bytes(4))
        return int_value

def io_float(io:IO, float_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return struct.unpack('f', io.read(4))
    else:
        if float_value is None:
            raise ValueError("Requested to write a None float.")
        io.write((float_value).to_bytes(4))
        return float_value

def io_str(io:IO, string_value:str, operation:IOOperation):
    if operation == IOOperation.READ:
        length = len(string_value)*4
        # return struct.unpack('s', io.read(length))
        return struct.unpack("B", io.read(length))[0].decode()
    else:
        if string_value is None:
            raise ValueError("Requested to write a None string.")
        io.write(string_value)
        return string_value
    
def io_bytes(io:IO, bytes_value:Any, bytes_count:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return io.read(bytes_count)
    else:
        if bytes_value is None:
            raise ValueError("Requested to write a None integer.")
        io.write(bytes_value)
        return bytes_value
    