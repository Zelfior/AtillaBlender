from typing import List, Tuple
from src.cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString

from src.mesh_editor import MeshEditor

from src.collection_manager import CollectionManager

class Cs2ToBlender:
    def __init__(self, ):
        self.cm = CollectionManager()
        self.me = MeshEditor()


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
        ob = self.me.make_object_from_data(f"{name}_bounding_box", v, e, f)
        self.cm.move_object_to_collection(ob, collection_name)
    
    def make_building_piece(self, name:str, collection_name:str, bp:BuildingPiece, transform_matrixes:List[TransformMatrix]):
        print(f"Making building piece {bp.pieceName.value}")
        self.cm.new_collection(bp.pieceName.value, collection_name)
        
        if bp.placementNode.nodeName.value == "":
            bp.placementNode.nodeName.value = collection_name+"_building_piece_placement"
        self.make_tech_node(collection_name, bp.placementNode, transform_matrixes)
        transform_matrix = bp.placementNode.NodeTransform
        
        for d in range(bp.destructCount):
            self.make_destruct(name, bp.pieceName.value, bp.destructs[d], transform_matrixes + [transform_matrix])

    def make_destruct(self, name:str, collection_name:str, destruct:DestructLevel, transform_matrixes:List[TransformMatrix]):
        print(f"Making destruct {destruct.destructName.value}")
        self.cm.new_collection(destruct.destructName.value, collection_name)
        
        self.make_collision3d(destruct.destructName.value, destruct.collision3dMesh, transform_matrixes)
        
        if destruct.numWindows > 0:
            window_collection = destruct.destructName.value+"_windows"
            self.cm.new_collection(window_collection, destruct.destructName.value)
            
        if destruct.numDoors > 0:
            door_collection = destruct.destructName.value+"_doors"
            self.cm.new_collection(door_collection, destruct.destructName.value)
            
        if destruct.numSpecial > 0:
            special_collection = destruct.destructName.value+"_specials"
            self.cm.new_collection(special_collection, destruct.destructName.value)
            
        if destruct.numLines > 0:
            line_collection = destruct.destructName.value+"_lines"
            self.cm.new_collection(line_collection, destruct.destructName.value)
            
        if destruct.numNogo > 0:
            nogo_collection = destruct.destructName.value+"_nogos"
            self.cm.new_collection(nogo_collection, destruct.destructName.value)
                    
        if destruct.numPipes > 0:
            pipes_collection = destruct.destructName.value + "_pipes"
            self.cm.new_collection(pipes_collection, destruct.destructName.value)

        if destruct.numCannons > 0:
            cannons_collection = destruct.destructName.value + "_cannons"
            self.cm.new_collection(cannons_collection, destruct.destructName.value)

        if destruct.numArrowEmitters > 0:
            arrow_emitters_collection = destruct.destructName.value + "_arrow_emitters"
            self.cm.new_collection(arrow_emitters_collection, destruct.destructName.value)

        if destruct.numDockingPoints > 0:
            docking_points_collection = destruct.destructName.value + "_docking_points"
            self.cm.new_collection(docking_points_collection, destruct.destructName.value)

        if destruct.numSoftCollisions > 0:
            soft_collisions_collection = destruct.destructName.value + "_soft_collisions"
            self.cm.new_collection(soft_collisions_collection, destruct.destructName.value)

        if destruct.numFileRefs > 0:
            file_refs_collection = destruct.destructName.value + "_file_refs"
            self.cm.new_collection(file_refs_collection, destruct.destructName.value)

        if destruct.numEFLines > 0:
            eflines_collection = destruct.destructName.value + "_eflines"
            self.cm.new_collection(eflines_collection, destruct.destructName.value)

        if destruct.numActionVFX > 0:
            actionVFX_collection = destruct.destructName.value + "_actionVFX"
            self.cm.new_collection(actionVFX_collection, destruct.destructName.value)

        if destruct.numAttActionVFX > 0:
            att_actionVFX_collection = destruct.destructName.value + "_att_actionVFX"
            self.cm.new_collection(att_actionVFX_collection, destruct.destructName.value)

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

            fake_line = LineNode(UnicodeString(len(f"nogo_{i}"), f"nogo_{i}"), 
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

    def make_cs2(self, cs2:Cs2File, name:str):
        print(f"Making cs2 {name}")
        self.cm.new_collection(f"cs2_parsed_{name}_collection", "")

        collection_name = f"cs2_parsed_{name}_collection"
        self.make_bounding_box(name, collection_name, cs2.bbox)

        if cs2.flag.nodeName.value == "":
            cs2.flag.nodeName.value = collection_name+"_flag"
        self.make_tech_node(collection_name, cs2.flag, [])
        transform_matrix = cs2.flag.NodeTransform
        
        for p in range(cs2.piece_count):
            self.make_building_piece(name, collection_name, cs2.building_pieces[p], [transform_matrix])

    def make_tech_node(self, collection_name:str, t:TechNode, transform_matrixes:List[TransformMatrix]):
        if t.nodeName.value == "":
            t.nodeName.value = collection_name+"_tech_node"
        print(f"Making tech node {t.nodeName.value}")

        empty = self.me.make_empty(t.nodeName.value, t.NodeTransform)

        self.cm.move_object_to_collection(empty, collection_name)
        

    def make_platform(self, collection_name:str, p:Platform, transform_matrixes:List[TransformMatrix]):
        print(f"Making platform for {collection_name}")
        vert_count_platform = 0
        vert_count_ground = 0

        platform_verts: List = []
        ground_verts: List = []

        platform_faces: List = []
        ground_faces: List = []

        for pol in p.dataPolygons:
            if pol.isPlatformGround:
                ground_verts += pol.dataVerts
                ground_faces += [[vert_count_ground+i for i in range(len(pol.dataVerts))]]

                vert_count_ground = len(ground_verts) 

            else:
                platform_verts += pol.dataVerts
                platform_faces += [[vert_count_platform+i for i in range(len(pol.dataVerts))]]

                vert_count_platform = len(platform_verts) 

        if len(platform_verts) > 0:
            ob = self.me.make_object_from_data(collection_name+"_platform", platform_verts, [], platform_faces)
            self.cm.move_object_to_collection(ob, collection_name)

            # self.apply_transform_matrixes(collection_name+"_platform", transform_matrixes)

        if len(ground_verts) > 0:
            ob = self.me.make_object_from_data(collection_name+"_ground", ground_verts, [], ground_faces)
            self.cm.move_object_to_collection(ob, collection_name)

            # self.apply_transform_matrixes(collection_name+"_ground", transform_matrixes)
            
        # TODO: "revert normals?"

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
        
        ob = self.me.make_object_from_data(c3d.collisionName.value, c3d.dataVerts, [], c3d.dataFaces)
        self.cm.move_object_to_collection(ob, collection_name)

        # self.apply_transform_matrixes(c3d.collisionName.value, transform_matrixes)

    def make_line(self, collection_name:str, ln:LineNode, transform_matrixes:List[TransformMatrix], closed = False, swap_yz = True):
        print(f"Making line {ln.lineName.value}")
        
        edges = [(i, i+1) for i in range(len(ln.dataVerts) - 1)]
        if closed:
            edges.append((len(ln.dataVerts)-1, 0))

        ob = self.me.make_object_from_data(ln.lineName.value, ln.dataVerts, edges, [], swap_yz=swap_yz)
        self.cm.move_object_to_collection(ob, collection_name)

        # self.apply_transform_matrixes(ln.lineName.value, transform_matrixes)

    def make_vfx_attachment(self, collection_name:str, vfxA:VFXAttachment, transform_matrixes:List[TransformMatrix]):
        print(vfxA, vfxA.dataIndices)
        # raise NotImplementedError("Build a blender version of VFXAttachment was not implemented.")
