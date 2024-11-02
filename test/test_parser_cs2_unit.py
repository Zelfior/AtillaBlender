import os
import glob
from pathlib import Path

package_path = Path(__file__).absolute().parent.parent

from src.cs2_parsed_io import Cs2File, Platform, EFLine, BoundingBox, TechNode, BuildingPiece, TransformMatrix, Collision3D, DestructLevel, LineNode, SoftCollision, FileRef, VFXAttachment, NogoZone, UnicodeString, Vec2d, Vec3d

from src.io_elementary import IOOperation

os.makedirs("garbage", exist_ok=True)

files = glob.glob('garbage/*')
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
    file_path = package_path/"garbage/vec2d.cs2.parsed"

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
    file_path = package_path/"garbage/vec2d.cs2.parsed"

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
    file_path = package_path/"garbage/unicode_string.cs2.parsed"

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
    file_path = package_path/"garbage/no_go.cs2.parsed"

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
    file_path = package_path/"garbage/vfx_attachment.cs2.parsed"

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
    file_path = package_path/"garbage/file_ref.cs2.parsed"

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
    file_path = package_path/"garbage/transform_matrix.cs2.parsed"

    tm = TransformMatrix(*list(range(16)))

    with open(file_path, "wb") as f:
        tm.from_to_file(f, IOOperation.WRITE)

    test_read_transform_matrix(file_path=file_path)



if __name__ == "__main__":
    test_read_unicode_string()