from typing import List, Tuple
from src.cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString

try:
    from src.mesh_editor import MeshEditor
    from src.collection_manager import CollectionManager
except (ImportError, AttributeError):
    from src.fake_bpy import FakeMeshEditor as MeshEditor
    from src.fake_bpy import FakeCollectionManager as CollectionManager

from src.prefix_suffix import *

class Cs2ToBlender:
    def __init__(self, ):
        self.cm = CollectionManager()
        self.me = MeshEditor(cm = self.cm)


    def make_bounding_box_data(self, bb:BoundingBox):
        vertex_list:List[Tuple[float, float, float]] = [(bb.minX, bb.minY, bb.minZ),
                                                        (bb.maxX, bb.minY, bb.minZ),
                                                        (bb.maxX, bb.maxY, bb.minZ),
                                                        (bb.minX, bb.maxY, bb.minZ),
                                                        (bb.minX, bb.minY, bb.maxZ),
                                                        (bb.maxX, bb.minY, bb.maxZ),
                                                        (bb.maxX, bb.maxY, bb.maxZ),
                                                        (bb.minX, bb.maxY, bb.maxZ)]
        edge_list:List[Tuple[int, int]] = [(0, 1), 
                                           (1, 2), 
                                           (2, 3), 
                                           (3, 0),
                                           (0, 4), 
                                           (1, 5), 
                                           (2, 6), 
                                           (3, 7),
                                           (4, 5), 
                                           (5, 6), 
                                           (6, 7), 
                                           (7, 4)]
        face_list:List[List[float]] = []

        return vertex_list, edge_list, face_list
        
    def make_bounding_box(self, name:str, collection_name:str, bb:BoundingBox):
        print(f"Making bounding box {name}")
        v, e, f = self.make_bounding_box_data(bb)
        ob = self.me.make_object_from_data(f"{name}{object_bounding_box_suffix}", v, e, f)
        self.cm.move_object_to_collection(ob, collection_name)
    
    def make_building_piece(self, name:str, collection_name:str, bp:BuildingPiece, transform_matrixes:List[TransformMatrix]):
        print(f"Making building piece {bp.pieceName.value}")
        self.cm.new_collection(bp.pieceName.value, collection_name)
        
        if bp.placementNode.nodeName.value == "":
            self.make_tech_node(collection_name, TechNode(UnicodeString(len(bp.pieceName.value+object_bounding_piece_position_suffix), 
                                                                        bp.pieceName.value+object_bounding_piece_position_suffix), 
                                                                        bp.placementNode.NodeTransform), [])
        else:
            self.make_tech_node(collection_name, bp.placementNode, [])

        self.make_tech_node(bp.pieceName.value, bp.placementNode, transform_matrixes)
        transform_matrix = bp.placementNode.NodeTransform
        
        for d in range(bp.destructCount):
            self.make_destruct(name, bp.pieceName.value, bp.destructs[d], transform_matrixes + [transform_matrix])

    def make_destruct(self, name:str, collection_name:str, destruct:DestructLevel, transform_matrixes:List[TransformMatrix]):
        print(f"Making destruct {destruct.destructName.value}")
        self.cm.new_collection(destruct.destructName.value, collection_name)
        
        self.make_collision3d(destruct.destructName.value, destruct.collision3dMesh, transform_matrixes)
        
        if destruct.numWindows > 0:
            window_collection = destruct.destructName.value+collection_windows_suffix
            self.cm.new_collection(window_collection, destruct.destructName.value)
            
        if destruct.numDoors > 0:
            door_collection = destruct.destructName.value+collection_doors_suffix
            self.cm.new_collection(door_collection, destruct.destructName.value)
            
        if destruct.numSpecial > 0:
            special_collection = destruct.destructName.value+collection_specials_suffix
            self.cm.new_collection(special_collection, destruct.destructName.value)
            
        if destruct.numLines > 0:
            line_collection = destruct.destructName.value+collection_lines_suffix
            self.cm.new_collection(line_collection, destruct.destructName.value)
            
        if destruct.numNogo > 0:
            nogo_collection = destruct.destructName.value+collection_nogos_suffix
            self.cm.new_collection(nogo_collection, destruct.destructName.value)
                    
        if destruct.numPipes > 0:
            pipes_collection = destruct.destructName.value +collection_pipes_suffix
            self.cm.new_collection(pipes_collection, destruct.destructName.value)

        if destruct.numCannons > 0:
            cannons_collection = destruct.destructName.value +collection_cannons_suffix
            self.cm.new_collection(cannons_collection, destruct.destructName.value)

        if destruct.numArrowEmitters > 0:
            arrow_emitters_collection = destruct.destructName.value +collection_arrow_emitters_suffix
            self.cm.new_collection(arrow_emitters_collection, destruct.destructName.value)

        if destruct.numDockingPoints > 0:
            docking_points_collection = destruct.destructName.value +collection_docking_points_suffix
            self.cm.new_collection(docking_points_collection, destruct.destructName.value)

        if destruct.numSoftCollisions > 0:
            soft_collisions_collection = destruct.destructName.value +collection_soft_collisions_suffix
            
            self.cm.new_collection(soft_collisions_collection, destruct.destructName.value)
            # exit()

        if destruct.numFileRefs > 0:
            file_refs_collection = destruct.destructName.value +collection_file_refs_suffix
            self.cm.new_collection(file_refs_collection, destruct.destructName.value)

        if destruct.numEFLines > 0:
            eflines_collection = destruct.destructName.value +collection_eflines_suffix
            self.cm.new_collection(eflines_collection, destruct.destructName.value)

        if destruct.numActionVFX > 0:
            actionVFX_collection = destruct.destructName.value +collection_actionVFX_suffix
            self.cm.new_collection(actionVFX_collection, destruct.destructName.value)

        if destruct.numAttActionVFX > 0:
            att_actionVFX_collection = destruct.destructName.value +collection_att_actionVFX_suffix
            self.cm.new_collection(att_actionVFX_collection, destruct.destructName.value)

        if destruct.numActionVFX2 > 0:
            actionVFX2_collection = destruct.destructName.value +collection_actionVFX2_suffix
            self.cm.new_collection(actionVFX2_collection, destruct.destructName.value)

        if destruct.numAttActionVFX2 > 0:
            att_actionVFX2_collection = destruct.destructName.value +collection_att_actionVFX2_suffix
            self.cm.new_collection(att_actionVFX2_collection, destruct.destructName.value)

        for i in range(destruct.numWindows):
            self.make_collision3d(window_collection, destruct.collision3dWindows[i], transform_matrixes)
        
        for i in range(destruct.numDoors):
            self.make_collision3d(door_collection, destruct.collision3dDoors[i], transform_matrixes)
        
        for i in range(destruct.numSpecial):
            self.make_collision3d(special_collection, destruct.collision3dSpecial[i], transform_matrixes)
        
        for i in range(destruct.numLines):
            self.make_line(line_collection, destruct.dataLines[i], transform_matrixes, closed=True)
        
        for i in range(destruct.numNogo):
            nogo = destruct.dataNogo[i]

            nogo_name = f"{destruct.destructName.value}_{i}{object_nogo_suffix}"

            fake_line = LineNode(UnicodeString(len(nogo_name), nogo_name), 
                                    len(nogo.dataLines), 
                                    [(nogo.dataLines[j].x, nogo.dataLines[j].y, 0.) for j in range(len(nogo.dataLines))]
                                    , 0)
            
            self.make_line(nogo_collection, fake_line, transform_matrixes, closed=True, swap_yz = False)

        for i in range(destruct.numPipes):
            self.make_line(pipes_collection, destruct.dataPipes[i], transform_matrixes, closed = False)

        self.make_platform(destruct.destructName.value, destruct.platforms, transform_matrixes)

        for i in range(destruct.numCannons):
            self.make_tech_node(cannons_collection, destruct.dataCannons[i], transform_matrixes)

        for i in range(destruct.numArrowEmitters):
            self.make_tech_node(arrow_emitters_collection, destruct.dataArrowEmitters[i], transform_matrixes)

        for i in range(destruct.numDockingPoints):
            self.make_tech_node(docking_points_collection, destruct.dataDockingPoints[i], transform_matrixes)

        for i in range(destruct.numSoftCollisions):
            self.make_soft_collision(soft_collisions_collection, destruct.dataSoftCollisions[i], transform_matrixes)
            
        for i in range(destruct.numFileRefs):
            self.make_file_ref(file_refs_collection, destruct.dataFileRefs[i], transform_matrixes)

        for i in range(destruct.numEFLines):
            self.make_efline(eflines_collection, destruct.dataEFLines[i], transform_matrixes)

        for i in range(destruct.numActionVFX):
            self.make_tech_node(actionVFX_collection, destruct.ActionVFX[i], transform_matrixes)

        for i in range(destruct.numAttActionVFX):
            self.make_vfx_attachment(att_actionVFX_collection, destruct.attActionVFX[i], transform_matrixes)

        for i in range(destruct.numActionVFX2):
            self.make_tech_node(actionVFX2_collection, destruct.ActionVFX2[i], transform_matrixes)

        for i in range(destruct.numAttActionVFX2):
            self.make_vfx_attachment(att_actionVFX2_collection, destruct.attActionVFX2[i], transform_matrixes)

    def make_cs2(self, cs2:Cs2File, name:str):
        print(f"Making cs2 {name}")
        collection_name = f"cs2_parsed_{name}_collection"
        self.cm.new_collection(collection_name, "")

        self.make_bounding_box(name, collection_name, cs2.bbox)

        if cs2.flag.nodeName.value == "":
            self.make_tech_node(collection_name, TechNode(UnicodeString(len(collection_name+object_flag_suffix), collection_name+object_flag_suffix), cs2.flag.NodeTransform), [])
        else:
            self.make_tech_node(collection_name, cs2.flag, [])

        transform_matrix = cs2.flag.NodeTransform
        
        for p in range(cs2.piece_count):
            self.make_building_piece(name, collection_name, cs2.building_pieces[p], [transform_matrix])

        

    def make_tech_node(self, collection_name:str, t:TechNode, transform_matrixes:List[TransformMatrix]):
        
        name = t.nodeName.value
        if name == "":
            name = collection_name+object_flag_suffix
        print(f"Making tech node {t.nodeName.value}")

        empty = self.me.make_empty(name, t.NodeTransform)

        self.cm.move_object_to_collection(empty, collection_name)


    def make_platform(self, collection_name:str, p:Platform, transform_matrixes:List[TransformMatrix]):
        print(f"Making platform for {collection_name}")
        vert_count_platform = 0
        vert_count_ground = 0

        platform_verts: List = []
        ground_verts: List = []

        platform_faces: List = []
        ground_faces: List = []

        platform_normals: List = []
        ground_normals: List = []

        for pol in p.dataPolygons:
            if pol.isPlatformGround:
                ground_verts += pol.dataVerts
                ground_faces += [[vert_count_ground+i for i in range(len(pol.dataVerts))]]

                vert_count_ground = len(ground_verts) 

                ground_normals.append(pol.normal)

            else:
                platform_verts += pol.dataVerts
                platform_faces += [[vert_count_platform+i for i in range(len(pol.dataVerts))]]

                vert_count_platform = len(platform_verts) 
                
                platform_normals.append(pol.normal)

        if len(platform_verts) > 0:
            ob = self.me.make_object_from_data(collection_name+object_platform_suffix, platform_verts, [], platform_faces, normals = platform_normals)
            self.cm.move_object_to_collection(ob, collection_name)

            # self.apply_transform_matrixes(collection_name+"_platform", transform_matrixes)

        if len(ground_verts) > 0:
            ob = self.me.make_object_from_data(collection_name+object_ground_suffix, ground_verts, [], ground_faces, normals = ground_normals)
            self.cm.move_object_to_collection(ob, collection_name)

            # self.apply_transform_matrixes(collection_name+"_ground", transform_matrixes)

    def make_file_ref(self, collection_name:str, fr:FileRef, transform_matrixes:List[TransformMatrix]):  
        print(f"Making file reference {fr.fileKey.value}")
        empty = self.me.make_empty(fr.fileKey.value, fr.fileTransform)
        
        self.cm.move_object_to_collection(empty, collection_name)
        
    def make_soft_collision(self, collection_name:str, sc:SoftCollision, transform_matrixes:List[TransformMatrix]):
        print(f"Making soft collision {sc.nodeName.value}")

        self.me.make_cylinder(sc.cylinderRadius, sc.cylinderHeight, sc.nodeName.value, collection_name, sc.nodeTransform)
        # self.me.apply_transform_matrixes(collection_name, transform_matrixes)

    def make_efline(self, collection_name:str, ef:EFLine, transform_matrixes:List[TransformMatrix]):
        print(f"Making efline {ef.lineName.value}")
        ob = self.me.make_object_from_data(ef.lineName.value, [ef.lineStart, ef.lineEnd], [(0, 1)], [])
        self.cm.move_object_to_collection(ob, collection_name)

        # self.apply_transform_matrixes(ef.lineName.value, transform_matrixes)

    def make_collision3d(self, collection_name:str, c3d:Collision3D, transform_matrixes:List[TransformMatrix]):
        print(f"Making collision 3d {c3d.collisionName.value}")
        
        if not c3d.collisionName.value.endswith(object_collision3d_suffix):
            c3d.collisionName.value += object_collision3d_suffix

        ob = self.me.make_object_from_data(c3d.collisionName.value, c3d.dataVerts, [], c3d.dataFaces)
        self.cm.move_object_to_collection(ob, collection_name)

        # self.apply_transform_matrixes(c3d.collisionName.value, transform_matrixes)

    def make_line(self, collection_name:str, ln:LineNode, transform_matrixes:List[TransformMatrix], closed = False, swap_yz = True):
        print(f"Making line {ln.lineName.value}")
        
        # print("LINE_TYPE", ln.lineType)

        edges = [(i, i+1) for i in range(len(ln.dataVerts) - 1)]
        if closed:
            edges.append((len(ln.dataVerts)-1, 0))

        ob = self.me.make_object_from_data(ln.lineName.value, ln.dataVerts, edges, [], swap_yz=swap_yz)
        self.cm.move_object_to_collection(ob, collection_name)

        # self.apply_transform_matrixes(ln.lineName.value, transform_matrixes)

    def make_vfx_attachment(self, collection_name:str, vfxA:VFXAttachment, transform_matrixes:List[TransformMatrix]):
        pass
        # print(vfxA, vfxA.dataIndices)
        # raise NotImplementedError("Build a blender version of VFXAttachment was not implemented.")
