
import math
import struct
from pathlib import Path
from typing import IO, Any, List

import numpy as np

from src.io_elementary import IOOperation, io_bytes, io_float, io_int, io_str, io_short, UnicodeString, Vec2d, Vec3d, SomeBytes

debug = False

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
    def __eq__(self, other:'BoundingBox'):
        return  self.minX == other.minX and \
                self.minY == other.minY and \
                self.minZ == other.minZ and \
                self.maxX == other.maxX and \
                self.maxY == other.maxY and \
                self.maxZ == other.maxZ
    def __repr__(self,):
        return f"BoundingBox ([{self.minX}, {self.maxX}], [{self.minY}, {self.maxY}], [{self.minZ}, {self.maxZ}])"

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

    def __eq__(self, other:'TransformMatrix'):
        are_equal = abs(self.row0_col0 - other.row0_col0) < 1e-5 and \
                    abs(self.row1_col0 - other.row1_col0) < 1e-5 and \
                    abs(self.row2_col0 - other.row2_col0) < 1e-5 and \
                    abs(self.row3_col0 - other.row3_col0) < 1e-5 and \
                    abs(self.row0_col1 - other.row0_col1) < 1e-5 and \
                    abs(self.row1_col1 - other.row1_col1) < 1e-5 and \
                    abs(self.row2_col1 - other.row2_col1) < 1e-5 and \
                    abs(self.row3_col1 - other.row3_col1) < 1e-5 and \
                    abs(self.row0_col2 - other.row0_col2) < 1e-5 and \
                    abs(self.row1_col2 - other.row1_col2) < 1e-5 and \
                    abs(self.row2_col2 - other.row2_col2) < 1e-5 and \
                    abs(self.row3_col2 - other.row3_col2) < 1e-5 and \
                    abs(self.row0_col3 - other.row0_col3) < 1e-5 and \
                    abs(self.row1_col3 - other.row1_col3) < 1e-5 and \
                    abs(self.row2_col3 - other.row2_col3) < 1e-5 and \
                    abs(self.row3_col3 - other.row3_col3) < 1e-5 

        if not are_equal:
            print(self)
            print(other)
            return False
        return True
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
    def __eq__(self, other:'TechNode'):
        
        for param in ["nodeName", "NodeTransform"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"TechNode have different {param}, found \n{self.__getattribute__(param)} and \n{other.__getattribute__(param)}")
                return False
        return True


class FaceEdge():
    vertexIndex0:int
    vertexIndex1:int
    faceIndex:int
    edgeIndex:int
    neighbourFaceIndex:int
    def __init__(self, 
                    vertexIndex0:int,
                    vertexIndex1:int,
                    faceIndex:int,
                    edgeIndex:int,
                    neighbourFaceIndex:int):
        self.vertexIndex0 = vertexIndex0
        self.vertexIndex1 = vertexIndex1
        self.faceIndex = faceIndex
        self.edgeIndex = edgeIndex
        self.neighbourFaceIndex = neighbourFaceIndex
    def new_face_edge():
        return FaceEdge(None, None, None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.vertexIndex0 = io_int(io, self.vertexIndex0, operation)
        self.vertexIndex1 = io_int(io, self.vertexIndex1, operation)
        self.faceIndex = io_int(io, self.faceIndex, operation)
        self.edgeIndex = io_int(io, self.edgeIndex, operation)
        self.neighbourFaceIndex = io_int(io, self.neighbourFaceIndex, operation)

        if debug:
            print(self)
    def __repr__(self):
        return f"FaceEdge : {self.vertexIndex0}, {self.vertexIndex1}, {self.faceIndex}, {self.edgeIndex}, {self.neighbourFaceIndex}"
    def __eq__(self, other:'FaceEdge'):
        return self.vertexIndex0 == other.vertexIndex0 and \
                self.vertexIndex1 == other.vertexIndex1 and\
                self.edgeIndex  == other.edgeIndex  and\
                self.faceIndex == other.faceIndex  and\
                self.neighbourFaceIndex == other.neighbourFaceIndex
    
class FaceEdgeData():
    edge0:FaceEdge
    edge1:FaceEdge
    edge2:FaceEdge
    someint:int = 0
    def __init__(self, 
                    edge0:FaceEdge,
                    edge1:FaceEdge,
                    edge2:FaceEdge):
        self.edge0 = edge0
        self.edge1 = edge1
        self.edge2 = edge2
    def new_face_edge_data():
        return FaceEdgeData(None, None, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        if operation == IOOperation.READ:
            self.edge0 = FaceEdge.new_face_edge()
            self.edge1 = FaceEdge.new_face_edge()
            self.edge2 = FaceEdge.new_face_edge()
        self.edge0.from_to_file(io, operation)
        self.edge1.from_to_file(io, operation)
        self.edge2.from_to_file(io, operation)
        self.someint = io_int(io, self.someint, operation)
    def __repr__(self):
        return f"FaceEdgeData :\n     {self.edge0},\n     {self.edge1},\n     {self.edge2}"
    def __eq__(self, other:'FaceEdgeData'):
        return self.edge0 == other.edge0 and \
                self.edge1 == other.edge1 and\
                self.edge2 == other.edge2

class Face():
    faceIndex:int
    vertIndex0:int
    vertIndex1:int
    vertIndex2:int
    edgeData:FaceEdgeData
    padding=SomeBytes(1, b"\x00")

    def __init__(self, 
                    faceIndex:int,
                    vertIndex0:int,
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

    def __repr__(self,):
        return f"Face index {self.faceIndex} :\n     {self.padding.value}\n     {self.vertIndex0}\n     {self.vertIndex1}\n     {self.vertIndex2} \n{self.edgeData}"

    def __eq__(self, other:'Face'):
        return  self.faceIndex == other.faceIndex and \
                self.vertIndex0 == other.vertIndex0 and\
                self.vertIndex1  == other.vertIndex1  and\
                self.vertIndex2 == other.vertIndex2 and \
                self.edgeData == other.edgeData

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
        if debug:
            print(f"collision 3D node index {self.nodeIndex}")
        self.unknown2 = io_int(io, self.unknown2, operation)

        self.numVerts = io_int(io, self.numVerts, operation)
        if debug:
            print(f"collision 3D num verts {self.numVerts}")
        
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
                
    def __eq__(self, other:'Collision3D'):
        # Not testing nodeIndex.
        for param in ["collisionName", "unknown2", "numVerts", "numFaces"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"Collision3D have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.dataVerts)):
            if self.dataVerts[i] != other.dataVerts[i]:
                print(f"Collision3D have different vertex {i}, found {self.dataVerts[i]} and {other.dataVerts[i]}")
                return False
            
        for i in range(len(self.dataFaces)):
            if self.dataFaces[i] != other.dataFaces[i]:
                print(f"Collision3D have different face {i}, found {self.dataFaces[i]} and {other.dataFaces[i]}")
                return False
        return True


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
        
    def __eq__(self, other:'LineNode'):
        for param in ["lineName", "numVerts", "lineType"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"LineNode have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.dataVerts)):
            if self.dataVerts[i] != other.dataVerts[i]:
                print(f"LineNode have different vertex {i}")
                return False
            
        return True

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
                
    def __eq__(self, other:'NogoZone'):
        for param in ["numLines", "numLinesConnected"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"LineNode have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.dataLines)):
            if self.dataLines[i] != other.dataLines[i]:
                print(f"LineNode have different vertex {i}")
                return False
            
        return True

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

    def __eq__(self, other:'Polygon'):
        for param in ["numVerts", "isPlatformGround"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"Polygons have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
            
        if sum([self.normal.x * other.normal.x, self.normal.y * other.normal.y, self.normal.z * other.normal.z ]) < 0.95:
                print(f"Polygons have different notmals, found {self.normal} and {other.normal}")
                return False


        self_np_polygon_list = [[vert.x, vert.y, vert.z] for vert in self.dataVerts]
        other_np_polygon_list = [[vert.x, vert.y, vert.z] for vert in other.dataVerts]

        unique_self_np_polygon_list = np.unique(self_np_polygon_list, axis=0)
        unique_other_np_polygon_list = np.unique(other_np_polygon_list, axis=0)

        for vert in unique_self_np_polygon_list:
            valid = False
            min_distance = 1
            for vert2 in unique_other_np_polygon_list:
                distance = math.sqrt(sum([math.pow(vert[0] - vert2[0], 2), math.pow(vert[1] - vert2[1], 2), math.pow(vert[2] - vert2[2], 2)]))
                min_distance = min(min_distance, distance)
                if distance < 1e-4:
                    valid = True
                    break
            if not valid:
                print(f"Polygons have different vertices, found {unique_self_np_polygon_list} and {unique_other_np_polygon_list}, minimum distance =", min_distance)
                return False
            
        return True

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


    def __eq__(self, other:'Platform'):
        for param in ["numPolygons", "some_int"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"Platform have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        polygon_index = 0
        for polygon in self.dataPolygons:
            valid = False
            for polygon2 in other.dataPolygons:
                if polygon == polygon2:
                    valid = True
                    break
            if not valid:
                print(f"Polygon {polygon} not found in other platform.")
                return False

            polygon_index += 1
        # if not set(self.dataPolygons) == set(other.dataPolygons):
        #     HASH
        #     print(f"Platform have different polygons, found {self.dataPolygons} and {other.dataPolygons}")
            # return False
        # for i in range(len(self.dataPolygons)):

        #     for polygon in self.dataPolygons:
        #         if not polygon in other.dataPolygons:
        #             print(f"Polygon {i} not found in other platform.")
        #             return False
            # if self.dataPolygons[i] != other.dataPolygons[i]:
            #     print(f"Platform have different polygon {i}")
            #     return False
            
        return True
    

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

    def __repr__(self):
        return f"SoftCollision {self.nodeName.value} : \n    r {self.cylinderRadius}\n    h {self.cylinderHeight}\n    matrix \n{self.nodeTransform}"

    
    def __eq__(self, other:'SoftCollision'):
        # not testing someshort
        for param in ["nodeName", "nodeTransform", "cylinderRadius", "cylinderHeight", ]: #, "some_short"
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"SoftCollision have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
            
        return True
    
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

    def __eq__(self, other:'FileRef'):
        for param in ["fileKey", "fileName", "fileTransform"]:#, "some_short"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"FileRef have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
            
        return True

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

        if True or debug:
            print(f"line {self.lineName.value}, parent {self.parentIndex}, lineAction {self.lineAction}")
            print(f"start {self.lineStart.x}, {self.lineStart.y}, {self.lineStart.z}")
            print(f"End {self.lineEnd.x}, {self.lineEnd.y}, {self.lineEnd.z}")
            print(f"Dir {self.lineDir.x}, {self.lineDir.y}, {self.lineDir.z}")
    def __eq__(self, other:'EFLine'):
        # not testing lineaction and parent index
        for param in ["lineName", "lineStart", "lineEnd"]:#, "lineAction", "parentIndex"
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"EFLine have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        if abs(other.lineDir.x - self.lineDir.x) + abs(other.lineDir.y - self.lineDir.y) + abs(other.lineDir.z - self.lineDir.z) > 1e-2:
                print(f"EFLine have different lineDir, found {self.__getattribute__('lineDir')} and {other.__getattribute__('lineDir')}")
                return False
            
        return True




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

    def __eq__(self, other:'VFXAttachment'):
        for param in ["numIndices"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"VFXAttachment have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.dataIndices)):
            if self.dataIndices[i] != other.dataIndices[i]:
                print(f"VFXAttachment have different index {i}")
                return False
            
        return True
    
        

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
    bounding_box:BoundingBox
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
    numActionVFX2:int
    ActionVFX2:List[TechNode]
    numAttActionVFX:int
    attActionVFX:List[VFXAttachment]
    numAttActionVFX2:int
    attActionVFX2:List[VFXAttachment]

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
                    bounding_box:BoundingBox,
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
                    numActionVFX2:int,
                    ActionVFX2:List[TechNode],
                    numAttActionVFX:int,
                    attActionVFX:List[VFXAttachment],
                    numAttActionVFX2:int,
                    attActionVFX2:List[VFXAttachment]):
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
        self.bounding_box = bounding_box
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
        self.numActionVFX2 = numActionVFX2
        self.ActionVFX2 = ActionVFX2
        self.numAttActionVFX = numAttActionVFX
        self.attActionVFX = attActionVFX
        self.numAttActionVFX2 = numAttActionVFX2
        self.attActionVFX2 = attActionVFX2

    def new_destruct_level():
        return DestructLevel(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,None,
                             None, None, None, None, None,
                             None, None, None, None, None, 
                             None, None, None, 0, None, 0, None,
                             0, None,
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
            self.ActionVFX2 = []
            self.attActionVFX2 = []

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

        if operation == IOOperation.READ:
            self.platforms = Platform.new_platform()
        self.platforms.from_to_file(io, operation)

        if operation == IOOperation.READ:
            self.bounding_box:BoundingBox = BoundingBox.new_bounding_box()
        self.bounding_box.from_to_file(io, operation)

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
            
            self.numActionVFX2 = io_int(io, self.numActionVFX2, operation)
            for i in range(self.numActionVFX2):
                if operation == IOOperation.READ:
                    self.ActionVFX2.append(TechNode.new_tech_node())
                
                self.ActionVFX2[i].from_to_file(io, operation)
                

            
            self.numAttActionVFX = io_int(io, self.numAttActionVFX, operation)
            for i in range(self.numAttActionVFX):
                if operation == IOOperation.READ:
                    self.attActionVFX.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX[i].from_to_file(io, operation)
            
            self.numAttActionVFX2 = io_int(io, self.numAttActionVFX2, operation)
            for i in range(self.numAttActionVFX2):
                if operation == IOOperation.READ:
                    self.attActionVFX2.append(VFXAttachment.new_vfx_attachment())
                
                self.attActionVFX2[i].from_to_file(io, operation)
        
    def __eq__(self, other:'DestructLevel'):
        for param in ["destructName", "destructIndex", "collision3dMesh", "numWindows", "numDoors", "numSpecial", "numLines", "numNogo", "numPipes", "platforms", "bounding_box", "numCannons", "numArrowEmitters", "numDockingPoints", "numSoftCollisions", "numFileRefs", "numEFLines", "numActionVFX", "numActionVFX2"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"DestructLevel have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        #   Not comparing the vfx attachments
        for param in ["collision3dWindows", "collision3dDoors", "collision3dSpecial", "dataLines", "dataNogo", "dataPipes", "dataCannons", "dataArrowEmitters", "dataDockingPoints", "dataSoftCollisions", "dataFileRefs", "dataEFLines", "ActionVFX", "ActionVFX2"]:    
            if len(self.__getattribute__(param)) != len(other.__getattribute__(param)):
                print(f"Params {param} have different length, found {len(self.__getattribute__(param))} and {len(other.__getattribute__(param))}")
            for i in range(len(self.__getattribute__(param))):
                
                if self.__getattribute__(param)[i] != other.__getattribute__(param)[i]:
                    print(f"DestructLevel have different {param}, found {self.__getattribute__(param)[i]} and {other.__getattribute__(param)[i]}")
                    return False
            
        return True
        
    def __repr__(self,):
        return f"Destruct of name {self.destructName}, index {self.destructIndex}, with:\n"+\
                f" - {self.numWindows} Windows;\n"+\
                f" - {self.numDoors} Doors;\n"+\
                f" - {self.numSpecial} Special;\n"+\
                f" - {self.numLines} Lines;\n"+\
                f" - {self.numNogo} Nogo;\n"+\
                f" - {self.numPipes} Pipes;\n"+\
                f" - {self.numCannons} Cannons;\n"+\
                f" - {self.numArrowEmitters} ArrowEmitters;\n"+\
                f" - {self.numDockingPoints} DockingPoints;\n"+\
                f" - {self.numSoftCollisions} SoftCollisions;\n"+\
                f" - {self.numFileRefs} FileRefs;\n"+\
                f" - {self.numEFLines} EFLines;\n"+\
                f" - {self.numActionVFX} ActionVFX;\n"+\
                f" - {self.numActionVFX2} ActionVFX2;\n"+\
                f" - {self.numAttActionVFX} AttActionVFX;\n"+\
                f" - {self.numAttActionVFX2} AttActionVFX2;\n"

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
    def __eq__(self, other:'BuildingPiece'):
        for param in ["pieceName", "placementNode", "parentIndex", "destructCount"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"BuildingPiece have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.destructs)):
            if self.destructs[i] != other.destructs[i]:
                print(f"BuildingPiece have different destructs {i}")
                return False
            
        return True


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
    def __eq__(self, other:'Cs2File'):
        for param in ["version",    "bbox",    "flag",    "piece_count"]:
            if self.__getattribute__(param) != other.__getattribute__(param):
                print(f"Cs2File have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
                return False
        
        for i in range(len(self.building_pieces)):
            if self.building_pieces[i] != other.building_pieces[i]:
                print(f"Cs2File have different BuildingPiece {i}")
                return False
            
        return True

    
if __name__ == "__main__":
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\30_30_10\\30_30_10_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\arena\\arena_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\attila_cliff_01\\attila_cliff_01_tech.cs2.parsed")
    input_path = Path("F:\\Workspace\\TotalWarModding\\files\\cs2_parsed\\athens_acropolis\\athens_acropolis_tech.cs2.parsed")
    cs2 = Cs2File.new_cs2file()

    has_ = True

    try:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=True)
    except struct.error:
        cs2.read_write_file(input_path.absolute(), 
                                IOOperation.READ, has_vfx=False)
        has_ = False
        