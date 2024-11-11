import math
from typing import List, Tuple
from src.cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, Polygon, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString, Vec2d, Vec3d, Face, FaceEdgeData, FaceEdge

try:
    from src.mesh_editor import MeshEditor
    from src.collection_manager import CollectionManager
except (ImportError, AttributeError):
    from src.fake_bpy import FakeMeshEditor as MeshEditor
    from src.fake_bpy import FakeCollectionManager as CollectionManager

from src.prefix_suffix import *

class BlenderToCs2:
    def __init__(self, cm = None, me = None):
        if cm is None:
            self.cm = CollectionManager()
        else:
            self.cm = cm
            
        if me is None:
            self.me = MeshEditor()
        else:
            self.me = me

    def make_transform_from_matrix_world(self, name:str) -> TransformMatrix:
        return self.me.read_transform_matrix(name)
        
    def read_bounding_box(self, name:str):
        print(f"Reading bounding box {name}")
        vertices, _, _, _ = self.me.make_py_data(name)

        min_x = min([v.x for v in vertices])
        min_y = min([v.y for v in vertices])
        min_z = min([v.z for v in vertices])
        max_x = max([v.x for v in vertices])
        max_y = max([v.y for v in vertices])
        max_z = max([v.z for v in vertices])

        return BoundingBox(min_x, min_y, min_z, max_x, max_y, max_z)
    
    def read_building_piece(self, name:str):
        print(f"Reading building piece {name}")

        objects = self.cm.get_collection_object_list(name)
        children = self.cm.get_collection_children(name)
        
        if len(objects) == 0:
            print(f"No placement found for piece {name}, using the origin")
            node = TechNode().new_tech_node()
            node.nodeName = UnicodeString(0, "")
            node.NodeTransform = TransformMatrix.new_transform_matrix()
        else:
            found_placement = False
            for o in objects:
                if o.endswith(object_bounding_piece_position_suffix):
                    found_placement = True
                    placement_name = o
                    break
            
            if found_placement:
                node = self.read_tech_node(placement_name)
                if placement_name == f"{name}{object_bounding_piece_position_suffix}":
                    node.nodeName = UnicodeString(0, "")
            else:
                node = TechNode.new_tech_node()
                node.nodeName = UnicodeString(0, "")
                node.NodeTransform = TransformMatrix.new_transform_matrix()

        destruct_list = []
        for i in range(len(children)):
            destruct_list.append(self.read_destruct(children[i], i))

        return BuildingPiece(pieceName=UnicodeString(len(name), name),
                             placementNode=node,
                             parentIndex=-1, 
                             destructCount=len(children),
                             destructs=destruct_list)
    

    def read_destruct(self, name:str, index:int):
        print(f"Reading destruct {name}")
        objects = self.cm.get_collection_object_list(name)
        children = self.cm.get_collection_children(name)
        
        found_collision3d = False
        for o in objects:
            if o.endswith(object_collision3d_suffix):
                found_collision3d = True
                collision3d_name = o
        if not found_collision3d:
            raise Exception
                
        collision3dMesh = self.read_collision3d(collision3d_name)

        bounding_box = self.read_bounding_box(collision3d_name)

        windows_data = []
        num_windows = 0
        doors_data = []
        num_doors = 0
        specials_data = []
        num_specials = 0
        lines_data = []
        num_lines = 0
        nogos_data = []
        num_nogos = 0
        pipes_data = []
        num_pipes = 0
        cannons_data = []
        num_cannons = 0
        arrow_emitters_data = []
        num_arrow_emitters = 0
        docking_points_data = []
        num_docking_points = 0
        soft_collisions_data = []
        num_soft_collisions = 0
        file_refs_data = []
        num_file_refs = 0
        eflines_data = []
        num_eflines = 0
        actionVFX_data = []
        num_actionVFX = 0
        att_actionVFX_data = []
        num_att_actionVFX = 0
        actionVFX2_data = []
        num_actionVFX2 = 0
        att_actionVFX2_data = []
        num_att_actionVFX2 = 0
        
        # print("EEEEEEEE", children)
        for collection_name in children:
            if collection_name.endswith(collection_windows_suffix):
                windows_objects = self.cm.get_collection_object_list(collection_name)
                num_windows = len(windows_objects)
                
                for i in range(num_windows):
                    windows_data.append(self.read_collision3d(windows_objects[i]))

            if collection_name.endswith(collection_doors_suffix):
                doors_objects = self.cm.get_collection_object_list(collection_name)
                num_doors = len(doors_objects)
                
                for i in range(num_doors):
                    doors_data.append(self.read_collision3d(doors_objects[i]))

            if collection_name.endswith(collection_specials_suffix):
                specials_objects = self.cm.get_collection_object_list(collection_name)
                num_specials = len(specials_objects)
                
                for i in range(num_specials):
                    specials_data.append(self.read_collision3d(specials_objects[i]))

            if collection_name.endswith(collection_lines_suffix):
                lines_objects = self.cm.get_collection_object_list(collection_name)
                num_lines = len(lines_objects)
                
                for i in range(num_lines):
                    lines_data.append(self.read_line(lines_objects[i], line_type=5))

            if collection_name.endswith(collection_nogos_suffix):
                nogos_objects = self.cm.get_collection_object_list(collection_name)
                num_nogos = len(nogos_objects)
                
                for i in range(num_nogos):
                    nogo_object = self.read_line(nogos_objects[i], swap_yz=False)

                    nogo_object = NogoZone(nogo_object.numVerts, [Vec2d(e.x, e.y) for e in nogo_object.dataVerts], [2 for _ in range(nogo_object.numVerts)])

                    nogos_data.append(nogo_object)

            if collection_name.endswith(collection_pipes_suffix):
                pipes_objects = self.cm.get_collection_object_list(collection_name)
                num_pipes = len(pipes_objects)
                
                for i in range(num_pipes):
                    pipes_data.append(self.read_line(pipes_objects[i]))       

            if collection_name.endswith(collection_cannons_suffix):
                cannons_objects = self.cm.get_collection_object_list(collection_name)
                num_cannons = len(cannons_objects)
                
                for i in range(num_cannons):
                    cannons_data.append(self.read_tech_node(cannons_objects[i]))

            if collection_name.endswith(collection_arrow_emitters_suffix):
                arrow_emitters_objects = self.cm.get_collection_object_list(collection_name)
                num_arrow_emitters = len(arrow_emitters_objects)
                
                for i in range(num_arrow_emitters):
                    arrow_emitters_data.append(self.read_tech_node(arrow_emitters_objects[i]))

            if collection_name.endswith(collection_docking_points_suffix):
                docking_points_objects = self.cm.get_collection_object_list(collection_name)
                num_docking_points = len(docking_points_objects)
                
                for i in range(num_docking_points):
                    docking_points_data.append(self.read_tech_node(docking_points_objects[i]))

            if collection_name.endswith(collection_soft_collisions_suffix):
                soft_collisions_objects = self.cm.get_collection_object_list(collection_name)
                num_soft_collisions = len(soft_collisions_objects)
                
                for i in range(num_soft_collisions):
                    soft_collisions_data.append(self.read_soft_collision(soft_collisions_objects[i]))

            if collection_name.endswith(collection_file_refs_suffix):
                file_refs_objects = self.cm.get_collection_object_list(collection_name)
                num_file_refs = len(file_refs_objects)
                
                for i in range(num_file_refs):
                    file_refs_data.append(self.read_file_ref(file_refs_objects[i], name))

            if collection_name.endswith(collection_eflines_suffix):
                eflines_objects = self.cm.get_collection_object_list(collection_name)
                num_eflines = len(eflines_objects)
                
                for i in range(num_eflines):
                    eflines_data.append(self.read_efline(eflines_objects[i]))

            if collection_name.endswith(collection_actionVFX_suffix):
                actionVFX_objects = self.cm.get_collection_object_list(collection_name)
                num_actionVFX = len(actionVFX_objects)
                
                for i in range(num_actionVFX):
                    actionVFX_data.append(self.read_tech_node(actionVFX_objects[i]))

            if collection_name.endswith(collection_att_actionVFX_suffix):
                att_actionVFX_objects = self.cm.get_collection_object_list(collection_name)
                num_att_actionVFX = len(att_actionVFX_objects)
                
                for i in range(num_att_actionVFX):
                    att_actionVFX_data.append(self.read_vfx_attachment(att_actionVFX_objects[i]))

            if collection_name.endswith(collection_actionVFX2_suffix):
                actionVFX2_objects = self.cm.get_collection_object_list(collection_name)
                num_actionVFX2 = len(actionVFX2_objects)
                
                for i in range(num_actionVFX2):
                    actionVFX2_data.append(self.read_tech_node(actionVFX2_objects[i]))

            if collection_name.endswith(collection_att_actionVFX2_suffix):
                att_actionVFX2_objects = self.cm.get_collection_object_list(collection_name)
                num_att_actionVFX2 = len(att_actionVFX2_objects)
                
                for i in range(num_att_actionVFX2):
                    att_actionVFX2_data.append(self.read_vfx_attachment(att_actionVFX2_objects[i]))
                    

        platform = self.read_platform(name)     

        return DestructLevel(
                        destructName=UnicodeString(len(name), name),
                        destructIndex=index,
                        collision3dMesh = collision3dMesh,
                        numWindows=num_windows,
                        collision3dWindows=windows_data,
                        numDoors=num_doors,
                        collision3dDoors=doors_data,
                        numSpecial=num_specials,
                        collision3dSpecial=specials_data,
                        numLines=num_lines,
                        dataLines=lines_data,
                        numNogo=num_nogos,
                        dataNogo=nogos_data,
                        numPipes=num_pipes,
                        dataPipes=pipes_data,
                        platforms = platform,
                        bounding_box = bounding_box,
                        numCannons=num_cannons,
                        dataCannons=cannons_data,
                        numArrowEmitters=num_arrow_emitters,
                        dataArrowEmitters=arrow_emitters_data,
                        numDockingPoints=num_docking_points,
                        dataDockingPoints=docking_points_data,
                        numSoftCollisions=num_soft_collisions,
                        dataSoftCollisions=soft_collisions_data,
                        numFileRefs=num_file_refs,
                        dataFileRefs=file_refs_data,
                        numEFLines=num_eflines,
                        dataEFLines=eflines_data,
                        numActionVFX=num_actionVFX,
                        ActionVFX=actionVFX_data,
                        numAttActionVFX=num_att_actionVFX,
                        attActionVFX=att_actionVFX_data,
                        numActionVFX2=num_actionVFX2,
                        ActionVFX2=actionVFX2_data,
                        numAttActionVFX2=num_att_actionVFX2,
                        attActionVFX2=att_actionVFX2_data)
    
    def make_cs2(self, version = 11):
        collection_name = self.cm.get_selected_collection()

        print(f"Making cs2 from collection {collection_name}")

        objects = self.cm.get_collection_object_list(collection_name)

        found_bounding_box = False
        for obj in objects:
            if obj.endswith(object_bounding_box_suffix):
                found_bounding_box = True
                bb_name = obj
        if not found_bounding_box:
            raise Exception(f"No bounding box found in collection {collection_name}")
        
        bb = self.read_bounding_box(bb_name)

        found_flag = False
        for obj in objects:
            if obj.endswith(object_flag_suffix):
                found_flag = True
                flag_name = obj
        if not found_flag:
            raise Exception(f"No bounding box found in collection {collection_name}")

        flag = self.read_tech_node(flag_name)
        
        if flag_name == f"{collection_name}{object_flag_suffix}":
            flag.nodeName.value = ""
            flag.nodeName.length = 0
        
        collection_children = self.cm.get_collection_children(collection_name)

        list_pieces = []

        for c in collection_children:
            list_pieces.append(self.read_building_piece(c))

        return Cs2File(version, bb, flag, len(collection_children), list_pieces)

    def read_tech_node(self, name:str) -> TechNode:
        #   Removing the integer added by blender
        new_name = name
        if "." in name and name.split(".")[-1].isdigit():
            new_name = ".".join(name.split(".")[:-1])
        return TechNode(UnicodeString(len(new_name), new_name), self.make_transform_from_matrix_world(name))
        

    def read_platform(self, collection_name:str):
        print(f"Reading platform for {collection_name}")
        objects = self.cm.get_collection_object_list(collection_name)

        platform_polygons = []
        ground_polygons = []

        len_platform = 0
        len_ground = 0

        for ob_ in objects:
            if ob_.endswith(object_platform_suffix):
                platform_data = self.me.make_py_data(ob_)
                platform_vertices = platform_data[0]
                platform_faces = platform_data[2]
                platform_normals = ground_data[3]
                len_platform = len(platform_faces)
                platform_polygons = [Polygon(platform_normals[f], 
                                             len(platform_faces[f]), 
                                             [platform_vertices[platform_faces[f][j]] for j in range(len(platform_faces[f]))],
                                             False) for f in range(len(platform_faces))]
                
            elif ob_.endswith(object_ground_suffix):
                ground_data = self.me.make_py_data(ob_)
                ground_vertices = ground_data[0]
                ground_faces = ground_data[2]
                ground_normals = ground_data[3]
                len_ground = len(ground_faces)

                ground_polygons = [Polygon(ground_normals[f], 
                                           len(ground_faces[f]), 
                                           [ground_vertices[ground_faces[f][j]] for j in range(len(ground_faces[f]))], 
                                           True) for f in range(len(ground_faces))]

        return Platform(numPolygons= len_platform + len_ground,
                        dataPolygons= platform_polygons + ground_polygons, 
                        some_int= -1)

    def read_file_ref(self, name:str, destruct_name:str) -> FileRef:  
        new_name = name
        if "." in name and name.split(".")[-1].isdigit():
            new_name = ".".join(name.split(".")[:-1])
    
        file_name = destruct_name+"_file:"+new_name
        return FileRef(UnicodeString(len(new_name), new_name), 
                       UnicodeString(len(file_name), file_name), 
                       self.make_transform_from_matrix_world(name),
                       150)

    def read_soft_collision(self, name:str):
        print(f"Reading soft collision {name}")
        
        bb = self.read_bounding_box(name)

        radius = 0.5*(bb.maxX - bb.minX)
        height = 0.5*(bb.maxZ - bb.minZ)

        center_x = 0.5*(bb.maxX + bb.minX)
        center_y = 0.5*(bb.maxY + bb.minY)
        center_z = 0.5*(bb.maxZ + bb.minZ)

        print(bb)

        matrix = TransformMatrix.new_transform_matrix()

        matrix.row0_col3 = center_x
        matrix.row1_col3 = center_y
        matrix.row2_col3 = center_z# - height
        
        new_name = name
        if "." in name and name.split(".")[-1].isdigit():
            new_name = ".".join(name.split(".")[:-1])

        return SoftCollision(
                                UnicodeString(len(new_name), new_name),
                                matrix,
                                0,
                                radius,
                                height
                            )
    
    def read_efline(self, name:str) -> EFLine:
        verts, edges, faces, _ = self.me.make_py_data(name)

        dir_x = verts[1].z - verts[0].z
        dir_y = 0
        dir_z = verts[0].x -verts[1].x

        norm_dir = math.sqrt(dir_x**2 + dir_z**2)

        #   God knows why these vectors are 0.15 inch long...
        dir_x *= -0.381/norm_dir
        dir_z *= -0.381/norm_dir

        return EFLine(lineName=UnicodeString(len(name), name), 
                        lineAction=1, 
                        lineStart=verts[0], 
                        lineEnd=verts[1], 
                        lineDir=Vec3d(dir_x, dir_y, dir_z), 
                        parentIndex=0)

    def read_collision3d(self, name:str) -> Collision3D:
        print(f"Reading collision 3d {name}")
        verts, edges, faces, _ = self.me.make_py_data(name)

        neighbour_face_01 = []
        neighbour_face_12 = []
        neighbour_face_20 = []

        for face in range(len(faces)):
            defined = 0
            index_0 = faces[face].vertIndex0
            index_1 = faces[face].vertIndex1
            index_2 = faces[face].vertIndex2

            for j in range(len(faces)):
                face_j_indexes = [faces[j].vertIndex0, faces[j].vertIndex1, faces[j].vertIndex2, ]
                if defined == 3:
                    break

                if j != face:
                    if index_0 in face_j_indexes and index_1 in face_j_indexes:
                        neighbour_face_01.append(j)
                    if index_2 in face_j_indexes and index_1 in face_j_indexes:
                        neighbour_face_12.append(j)
                    if index_0 in face_j_indexes and index_2 in face_j_indexes:
                        neighbour_face_20.append(j)

            if defined < 3:
                if len(neighbour_face_01) < face + 1:
                    neighbour_face_01.append(-1)
                if len(neighbour_face_12) < face + 1:
                    neighbour_face_12.append(-1)
                if len(neighbour_face_20) < face + 1:
                    neighbour_face_20.append(-1)

        return Collision3D(collisionName=UnicodeString(len(name), name),
                            nodeIndex=0,
                            unknown2=0,
                            numVerts=len(verts),
                            numFaces=len(faces),
                            dataVerts=verts,
                            dataFaces=[
                                            Face(
                                                    i, 
                                                    faces[i].vertIndex0,
                                                    faces[i].vertIndex1,
                                                    faces[i].vertIndex2,
                                                    FaceEdgeData(
                                                                    FaceEdge(faces[i].vertIndex0, faces[i].vertIndex1, i, 0, neighbour_face_01[i]),
                                                                    FaceEdge(faces[i].vertIndex1, faces[i].vertIndex2, i, 1, neighbour_face_12[i]),
                                                                    FaceEdge(faces[i].vertIndex2, faces[i].vertIndex0, i, 2, neighbour_face_20[i])
                                                                    ))
                                            for i in range(len(faces))
                                        ])

    def read_line(self, name:str, line_type=0, swap_yz = True) -> LineNode:
        print(f"Reading line {name}")
        verts, edges, faces, _ = self.me.make_py_data(name, swap_yz=swap_yz)
        return LineNode(UnicodeString(len(name), name),
                            len(verts),
                            verts,
                            line_type)

    def read_vfx_attachment(self, name:str):
        # TODO here
        return VFXAttachment(0, [])
