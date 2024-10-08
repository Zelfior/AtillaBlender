from enum import Enum
import struct
from typing import IO

class IOOperation(Enum):
    READ=0
    WRITE=0

def io_int(io:IO, int_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return struct.unpack('i', io.read(4))
    else:
        io.write(int_value)
        return int_value

def io_float(io:IO, float_value:int, operation:IOOperation):
    if operation == IOOperation.READ:
        return struct.unpack('f', io.read(4))
    else:
        io.write(float_value)
        return float_value

def io_str(io:IO, string_value:str, operation:IOOperation):
    if operation == IOOperation.READ:
        length = len(string_value)*4
        return struct.unpack('s', io.read(length))
    else:
        io.write(string_value)
        return string_value
    