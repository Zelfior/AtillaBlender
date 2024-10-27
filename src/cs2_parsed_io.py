
import struct
from pathlib import Path
from typing import IO, Any, List

from src.io_elementary import IOOperation, io_bytes, io_float, io_int, io_str, io_short

debug = False

class SomeBytes():
    length:int
    value:Any
    def __init__(self, length:int, value:Any):
        self.length = length
        self.value = value
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.value, self.length = io_bytes(io, self.value, self.length, operation)
        if debug:
            print(f"bytes of length {self.length} : {self.value} at {hex(io.tell()-1)}")

class UnicodeString():
    length:int
    value:str
    def __init__(self, length:int, value:str):
        self.length = length
        self.value = value
    def new_unicodestring():
        return UnicodeString(0, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.length = io_short(io, self.length, operation)

        if operation == IOOperation.READ:
            self.value = io_str(io, "o"*self.length, operation)
        else:
            self.value = io_str(io, self.value, operation)

        if debug:
            print(f"string of length {self.length} : {self.value}")
    
class Vec2d():
    x:float
    y:float
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def new_vec2d():
        return Vec2d(None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.x = io_float(io, self.x, operation)
        self.y = io_float(io, self.y, operation)

        if debug:
            print(f"vec2d ({self.x}, {self.y})")
    
class Vec3d():
    x:float
    y:float
    z:float
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z
    def new_vec3d():
        return Vec3d(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11, inverse = True):
        self.x = io_float(io, self.x, operation)
        inverse = False
        if inverse:
            self.z = io_float(io, self.z, operation)
            self.y = io_float(io, self.y, operation)
        else:
            self.y = io_float(io, self.y, operation)
            self.z = io_float(io, self.z, operation)

        if debug:
            print(f"vec3d ({self.x}, {self.y}, {self.z})")
    
class BoundingBox():
    minX:float
    minY:float
    minZ:float
    maxX:float
    maxY:float
    maxZ:float
    def __init__(self, 
                    minX:float, 
                    minY:float, 
                    minZ:float, 
                    maxX:float, 
                    maxY:float, 
                    maxZ:float):
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ
    def new_bounding_box():
        return BoundingBox(None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.minX = io_float(io, self.minX, operation)
        self.minY = io_float(io, self.minY, operation)
        self.minZ = io_float(io, self.minZ, operation)
        self.maxX = io_float(io, self.maxX, operation)
        self.maxY = io_float(io, self.maxY, operation)
        self.maxZ = io_float(io, self.maxZ, operation)

        if debug:
            print(f"bounding box ([{self.minX}, {self.maxX}], [{self.minY}, {self.maxY}], [{self.minZ}, {self.maxZ}])")

class TransformMatrix():
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

    def __init__(self, 
                    row0_col0:float,
                    row1_col0:float,
                    row2_col0:float,
                    row3_col0:float,
                    row0_col1:float,
                    row1_col1:float,
                    row2_col1:float,
                    row3_col1:float,
                    row0_col2:float,
                    row1_col2:float,
                    row2_col2:float,
                    row3_col2:float,
                    row0_col3:float,
                    row1_col3:float,
                    row2_col3:float,
                    row3_col3:float):
        self.row0_col0 = row0_col0
        self.row1_col0 = row1_col0
        self.row2_col0 = row2_col0
        self.row3_col0 = row3_col0
        self.row0_col1 = row0_col1
        self.row1_col1 = row1_col1
        self.row2_col1 = row2_col1
        self.row3_col1 = row3_col1
        self.row0_col2 = row0_col2
        self.row1_col2 = row1_col2
        self.row2_col2 = row2_col2
        self.row3_col2 = row3_col2
        self.row0_col3 = row0_col3
        self.row1_col3 = row1_col3
        self.row2_col3 = row2_col3
        self.row3_col3 = row3_col3
    def new_transform_matrix():
        return TransformMatrix(1, 0, 0, 0, 
                               0, 1, 0, 0, 
                               0, 0, 1, 0, 
                               0, 0, 0, 1)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
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
    
        if debug:
            print(f"transform matrix {self.to_matrix()}")

    def to_matrix(self, transpose = False):
        if transpose:
            return [[self.row0_col0, self.row1_col0, self.row2_col0, self.row3_col0],
                    [self.row0_col1, self.row1_col1, self.row2_col1, self.row3_col1],
                    [self.row0_col2, self.row1_col2, self.row2_col2, self.row3_col2],
                    [self.row0_col3, self.row1_col3, self.row2_col3, self.row3_col3]]
        
        return [[self.row0_col0, self.row0_col1, self.row0_col2, self.row0_col3],
                [self.row1_col0, self.row1_col1, self.row1_col2, self.row1_col3],
                [self.row2_col0, self.row2_col1, self.row2_col2, self.row2_col3],
                [self.row3_col0, self.row3_col1, self.row3_col2, self.row3_col3]]
    
    def __repr__(self,):
        return f"| {self.row0_col0},\t{self.row0_col1},\t{self.row0_col2},\t{self.row0_col3} |\n" +\
               f"| {self.row1_col0},\t{self.row1_col1},\t{self.row1_col2},\t{self.row1_col3} |\n" +\
               f"| {self.row2_col0},\t{self.row2_col1},\t{self.row2_col2},\t{self.row2_col3} |\n" +\
               f"| {self.row3_col0},\t{self.row3_col1},\t{self.row3_col2},\t{self.row3_col3} |\n"


class TechNode():
    nodeName:UnicodeString
    NodeTransform:TransformMatrix
    def __init__(self, nodeName:UnicodeString, NodeTransform:TransformMatrix):
        self.nodeName = nodeName
        self.NodeTransform = NodeTransform
    def new_tech_node():
        return TechNode(None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print("from_to_file technode")
        if operation == IOOperation.READ:
            self.nodeName = UnicodeString.new_unicodestring()
            self.NodeTransform = TransformMatrix.new_transform_matrix()
        
        self.nodeName.from_to_file(io, operation, version = version)
        self.NodeTransform.from_to_file(io, operation, version = version)

        if debug:
            print(f"tech_node {self.nodeName.value} : {self.NodeTransform.to_matrix()}")


class FaceEdge():
    vertexIndex0:int
    vertexIndex1:int
    edgeIndex:int
    unknown:int
    def __init__(self, 
                    vertexIndex0:int,
                    vertexIndex1:int,
                    edgeIndex:int,
                    unknown:int):
        self.vertexIndex0 = vertexIndex0
        self.vertexIndex1 = vertexIndex1
        self.edgeIndex = edgeIndex
        self.unknown = unknown
    def new_face_edge():
        return FaceEdge(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.vertexIndex0 = io_int(io, self.vertexIndex0, operation)
        self.vertexIndex1 = io_int(io, self.vertexIndex1, operation)
        self.edgeIndex = io_int(io, self.edgeIndex, operation)
        self.unknown = io_int(io, self.unknown, operation)

        if debug:
            print(f"faceedge : {self.vertexIndex0}, {self.vertexIndex1}, {self.edgeIndex}, {self.unknown}")

class FaceEdgeData():
    edge0:FaceEdge
    edge1:FaceEdge
    edge2:FaceEdge
    edge3:FaceEdge
    def __init__(self, 
                    edge0:FaceEdge,
                    edge1:FaceEdge,
                    edge2:FaceEdge,
                    edge3:FaceEdge):
        self.edge0 = edge0
        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3
    def new_face_edge_data():
        return FaceEdgeData(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if operation == IOOperation.READ:
            self.edge0 = FaceEdge.new_face_edge()
            self.edge1 = FaceEdge.new_face_edge()
            self.edge2 = FaceEdge.new_face_edge()
            self.edge3 = FaceEdge.new_face_edge()
        self.edge0.from_to_file(io, operation)
        self.edge1.from_to_file(io, operation)
        self.edge2.from_to_file(io, operation)
        self.edge3.from_to_file(io, operation)

class Face():
    faceIndex:int
    vertIndex0:Any
    vertIndex1:int
    vertIndex2:int
    edgeData:FaceEdgeData

    def __init__(self, 
                    faceIndex:int,
                    vertIndex0:Any,
                    vertIndex1:int,
                    vertIndex2:int,
                    edgeData:FaceEdgeData):
        self.faceIndex = faceIndex
        self.vertIndex0 = vertIndex0
        self.vertIndex1 = vertIndex1
        self.vertIndex2 = vertIndex2
        self.edgeData = edgeData
    def new_face():
        return Face(None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if operation == IOOperation.READ:
            self.edgeData = FaceEdgeData.new_face_edge_data()

        self.faceIndex = io_int(io, self.faceIndex, operation)

        if operation == IOOperation.READ:
            self.padding = SomeBytes(1, None)
        else:
            self.padding = SomeBytes(1, b"\x00")

        self.padding.from_to_file(io, operation)
        
        self.vertIndex0 = io_int(io, self.vertIndex0, operation)
        self.vertIndex1 = io_int(io, self.vertIndex1, operation)
        self.vertIndex2 = io_int(io, self.vertIndex2, operation)
        self.edgeData.from_to_file(io, operation)


class Collision3D():
    collisionName:UnicodeString
    nodeIndex:int
    unknown2:int
    numVerts:int
    dataVerts:List[Vec3d]
    numFaces:int
    dataFaces:List[Face]
    
    def __init__(self, 
                    collisionName:UnicodeString,
                    nodeIndex:int,
                    unknown2:int,
                    numVerts:int,
                    dataVerts:List[Vec3d],
                    numFaces:int,
                    dataFaces:List[Face]):
        self.collisionName = collisionName
        self.nodeIndex = nodeIndex
        self.unknown2 = unknown2
        self.numVerts = numVerts
        self.dataVerts = dataVerts
        self.numFaces = numFaces
        self.dataFaces = dataFaces
        
    def new_collision_3d():
        return Collision3D(None, None, None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print("from_to_file collision3D")
        
        if operation == IOOperation.READ:
            self.collisionName = UnicodeString.new_unicodestring()
            self.dataVerts = []
            self.dataFaces = []

        self.collisionName.from_to_file(io, operation)

        self.nodeIndex = io_int(io, self.nodeIndex, operation)
        self.unknown2 = io_int(io, self.unknown2, operation)

        self.numVerts = io_int(io, self.numVerts, operation)
        
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
                
class LineNode():
    lineName:UnicodeString
    numVerts:int
    dataVerts:List[Vec3d]
    lineType:int
    
    def __init__(self,
                    lineName:UnicodeString,
                    numVerts:int,
                    dataVerts:List[Vec3d],
                    lineType:int ):
        self.lineName = lineName
        self.numVerts = numVerts
        self.dataVerts = dataVerts
        self.lineType = lineType    
    def new_line_node():
        return LineNode(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print("from_to_file linenode")
        if operation == IOOperation.READ:
            self.lineName = UnicodeString.new_unicodestring()
        self.lineName.from_to_file(io, operation)
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
        

class NogoZone():
    numLines:int
    dataLines:List[Vec2d]
    numLinesConnected:List[int]
    
    def __init__(self, 
                    numLines:int,
                    dataLines:List[Vec2d],
                    numLinesConnected:List[int]):
        self.numLines = numLines
        self.dataLines = dataLines
        self.numLinesConnected = numLinesConnected
    def new_nogo_zone():
        return NogoZone(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.numLines = io_int(io, self.numLines, operation)

        if operation == IOOperation.READ:
            self.dataLines = []
            self.numLinesConnected = [0 for _ in range(self.numLines)]

        for i in range(self.numLines):
            if operation == IOOperation.READ:
                self.dataLines.append(Vec2d(None, None))
                self.dataLines[i].from_to_file(io, operation)
                self.numLinesConnected[i] = io_int(io, self.numLinesConnected[i], operation)
                
            else:
                self.dataLines[i].from_to_file(io, operation)
                self.numLinesConnected[i] = io_int(io, self.numLinesConnected[i], operation)
                

class Polygon():
    normal:Vec3d
    numVerts:int
    dataVerts:List[Vec3d]
    isPlatformGround:bool
    
    def __init__(self, 
                    normal:Vec3d,
                    numVerts:int,
                    dataVerts:List[Vec3d],
                    isPlatformGround:bool):
        self.normal = normal
        self.numVerts = numVerts
        self.dataVerts = dataVerts
        self.isPlatformGround = isPlatformGround

    def new_polygon():
        return Polygon(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if operation == IOOperation.READ:
            self.dataVerts = []
            self.normal = Vec3d(None, None, None)

        self.normal.from_to_file(io = io, 
                                    operation = operation, 
                                    inverse=False)
        
        self.numVerts = io_int(io, self.numVerts, operation)
        
        if debug:
            print(f"Reading {self.numVerts} verts at {hex(io.tell())}/{hex(io.tell())}")
        for i in range(self.numVerts):
            if operation == IOOperation.READ:
                self.dataVerts.append(Vec3d(None, None, None))
                self.dataVerts[i].from_to_file(io, operation)
            else:
                self.dataVerts[i].from_to_file(io, operation)
        
        if operation == IOOperation.READ:
            self.somebyte_1 = SomeBytes(1, None)
            self.somebyte_2 = SomeBytes(1, None)
            self.groundPlatformByte = SomeBytes(1, None)
        else:
            self.somebyte_1 = SomeBytes(1, b"\x00")
            self.somebyte_2 = SomeBytes(1, b"\x00")
            if self.isPlatformGround:
                self.groundPlatformByte = SomeBytes(1, b"\x01")
            else:
                self.groundPlatformByte = SomeBytes(1, b"\x00")

        self.somebyte_1.from_to_file(io, operation)

        self.groundPlatformByte.from_to_file(io, operation)

        self.isPlatformGround = self.groundPlatformByte.value != b"\x00"
        
        self.somebyte_2.from_to_file(io, operation)

class Platform():
    numPolygons:int
    dataPolygons:List[Polygon]
    some_int:int
    
    def __init__(self, 
                    numPolygons:int,
                    dataPolygons:List[Polygon],
                    some_int:int):
        self.numPolygons = numPolygons
        self.dataPolygons = dataPolygons
        self.some_int = some_int
    def new_platform():
        return Platform(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.numPolygons = io_int(io, self.numPolygons, operation)

        if operation == IOOperation.READ:
            self.dataPolygons = []
            
        if debug:
            print(f"Reading {self.numPolygons} polygons  at {hex(io.tell())}/{hex(io.tell())}")
        for i in range(self.numPolygons):
            if operation == IOOperation.READ:
                self.dataPolygons.append(Polygon(None, None,None, None))
                self.dataPolygons[i].from_to_file(io, operation)
            else:
                self.dataPolygons[i].from_to_file(io, operation)
                
        if debug:
            print(f"Reading int at {hex(io.tell())}")
        self.some_int = io_int(io, self.some_int, operation)

class SoftCollision():
    nodeName:UnicodeString
    nodeTransform:TransformMatrix
    some_short:int
    cylinderRadius:float
    cylinderHeight:float
    
    def __init__(self, 
                    nodeName:UnicodeString,
                    nodeTransform:TransformMatrix,
                    some_short:int,
                    cylinderRadius:float,
                    cylinderHeight:float):
        self.nodeName = nodeName
        self.nodeTransform = nodeTransform
        self.some_short = some_short
        self.cylinderRadius = cylinderRadius
        self.cylinderHeight = cylinderHeight
    def new_soft_collision():
        return SoftCollision(None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print(f"Read soft collision at {hex(io.tell())}")

        if operation == IOOperation.READ:
            self.nodeName = UnicodeString.new_unicodestring()
            self.nodeTransform = TransformMatrix.new_transform_matrix()

        self.nodeName.from_to_file(io, operation)
        
        self.nodeTransform.from_to_file(io, operation)

        self.some_short = io_short(io, self.some_short, operation)

        self.cylinderRadius = io_float(io, self.cylinderRadius, operation)
        self.cylinderHeight = io_float(io, self.cylinderHeight, operation)    

class FileRef():
    fileKey:UnicodeString
    fileName:UnicodeString
    fileTransform:TransformMatrix
    some_short:int
    
    def __init__(self, 
                    fileKey:UnicodeString,
                    fileName:UnicodeString,
                    fileTransform:TransformMatrix,
                    some_short:int):
        self.fileKey = fileKey
        self.fileName = fileName
        self.fileTransform = fileTransform
        self.some_short = some_short
    def new_file_ref():
        return FileRef(None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print("from_to_file fileref")
        if operation == IOOperation.READ:
            self.fileKey = UnicodeString.new_unicodestring()
            self.fileName = UnicodeString.new_unicodestring()
            self.fileTransform = TransformMatrix.new_transform_matrix()

        self.fileName.from_to_file(io, operation)
        self.fileKey.from_to_file(io, operation)
        
        self.fileTransform.from_to_file(io, operation)
        self.some_short = io_short(io, self.some_short, operation)

class EFLine():
    lineName:UnicodeString
    lineAction:int
    lineStart:Vec3d
    lineEnd:Vec3d
    lineDir:Vec3d
    parentIndex:int
    
    def __init__(self, 
                    lineName:UnicodeString,
                    lineAction:int,
                    lineStart:Vec3d,
                    lineEnd:Vec3d,
                    lineDir:Vec3d,
                    parentIndex:int):
        self.lineName = lineName
        self.lineAction = lineAction
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.lineDir = lineDir
        self.parentIndex = parentIndex
    def new_ef_line():
        return EFLine(None, None, None, None, None, -1)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if debug:
            print("from_to_file efline")
        if operation == IOOperation.READ:
            self.lineName = UnicodeString.new_unicodestring()
            self.lineStart = Vec3d.new_vec3d()
            self.lineEnd = Vec3d.new_vec3d()
            self.lineDir = Vec3d.new_vec3d()
        self.lineName.from_to_file(io, operation)
        
        if debug:
            print(f"Reading {self.lineName}")
        
        self.lineAction = io_int(io, self.lineAction, operation)
        
        self.lineStart.from_to_file(io, operation)
        self.lineEnd.from_to_file(io, operation)
        self.lineDir.from_to_file(io, operation)

        self.parentIndex = io_int(io, self.parentIndex, operation)
        print("Parent index", self.parentIndex)

        if debug:
            print(f"line {self.lineName.value}, parent {self.parentIndex}")
            print(f"start {self.lineStart.x}, {self.lineStart.y}, {self.lineStart.z}")
            print(f"End {self.lineEnd.x}, {self.lineEnd.y}, {self.lineEnd.z}")
            print(f"Dir {self.lineDir.x}, {self.lineDir.y}, {self.lineDir.z}")

class VFXAttachment():
    numIndices:int
    dataIndices:List[int]
    
    def __init__(self, 
                    numIndices:int,
                    dataIndices:List[int]):
        self.numIndices = numIndices
        self.dataIndices = dataIndices
    def new_vfx_attachment():
        return VFXAttachment(None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if operation == IOOperation.READ:
            self.dataIndices = []

        self.numIndices = io_int(io, self.numIndices, operation)

        for i in range(self.numIndices):
            if operation == IOOperation.READ:
                self.dataIndices.append(0.)
                self.dataIndices[i] = io_short(io, self.dataIndices[i], operation)
            else:
                self.dataIndices[i] = io_short(io, self.dataIndices[i], operation)
        

class DestructLevel():

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
    numNogo:int
    dataNogo:List[NogoZone]
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
    numActionVFX:int
    ActionVFX:List[TechNode]
    numAttActionVFX:int
    attActionVFX:List[VFXAttachment]

    def __init__(self, 
                    destructName:UnicodeString,
                    destructIndex:int,
                    collision3dMesh:Collision3D,
                    numWindows:int,
                    collision3dWindows:List[Collision3D],
                    numDoors:int,
                    collision3dDoors:List[Collision3D],
                    numSpecial:int,
                    collision3dSpecial:List[Collision3D],
                    numLines:int,
                    dataLines:List[LineNode],
                    numNogo:int,
                    dataNogo:List[NogoZone],
                    numPipes:int,
                    dataPipes:List[LineNode],
                    platforms:Platform,
                    numCannons:int,
                    dataCannons:List[TechNode],
                    numArrowEmitters:int,
                    dataArrowEmitters:List[TechNode],
                    numDockingPoints:int,
                    dataDockingPoints:List[TechNode],
                    numSoftCollisions:int,
                    dataSoftCollisions:List[SoftCollision],
                    numFileRefs:int,
                    dataFileRefs:List[FileRef],
                    numEFLines:int,
                    dataEFLines:List[EFLine],
                    numActionVFX:int,
                    ActionVFX:List[TechNode],
                    numAttActionVFX:int,
                    attActionVFX:List[VFXAttachment]):
        self.destructName = destructName 
        self.destructIndex = destructIndex 
        self.collision3dMesh = collision3dMesh 
        self.numWindows = numWindows 
        self.collision3dWindows = collision3dWindows
        self.numDoors = numDoors 
        self.collision3dDoors = collision3dDoors
        self.numSpecial = numSpecial 
        self.collision3dSpecial = collision3dSpecial
        self.numLines = numLines 
        self.dataLines = dataLines
        self.numNogo = numNogo
        self.dataNogo = dataNogo
        self.numPipes = numPipes 
        self.dataPipes = dataPipes
        self.platforms = platforms 
        self.numCannons = numCannons 
        self.dataCannons = dataCannons
        self.numArrowEmitters = numArrowEmitters 
        self.dataArrowEmitters = dataArrowEmitters
        self.numDockingPoints = numDockingPoints 
        self.dataDockingPoints = dataDockingPoints
        self.numSoftCollisions = numSoftCollisions 
        self.dataSoftCollisions = dataSoftCollisions
        self.numFileRefs = numFileRefs 
        self.dataFileRefs = dataFileRefs
        self.numEFLines = numEFLines 
        self.dataEFLines = dataEFLines
        self.numActionVFX = numActionVFX
        self.ActionVFX = ActionVFX
        self.numAttActionVFX = numAttActionVFX
        self.attActionVFX = attActionVFX
    def new_destruct_level():
        return DestructLevel(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None, 
                             None, None, None, 0, None,
                             0, None)
    
    def from_to_file(self, io:IO, operation:IOOperation, version = 11, has_vfx = False):
        if debug:
            print("from_to_file destruct level")
        if operation == IOOperation.READ:
            self.collision3dWindows = []
            self.collision3dDoors = []
            self.collision3dSpecial = []
            self.dataLines = []
            self.dataNogo = []
            self.dataPipes = []
            self.dataCannons = []
            self.dataArrowEmitters = []
            self.dataDockingPoints = []
            self.dataSoftCollisions = []
            self.dataFileRefs = []
            self.dataEFLines = []

            self.destructName = UnicodeString.new_unicodestring()
            self.collision3dMesh = Collision3D.new_collision_3d()
            
            self.ActionVFX = []
            self.attActionVFX = []

        self.destructName.from_to_file(io, operation)
        self.destructIndex = io_int(io, self.destructIndex, operation)

        self.collision3dMesh.from_to_file(io, operation)

        self.numWindows = io_int(io, self.numWindows, operation)
        if debug:
            print(f"reading {self.numWindows} windows at {hex(io.tell())}")
        for _ in range(self.numWindows):
            if operation == IOOperation.READ:
                self.collision3dWindows.append(Collision3D.new_collision_3d())
            
            self.collision3dWindows[-1].from_to_file(io, operation)

        self.numDoors = io_int(io, self.numDoors, operation)
        if debug:
            print(f"reading {self.numDoors} doors at {hex(io.tell())}")
        for _ in range(self.numDoors):
            if operation == IOOperation.READ:
                self.collision3dDoors.append(Collision3D.new_collision_3d())
            
            self.collision3dDoors[-1].from_to_file(io, operation)

        self.numSpecial = io_int(io, self.numSpecial, operation)
        if debug:
            print(f"reading {self.numSpecial} special at {hex(io.tell())}")
        for _ in range(self.numSpecial):
            if operation == IOOperation.READ:
                self.collision3dSpecial.append(Collision3D.new_collision_3d())
                self.collision3dSpecial.append(Collision3D.new_collision_3d())
            
            self.collision3dSpecial[-2].from_to_file(io, operation)
            self.collision3dSpecial[-1].from_to_file(io, operation)

        self.numLines = io_int(io, self.numLines, operation)
        if debug:
            print(f"reading {self.numLines} lines at {hex(io.tell())}")
        for _ in range(self.numLines):
            if operation == IOOperation.READ:
                self.dataLines.append(LineNode.new_line_node())
            
            self.dataLines[-1].from_to_file(io, operation)

        self.numPipes = io_int(io, self.numPipes, operation)
        if debug:
            print(f"reading {self.numPipes} pipes at {hex(io.tell())}")
        for _ in range(self.numPipes):
            if operation == IOOperation.READ:
                self.dataPipes.append(LineNode.new_line_node())
            
            self.dataPipes[-1].from_to_file(io, operation)
        
        self.numNogo = io_int(io, self.numNogo, operation)
        if debug:
            print(f"reading {self.numNogo} noGo at {hex(io.tell())}")
        for i in range(self.numNogo):
            if operation == IOOperation.READ:
                self.dataNogo.append(NogoZone.new_nogo_zone())
            
            self.dataNogo[i].from_to_file(io, operation)

        if debug:
            print("platform")
        if operation == IOOperation.READ:
            self.platforms = Platform.new_platform()
        self.platforms.from_to_file(io, operation)

        if debug:
            print("OPERATION")
        if operation == IOOperation.READ:
            self.destruct_bbox:BoundingBox = BoundingBox.new_bounding_box()
        self.destruct_bbox.from_to_file(io, operation)

        self.numCannons = io_int(io, self.numCannons, operation)
        if debug:
            print(f"reading {self.numDoors} doors at {hex(io.tell())}")
        for i in range(self.numCannons):
            if operation == IOOperation.READ:
                self.dataCannons.append(TechNode.new_tech_node())
            
            self.dataCannons[i].from_to_file(io, operation)
        
        self.numArrowEmitters = io_int(io, self.numArrowEmitters, operation)
        if debug:
            print(f"reading {self.numArrowEmitters} ArrowEmitters")
        for i in range(self.numArrowEmitters):
            if operation == IOOperation.READ:
                self.dataArrowEmitters.append(TechNode.new_tech_node())
            
            self.dataArrowEmitters[i].from_to_file(io, operation)
        
        self.numDockingPoints = io_int(io, self.numDockingPoints, operation)
        if debug:
            print(f"reading {self.numDockingPoints} DockingPoints")
        for i in range(self.numDockingPoints):
            if operation == IOOperation.READ:
                self.dataDockingPoints.append(TechNode.new_tech_node())
            
            self.dataDockingPoints[i].from_to_file(io, operation)
        
        self.numSoftCollisions = io_int(io, self.numSoftCollisions, operation)
        if debug:
            print(f"reading {self.numSoftCollisions} SoftCollisions")
        for i in range(self.numSoftCollisions):
            if operation == IOOperation.READ:
                self.dataSoftCollisions.append(SoftCollision.new_soft_collision())
            
            self.dataSoftCollisions[i].from_to_file(io, operation)
        
        someArray = io_int(io, 0, operation)
        if someArray > 0:
            raise ValueError("Unknown data detected.")

        self.numFileRefs = io_int(io, self.numFileRefs, operation)
        if debug:
            print(f"reading {self.numFileRefs} FileRefs")
        for i in range(self.numFileRefs):
            if operation == IOOperation.READ:
                self.dataFileRefs.append(FileRef.new_file_ref())
            
            self.dataFileRefs[i].from_to_file(io, operation)
        
        self.numEFLines = io_int(io, self.numEFLines, operation)
        if debug:
            print(f"reading {self.numEFLines} EFLines")
        for i in range(self.numEFLines):
            if operation == IOOperation.READ:
                self.dataEFLines.append(EFLine.new_ef_line())
            
            self.dataEFLines[i].from_to_file(io, operation)
        
        someArray = io_int(io, 0, operation)
        if someArray > 0:
            raise ValueError("Unknown data detected.")
        
        
        # if operation == IOOperation.READ:
        #     print(f"VFX start {hex(io.tell())}")
        #     current_position = io.tell()

        #     has_vfx = io_int(io, 0, operation) != 0

        #     io.seek(current_position)
        
        # if operation == IOOperation.WRITE:
        #     has_vfx = True

        if has_vfx:
            if debug:
                print("Starting to read/write VFX")
            self.numActionVFX = io_int(io, self.numActionVFX, operation)
            if debug:
                print(f"Found {self.numActionVFX} ActionVFX")
            for i in range(self.numActionVFX):
                if operation == IOOperation.READ:
                    self.ActionVFX.append(TechNode.new_tech_node())
                
                self.ActionVFX[i].from_to_file(io, operation)
            
            self.numActionVFX = io_int(io, self.numActionVFX, operation)
            for i in range(self.numActionVFX):
                if operation == IOOperation.READ:
                    self.ActionVFX.append(TechNode.new_tech_node())
                
                self.ActionVFX[i].from_to_file(io, operation)
                

            
            self.numAttActionVFX = io_int(io, self.numAttActionVFX, operation)
            for i in range(self.numAttActionVFX):
                if operation == IOOperation.READ:
                    self.attActionVFX.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX[i].from_to_file(io, operation)
            
            self.numAttActionVFX = io_int(io, self.numAttActionVFX, operation)
            for i in range(self.numAttActionVFX):
                if operation == IOOperation.READ:
                    self.attActionVFX.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX[i].from_to_file(io, operation)
        
        

class BuildingPiece():
    pieceName:UnicodeString
    placementNode:TechNode
    parentIndex:int
    destructCount:int
    destructs:List[DestructLevel]
    def __init__(self, 
                    pieceName:UnicodeString,
                    placementNode:TechNode,
                    parentIndex:int,
                    destructCount:int,
                    destructs:List[DestructLevel]):
        self.pieceName = pieceName
        self.placementNode = placementNode
        self.parentIndex = parentIndex
        self.destructCount = destructCount
        self.destructs = destructs
    def new_building_piece():
        return BuildingPiece(None, None, -1, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11, has_vfx = False):
        if debug:
            ("from_to_file buildingpiece")
        if operation == IOOperation.READ:
            self.destructs = []
            self.pieceName = UnicodeString.new_unicodestring()
            self.placementNode = TechNode.new_tech_node()

        self.pieceName.from_to_file(io, operation)
        
        self.placementNode.from_to_file(io, operation)
        
        self.parentIndex = io_int(io, self.parentIndex, operation)
        print("Parent index", self.parentIndex)
        self.destructCount = io_int(io, self.destructCount, operation)

        if debug:
            print(f"Loading {self.destructCount} destruct level at {hex(io.tell())}.")
        for i in range(self.destructCount):
            if operation == IOOperation.READ:
                self.destructs.append(DestructLevel.new_destruct_level())
                self.destructs[i].from_to_file(io, operation, has_vfx = has_vfx)
            else:
                self.destructs[i].from_to_file(io, operation, has_vfx = has_vfx)
                
        array_size = io_int(io, 0, operation)

        if array_size > 0:
            raise ValueError("Unknown array detected.")

class Cs2File:
    version:int
    bbox:BoundingBox
    flag:TechNode
    piece_count:int
    building_pieces:List[BuildingPiece]
    def __init__(self,
        version:int,
        bbox:BoundingBox,
        flag:TechNode,
        piece_count:int,
        building_pieces:List[BuildingPiece]):
        self.version = version
        self.bbox = bbox
        self.flag = flag
        self.piece_count = piece_count
        self.building_pieces = building_pieces
    def new_cs2file():
        return Cs2File(None, None, None, None, None)
    def read_write_file(self, file_path:str, operation:IOOperation, has_vfx = False):
        file_open_type = "rb" if operation == IOOperation.READ else "wb"

        if operation == IOOperation.READ:
            print(f"Starting to read file : {file_path}")
        else:
            print(f"Starting to write file : {file_path}")

        with open(file_path, file_open_type) as f:
            self.version = io_int(f, self.version, operation)
            print(f"Version found : {self.version}")

            if not self.version in [11, 13]:
                raise ValueError(f"Version {self.version} is not supported.")

            if operation == IOOperation.READ:
                self.bbox = BoundingBox.new_bounding_box()
            self.bbox.from_to_file(f, operation, version = self.version)

            if operation == IOOperation.READ:
                self.flag = TechNode.new_tech_node()
            self.flag.from_to_file(f, operation, version = self.version)

            some_array_size = io_int(f, 0, operation)
            if some_array_size > 0:
                raise ValueError("Unknown data detected.")
            
            self.piece_count = io_int(f, self.piece_count, operation)
            if debug:
                print(f"Reading {self.piece_count} pieces.")
            
            if operation == IOOperation.READ:
                self.building_pieces = []
                for _ in range(self.piece_count):
                    self.building_pieces.append(BuildingPiece.new_building_piece())

            for i in range(self.piece_count):
                self.building_pieces[i].from_to_file(f, operation, version=self.version, has_vfx=has_vfx)
    
if __name__ == "__main__":
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\30_30_10\\30_30_10_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\arena\\arena_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\athens_acropolis\\athens_acropolis_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\attila_cliff_01\\attila_cliff_01_tech.cs2.parsed")
    cs2 = Cs2File.new_cs2file()

    has_ = True

    try:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=True)
    except struct.error:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=False)
        has_ = False
        