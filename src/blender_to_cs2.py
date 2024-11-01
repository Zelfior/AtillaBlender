from typing import List, Tuple
from src.cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString, Vec2d, Vec3d, Face, FaceEdgeData, FaceEdge

import bpy

from src.mesh_editor import MeshEditor

from src.collection_manager import CollectionManager

class Cs2ToBlender:
    def __init__(self, ):
        self.cm = CollectionManager()
        self.me = MeshEditor()

    def make_transform_from_matrix_world(self, name:str) -> TransformMatrix:
        return TransformMatrix(**[e for col in bpy.data.objects[name].matrix_world for e in col])
        
    def read_bounding_box(self, name:str):
        print(f"Reading bounding box {name}")
        vertices, _, _ = self.me.make_py_data(name)

        min_x = min([v[0] for v in vertices])
        min_y = min([v[0] for v in vertices])
        min_z = min([v[1] for v in vertices])
        max_x = max([v[1] for v in vertices])
        max_y = max([v[2] for v in vertices])
        max_z = max([v[2] for v in vertices])

        return BoundingBox(min_x, min_y, min_z, max_x, max_y, max_z)
    
    # def make_building_piece(self, name:str, collection_name:str, bp:BuildingPiece, transform_matrixes:List[TransformMatrix]):
    #     print(f"Making building piece {bp.pieceName.value}")
    #     self.cm.new_collection(bp.pieceName.value, collection_name)
        
    #     if bp.placementNode.nodeName.value == "":
    #         bp.placementNode.nodeName.value = collection_name+"_building_piece_placement"
    #     self.make_tech_node(collection_name, bp.placementNode, transform_matrixes)
    #     transform_matrix = bp.placementNode.NodeTransform
        
    #     for d in range(bp.destructCount):
    #         self.make_destruct(name, bp.pieceName.value, bp.destructs[d], transform_matrixes + [transform_matrix])

    # def make_destruct(self, name:str, collection_name:str, destruct:DestructLevel, transform_matrixes:List[TransformMatrix]):
    #     print(f"Making destruct {destruct.destructName.value}")
    #     self.cm.new_collection(destruct.destructName.value, collection_name)
        
    #     self.make_collision3d(destruct.destructName.value, destruct.collision3dMesh, transform_matrixes)
        
    #     if destruct.numWindows > 0:
    #         window_collection = destruct.destructName.value+"_windows"
    #         self.cm.new_collection(window_collection, destruct.destructName.value)
            
    #     if destruct.numDoors > 0:
    #         door_collection = destruct.destructName.value+"_doors"
    #         self.cm.new_collection(door_collection, destruct.destructName.value)
            
    #     if destruct.numSpecial > 0:
    #         special_collection = destruct.destructName.value+"_specials"
    #         self.cm.new_collection(special_collection, destruct.destructName.value)
            
    #     if destruct.numLines > 0:
    #         line_collection = destruct.destructName.value+"_lines"
    #         self.cm.new_collection(line_collection, destruct.destructName.value)
            
    #     if destruct.numNogo > 0:
    #         nogo_collection = destruct.destructName.value+"_nogos"
    #         self.cm.new_collection(nogo_collection, destruct.destructName.value)
                    
    #     if destruct.numPipes > 0:
    #         pipes_collection = destruct.destructName.value + "_pipes"
    #         self.cm.new_collection(pipes_collection, destruct.destructName.value)

    #     if destruct.numCannons > 0:
    #         cannons_collection = destruct.destructName.value + "_cannons"
    #         self.cm.new_collection(cannons_collection, destruct.destructName.value)

    #     if destruct.numArrowEmitters > 0:
    #         arrow_emitters_collection = destruct.destructName.value + "_arrow_emitters"
    #         self.cm.new_collection(arrow_emitters_collection, destruct.destructName.value)

    #     if destruct.numDockingPoints > 0:
    #         docking_points_collection = destruct.destructName.value + "_docking_points"
    #         self.cm.new_collection(docking_points_collection, destruct.destructName.value)

    #     if destruct.numSoftCollisions > 0:
    #         soft_collisions_collection = destruct.destructName.value + "_soft_collisions"
    #         self.cm.new_collection(soft_collisions_collection, destruct.destructName.value)

    #     if destruct.numFileRefs > 0:
    #         file_refs_collection = destruct.destructName.value + "_file_refs"
    #         self.cm.new_collection(file_refs_collection, destruct.destructName.value)

    #     if destruct.numEFLines > 0:
    #         eflines_collection = destruct.destructName.value + "_eflines"
    #         self.cm.new_collection(eflines_collection, destruct.destructName.value)

    #     if destruct.numActionVFX > 0:
    #         actionVFX_collection = destruct.destructName.value + "_actionVFX"
    #         self.cm.new_collection(actionVFX_collection, destruct.destructName.value)

    #     if destruct.numAttActionVFX > 0:
    #         att_actionVFX_collection = destruct.destructName.value + "_att_actionVFX"
    #         self.cm.new_collection(att_actionVFX_collection, destruct.destructName.value)

    #     for i in range(destruct.numWindows):
    #         self.make_collision3d(window_collection, destruct.collision3dWindows[i], transform_matrixes)
        
    #     for i in range(destruct.numDoors):
    #         self.make_collision3d(door_collection, destruct.collision3dDoors[i], transform_matrixes)
        
    #     for i in range(destruct.numSpecial):
    #         self.make_collision3d(special_collection, destruct.collision3dSpecial[i], transform_matrixes)
        
    #     for i in range(destruct.numLines):
    #         self.make_line(line_collection, destruct.dataLines[i], transform_matrixes, closed=True)
        
    #     for i in range(destruct.numNogo):
    #         nogo = destruct.dataNogo[i]

    #         fake_line = LineNode(UnicodeString(len(f"nogo_{i}"), f"nogo_{i}"), 
    #                                 len(nogo.dataLines), 
    #                                 [(nogo.dataLines[j].x, nogo.dataLines[j].y, 0.) for j in range(len(nogo.dataLines))]
    #                                 , 0)
            
    #         self.make_line(nogo_collection, fake_line, transform_matrixes, closed=True, swap_yz = False)

    #     for i in range(destruct.numPipes):
    #         self.make_line(pipes_collection, destruct.dataPipes[i], transform_matrixes, closed = False)

    #     self.make_platform(destruct.destructName.value, destruct.platforms, transform_matrixes)

    #     for i in range(destruct.numCannons):
    #         self.make_tech_node(cannons_collection, destruct.dataCannons[i], transform_matrixes)

    #     for i in range(destruct.numArrowEmitters):
    #         self.make_tech_node(arrow_emitters_collection, destruct.dataArrowEmitters[i], transform_matrixes)

    #     for i in range(destruct.numDockingPoints):
    #         self.make_tech_node(docking_points_collection, destruct.dataDockingPoints[i], transform_matrixes)

    #     for i in range(destruct.numSoftCollisions):
    #         self.make_soft_collision(soft_collisions_collection, destruct.dataSoftCollisions[i], transform_matrixes)
            
    #     for i in range(destruct.numFileRefs):
    #         self.make_file_ref(file_refs_collection, destruct.dataFileRefs[i], transform_matrixes)

    #     for i in range(destruct.numEFLines):
    #         self.make_efline(eflines_collection, destruct.dataEFLines[i], transform_matrixes)

    #     for i in range(destruct.numActionVFX):
    #         self.make_tech_node(actionVFX_collection, destruct.ActionVFX[i], transform_matrixes)

    #     for i in range(destruct.numAttActionVFX):
    #         self.make_vfx_attachment(att_actionVFX_collection, destruct.attActionVFX[i], transform_matrixes)

    # def make_cs2(self, cs2:Cs2File, name:str):
    #     print(f"Making cs2 {name}")
    #     self.cm.new_collection(f"cs2_parsed_{name}_collection", "")

    #     collection_name = f"cs2_parsed_{name}_collection"
    #     self.make_bounding_box(name, collection_name, cs2.bbox)

    #     if cs2.flag.nodeName.value == "":
    #         cs2.flag.nodeName.value = collection_name+"_flag"
    #     self.make_tech_node(collection_name, cs2.flag, [])
    #     transform_matrix = cs2.flag.NodeTransform
        
    #     for p in range(cs2.piece_count):
    #         self.make_building_piece(name, collection_name, cs2.building_pieces[p], [transform_matrix])

    def read_tech_node(self, name:str) -> TechNode:
        return TechNode(UnicodeString(len(name), name), self.make_transform_from_matrix_world(name))
        

    # def make_platform(self, collection_name:str, p:Platform, transform_matrixes:List[TransformMatrix]):
    #     print(f"Making platform for {collection_name}")
    #     vert_count_platform = 0
    #     vert_count_ground = 0

    #     platform_verts: List = []
    #     ground_verts: List = []

    #     platform_faces: List = []
    #     ground_faces: List = []

    #     for pol in p.dataPolygons:
    #         if pol.isPlatformGround:
    #             ground_verts += pol.dataVerts
    #             ground_faces += [[vert_count_ground+i for i in range(len(pol.dataVerts))]]

    #             vert_count_ground = len(ground_verts) 

    #         else:
    #             platform_verts += pol.dataVerts
    #             platform_faces += [[vert_count_platform+i for i in range(len(pol.dataVerts))]]

    #             vert_count_platform = len(platform_verts) 

    #     if len(platform_verts) > 0:
    #         ob = self.me.make_object_from_data(collection_name+"_platform", platform_verts, [], platform_faces)
    #         self.cm.move_object_to_collection(ob, collection_name)

    #         # self.apply_transform_matrixes(collection_name+"_platform", transform_matrixes)

    #     if len(ground_verts) > 0:
    #         ob = self.me.make_object_from_data(collection_name+"_ground", ground_verts, [], ground_faces)
    #         self.cm.move_object_to_collection(ob, collection_name)

    #         # self.apply_transform_matrixes(collection_name+"_ground", transform_matrixes)
            
    #     # TODO: "revert normals?"

    def read_file_ref(self, name:str) -> FileRef:  
        return FileRef(UnicodeString(len(name), name), UnicodeString(len(name), name), self.make_transform_from_matrix_world(name))

    def read_soft_collision(self, name:str):
        print(f"Reading soft collision {name}")
        
        bb = self.read_bounding_box(name)

        radius = 0.5*(bb.maxX - bb.minX)
        height = 0.5*(bb.maxZ - bb.minZ)

        matrix = self.me.read_transform_matrix(name)

        matrix.row1_col2 -= 0.5*height
        
        return SoftCollision(
                                UnicodeString(len(name), name),
                                matrix,
                                0,
                                radius,
                                height
                            )
    
    def read_efline(self, name:str) -> EFLine:
        verts, edges, faces = self.me.make_py_data(name)
        return EFLine(lineName=UnicodeString(len(name), name), 
                        lineAction=0, 
                        lineStart=Vec3d(**verts[0]), 
                        lineEnd=Vec3d(**verts[1]), 
                        lineDir=Vec3d(**[verts[1][i] - verts[0][i] for i in range(3)]), 
                        parentIndex=0)

    def read_collision3d(self, name:str) -> Collision3D:
        print(f"Reading collision 3d {name}")
        verts, edges, faces = self.me.make_py_data(name)

        neighbour_face_01 = []
        neighbour_face_12 = []
        neighbour_face_20 = []

        for face in range(len(faces)):
            defined = 0
            index_0 = faces[face][0]
            index_1 = faces[face][1]
            index_2 = faces[face][2]

            for j in range(len(faces)):
                if defined == 3:
                    break

                if j != face:
                    if index_0 in faces[j] and index_1 in faces[j]:
                        neighbour_face_01.append(j)
                    if index_2 in faces[j] and index_1 in faces[j]:
                        neighbour_face_12.append(j)
                    if index_0 in faces[j] and index_2 in faces[j]:
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
                            dataVerts=[Vec3d(**v) for v in verts],
                            dataFaces=[
                                            Face(i, 
                                                    faces[0], 
                                                    faces[1], 
                                                    faces[2], 
                                                    FaceEdgeData(
                                                                    FaceEdge(faces[0], faces[1], i, 0), 
                                                                    FaceEdge(neighbour_face_01[i], faces[1], faces[2], i), 
                                                                    FaceEdge(1, neighbour_face_12[i], faces[2], faces[0]), 
                                                                    FaceEdge(i, 2, neighbour_face_20[i], 0))) 
                                            for i in range(len(faces))
                                        ])

    def read_line(self, name:str) -> LineNode:
        print(f"Reading line {name}")
        verts, edges, faces = self.me.make_py_data(name)
        return LineNode(UnicodeString(len(name), name),
                            len(verts),
                            [Vec3d(**v) for v in verts],
                            0)

    def make_vfx_attachment(self, name:str):
        # TODO here
        return VFXAttachment(0, [])
