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

def skip_bytes(io:IO, bytes_value:bytes, bytes_count:int, operation:IOOperation):
    trashed_bytes = io_bytes(io, bytes_value*bytes_count, bytes_count, operation)
    if not trashed_bytes == bytes_value*bytes_count:
        raise ValueError(f"Trashed bytes values is not null, found : {trashed_bytes}")
    
class SomeBytes():
    length:int
    value:Any
    def __init__(self, length:int, value:Any):
        self.length = length
        self.value = value
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.value, self.length = io_bytes(io, self.value, self.length, operation)
        if debug:
            print(f"bytes of length {self.length} : {self.value} at {hex(io.tell()-1)}")
    def __eq__(self, other:'SomeBytes'):
        return self.length == other.length and self.value == other.value

class UnicodeString():
    length:int
    value:str
    def __init__(self, length:int, value:str):
        self.length = length
        self.value = value
    def new_unicodestring():
        return UnicodeString(0, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.length = io_short(io, self.length, operation)

        if operation == IOOperation.READ:
            self.value = io_str(io, "o"*self.length, operation)
        else:
            self.value = io_str(io, self.value, operation)

        if debug:
            print(f"string of length {self.length} : {self.value}")
    def __eq__(self, other:'UnicodeString'):
        return self.length == other.length and self.value == other.value
    def __repr__(self,):
        return f"Unicode string of length {self.length} and value {self.value}"
    
class Vec2d():
    x:float
    y:float
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def new_vec2d():
        return Vec2d(None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.x = io_float(io, self.x, operation)
        self.y = io_float(io, self.y, operation)

        if debug:
            print(f"vec2d ({self.x}, {self.y})")
    def __eq__(self, other:'Vec2d'):
        return self.x == other.x and self.y == other.y
    
class Vec3d():
    x:float
    y:float
    z:float
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z
    def new_vec3d():
        return Vec3d(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11, inverse = True):
        self.x = io_float(io, self.x, operation)
        inverse = False
        if inverse:
            self.z = io_float(io, self.z, operation)
            self.y = io_float(io, self.y, operation)
        else:
            self.y = io_float(io, self.y, operation)
            self.z = io_float(io, self.z, operation)

        if debug:
            print(f"vec3d ({self.x}, {self.y}, {self.z})")
    def __eq__(self, other:'Vec3d'):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __repr__(self,):
        return f"Vec3d({self.x}, {self.y}, {self.z})"
    