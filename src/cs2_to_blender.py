from typing import List, Tuple
from cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone
from mathutils import Matrix
import bpy

from MeshEditor import MeshEditor

from CollectionManager import CollectionManager

class Cs2ToBlender:
    def __init__(self, ):
        self.cm = CollectionManager()
        self.me = MeshEditor()

    def apply_transform_matrixes(self, object_name:str, matrixes_list:List[TransformMatrix]):
        pass
        # obj:bpy.types.Object = bpy.data.objects[object_name]

        # matrix = ...

        # obj.matrix_world = matrix

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
        v, e, f = self.make_bounding_box_data(bb)
        self.me.make_object_from_data(f"{name}_bounding_box", v, e, f)
        self.cm.move_object_to_collection(f"{name}_bounding_box", collection_name)
    
    def make_building_piece(self, name:str, collection_name:str, bp:BuildingPiece, transform_matrixes:List[TransformMatrix]):
        self.cm.new_collection(bp.pieceName, collection_name)
        
        self.make_tech_node(collection_name, bp.placementNode, transform_matrixes)
        transform_matrix = bp.placementNode.NodeTransform
        
        for d in range(bp.destructCount):
            self.make_destruct(name, bp.pieceName, bp.destructs[d], transform_matrixes + [transform_matrix])

    def make_destruct(self, name:str, collection_name:str, destruct:DestructLevel, transform_matrixes:List[TransformMatrix]):
        self.cm.new_collection(destruct.destructName, collection_name)
        
        self.make_collision3d(destruct.destructName, destruct.collision3dMesh, transform_matrixes)
        
        if destruct.numWindows > 0:
            window_collection = destruct.destructName+"_windows"
            self.cm.new_collection(window_collection, destruct.destructName)
            
        if destruct.numDoors > 0:
            door_collection = destruct.destructName+"_doors"
            self.cm.new_collection(door_collection, destruct.destructName)
            
        if destruct.numSpecial > 0:
            special_collection = destruct.destructName+"_specials"
            self.cm.new_collection(special_collection, destruct.destructName)
            
        if destruct.numLines > 0:
            line_collection = destruct.destructName+"_lines"
            self.cm.new_collection(line_collection, destruct.destructName)
            
        if destruct.numNogo > 0:
            nogo_collection = destruct.destructName+"_nogos"
            self.cm.new_collection(nogo_collection, destruct.destructName)
                    
        if destruct.numPipes > 0:
            pipes_collection = destruct.destructName + "_pipes"
            self.cm.new_collection(pipes_collection, destruct.destructName)

        if destruct.numCannons > 0:
            cannons_collection = destruct.destructName + "_cannons"
            self.cm.new_collection(cannons_collection, destruct.destructName)

        if destruct.numArrowEmitters > 0:
            arrow_emitters_collection = destruct.destructName + "_arrow_emitters"
            self.cm.new_collection(arrow_emitters_collection, destruct.destructName)

        if destruct.numDockingPoints > 0:
            docking_points_collection = destruct.destructName + "_docking_points"
            self.cm.new_collection(docking_points_collection, destruct.destructName)

        if destruct.numSoftCollisions > 0:
            soft_collisions_collection = destruct.destructName + "_soft_collisions"
            self.cm.new_collection(soft_collisions_collection, destruct.destructName)

        if destruct.numFileRefs > 0:
            file_refs_collection = destruct.destructName + "_file_refs"
            self.cm.new_collection(file_refs_collection, destruct.destructName)

        if destruct.numEFLines > 0:
            eflines_collection = destruct.destructName + "_eflines"
            self.cm.new_collection(eflines_collection, destruct.destructName)

        if destruct.numActionVFX > 0:
            actionVFX_collection = destruct.destructName + "_actionVFX"
            self.cm.new_collection(actionVFX_collection, destruct.destructName)

        if destruct.numAttActionVFX > 0:
            att_actionVFX_collection = destruct.destructName + "_att_actionVFX"
            self.cm.new_collection(att_actionVFX_collection, destruct.destructName)

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

            fake_line = LineNode(f"nogo_{i}", 
                                    len(nogo.dataLines), 
                                    [(nogo.dataLines[j][0], nogo.dataLines[j][1], 0.) for j in range(len(nogo.dataLines))]
                                    , 0)
            
            self.make_line(nogo_collection, fake_line, transform_matrixes, closed=True)

        for i in range(destruct.numPipes):
            self.make_line(pipes_collection, destruct.dataPipes[i], transform_matrixes, closed = False)

        self.make_platform(destruct.destructName, destruct.platforms, transform_matrixes)

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
        self.cm.new_collection(f"cs2_parsed_{name}_collection")

        collection_name = f"cs2_parsed_{name}_collection"
        self.make_bounding_box(name, collection_name, cs2.bbox)

        self.make_tech_node(collection_name, cs2.flag, [])
        transform_matrix = cs2.flag.NodeTransform
        
        for p in range(cs2.piece_count):
            self.make_building_piece(name, collection_name, cs2.building_pieces[p], [transform_matrix])

    def make_tech_node(self, collection_name:str, t:TechNode, transform_matrixes:List[TransformMatrix]):
        t.nodeName
        t.NodeTransform

        empty:bpy.types.Object = bpy.ops.object.empty_add(type='PLAIN_AXES', 
                                            align='WORLD', 
                                            location=(0, 0, 0), 
                                            rotation=(0, 0, 0), 
                                            scale=(1, 1, 1))

        empty.name = t.nodeName
        empty.matrix_world = t.NodeTransform.to_matrix()

        self.cm.move_object_to_collection(t.nodeName, transform_matrixes)
        


    def make_platform(self, collection_name:str, p:Platform, transform_matrixes:List[TransformMatrix]):
        verts = []

        faces = []

        vert_count = 0

        for pol in p.dataPolygons:
            verts += pol.dataVerts
            faces += [vert_count+i for i in range(len(pol.dataVerts))]

            vert_count = len(verts) 

            # TODO: "revert normals?"

            # TODO: separate ground from platform

        self.me.make_object_from_data(collection_name+"_platform", verts, [], faces)
        self.cm.move_object_to_collection(collection_name+"_platform", collection_name)

        self.apply_transform_matrixes(collection_name+"_platform", transform_matrixes)

    def make_file_ref(self, collection_name:str, fr:FileRef, transform_matrixes:List[TransformMatrix]):  

        empty:bpy.types.Object = bpy.ops.object.empty_add(type='ARROWS', 
                                            align='WORLD', 
                                            location=(2, 2, 0), 
                                            rotation=(0.872665, 0.872665, 0), 
                                            scale=(1, 1, 1))

        empty.name = fr.fileKey
        empty.matrix_world = fr.fileTransform


    def make_soft_collision(self, collection_name:str, sc:SoftCollision, transform_matrixes:List[TransformMatrix]):
        
        cyl:bpy.types.Object = bpy.ops.mesh.primitive_cylinder_add(radius=sc.cylinderRadius, 
                                                    depth=sc.cylinderHeight, 
                                                    enter_editmode=False, 
                                                    align='WORLD', 
                                                    location=(0, 0, 0), 
                                                    rotation=(0, 0, 0), 
                                                    scale=(1, 1, 1))
        
        cyl.name = sc.nodeName
        cyl.matrix_world = sc.nodeTransform

        self.cm.move_object_to_collection(collection_name, collection_name)

        self.apply_transform_matrixes(collection_name, transform_matrixes)

    def make_efline(self, collection_name:str, ef:EFLine, transform_matrixes:List[TransformMatrix]):
        self.me.make_object_from_data(ef.lineName, [ef.lineStart, ef.lineEnd], [(0, 1)], [])
        self.cm.move_object_to_collection(ef.lineName, collection_name)

        self.apply_transform_matrixes(ef.lineName, transform_matrixes)

    def make_collision3d(self, collection_name:str, c3d:Collision3D, transform_matrixes:List[TransformMatrix]):
        
        self.me.make_object_from_data(c3d.collisionName, c3d.dataVerts, [], c3d.dataFaces)
        self.cm.move_object_to_collection(c3d.collisionName, collection_name)

        self.apply_transform_matrixes(c3d.collisionName, transform_matrixes)

    def make_line(self, collection_name:str, ln:LineNode, transform_matrixes:List[TransformMatrix], closed = False):
        
        edges = [(i, i+1) for i in range(len(ln.dataVerts) - 1)]
        if closed:
            edges.append(len(ln.dataVerts)-1, 0)

        self.me.make_object_from_data(ln.lineName, ln.dataVerts, edges, [])
        self.cm.move_object_to_collection(ln.lineName, collection_name)

        self.apply_transform_matrixes(ln.lineName, transform_matrixes)

    def make_vfx_attachment(self, collection_name:str, ln:VFXAttachment, transform_matrixes:List[TransformMatrix]):
        raise NotImplementedError("Build a blender version of VFXAttachment was not implemented.")
