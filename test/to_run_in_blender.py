import sys

sys.path.insert(0, "F://Workspace/TotalWarModding")
sys.path.insert(0, "F://Workspace/TotalWarModding/test")

from test_blender_interfaces import *
from src.collection_manager import CollectionManager

for test_function in [test_30_30_10_tech]:
    CollectionManager().reset()
    test_function()
    