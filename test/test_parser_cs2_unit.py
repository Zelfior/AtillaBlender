import os
import glob
from pathlib import Path

package_path = Path(__file__).absolute().parent.parent

from src.cs2_parsed_io import Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString, Vec2d, Vec3d, Polygon, FaceEdgeData, FaceEdge

from src.io_elementary import IOOperation

os.makedirs("garbage", exist_ok=True,)
os.makedirs("garbage/test_generated_files", exist_ok=True,)

files = glob.glob('garbage/test_generated_files/*')
for f in files:
    if os.path.isfile(f):
        os.remove(f)

"""

    The files present in files/unit_test_cs2_parsed were writen with a module version that could read/write all of fileS/cs2_parsed files.


"""

def compare_binaries(input_path_reference, file_name):
    with open(input_path_reference.absolute(), "rb") as ref_file:
        with open(file_name, "rb") as output_file:
            i = 0
            past_position = -1
            while True:
                ref_byte = ref_file.read(1)
                output_byte = output_file.read(1)

                if ref_file.tell() == past_position:
                    break
                else:
                    past_position = ref_file.tell()

                if ref_byte == output_byte:
                    i += 1
                else:
                    assert False, f"Error at position {i} : {hex(i)}, ref {ref_byte}, found {output_byte}"
            
            print("Both files are identical")
            assert True




def test_read_vec2d(file_path = package_path/"files/unit_test_cs2_parsed/vec2d.cs2.parsed"):
    
    v = Vec2d.new_vec2d()
    with open(file_path, "rb") as f:
        v.from_to_file(f, IOOperation.READ)

        assert v.x == 5.
        assert v.y == 12.

def test_write_vec2d():
    file_path = package_path/"garbage/test_generated_files/vec2d.cs2.parsed"

    v = Vec2d(5, 12.)

    with open(file_path, "wb") as f:
        v.from_to_file(f, IOOperation.WRITE)

    test_read_vec2d(file_path=file_path)






def test_read_vec3d(file_path = package_path/"files/unit_test_cs2_parsed/vec2d.cs2.parsed"):
    
    v = Vec3d.new_vec3d()
    with open(file_path, "rb") as f:
        v.from_to_file(f, IOOperation.READ)

        assert v.x == 5.
        assert v.y == 12.
        assert v.z == 17.

def test_write_vec3d():
    file_path = package_path/"garbage/test_generated_files/vec2d.cs2.parsed"

    v = Vec3d(5, 12., 17.)

    with open(file_path, "wb") as f:
        v.from_to_file(f, IOOperation.WRITE)

    test_read_vec3d(file_path=file_path)






def test_read_unicode_string(file_path = package_path/"files/unit_test_cs2_parsed/unicode_string.cs2.parsed"):
    us = UnicodeString.new_unicodestring()
    with open(file_path, "rb") as f:
        us.from_to_file(f, IOOperation.READ)
        assert us.value == "hello world"
        assert us.length == 11

def test_write_unicode_string():
    file_path = package_path/"garbage/test_generated_files/unicode_string.cs2.parsed"

    us = UnicodeString(11, "hello world")
    with open(file_path, "wb") as f:
        us.from_to_file(f, IOOperation.WRITE)

    test_read_unicode_string(file_path=file_path)






def test_read_nogo(file_path = package_path/"files/unit_test_cs2_parsed/no_go.cs2.parsed"):
    
    us = NogoZone.new_nogo_zone()
    with open(file_path, "rb") as f:
        us.from_to_file(f, IOOperation.READ)

        ref = [Vec2d(0., 0.), Vec2d(1., 0.), Vec2d(2., 12.), Vec2d(5.2, 0.), Vec2d(6.3, 1.2)]
        for i in range(5):
            assert abs(us.dataLines[i].x - ref[i].x) < 1e-3
            assert abs(us.dataLines[i].y - ref[i].y) < 1e-3
        assert us.numLines == 5
        assert us.numLinesConnected == list(range(5))

def test_write_nogo():
    file_path = package_path/"garbage/test_generated_files/no_go.cs2.parsed"

    us = NogoZone(5, [Vec2d(0., 0.), Vec2d(1., 0.), Vec2d(2., 12.), Vec2d(5.2, 0.), Vec2d(6.3, 1.2)], list(range(5)))

    with open(file_path, "wb") as f:
        us.from_to_file(f, IOOperation.WRITE)

    test_read_nogo(file_path=file_path)





def test_read_vfx_attachment(file_path = package_path/"files/unit_test_cs2_parsed/vfx_attachment.cs2.parsed"):
    
    va = VFXAttachment.new_vfx_attachment()
    with open(file_path, "rb") as f:
        va.from_to_file(f, IOOperation.READ)

        assert va.dataIndices == [0, 0, 5]
        assert va.numIndices == 3

def test_write_vfx_attachment():
    file_path = package_path/"garbage/test_generated_files/vfx_attachment.cs2.parsed"

    va = VFXAttachment(3, [0, 0, 5])

    with open(file_path, "wb") as f:
        va.from_to_file(f, IOOperation.WRITE)

    test_read_vfx_attachment(file_path=file_path)






def test_read_file_ref(file_path = package_path/"files/unit_test_cs2_parsed/file_ref.cs2.parsed"):
    
    fr = FileRef.new_file_ref()
    with open(file_path, "rb") as f:
        fr.from_to_file(f, IOOperation.READ)

        assert fr.fileKey.value == "hello world"
        assert fr.fileName.value == "hello world2"
        assert fr.fileTransform.to_matrix(transpose=True) == [[int(j) for j in range(4*i, 4*(i+1))] for i in range(4)]
        assert fr.some_short == 1


def test_write_file_ref():
    file_path = package_path/"garbage/test_generated_files/file_ref.cs2.parsed"

    fr = FileRef(UnicodeString(11, "hello world"), UnicodeString(12, "hello world2"), TransformMatrix(*list(range(16))), 1)

    with open(file_path, "wb") as f:
        fr.from_to_file(f, IOOperation.WRITE)

    test_read_file_ref(file_path=file_path)







def test_read_transform_matrix(file_path = package_path/"files/unit_test_cs2_parsed/transform_matrix.cs2.parsed"):
    
    tm = TransformMatrix.new_transform_matrix()
    with open(file_path, "rb") as f:
        tm.from_to_file(f, IOOperation.READ)

        assert tm.to_matrix(transpose=True) == [[int(j) for j in range(4*i, 4*(i+1))] for i in range(4)]


def test_write_transform_matrix():
    file_path = package_path/"garbage/test_generated_files/transform_matrix.cs2.parsed"

    tm = TransformMatrix(*list(range(16)))

    with open(file_path, "wb") as f:
        tm.from_to_file(f, IOOperation.WRITE)

    test_read_transform_matrix(file_path=file_path)








def test_read_soft_collision(file_path = package_path/"files/unit_test_cs2_parsed/soft_collision.cs2.parsed"):
    
    sc = SoftCollision.new_soft_collision()
    with open(file_path, "rb") as f:
        sc.from_to_file(f, IOOperation.READ)

        assert sc.nodeName.value == "hello world"
        assert sc.cylinderRadius == 12.
        assert sc.cylinderHeight == 42.
        assert sc.nodeTransform.to_matrix(transpose=True) == [[int(j) for j in range(4*i, 4*(i+1))] for i in range(4)]


def test_write_soft_collision():
    file_path = package_path/"garbage/test_generated_files/soft_collision.cs2.parsed"

    sc = SoftCollision(UnicodeString(11, "hello world"), TransformMatrix(*list(range(16))), 1, 12., 42.)

    with open(file_path, "wb") as f:
        sc.from_to_file(f, IOOperation.WRITE)

    test_read_soft_collision(file_path=file_path)








def test_read_line_node(file_path = package_path/"files/unit_test_cs2_parsed/line_node.cs2.parsed"):
    
    ln = LineNode.new_line_node()
    with open(file_path, "rb") as f:
        ln.from_to_file(f, IOOperation.READ)

        assert ln.lineName.value == "hello world"
        assert ln.lineType == 13
        assert ln.numVerts == 12

        for i in range(12):
            assert ln.dataVerts[i].x == i
            assert ln.dataVerts[i].y == i+1
            assert ln.dataVerts[i].z == i+2


def test_write_line_node():
    file_path = package_path/"garbage/test_generated_files/line_node.cs2.parsed"

    ln = LineNode(UnicodeString(11, "hello world"), 12, [Vec3d(i, i+1, i+2) for i in range(12)], 13)

    with open(file_path, "wb") as f:
        ln.from_to_file(f, IOOperation.WRITE)

    test_read_line_node(file_path=file_path)






def test_read_tech_node(file_path = package_path/"files/unit_test_cs2_parsed/tech_node.cs2.parsed"):
    
    tn = TechNode.new_tech_node()
    with open(file_path, "rb") as f:
        tn.from_to_file(f, IOOperation.READ)

        assert tn.nodeName.value == "hello world"
        assert tn.NodeTransform.to_matrix(transpose=True) == [[int(j) for j in range(4*i, 4*(i+1))] for i in range(4)]


def test_write_tech_node():
    file_path = package_path/"garbage/test_generated_files/tech_node.cs2.parsed"

    tn = TechNode(UnicodeString(11, "hello world"), TransformMatrix(*list(range(16))))

    with open(file_path, "wb") as f:
        tn.from_to_file(f, IOOperation.WRITE)

    test_read_tech_node(file_path=file_path)







def test_read_bounding_box(file_path = package_path/"files/unit_test_cs2_parsed/bounding_box.cs2.parsed"):
    
    bb = BoundingBox.new_bounding_box()
    with open(file_path, "rb") as f:
        bb.from_to_file(f, IOOperation.READ)

        assert bb.minX == 0.
        assert bb.minY == 1.
        assert bb.minZ == 0.
        assert bb.maxX == 20.
        assert bb.maxY == 12.
        assert bb.maxZ == 43.


def test_write_bounding_box():
    file_path = package_path/"garbage/test_generated_files/bounding_box.cs2.parsed"

    bb = BoundingBox(0., 1., 0., 20, 12, 43)

    with open(file_path, "wb") as f:
        bb.from_to_file(f, IOOperation.WRITE)

    test_read_bounding_box(file_path=file_path)







def test_read_ef_line(file_path = package_path/"files/unit_test_cs2_parsed/ef_line.cs2.parsed"):
    
    ef = EFLine.new_ef_line()
    with open(file_path, "rb") as f:
        ef.from_to_file(f, IOOperation.READ)

        assert ef.lineName.value == "hello world"
        assert ef.parentIndex == 13
        assert ef.lineAction == 12
        
        assert ef.lineStart.x == 0.
        assert ef.lineStart.y == 1.
        assert ef.lineStart.z == 0.
        
        assert ef.lineEnd.x == 5.
        assert ef.lineEnd.y == 1.
        assert ef.lineEnd.z == 3.
        
        assert ef.lineDir.x == 2.
        assert ef.lineDir.y == 2.
        assert ef.lineDir.z == 0.


def test_write_ef_line():
    file_path = package_path/"garbage/test_generated_files/ef_line.cs2.parsed"

    ef = EFLine(UnicodeString(11, "hello world"), 12, Vec3d(0., 1., 0.), Vec3d(5., 1., 3.), Vec3d(2., 2., 0.), 13)

    with open(file_path, "wb") as f:
        ef.from_to_file(f, IOOperation.WRITE)

    test_read_ef_line(file_path=file_path)





def test_read_platform(file_path = package_path/"files/unit_test_cs2_parsed/platform.cs2.parsed"):
    
    pl = Platform.new_platform()
    with open(file_path, "rb") as f:
        pl.from_to_file(f, IOOperation.READ)

        assert pl.numPolygons == 2
        assert pl.some_int == 12
        for p in pl.dataPolygons:
            assert p.numVerts == 3
            assert p.normal.x == 1
            assert p.normal.y == 0
            assert p.normal.z == 2
            
            for v in p.dataVerts:
                assert v.x == 1
                assert v.y == 23
                assert v.z == 12

            assert p.isPlatformGround == True

def test_write_platform():
    file_path = package_path/"garbage/test_generated_files/platform.cs2.parsed"

    pl = Platform(2, [Polygon(Vec3d(1, 0, 2), 3, [Vec3d(1, 23, 12)]*3, True)]*2, 12)

    with open(file_path, "wb") as f:
        pl.from_to_file(f, IOOperation.WRITE)

    test_read_platform(file_path=file_path)










def test_read_face_edge_data(file_path = package_path/"files/unit_test_cs2_parsed/face_edge_data.cs2.parsed"):
    
    fed = FaceEdgeData.new_face_edge_data()
    with open(file_path, "rb") as f:
        fed.from_to_file(f, IOOperation.READ)

        edges = [fed.edge0, fed.edge1, fed.edge2]

        for i in range(3):
            assert edges[i].vertexIndex0 == i
            assert edges[i].vertexIndex1 == i+1
            assert edges[i].faceIndex == i+2
            assert edges[i].edgeIndex == i+3
            assert edges[i].neighbourFaceIndex == i+4


def test_write_face_edge_data():
    file_path = package_path/"garbage/test_generated_files/face_edge_data.cs2.parsed"

    fed = FaceEdgeData(*[FaceEdge(i, i+1, i+2, i+3, i+4) for i in range(3)])

    with open(file_path, "wb") as f:
        fed.from_to_file(f, IOOperation.WRITE)

    test_read_face_edge_data(file_path=file_path)









def test_read_face_edge(file_path = package_path/"files/unit_test_cs2_parsed/face_edge.cs2.parsed"):
    
    fe = FaceEdge.new_face_edge()
    with open(file_path, "rb") as f:
        fe.from_to_file(f, IOOperation.READ)

        assert fe.vertexIndex0 == 12
        assert fe.vertexIndex1 == 13
        assert fe.faceIndex == 42
        assert fe.edgeIndex == 46
        assert fe.neighbourFaceIndex == 12


def test_write_face_edge():
    file_path = package_path/"garbage/test_generated_files/face_edge.cs2.parsed"

    fe = FaceEdge(12, 13, 42, 46, 12)

    with open(file_path, "wb") as f:
        fe.from_to_file(f, IOOperation.WRITE)

    test_read_face_edge(file_path=file_path)



# TODO : Collision3D, BuildingPiece, DestructLevel


if __name__ == "__main__":
    test_read_unicode_string()