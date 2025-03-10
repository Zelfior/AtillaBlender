
import os
from pathlib import Path
import struct

from src.blender_to_cs2 import BlenderToCs2
from src.cs2_to_blender import Cs2ToBlender

package_path = Path(__file__).absolute().parent.parent

from src.cs2_parsed_io import Cs2File
from src.io_elementary import IOOperation


def run_test(file_path, version = 11):

    if not os.path.exists(file_path):
        print(file_path)
        print(os.getcwd())
        print(os.listdir(os.getcwd()))
        
    input_path = Path(file_path)

    cs2 = Cs2File.new_cs2file()

    try:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, 
                                has_vfx=True)
        
    except struct.error:
        cs2 = Cs2File.new_cs2file()
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, 
                                has_vfx=False)
        
    c2b = Cs2ToBlender()
    c2b.make_cs2(cs2, "")

    b2c = BlenderToCs2(c2b.cm, c2b.me)
    cs2_output = b2c.make_cs2(version=version, collection_name="cs2_parsed__collection")

    assert cs2 == cs2_output, f"Test failed!, found \n\n{cs2}\n\n instead of \n\n{cs2_output}"

    print(f"Test on {file_path} passed!")
















def test_30_30_10_tech():
    file_path = package_path/"files/cs2_parsed/30_30_10/30_30_10_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_arena_tech():
    file_path = package_path/"files/cs2_parsed/arena/arena_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_athens_acropolis_tech():
    file_path = package_path/"files/cs2_parsed/athens_acropolis/athens_acropolis_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_attila_cliff_01_tech():
    file_path = package_path/"files/cs2_parsed/attila_cliff_01/attila_cliff_01_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_banner01_tech():
    file_path = package_path/"files/cs2_parsed/banner01/banner01_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_barbarian_fort_curved_bastion_tech():
    file_path = package_path/"files/cs2_parsed/barbarian_fort_curved_bastion/barbarian_fort_curved_bastion_tech.cs2.parsed"

    run_test(file_path.absolute())

def test_bridge_stone_1_tech():
    file_path = package_path/"files/cs2_parsed/bridge_stone_1/bridge_stone_1_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_crane_tech():
    file_path = package_path/"files/cs2_parsed/crane/crane_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_eastern_villa_house01_tech():
    file_path = package_path/"files/cs2_parsed/eastern_villa_house01/eastern_villa_house01_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_eastern_villa_stables_tech():
    file_path = package_path/"files/cs2_parsed/eastern_villa_stables/eastern_villa_stables_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_western_villa_house02_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_house02/western_villa_house02_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_western_villa_stables_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_stables/western_villa_stables_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_western_villa_straight01_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_straight01/western_villa_straight01_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_western_villa_straight02_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_straight02/western_villa_straight02_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

def test_western_villa_tabernae_tech():
    file_path = package_path/"files/cs2_parsed/western_villa_tabernae/western_villa_tabernae_tech.cs2.parsed"

    run_test(file_path.absolute(), version=13)

if __name__ == "__main__":
    # test_athens_acropolis_tech()
    ...