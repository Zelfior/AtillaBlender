
from ast import NodeTransformer
from typing import IO, Any, List, NamedTuple

import inspect

from io_elementary import IOOperation, io_bytes, io_float, io_int, io_str, io_short


class SomeBytes(NamedTuple):
    length:int
    value:Any
    def from_to_file(self, io:IO, operation:IOOperation):
        self.value = io_bytes(io, self.value, self.length, operation)
    

class UnicodeString(NamedTuple):
    length:int
    value:str
    def new_unicodestring():
        return UnicodeString(0, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.length = io_int(io, self.length, operation)

        if operation == IOOperation.READ:
            self.length = io_int(io, self.length, operation)
            self.value = io_str(io, "o"*self.length, operation)
        else:
            self.length = io_int(io, self.length, operation)
            self.value = io_str(io, self.value, operation)
    
class Vec2d(NamedTuple):
    x:float
    y:float
    def new_vec2d():
        return Vec2d(None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.x = io_float(io, self.x, operation)
        self.y = io_float(io, self.y, operation)
    
class Vec3d(NamedTuple):
    x:float
    y:float
    z:float
    def new_vec3d():
        return Vec3d(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.x = io_float(io, self.x, operation)
        self.y = io_float(io, self.y, operation)
        self.z = io_float(io, self.z, operation)
    
class BoundingBox(NamedTuple):
    minX:float
    minY:float
    minZ:float
    maxX:float
    maxY:float
    maxZ:float
    def new_bounding_box():
        return BoundingBox(None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.minX = io_float(io, self.minX, operation)
        self.minY = io_float(io, self.minY, operation)
        self.minZ = io_float(io, self.minZ, operation)
        self.maxX = io_float(io, self.maxX, operation)
        self.maxY = io_float(io, self.maxY, operation)
        self.maxZ = io_float(io, self.maxZ, operation)

class TransformMatrix(NamedTuple):
    row0_col0:float
    row1_col0:float
    row2_col0:float
    row3_col0:float
    row0_col1:float
    row1_col1:float
    row2_col1:float
    row3_col1:float
    row0_col2:float
    row1_col2:float
    row2_col2:float
    row3_col2:float
    row0_col3:float
    row1_col3:float
    row2_col3:float
    row3_col3:float

    def new_transform_matrix():
        return TransformMatrix(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.row0_col0 = io_float(io, self.row0_col0, operation)
        self.row1_col0 = io_float(io, self.row1_col0, operation)
        self.row2_col0 = io_float(io, self.row2_col0, operation)
        self.row3_col0 = io_float(io, self.row3_col0, operation)
        self.row0_col1 = io_float(io, self.row0_col1, operation)
        self.row1_col1 = io_float(io, self.row1_col1, operation)
        self.row2_col1 = io_float(io, self.row2_col1, operation)
        self.row3_col1 = io_float(io, self.row3_col1, operation)
        self.row0_col2 = io_float(io, self.row0_col2, operation)
        self.row1_col2 = io_float(io, self.row1_col2, operation)
        self.row2_col2 = io_float(io, self.row2_col2, operation)
        self.row3_col2 = io_float(io, self.row3_col2, operation)
        self.row0_col3 = io_float(io, self.row0_col3, operation)
        self.row1_col3 = io_float(io, self.row1_col3, operation)
        self.row2_col3 = io_float(io, self.row2_col3, operation)
        self.row3_col3 = io_float(io, self.row3_col3, operation)
    
    def to_matrix(self,):
        return [[self.row0_col0, self.row0_col1, self.row0_col2],
                [self.row1_col0, self.row1_col1, self.row1_col2],
                [self.row2_col0, self.row2_col1, self.row2_col2],
                [self.row3_col0, self.row3_col2, self.row3_col1]]


class TechNode(NamedTuple):
    nodeName:str
    NodeTransform:TransformMatrix
    def new_tech_node():
        return TechNode(None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.nodeName

class FaceEdge(NamedTuple):
    vertexIndex0:int
    vertexIndex1:int
    edgeIndex:int
    unknown:int
    def new_face_edge():
        return FaceEdge(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.minX = io_float(io, self.minX, operation)
        self.minY = io_float(io, self.minY, operation)
        self.minZ = io_float(io, self.minZ, operation)
        self.maxX = io_float(io, self.maxX, operation)

class FaceEdgeData(NamedTuple):
    edge0:FaceEdge
    edge1:FaceEdge
    edge2:FaceEdge
    edge3:FaceEdge
    def new_face_edge_data():
        return FaceEdgeData(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.edge0 = self.edge0.from_to_file(io, operation)
        self.edge1 = self.edge1.from_to_file(io, operation)
        self.edge2 = self.edge2.from_to_file(io, operation)
        self.edge3 = self.edge3.from_to_file(io, operation)

class Face(NamedTuple):
    faceIndex:int
    vertIndex0:Any
    vertIndex1:int
    vertIndex2:int
    edgeData:FaceEdgeData

    def new_face():
        return Face(None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.faceIndex = io_int(io, self.faceIndex, operation)

        if operation == IOOperation.READ:
            self.padding = SomeBytes(1, None)
        else:
            self.padding = SomeBytes(1, 0)

        self.padding = self.padding.from_to_file(io, operation)
        
        self.vertIndex0 = io_int(io, self.vertIndex0, operation)
        self.vertIndex1 = io_int(io, self.vertIndex1, operation)
        self.vertIndex2 = io_int(io, self.vertIndex2, operation)
        self.edgeData = self.edgeData.from_to_file(io, operation)


class Collision3D(NamedTuple):
    collisionName:UnicodeString
    nodeIndex:int
    unknown2:int
    numVerts:int
    dataVerts:List[Vec3d]
    numFaces:int
    dataFaces:List[Face]
    
    def new_collision_3d():
        return Collision3D(None, None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.collisionName = self.collisionName.from_to_file(io, operation)

        self.nodeIndex = io_int(io, self.nodeIndex, operation)
        self.unknown2 = io_int(io, self.unknown2, operation)

        self.numVerts = io_int(io, self.numVerts, operation)

        if operation == IOOperation.READ:
            self.dataVerts = []
            self.dataFaces = []
        
        for i in range(self.numVerts):
            if operation == IOOperation.READ:
                self.dataVerts.append(Vec3d(None, None, None))
                self.dataVerts[i].from_to_file(io, operation)
            else:
                self.dataVerts[i].from_to_file(io, operation)

        self.numFaces = io_int(io, self.numFaces, operation)
        
        for i in range(self.numFaces):
            if operation == IOOperation.READ:
                self.dataFaces.append(Face(None, None, None, None, None))
                self.dataFaces[i].from_to_file(io, operation)
            else:
                self.dataFaces[i].from_to_file(io, operation)
                
class LineNode(NamedTuple):
    lineName:UnicodeString
    numVerts:int
    dataVerts:List[Vec3d]
    lineType:int
    
    def new_line_node():
        return LineNode(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.lineName = self.lineName.from_to_file(io, operation)
        self.numVerts = io_int(io, self.numVerts, operation)

        if operation == IOOperation.READ:
            self.dataVerts = []
        
        for i in range(self.numVerts):
            if operation == IOOperation.READ:
                self.dataVerts.append(Vec3d(None, None, None))
                self.dataVerts[i].from_to_file(io, operation)
            else:
                self.dataVerts[i].from_to_file(io, operation)
        
        self.lineType = io_int(io, self.lineType, operation)
        

class NogoZone(NamedTuple):
    numLines:int
    dataLines:List[Vec2d]
    
    def new_nogo_zone():
        return NogoZone(None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.numLines = io_int(io, self.numLines, operation)

        if operation == IOOperation.READ:
            self.dataLines = []

        for i in range(self.numLines):
            if operation == IOOperation.READ:
                self.dataLines.append(Vec2d(None, None))
                self.dataLines[i].from_to_file(io, operation)
                numLinesConnected = io_int(io, 0, operation)
                somestuffhere
            else:
                self.dataLines[i].from_to_file(io, operation)
                numLinesConnected = io_int(io, 0, operation)
                somestuffhere

class Polygon(NamedTuple):
    normal:Vec3d
    numVerts:int
    dataVerts:List[Vec3d]
    isPlatformGround:bool
    
    def new_polygon():
        return Polygon(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        if operation == IOOperation.READ:
            self.dataVerts = []
            self.normal = Vec3d(None, None, None)

        self.normal = self.normal.from_to_file(io, operation)
        
        self.numVerts = io_int(io, self.numVerts, operation)
        
        for i in range(self.numVerts):
            if operation == IOOperation.READ:
                self.dataVerts.append(Vec3d(None, None, None))
                self.dataVerts[i].from_to_file(io, operation)
            else:
                self.dataVerts[i].from_to_file(io, operation)
        
        if operation == IOOperation.READ:
            self.somebyte_1 = SomeBytes(1, None)
        else:
            self.somebyte_1 = SomeBytes(1, 0)

        self.somebyte_1 = self.somebyte_1.from_to_file(io, operation)

        self.isPlatformGround = io_int(io, self.isPlatformGround, operation) != 0
        
        if operation == IOOperation.READ:
            self.somebyte_2 = SomeBytes(1, None)
        else:
            self.somebyte_2 = SomeBytes(1, 0)

        self.somebyte_2 = self.somebyte_2.from_to_file(io, operation)

class Platform(NamedTuple):
    numPolygons:int
    dataPolygons:List[Polygon]
    
    def new_platform():
        return Platform(None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.numPolygons = io_int(io, self.numPolygons, operation)

        if operation == IOOperation.READ:
            self.dataPolygons = []
            
        for i in range(self.numPolygons):
            if operation == IOOperation.READ:
                self.dataPolygons.append(Polygon(None, None,None, None))
                self.dataPolygons[i].from_to_file(io, operation)
            else:
                self.dataPolygons[i].from_to_file(io, operation)
                
        some_stuff = io_int(io, 0, operation)

class SoftCollision(NamedTuple):
    nodeName:UnicodeString
    nodeTransform:TransformMatrix
    cylinderRadius:float
    cylinderHeight:float
    
    def new_soft_collision():
        return SoftCollision(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        # if operation == IOOperation.READ:
        #     self.nodeName = UnicodeString(None, None)
        #     self.nodeTransform = UnicodeString(None, None)

        self.nodeName = self.nodeName.from_to_file(io, operation)
        
        self.nodeTransform = self.nodeTransform.from_to_file(io, operation)

        self.some_short = io_short(io, operation)

        self.cylinderRadius = io_float(io, self.cylinderRadius, operation)
        self.cylinderHeight = io_float(io, self.cylinderHeight, operation)    

class FileRef(NamedTuple):
    fileKey:UnicodeString
    fileName:UnicodeString
    fileTransform:TransformMatrix
    
    def new_file_ref():
        return FileRef(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):

        self.fileName = self.fileName.from_to_file(io, operation)
        self.fileKey = self.fileKey.from_to_file(io, operation)
        
        self.fileTransform = self.fileTransform.from_to_file(io, operation)
        self.some_short = io_short(io, operation)

class EFLine(NamedTuple):
    lineName:UnicodeString
    lineAction:int
    lineStart:Vec3d
    lineEnd:Vec3d
    lineDir:Vec3d
    parentIndex:int
    
    def new_ef_line():
        return EFLine(None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        self.lineName = self.lineName.from_to_file(io, operation)
        
        self.lineAction = io_int(io, self.lineAction, operation)
        
        self.lineStart = self.lineStart.from_to_file(io, operation)
        self.lineEnd = self.lineEnd.from_to_file(io, operation)
        self.lineDir = self.lineDir.from_to_file(io, operation)

        self.parentIndex = io_int(io, self.parentIndex, operation)

class VFXAttachment(NamedTuple):
    numIndices:int
    dataIndices:List[int]
    
    def new_vfx_attachment():
        return VFXAttachment(None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        if operation == IOOperation.READ:
            self.dataIndices = []

        self.numIndices = io_int(io, self.numIndices, operation)

        for i in range(self.numIndices):
            if operation == IOOperation.READ:
                self.dataIndices.append(0.)
                self.dataIndices[i] = io_short(io, self.dataIndices[i], operation)
            else:
                self.dataIndices[i] = io_short(io, self.dataIndices[i], operation)
        

class DestructLevel(NamedTuple):

    destructName:UnicodeString
    destructIndex:int
    collision3dMesh:Collision3D
    numWindows:int
    collision3dWindows:List[Collision3D]
    numDoors:int
    collision3dDoors:List[Collision3D]
    numSpecial:int
    collision3dSpecial:List[Collision3D]
    numLines:int
    dataLines:List[LineNode]
    numPipes:int
    dataPipes:List[LineNode]
    platforms:Platform
    numCannons:int
    dataCannons:List[TechNode]
    numArrowEmitters:int
    dataArrowEmitters:List[TechNode]
    numDockingPoints:int
    dataDockingPoints:List[TechNode]
    numSoftCollisions:int
    dataSoftCollisions:List[SoftCollision]
    numFileRefs:int
    dataFileRefs:List[FileRef]
    numEFLines:int
    dataEFLines:List[EFLine]
    
    def new_destruct_level():
        return DestructLevel(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None)
    
    def from_to_file(self, io:IO, operation:IOOperation):
        if operation == IOOperation.READ:
            self.collision3dWindows = []
            self.collision3dDoors = []
            self.collision3dSpecial = []
            self.dataLines = []
            self.dataPipes = []
            self.dataCannons = []
            self.dataArrowEmitters = []
            self.dataDockingPoints = []
            self.dataSoftCollisions = []
            self.dataFileRefs = []
            self.dataEFLines = []

            self.destructName = UnicodeString.new_unicodestring()
            self.collision3dMesh = Collision3D.new_collision_3d()

        self.destructName = self.destructName.from_to_file(io, operation)
        self.destructIndex = io_int(io, self.destructIndex, operation)

        self.collision3dMesh = self.collision3dMesh.from_to_file(io, operation)

        self.numWindows = io_int(io, self.numWindows, operation)
        for _ in range(self.numWindows):
            if operation == IOOperation.READ:
                self.collision3dWindows.append(Collision3D.new_collision_3d())
            
            self.collision3dWindows[-1] = self.collision3dWindows[-1].from_to_file(io, operation)

        self.numDoors = io_int(io, self.numDoors, operation)
        for _ in range(self.numDoors):
            if operation == IOOperation.READ:
                self.collision3dDoors.append(Collision3D.new_collision_3d())
            
            self.collision3dDoors[-1] = self.collision3dDoors[-1].from_to_file(io, operation)

        self.numSpecial = io_int(io, self.numSpecial, operation)
        for _ in range(self.numSpecial):
            if operation == IOOperation.READ:
                self.collision3dSpecial.append(Collision3D.new_collision_3d())
                self.collision3dSpecial.append(Collision3D.new_collision_3d())
            
            self.collision3dSpecial[-2] = self.collision3dSpecial[-2].from_to_file(io, operation)
            self.collision3dSpecial[-1] = self.collision3dSpecial[-1].from_to_file(io, operation)

        self.numLines = io_int(io, self.numLines, operation)
        for _ in range(self.numLines):
            if operation == IOOperation.READ:
                self.dataLines.append(LineNode.new_line_node())
            
            self.dataLines[-1] = self.dataLines[-1].from_to_file(io, operation)

        self.numPipes = io_int(io, self.numPipes, operation)
        for _ in range(self.numPipes):
            if operation == IOOperation.READ:
                self.dataPipes.append(LineNode.new_line_node())
            
            self.dataPipes[-1] = self.dataPipes[-1].from_to_file(io, operation)
        
        """
            Wasted data?
        """
        self.numNogo = io_int(io, self.numNogo, operation)
        self.nogo:List[NogoZone] = []
        for _ in range(self.numNogo):
            if operation == IOOperation.READ:
                self.nogo.append(NogoZone.new_nogo_zone())
            
            self.nogo[-1] = self.nogo[-1].from_to_file(io, operation)

        if operation == IOOperation.READ:
            self.platforms = Platform.new_platform()
        self.platforms = self.platforms.from_to_file(io, operation)

        if operation == IOOperation.READ:
            self.destruct_bbox:BoundingBox = BoundingBox.new_bounding_box()
        self.destruct_bbox = self.destruct_bbox.from_to_file(io, operation)

        self.numCannons = io_int(io, self.numCannons, operation)
        for _ in range(self.numCannons):
            if operation == IOOperation.READ:
                self.dataCannons.append(TechNode.new_tech_node())
            
            self.dataCannons[-1] = self.dataCannons[-1].from_to_file(io, operation)
        
        self.numArrowEmitters = io_int(io, self.numArrowEmitters, operation)
        for _ in range(self.numArrowEmitters):
            if operation == IOOperation.READ:
                self.dataArrowEmitters.append(TechNode.new_tech_node())
            
            self.dataArrowEmitters[-1] = self.dataArrowEmitters[-1].from_to_file(io, operation)
        
        self.numDockingPoints = io_int(io, self.numDockingPoints, operation)
        for _ in range(self.numDockingPoints):
            if operation == IOOperation.READ:
                self.dataDockingPoints.append(TechNode.new_tech_node())
            
            self.dataDockingPoints[-1] = self.dataDockingPoints[-1].from_to_file(io, operation)
        
        self.numSoftCollisions = io_int(io, self.numSoftCollisions, operation)
        for _ in range(self.numSoftCollisions):
            if operation == IOOperation.READ:
                self.dataSoftCollisions.append(TechNode.new_tech_node())
            
            self.dataSoftCollisions[-1] = self.dataSoftCollisions[-1].from_to_file(io, operation)
        
        someArray = io_int(io, 0, operation)
        if someArray > 0:
            raise ValueError("Unknown data detected.")

        self.numFileRefs = io_int(io, self.numFileRefs, operation)
        for _ in range(self.numFileRefs):
            if operation == IOOperation.READ:
                self.dataFileRefs.append(FileRef.new_file_ref())
            
            self.dataFileRefs[-1] = self.dataFileRefs[-1].from_to_file(io, operation)
        
        self.numEFLines = io_int(io, self.numEFLines, operation)
        for _ in range(self.numEFLines):
            if operation == IOOperation.READ:
                self.dataEFLines.append(FileRef.new_file_ref())
            
            self.dataEFLines[-1] = self.dataEFLines[-1].from_to_file(io, operation)
        
        someArray = io_int(io, 0, operation)
        if someArray > 0:
            raise ValueError("Unknown data detected.")
        
        if version == 11:
            return 0.
        else:
            self.ActionVFX:List[TechNode] = []
            
            self.numActionVFX = io_int(io, 0, operation)
            for _ in range(self.numActionVFX):
                if operation == IOOperation.READ:
                    self.ActionVFX.append(TechNode.new_tech_node())
                
                self.ActionVFX[-1] = self.ActionVFX[-1].from_to_file(io, operation)
            
            self.numActionVFX = io_int(io, self.numActionVFX, operation)
            for _ in range(self.numActionVFX):
                if operation == IOOperation.READ:
                    self.ActionVFX.append(TechNode.new_tech_node())
                
                self.ActionVFX[-1] = self.ActionVFX[-1].from_to_file(io, operation)
                

            self.attActionVFX:List[VFXAttachment] = []
            
            self.numAttActionVFX = io_int(io, 0, operation)
            for _ in range(self.numAttActionVFX):
                if operation == IOOperation.READ:
                    self.attActionVFX.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX[-1] = self.attActionVFX[-1].from_to_file(io, operation)
            
            self.numAttActionVFX = io_int(io, self.numAttActionVFX, operation)
            for _ in range(self.numAttActionVFX):
                if operation == IOOperation.READ:
                    self.attActionVFX.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX[-1] = self.attActionVFX[-1].from_to_file(io, operation)
        
        

class BuildingPiece(NamedTuple):
    pieceName:UnicodeString
    placementNode:TechNode
    parentIndex:int
    destructCount:int
    destructs:List[DestructLevel]
    def new_building_piece():
        return BuildingPiece(None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation):
        if operation == IOOperation.READ:
            self.destructs = []

        self.pieceName = self.pieceName.from_to_file(io, operation)
        
        self.placementNode = self.placementNode.from_to_file(io, operation)
        
        self.parentIndex = io_int(io, self.parentIndex, operation)
        self.destructCount = io_int(io, self.destructCount, operation)

        for i in range(self.destructCount):
            if operation == IOOperation.READ:
                self.destructs.append(DestructLevel.new_destruct_level())
                self.destructs[i].from_to_file(io, operation)
            else:
                self.destructs[i].from_to_file(io, operation)
                
        array_size = io_int(io, array_size, operation)
        if array_size > 0:
            raise ValueError("Unknown array detected.")

if __name__ == "__main__":
    v2 = Vec2d.new_vec2d()
    v2 = Vec2d(1, 2)
    # dl = get_empty(DestructLevel)

