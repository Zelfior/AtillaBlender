from typing import List, Tuple
import bpy
import bmesh

from src.collection_manager import CollectionManager
from src.cs2_parsed_io import Vec3d, Face, TransformMatrix


"""
    MeshEditor is cool

    thanks
"""
class MeshEditor:
    
    def __init__(self):
        self.all_edit_object_data:bpy.types.Mesh = {}
        self.all_edit_object_bmesh:bmesh.types.BMesh = {}

        self.cm = CollectionManager()
        
    def apply_transform_matrix(self, object_name:str, matrix:TransformMatrix):
        obj:bpy.types.Object = bpy.data.objects[object_name]

        mat = matrix.to_matrix(transpose=True)

        col_save = mat[1]
        mat[1] = mat[2]
        mat[2] = col_save

        for i in range(4):
            e_save = mat[i][1]
            mat[i][1] = mat[i][2]
            mat[i][2] = e_save

        obj.matrix_world = mat

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

                self.all_edit_object_data:bpy.types.Mesh = {}
                self.all_edit_object_bmesh:bmesh.types.BMesh = {}

                for object in bpy.context.selected_objects:
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
        
    def make_py_data(self, object_name:str):
        obj_data = bpy.data.objects[object_name].data

        vertex_list = []
        for v in obj_data.vertices:
            vertex_list.append((v.co[0], v.co[1], v.co[2]))
            
        edge_list = []
        for e in obj_data.edges:
            edge_list.append((e.vertices[0], e.vertices[1]))
            
        face_list = []
        for p in obj_data.polygons:
            face_list.append((v for v in p.vertices))

        return vertex_list, edge_list, face_list


    def make_object_from_data(self, 
                              object_name:str, 
                              vertex_list:List[Tuple[float, float, float] | Vec3d], 
                              edge_list:List[Tuple[int, int]], 
                              face_list:List[List[float] | Face],
                              swap_yz = True):
        
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

        return ob

    def make_empty(self, empty_name:str, matrix):
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', 
                                    align='WORLD', 
                                    location=(0, 0, 0), 
                                    rotation=(0, 0, 0), 
                                    scale=(1, 1, 1))
        
        empty:bpy.types.Object = bpy.context.view_layer.objects.active #bpy.data.objects[-1]
        self.cm.rename_object(empty, empty_name)

        self.apply_transform_matrix(empty_name, matrix)

        return empty
