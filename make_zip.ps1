Remove-Item atilla_blender.zip

# Create a zip file with the contents of C:\Stuff\
Compress-Archive -Path blender_module.py -DestinationPath atilla_blender.zip

# Add more files to the zip file
# (Existing files in the zip file with the same name are replaced)
Compress-Archive -Path src -Update -DestinationPath atilla_blender.zip
