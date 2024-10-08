
from typing import IO, Any, List, NamedTuple

from io_elementary import IOOperation, io_float, io_int, io_str

class UnicodeString(NamedTuple):
    length:int
    value:str
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
    def from_to_file(self, io:IO, operation:IOOperation):
        self.x = io_float(io, self.x, operation)
        self.y = io_float(io, self.y, operation)
    
class Vec3d(NamedTuple):
    x:float
    y:float
    z:float
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


class TechNode:
    pass

class FaceEdge(NamedTuple):
    vertexIndex0:int
    vertexIndex1:int
    edgeIndex:int
    unknown:int
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

    def from_to_file(self, io:IO, operation:IOOperation):
        self.faceIndex = io_int(io, self.faceIndex, operation)

        padding = readByte(io)
        
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
        
        readByte(io)

        self.isPlatformGround = io_int(io, self.isPlatformGround, operation) != 0
        
        readByte(io)

class Platform(NamedTuple):
    numPolygons:int
    dataPolygons:List[Polygon]
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
    def from_to_file(self, io:IO, operation:IOOperation):
        # if operation == IOOperation.READ:
        #     self.nodeName = UnicodeString(None, None)
        #     self.nodeTransform = UnicodeString(None, None)

        self.nodeName = self.nodeName.from_to_file(io, operation)
        
        self.nodeTransform = self.nodeTransform.from_to_file(io, operation)

        readshort

        self.cylinderRadius = io_float(io, self.cylinderRadius, operation)
        self.cylinderHeight = io_float(io, self.cylinderHeight, operation)    

class FileRef(NamedTuple):
    fileKey:UnicodeString
    fileName:UnicodeString
    fileTransform:TransformMatrix
    def from_to_file(self, io:IO, operation:IOOperation):

        self.fileName = self.fileName.from_to_file(io, operation)
        self.fileKey = self.fileKey.from_to_file(io, operation)
        
        self.fileTransform = self.fileTransform.from_to_file(io, operation)
        readshort

class EFLine(NamedTuple):
    lineName:UnicodeString
    lineAction:int
    lineStart:Vec3d
    lineEnd:Vec3d
    lineDir:Vec3d
    parentIndex:int
    def from_to_file(self, io:IO, operation:IOOperation):
        self.lineName = self.lineName.from_to_file(io, operation)
        
        self.lineAction = io_int(io, self.lineAction, operation)
        
        self.lineStart = self.lineStart.from_to_file(io, operation)
        self.lineEnd = self.lineEnd.from_to_file(io, operation)
        self.lineDir = self.lineDir.from_to_file(io, operation)

        self.parentIndex = io_int(io, self.parentIndex, operation)

class VFXAttachment(NamedTuple):
    numIndices:int
    dataIndices:List[Short]
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
    def from_to_file(self, io:IO, operation:IOOperation):
        TODO

class BuildingPiece(NamedTuple):
    pieceName:UnicodeString
    placementNode:TechNode
    parentIndex:int
    destructCount:int
    destructs:List[DestructLevel]
    def from_to_file(self, io:IO, operation:IOOperation):
        if operation == IOOperation.READ:
            self.destructs = []

        self.pieceName = self.pieceName.from_to_file(io, operation)
        
        self.placementNode = self.placementNode.from_to_file(io, operation)
        
        self.parentIndex = io_int(io, self.parentIndex, operation)
        self.destructCount = io_int(io, self.destructCount, operation)

        for i in range(self.destructCount):
            if operation == IOOperation.READ:
                self.destructs.append(DestructLevel())
                self.destructs[i].from_to_file(io, operation)
            else:
                self.destructs[i].from_to_file(io, operation)
                
        array_size = io_int(io, array_size, operation)
        if array_size > 0:
            raise ValueError("Unknown array detected.")