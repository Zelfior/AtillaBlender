
from pathlib import Path

package_path = Path(__file__).absolute().parent.parent

from src.io_elementary import IOOperation, io_short, io_float, io_bytes, io_int, io_str

"""

    The files present in files/unit_test_cs2_parsed were writen with a module version that could read/write all of fileS/cs2_parsed files.


"""

def test_read_float():
    file_path = package_path/"files/unit_test_cs2_parsed/float_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val = io_float(f, 0., IOOperation.READ)
        assert val == 12.5

def test_write_float():
    file_path = package_path/"files/unit_test_cs2_parsed/float_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_float(f, 12.5, IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val = io_float(f, 0., IOOperation.READ)
        assert val == 12.5


def test_read_float():
    file_path = package_path/"files/unit_test_cs2_parsed/float_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val = io_float(f, 0., IOOperation.READ)
        assert val == 12.5

def test_write_float():
    file_path = package_path/"files/unit_test_cs2_parsed/float_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_float(f, 12.5, IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val = io_float(f, 0., IOOperation.READ)
        assert val == 12.5


def test_read_int():
    file_path = package_path/"files/unit_test_cs2_parsed/int_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val = io_int(f, 0., IOOperation.READ)
        assert val == 12

def test_write_int():
    file_path = package_path/"files/unit_test_cs2_parsed/int_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_int(f, 12, IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val = io_int(f, 0., IOOperation.READ)
        assert val == 12


def test_read_short():
    file_path = package_path/"files/unit_test_cs2_parsed/short_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val = io_short(f, 0., IOOperation.READ)
        assert val == 12

def test_write_short():
    file_path = package_path/"files/unit_test_cs2_parsed/short_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_short(f, 12, IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val = io_short(f, 0., IOOperation.READ)
        assert val == 12


def test_read_bytes():
    file_path = package_path/"files/unit_test_cs2_parsed/bytes_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val, count = io_bytes(f, b"", 4, IOOperation.READ)
        assert count == 4
        assert val == b"\x00\x01\x12\x20"

def test_write_bytes():
    file_path = package_path/"files/unit_test_cs2_parsed/bytes_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val, count = io_bytes(f, b"\x00\x01\x12\x20", 4, IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val, count = io_bytes(f, b"", 4, IOOperation.READ)
        assert count == 4
        assert val == b"\x00\x01\x12\x20"


def test_read_str():
    file_path = package_path/"files/unit_test_cs2_parsed/str_12.cs2.parsed"
    
    with open(file_path, "rb") as f:
        val = io_str(f, "o"*11, IOOperation.READ)
        assert val == "hello world"

def test_write_str():
    file_path = package_path/"files/unit_test_cs2_parsed/str_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_str(f, "hello world", IOOperation.WRITE)

    with open(file_path, "rb") as f:
        val = io_str(f, "o"*11, IOOperation.READ)
        assert val == "hello world"



if __name__ == "__main__":
    test_write_float()