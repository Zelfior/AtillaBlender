
import glob
import os
from pathlib import Path
import sys
import struct

package_path = Path(__file__).absolute().parent.parent
sys.path.append((package_path/"src").name)

from cs2_parsed_io import Cs2File
from io_elementary import IOOperation


def run_test(file_path):

    if not os.path.exists(file_path):
        print(file_path)
        print(os.getcwd())
        print(os.listdir(os.getcwd()))
        
    input_path = Path(file_path)

    file_name = "garbage/"+input_path.name

    os.makedirs("garbage", exist_ok=True)

    cs2 = Cs2File.new_cs2file()

    has_ = True

    try:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=True)
    except struct.error:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=False)
        has_ = False
        

    cs2.read_write_file(file_name,   
                            IOOperation.WRITE, has_vfx=has_)

    with open(input_path.absolute(), "rb") as ref_file:
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


def test_30_30_10_tech():
    file_path = package_path/"files/cs2_parsed/30_30_10/30_30_10_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_arena_tech():
    file_path = package_path/"files/cs2_parsed/arena/arena_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_athens_acropolis_tech():
    file_path = package_path/"files/cs2_parsed/athens_acropolis/athens_acropolis_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_attila_cliff_01_tech():
    file_path = package_path/"files/cs2_parsed/attila_cliff_01/attila_cliff_01_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_banner01_tech():
    file_path = package_path/"files/cs2_parsed/banner01/banner01_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_barbarian_fort_curved_bastion_tech():
    file_path = package_path/"files/cs2_parsed/barbarian_fort_curved_bastion/barbarian_fort_curved_bastion_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_bridge_stone_1_tech():
    file_path = package_path/"files/cs2_parsed/bridge_stone_1/bridge_stone_1_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_crane_tech():
    file_path = package_path/"files/cs2_parsed/crane/crane_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_eastern_villa_house01_tech():
    file_path = package_path/"files/cs2_parsed/eastern_villa_house01/eastern_villa_house01_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_eastern_villa_stables_tech():
    file_path = package_path/"files/cs2_parsed/eastern_villa_stables/eastern_villa_stables_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_western_villa_house02_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_house02/western_villa_house02_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_western_villa_stables_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_stables/western_villa_stables_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_western_villa_straight01_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_straight01/western_villa_straight01_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_western_villa_straight02_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_straight02/western_villa_straight02_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_western_villa_tabernae_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_tabernae/western_villa_tabernae_tech.cs2.parsed"

    run_test(file_path.absolute())

if __name__ == "__main__":
    test_athens_acropolis_tech()