from typing import Dict, List, Tuple
import bpy
import bmesh
from mathutils import Vector
import math

from . import  CollectionManager


"""
    MeshEditor is cool

    thanks
"""
class MeshEditor:
    
    def __init__(self, precision = 1):
        self.edit_object_data = None
        self.edit_object_bmesh = None

        if precision == 0:   
            self.shrink = False
            self.self_intersection = False
            self.hole_tolerant = False
        elif precision == 1:   
            self.shrink = True
            self.self_intersection = False
            self.hole_tolerant = False
        elif precision == 2:   
            self.shrink = True
            self.self_intersection = True
            self.hole_tolerant = False
        else :   
            self.shrink = True
            self.self_intersection = True
            self.hole_tolerant = True
            
        self.expansion_factor = 0.10121651
        self.shrink_source = True
        self.shrink_target = True

        self.limited_dissolve_angle = 0.01   

        self.coplanar_threshold = 0.00001
        
        self.rescale_factor = 100. # 100.

        self.all_edit_object_data:bpy.types.Mesh = {}
        self.all_edit_object_bmesh:bmesh.types.BMesh = {}

        self.CM = CollectionManager.CollectionManager()
        

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

        self.CM.move_object_to_collection(object_name, collection_name)

        return ob
    
    # def add_vertex_to_object(self, object_name:str, coordinates:Tuple[float, float, float]):
    #     if self.check_is_in_edit_mode(object_name):
    #         ...
    #         # TODO
    #     else:
    #         raise Exception(f"Object {object_name} is not in edit mode.")
        
    # def add_vertex_to_object(self, object_name:str, coordinates:Tuple[float, float, float]):
    #     if self.check_is_in_edit_mode(object_name):
    #         ...
    #         # TODO
    #     else:
    #         raise Exception(f"Object {object_name} is not in edit mode.")
        
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
                              vertex_list:List[Tuple[float, float, float]], 
                              edge_list:List[Tuple[int, int]], 
                              face_list:List[List[float]]):
        
        me = bpy.data.meshes.new(f"{object_name}_name")
        ob = bpy.data.objects.new(object_name, me)

        # Make a mesh from a list of vertices/edges/faces
        me.from_pydata(vertex_list, edge_list, face_list)

        # Update the mesh
        me.update()
