This is the draft of a blender plug-in to import and export TotalWar Attila .cs2.parsed file.

It is tested on the 4.2 version of blender, but should work beyond 3.0 (maybe 2.8).

To generate the extension zip, from windows run make_zip.ps1. On other OS, zip the blender_module.py file along with the src folder.


## How to use?

The export will require to have a collection selected that contains the following (here it would be cs2_parsed_cs2_parsed_collection). A cs2 file consists of:

- one "flag" that tells the origin of the whole thing (it should be facultative for you guys, if absent, will be set to (0, 0, 0)). I will look for an object whose name ends with flag in the main collection.

- One bounding box: a cube, with or without face, technically, i could also make it facultative. I will look in the collection for an object that ends with bounding_box, if there are two, then it will insult you.

- a list of building Pieces, for each piece,

  - its origin (like the flag before),  facultative (if absent set to 0 0 0), 

  - a list of destruct. For each destruct:

    - a 3D mesh (the mesh), name should end with collision3d

    - a mesh representing the ground, name should end with ground

    - a mesh representing the platforms, name should end with platform

    - for each of the [doors, windows, lines, nogos, ...], a collection containing a serie of object of the same type, whose name ends with the object type (ex. doors)


## Known Issues

**.cs2.parsed** file parsing/writing known issues:

- Collision3D has a parent index that was not retro-engineered, can lead to improper behavior.
- SoftCollision also has an undefined number
- FileRef also has an undefined number
- EFLine has an parent index that was not retro-engineered, can lead to improper behavior.
- Both CS2 file and Destruct level can host data that were not retro-engineered.


