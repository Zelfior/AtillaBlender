from typing import Dict
import bpy
import bmesh
from mathutils import Vector
import math

from . import  CollectionManager


"""
    TripoliMeshEditor is cool

    thanks
"""
class TripoliMeshEditor:
    
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

        self.CM = CollectionManager.TripoliCollectionManager()
        

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

                self.all_edit_object_data = {}
                self.all_edit_object_bmesh = {}

                for object in bpy.context.selected_objects:
                    self.all_edit_object_data[object.name] = object.data
                    self.all_edit_object_bmesh[object.name] = bmesh.from_edit_mesh(self.all_edit_object_data[object.name])

    def go_to_object_mode(self, update_mesh = True):
        if bpy.context.active_object == None:
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

