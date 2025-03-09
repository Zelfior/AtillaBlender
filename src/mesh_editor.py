from typing import Dict, List, Tuple, Union
import bpy
import bmesh
import mathutils

from src.collection_manager import CollectionManager
from src.cs2_parsed_io import Vec3d, Face, TransformMatrix, FaceEdge


"""
    MeshEditor is cool

    thanks
"""
class MeshEditor:
    
    def __init__(self, cm:CollectionManager = None):
        self.all_edit_object_data:Dict[str, bpy.types.Mesh] = {}
        self.all_edit_object_bmesh:Dict[str, bmesh.types.BMesh] = {}

        if cm is None:
            self.cm = CollectionManager()
        else:
            self.cm = cm
        
    def swap_y_z_matrix(self, mat:List[List[float]]):
        
        col_save = mat[1].copy()
        mat[1] = mat[2].copy()
        mat[2] = col_save.copy()

        for i in range(4):
            e_save = float(mat[i][1])
            mat[i][1] = float(mat[i][2])
            mat[i][2] = e_save

        return mat

    def apply_transform_matrix(self, object_name:str, matrix:TransformMatrix):
        mat = matrix.to_matrix(transpose=True)
        mat = self.swap_y_z_matrix(mat)

        bpy.data.objects[object_name].matrix_world = mat

    def read_transform_matrix(self, object_name:str):
        mat:mathutils.Matrix = bpy.data.objects[object_name].matrix_world.copy()

        mat.transpose()
        mat = self.swap_y_z_matrix(mat)
        mat_as_mapping = [mat[j][i] for j in range(4) for i in range(4)]

        return TransformMatrix(*mat_as_mapping)
    
    """
        Goes to edit mode, if an object is selected and not already in edit mode, its data are stored, and the bmesh is created.
    """
    def go_to_edit_mode(self):
        if len(bpy.context.selected_objects) == 0 and bpy.context.active_object == None:
            pass
        elif len(bpy.context.selected_objects) > 0 and bpy.context.active_object == None:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            self.go_to_edit_mode()
        else:
            if bpy.context.active_object.mode == 'EDIT':
                pass
            else:
                if not bpy.context.view_layer.objects.active in bpy.context.selected_objects :
                    raise EnvironmentError("Active object is not selected.")

                bpy.ops.object.mode_set(mode='EDIT', toggle=False)

                self.all_edit_object_data:Dict[str, bpy.types.Mesh] = {}
                self.all_edit_object_bmesh:Dict[str, bmesh.types.BMesh] = {}

                for object in bpy.context.selected_objects:
                    if object.data is not None:
                        self.all_edit_object_data[object.name] = object.data
                        self.all_edit_object_bmesh[object.name] = bmesh.from_edit_mesh(self.all_edit_object_data[object.name])

    def go_to_object_mode(self, update_mesh:bool = True):
        if bpy.context.active_object is None:
            pass
        else:
            if bpy.context.active_object.mode == 'EDIT':
                if update_mesh:
                    if not self.all_edit_object_data == {}:
                        for object_ in self.all_edit_object_data:
                            self.all_edit_object_data[object_].update()

                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            else:
                pass
    
    def check_is_in_edit_mode(self, object_name):
        if bpy.context.active_object.mode == 'EDIT' and object_name in self.all_edit_object_data:
            return True
        return False


    def create_object(self, object_name:str, collection_name:str):
        me = bpy.data.meshes.new(f"{object_name}_name")
        ob = bpy.data.objects.new("object_name", me)

        self.cm.move_object_to_collection(object_name, collection_name)

        return ob
        
    def make_py_data(self, object_name:str,
                              swap_yz = True):
        obj_data = bpy.data.objects[object_name].data

        vertex_list = []
        for v in obj_data.vertices:
            vertex_list.append((v.co[0], v.co[1], v.co[2]))
            
        if swap_yz:
            for i in range(len(vertex_list)):
                vertex_list[i] = Vec3d(vertex_list[i][0], vertex_list[i][2], vertex_list[i][1])

        edge_list = []
        for e in obj_data.edges:
            edge_list.append((e.vertices[0], e.vertices[1]))
            
        face_list = []
        for p in obj_data.polygons:
            face_list.append(list([v for v in p.vertices]))

        normal_list = [p.normal for p in obj_data.polygons]
        normal_list = [Vec3d(n.x, n.z, n.y) for n in normal_list]

        return vertex_list, edge_list, face_list, normal_list


    def make_object_from_data(self, 
                              object_name:str, 
                              vertex_list:List[Union[Tuple[float, float, float], Vec3d]], 
                              edge_list:List[Tuple[int, int]], 
                              face_list:List[Union[List[float], Face]],
                              swap_yz = True,
                              normals = []):
        
        me = bpy.data.meshes.new(f"{object_name}_name")
        self.cm.rename_object(me, f"{object_name}_name")
        ob = bpy.data.objects.new(object_name, me)
        self.cm.rename_object(ob, object_name)

        v_list = [[v.x, v.y, v.z] if isinstance(v, Vec3d) else v for v in vertex_list]
        f_list = [[f.vertIndex0, f.vertIndex1, f.vertIndex2] if isinstance(f, Face) else f for f in face_list]

        if swap_yz:
            for i in range(len(v_list)):
                v_list[i] = [v_list[i][0], v_list[i][2], v_list[i][1]]

        # Make a mesh from a list of vertices/edges/faces
        me.from_pydata(v_list, edge_list, f_list)

        # Update the mesh
        me.update()

        if normals != [] and len(normals) == len(ob.data.polygons):
            bpy.ops.object.select_all(action='DESELECT')

            self.cm.move_object_to_collection(ob, "Scene Collection")
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob
            self.go_to_edit_mode()

            self.all_edit_object_bmesh[object_name].faces.ensure_lookup_table()
            for p in range(len(ob.data.polygons)):
                if sum([ob.data.polygons[p].normal[0] * normals[p].x + \
                            ob.data.polygons[p].normal[2] * normals[p].y +\
                                ob.data.polygons[p].normal[1] * normals[p].z]) < 0:
                    self.all_edit_object_bmesh[object_name].faces[p].normal_flip()
            self.go_to_object_mode()

        return ob

    def make_empty(self, empty_name:str, matrix):
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', 
                                    align='WORLD', 
                                    location=(0, 0, 0), 
                                    rotation=(0, 0, 0), 
                                    scale=(1, 1, 1))
        
        empty:bpy.types.Object = bpy.context.view_layer.objects.active #bpy.data.objects[-1]
        self.cm.rename_object(empty, empty_name)

        self.apply_transform_matrix(empty.name, matrix)

        return empty

    def make_cylinder(self, radius:float, height:float, object_name:str, collection_name:str, node_transorm:TransformMatrix):
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, 
                                                    depth=height, 
                                                    enter_editmode=False, 
                                                    align='WORLD', 
                                                    location=(0, 0, height), 
                                                    rotation=(0, 0, 0), 
                                                    scale=(1., 1., 1.))
        
        cyl:bpy.types.Object = bpy.context.view_layer.objects.active
        self.cm.rename_object(cyl, object_name)
        self.apply_transform_matrix(cyl.name, node_transorm)
        
        bpy.data.objects[cyl.name].location.z += height/2

        self.cm.move_object_to_collection(cyl.name, collection_name)