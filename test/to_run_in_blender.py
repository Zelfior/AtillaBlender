import sys
print("hey")
sys.path.insert(0, "F://Workspace/TotalWarModding")
sys.path.insert(0, "F://Workspace/TotalWarModding/test")

from test_blender_interfaces import *
from src.collection_manager import CollectionManager
from src.blender_to_cs2 import BlenderToCs2
from src.cs2_parsed_io import *
from src.cs2_to_blender import Cs2ToBlender
from src.mesh_editor import MeshEditor

from importlib import reload 

# CollectionManager = reload(CollectionManager)
# BlenderToCs2 = reload(BlenderToCs2)
# Cs2ToBlender = reload(Cs2ToBlender)
# MeshEditor = reload(MeshEditor)

for test_function in [test_30_30_10_tech,
                        test_arena_tech,
                        test_athens_acropolis_tech,
                        test_attila_cliff_01_tech,
                        test_banner01_tech,
                        test_barbarian_fort_curved_bastion_tech,
                        test_bridge_stone_1_tech,
                        test_crane_tech,
                        test_eastern_villa_house01_tech,
                        test_eastern_villa_stables_tech,
                        test_western_villa_house02_tech,
                        test_western_villa_stables_tech,
                        test_western_villa_straight01_tech,
                        test_western_villa_straight02_tech,
                        test_western_villa_tabernae_tech]:
    CollectionManager().reset()
    test_function()
    



    