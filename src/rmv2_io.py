
from enum import Enum
import struct
from pathlib import Path
from typing import IO, Any, List

from src.io_elementary import IOOperation, io_bytes, io_float, io_int, io_str, io_short, skip_bytes, UnicodeString, Vec2d, Vec3d, SomeBytes

debug = False

RMV2_SIGNATURE = b"0x32564D52"; # binary for "RMV2"


class RigidMaterial(Enum) :
    BOW_WAVE= 22
    NON_RENDERABLE= 26
    TEXTURE_COMBO_VERTEX_WIND= 29
    TEXTURE_COMBO= 30
    DECAL_WATERFALL= 31
    STANDARD_SIMPLE= 32
    CAMPAIGN_TREES= 34
    POINT_LIGHT= 38
    STATIC_POINT_LIGHT= 45
    DEBUG_GEOMETRY= 46
    CUSTOM_TERRAIN= 49
    WEIGHTED_CLOTH= 58
    CLOTH= 60
    COLLISION= 61
    COLLISION_SHAPE= 62
    TILED_DIRTMAP= 63
    SHIP_AMBIENTMAP= 64
    WEIGHTED= 65
    PROJECTED_DECAL= 67
    DEFAULT= 68
    GRASS= 69
    WEIGHTED_SKIN= 70
    DECAL= 71
    DECAL_DIRTMAP= 72
    DIRTMAP= 73
    TREE= 74
    TREE_LEAF= 75
    WEIGHTED_DECAL= 77
    WEIGHTED_DECAL_DIRTMAP= 78
    WEIGHTED_DIRTMAP= 79
    WEIGHTED_SKIN_DECAL= 80
    WEIGHTED_SKIN_DECAL_DIRTMAP= 81
    WEIGHTED_SKIN_DIRTMAP= 82
    WATER= 83
    UNLIT= 84
    WEIGHTED_UNLIT= 85
    TERRAIN_BLEND= 86
    PROJECTED_DECAL_V2= 87
    IGNORE= 88
    TREE_BILLBOARD_MATERIAL= 89
    WATER_DISPLACE_VOLUME= 91
    ROPE= 93
    CAMPAIGN_VEGETATION= 94
    PROJECTED_DECAL_V3= 95
    WEIGHTED_TEXTURE_BLEND= 96
    PROJECTED_DECAL_V4= 97
    GLOBAL_TERRAIN= 98
    DECAL_OVERLAY= 99
    ALPHA_BLEND= 100

class TextureID(Enum) :
    T_ALBEDO= 0
    T_NORMAL= 1
    T_MASK= 3
    T_AMBIENT_OCCLUSION= 5
    T_TILING_DIRT_UV2= 7
    T_DIRT_ALPHA_MASK= 8
    T_SKIN_MASK= 10
    T_SPECULAR= 11
    T_GLOSS_MAP= 12
    T_DECAL_DIRTMAP= 13
    T_DECAL_DIRTMASK= 14
    T_DECAL_MASK= 15
    T_DIFFUSE_DAMAGE= 17


class AlphaMode(Enum) :
    OPAQUE		= 0
    ALPHA_TEST	= 1
    ALPHA_BLEND	= 2



class Header:
    skeleton: SomeBytes # 128-byte character array
    version: int = 0  # uint32_t
    lods_count: int = 0  # uint32_t

    def __init__(self, version:int, lods_count:int, skeleton:SomeBytes):
        self.version = version
        self.lods_count = lods_count
        self.skeleton = skeleton
    def new_header():
        return Header(0, 0, None)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.version = io_int(io, self.version, operation)

        if self.version == 5:
            raise ValueError(f"SHOGUN2 file format is not supported yet!")
        elif self.version < 5:
            raise ValueError(f"Games older than ROME2 are not supported!")

        self.lods_count = io_int(io, self.lods_count, operation)

        if operation == IOOperation.READ:
            self.skeleton = SomeBytes(128, b"")
        
        self.skeleton.from_to_file(io, operation)


class LodHeader:
    groups_count: int = 0  # uint32_t
    lod_offset: int = 0  # uint32_t

    def __init__(self, groups_count:int, lod_offset):
        self.groups_count = groups_count
        self.lod_offset = lod_offset
    def new_lod_header():
        return LodHeader(0, 0)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.groups_count = io_int(io, self.groups_count, operation)

        skip_bytes(io, b"\00", 8, operation)

        self.lod_offset = io_int(io, self.lod_offset, operation)

        skip_bytes(io, b"\00", 4, operation)
        
        if version == 8:
            skip_bytes(io, b"\00", 8, operation)


class Vertex:
    position: Vec3d  # XMFLOAT3 (3 floats)
    weight: float = 0.0  # float
    normal: Vec3d  # XMFLOAT3 (3 floats)
    weight1: float = 0.0  # float
    tangent: Vec3d  # XMFLOAT3 (3 floats)
    pad: float = 0.0  # float
    bitangent: Vec3d  # XMFLOAT3 (3 floats)
    pad1: float = 0.0  # float
    tex_coord: Vec2d  # XMFLOAT2 (2 floats)
    tex_coord2: Vec2d  # XMFLOAT2 (2 floats)
    bone_id0: int = 0  # byte
    bone_id1: int = 0  # byte
    pad3: bytes   # 12-byte padding



class Triangle:
    index1: int = 0  # uint16_t
    index2: int = 0  # uint16_t
    index3: int = 0  # uint16_t



class Texture:
    tex_path: str = ""  # std::wstring (converted to Python str)
    tex_id: int = 0  # TextureID (assuming it's an integer)

    def __init__(self, tex_path:str, tex_id):
        self.tex_path = tex_path
        self.tex_id = tex_id
    def new_texture():
        return Texture("", 0)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.tex_id = io_int(io, self.tex_id, operation)

        # skip_bytes(io, b"\00", 8, operation)

        # self.lod_offset = io_int(io, self.lod_offset, operation)

        # skip_bytes(io, b"\00", 4, operation)
        
        # if version == 8:
        #     skip_bytes(io, b"\00", 8, operation)

        # TODO
        # char tex[256];
        # file.read(reinterpret_cast<char *>(&tex), sizeof(tex));
        # replace_texture_path(tex, &texture.texPath, std::string(m_header.skeleton));
        # wstring path = filename.substr(0, filename.find_last_of(L"/\\"));

        # if (m_header.skeleton[0] == '\0')
        #     path = path.substr(0, path.size() - path.substr(path.find_last_of(L"/\\") + 1).size());

        # texture.texPath = path + texture.texPath;

class Group:
    vertices: List[Vertex]   # std::vector<Vertex>
    triangles: List[Triangle]   # std::vector<Triangle>
    textures: List[Texture]   # std::vector<Texture>
    vertex_format:int
    pivot: Vec3d  # XMFLOAT3 (3 floats)
    pad: float = 0.0  # float
    material_id: int = 0  # RigidMaterial (assuming integer)
    vertices_count: int = 0  # uint32_t
    indices_count: int = 0  # uint32_t
    textures_count: int = 0  # uint32_t
    group_name: bytes   # 32-byte character array
    alpha_mode: int = 0  # AlphaMode (assuming integer)
    attp_count: int = 0

    def __init__(self, 
                    vertices: List[Vertex],
                    triangles: List[Triangle],
                    textures: List[Texture],
                    vertex_format:int,
                    pivot: Vec3d,
                    pad: float,
                    material_id: int,
                    vertices_count: int,
                    indices_count: int,
                    textures_count: int,
                    group_name: bytes,
                    alpha_mode: int,
                    attp_count: int):
        self.vertices = vertices
        self.triangles = triangles
        self.textures = textures
        self.vertex_format = vertex_format
        self.pivot = pivot
        self.pad = pad
        self.material_id = material_id
        self.vertices_count = vertices_count
        self.indices_count = indices_count
        self.textures_count = textures_count
        self.group_name = group_name
        self.alpha_mode = alpha_mode
        self.attp_count = attp_count
    def new_group():
        return Group([],[],[],None, None, 0., 0, 0, 0, 0, None, 0, 0)
    def from_to_file(self, io:IO, operation:IOOperation, version = 11):
        self.material_id = io_int(io, self.material_id, operation)

        if self.material_id in [
                                    RigidMaterial.BOW_WAVE,
                                    RigidMaterial.PROJECTED_DECAL,
                                    RigidMaterial.PROJECTED_DECAL_V2,
                                    RigidMaterial.PROJECTED_DECAL_V3,
                                    RigidMaterial.PROJECTED_DECAL_V4,
                                    RigidMaterial.ALPHA_BLEND,
                                    RigidMaterial.STATIC_POINT_LIGHT,
                                    RigidMaterial.CLOTH
                                ]:
            raise ValueError("One of the specified rigid materials is not supported! This may cause errors during the runtime.")
        
        skip_bytes(io, b"\00", 8, operation)

        self.vertices_count = io_int(io, self.vertices_count, operation)

        skip_bytes(io, b"\00", 4, operation)

        self.indices_count = io_int(io, self.indices_count, operation)
        
        skip_bytes(io, b"\00", 56, operation)

        self.vertex_format = io_short(io, self.vertex_format, operation)

        if self.vertex_format in [6, 11, 12]:
            raise ValueError("Trees, ropes and campaign vegetation are not yet supported!")

        self.group_name = io_str(io, self.group_name, 32)
        print(f"Groupe name found {self.group_name}")

        skip_bytes(io, b"\00", 514, operation)

        if operation == IOOperation.READ:
            self.pivot = Vec3d.new_vec3d()
            self.textures = []
        
        self.pivot.from_to_file(io, operation)

        skip_bytes(io, b"\00", 152, operation)

        self.attp_count = io_int(io, self.attp_count, operation)
        self.textures_count = io_int(io, self.textures_count, operation)

        skip_bytes(io, b"\00", 140, operation)
        skip_bytes(io, b"\00", 84*self.attp_count, operation)
        
        for i in range(self.textures_count):
            if operation == IOOperation.READ:
                self.textures.append(Texture.new_texture())
            self.textures[i].from_to_file(io, operation)


	# 				file.seekg(4, ios_base::cur);
	# 				if (group.materialID == RigidMaterial::tiled_dirtmap)
	# 					file.seekg(16, ios_base::cur);
	# 				else if (group.materialID == RigidMaterial::decal
	# 					  || group.materialID == RigidMaterial::weighted_decal
	# 					  || group.materialID == RigidMaterial::weighted_skin_decal)
	# 					file.seekg(20, ios_base::cur);
	# 				else if (group.materialID == RigidMaterial::dirtmap
	# 					  || group.materialID == RigidMaterial::weighted_dirtmap
	# 					  || group.materialID == RigidMaterial::weighted_skin_dirtmap)
	# 					file.seekg(32, ios_base::cur);
	# 				else if (group.materialID == RigidMaterial::decal_dirtmap
	# 					  || group.materialID == RigidMaterial::weighted_decal_dirtmap
	# 					  || group.materialID == RigidMaterial::weighted_skin_decal_dirtmap)
	# 					file.seekg(52, ios_base::cur);
	# 				else if (group.materialID == RigidMaterial::tree)
	# 					file.seekg(56, ios_base::cur);

	# 				file.read(reinterpret_cast<char *>(&group.alphaMode), sizeof(group.alphaMode));

	# 				switch (vertexFormat[j])
	# 				{
	# 					case 0:
	# 					{
	# 						for (size_t k = 0; k < group.verticesCount; ++k)
	# 						{
	# 							read_default(file, XMLoadFloat3(&group.pivot), &vertex);
	# 							group.vertices.push_back(move(vertex));
	# 						}
	# 						break;
	# 					}
	# 					case 3:
	# 					{
	# 						for (size_t k = 0; k < group.verticesCount; ++k)
	# 						{
	# 							read_weighted(file, XMLoadFloat3(&group.pivot), &vertex);
	# 							group.vertices.push_back(move(vertex));
	# 						}
	# 						break;
	# 					}
	# 					case 4:
	# 					{
	# 						for (size_t k = 0; k < group.verticesCount; ++k)
	# 						{
	# 							read_cinematic(file, XMLoadFloat3(&group.pivot), &vertex);
	# 							group.vertices.push_back(move(vertex));
	# 						}
	# 						break;
	# 					}
	# 					case 6:
	# 					{
	# 						return false;
	# 					}
	# 					case 11:
	# 					{
	# 						return false;
	# 					}
	# 					case 12:
	# 					{
	# 						return false;
	# 					}

	# 					default:
	# 					{
	# 						MessageBoxA(nullptr, "The specified vertex format is not yet supported!", "Error: Unsupported vertex format", MB_OK);
	# 						return false;
	# 					}
	# 				}

	# 				for (size_t k = 0; k < group.indicesCount / 3; ++k)
	# 				{
	# 					file.read(reinterpret_cast<char *>(&triangle.index1), sizeof(triangle.index1));
	# 					file.read(reinterpret_cast<char *>(&triangle.index3), sizeof(triangle.index3));
	# 					file.read(reinterpret_cast<char *>(&triangle.index2), sizeof(triangle.index2));

	# 					group.triangles.push_back(move(triangle));
	# 				}





class Rmv2File:
    header:Header
    lod_headers:List[LodHeader]
    lods:List[List[Group]]


    
    # uint32_t temp;
    # Texture texture;
    # Vertex vertex;
    # Triangle triangle;
    # std::vector<uint16_t> vertexFormat;
    # uint32_t attp_count;
    
    def __init__(self,
        ):
        ...
        # self.version = version
        # self.piece_count = piece_count
    def new_rmv2file():
        return Rmv2File()
    
    def read_write_file(self, file_path:str, operation:IOOperation):
        file_open_type = "rb" if operation == IOOperation.READ else "wb"

        if operation == IOOperation.READ:
            print(f"Starting to read file : {file_path}")
        else:
            print(f"Starting to write file : {file_path}")

        with open(file_path, file_open_type) as f:
            if operation == IOOperation.READ:
                self.header = Header.new_header()
            
            signature = SomeBytes(4, RMV2_SIGNATURE)
            signature.from_to_file(f, operation)

            if not signature.value == RMV2_SIGNATURE:
                raise ValueError(f"The file you're attempting to read is not a rmv2 file!")
            
            self.header.from_to_file(f, operation)
            print(f"Version found : {self.header.version}")

            if operation == IOOperation.READ:
                self.lod_header = LodHeader.new_lod_header()

            self.lod_header.from_to_file(f, operation)
        
            for i in range(self.header.lods_count):
                if operation == IOOperation.READ:
                    self.lod_headers.append(LodHeader.new_lod_header())

                self.lod_headers[i].from_to_file(f, operation, version = self.header.version)

            for i in range(self.header.lods_count):
                if operation == IOOperation.READ:
                    self.lods.append([])

                for j in range(self.lod_headers[i].groups_count):
                    if operation == IOOperation.READ:
                        self.lods[i].append(Group.new_group())

                    self.lods[i][j].from_to_file(f, operation)

	# 				lod.push_back(move(group));
	# 				group.textures.resize(0);
	# 				group.vertices.resize(0);
	# 				group.triangles.resize(0);
	# 			}
	# 		}
	# 		m_model.push_back(move(lod));
	# 		lod.resize(0);
	# 		vertexFormat.resize(0);
	# 	}
	# 	file.close();
	# }
	# else
	# 	return false;

	# return true;
    # def __eq__(self, other:'Cs2File'):
    #     for param in ["version",    "bbox",    "flag",    "piece_count"]:
    #         if self.__getattribute__(param) != other.__getattribute__(param):
    #             print(f"Cs2File have different {param}, found {self.__getattribute__(param)} and {other.__getattribute__(param)}")
    #             return False
        
    #     for i in range(len(self.building_pieces)):
    #         if self.building_pieces[i] != other.building_pieces[i]:
    #             print(f"Cs2File have different BuildingPiece {i}")
    #             return False
            
    #     return True

    
if __name__ == "__main__":
    input_path = Path("F:\Workspace\TotalWarModding\files\cs2_parsed\sassanid_city_building_1\sassanid_city_building_1_piece01_destruct01.rigid_model_v2")
    
    rmv2 = Rmv2File.new_rmv2file()

    rmv2.read_write_file(input_path.absolute(), 
                            IOOperation.READ)