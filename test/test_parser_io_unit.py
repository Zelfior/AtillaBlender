import os
import glob
from pathlib import Path

package_path = Path(__file__).absolute().parent.parent

from src.io_elementary import IOOperation, io_short, io_float, io_bytes, io_int, io_str

"""

    The files present in files/unit_test_cs2_parsed were writen with a module version that could read/write all of fileS/cs2_parsed files.


"""

os.makedirs("garbage", exist_ok=True)
os.makedirs("garbage/test_generated_files", exist_ok=True,)

files = glob.glob('garbage/test_generated_files/*')
for f in files:
    if os.path.isfile(f):
        os.remove(f)


def compare_binaries(input_path_reference, file_name):
    with open(input_path_reference.absolute(), "rb") as ref_file:
        with open(file_name, "rb") as output_file:
            i = 0
            past_position = -1
            while True:
                ref_byte = ref_file.read(1)
                output_byte = output_file.read(1)

                if ref_file.tell() == past_position:
                    break
                else:
                    past_position = ref_file.tell()

                if ref_byte == output_byte:
                    i += 1
                else:
                    assert False, f"Error at position {i} : {hex(i)}, ref {ref_byte}, found {output_byte}"
            
            print("Both files are identical")
            assert True


def test_read_float(file_path = package_path/"files/unit_test_cs2_parsed/float_12.cs2.parsed"): 
    with open(file_path, "rb") as f:
        val = io_float(f, 0., IOOperation.READ)
        assert val == 12.5

def test_write_float():
    file_path = package_path/"garbage/test_generated_files/float_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_float(f, 12.5, IOOperation.WRITE)

    test_read_float(file_path = file_path)


def test_read_int(file_path = package_path/"files/unit_test_cs2_parsed/int_12.cs2.parsed"):
    with open(file_path, "rb") as f:
        val = io_int(f, 0., IOOperation.READ)
        assert val == 12

def test_write_int():
    file_path = package_path/"garbage/test_generated_files/int_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_int(f, 12, IOOperation.WRITE)

    test_read_int(file_path = file_path)


def test_read_short(file_path = package_path/"files/unit_test_cs2_parsed/short_12.cs2.parsed"):
    with open(file_path, "rb") as f:
        val = io_short(f, 0., IOOperation.READ)
        assert val == 12

def test_write_short():
    file_path = package_path/"garbage/test_generated_files/short_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_short(f, 12, IOOperation.WRITE)

    test_read_short(file_path = file_path)


def test_read_bytes(file_path = package_path/"files/unit_test_cs2_parsed/bytes_12.cs2.parsed"):
    with open(file_path, "rb") as f:
        val, count = io_bytes(f, b"", 4, IOOperation.READ)
        assert count == 4
        assert val == b"\x00\x01\x12\x20"

def test_write_bytes():
    file_path = package_path/"garbage/test_generated_files/bytes_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val, count = io_bytes(f, b"\x00\x01\x12\x20", 4, IOOperation.WRITE)

    test_read_bytes(file_path = file_path)


def test_read_str(file_path = package_path/"files/unit_test_cs2_parsed/str_12.cs2.parsed"):
    with open(file_path, "rb") as f:
        val = io_str(f, "o"*11, IOOperation.READ)
        assert val == "hello world"

def test_write_str():
    file_path = package_path/"garbage/test_generated_files/str_12.cs2.parsed"

    with open(file_path, "wb") as f:
        val = io_str(f, "hello world", IOOperation.WRITE)

    test_read_str(file_path = file_path)



if __name__ == "__main__":
    test_write_float()