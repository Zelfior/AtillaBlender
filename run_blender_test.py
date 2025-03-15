import os

os.system("blender.exe  --background   --python test/to_run_in_blender.py > log_blender")

print("Blender execution finished.")