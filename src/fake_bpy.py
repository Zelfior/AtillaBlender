
from typing import Any, Dict, List, Tuple
from src.cs2_parsed_io import Vec3d, Face, TransformMatrix


"""
    FakeMeshEditor to test the blender interface
"""
class FakeMeshEditor:
    
    def __init__(self):
        self.cm = FakeCollectionManager()

        self.objects_data:Dict[str, Tuple[List[Vec3d], List[Tuple[int, int]], List[Face]]] = {}
        self.objects_transform:Dict[str, TransformMatrix] = {}
        self.empty:Dict[str, TransformMatrix] = {}
        
    def apply_transform_matrix(self, object_name:str, matrix:TransformMatrix):
        self.objects_transform[object_name] = matrix

    def read_transform_matrix(self, object_name:str):
        if object_name in self.objects_transform:
            return self.objects_transform[object_name]
        elif object_name in self.empty:
            return self.empty[object_name]
        else:
            raise KeyError
    
    def make_py_data(self, object_name:str,
                              swap_yz = True):
        vertex_list, edge_list, face_list = self.objects_data[object_name]

        if swap_yz:
            for i in range(len(vertex_list)):
                vertex_list[i] = [vertex_list[i].x, vertex_list[i].z, vertex_list[i].y]

        print(vertex_list )
        return vertex_list, edge_list, face_list


    def make_object_from_data(self, 
                              object_name:str, 
                              vertex_list:List[Tuple[float, float, float] | Vec3d], 
                              edge_list:List[Tuple[int, int]], 
                              face_list:List[List[float] | Face],
                              swap_yz = True):
        print(f"Making object {object_name}")
        v_list = [[v.x, v.y, v.z] if isinstance(v, Vec3d) else v for v in vertex_list]
        f_list = [f if isinstance(f, Face) else Face(*f) for f in face_list]

        if swap_yz:
            for i in range(len(v_list)):
                v_list[i] = [v_list[i][0], v_list[i][2], v_list[i][1]]

        for i in range(len(v_list)):
            v_list[i] = Vec3d(*v_list[i])

        self.objects_data[object_name] = (v_list, edge_list, f_list)

        return object_name

    def make_empty(self, empty_name:str, matrix):
        self.empty[empty_name] = matrix

        return empty_name

    def make_cylinder(self, radius:float, height:float, name:str, collection_name:str, node_transorm:TransformMatrix):
        center_coordinates = (0, 0, 0)

        self.make_object_from_data(name, [
            [center_coordinates[0]-radius, center_coordinates[1]-radius, center_coordinates[2]],
            [center_coordinates[0]-radius, center_coordinates[1]-radius, center_coordinates[2]+height]
        ], [], [])

        self.cm.move_object_to_collection(name, collection_name)

class CollectionElement:
    def __init__(self, name):
        self.name = name
        self.parent = ""
        self.children:List[CollectionElement] = []
        self.objects:List[str] = []

    def remove_object_recursive(self, object_name:str):
        if object_name in self.objects:
            self.objects.remove(object_name)
            return True
        
        for child in self.children:
            if child.remove_object_recursive(object_name):
                return True
        return False
    
    def get_object_parent_recursive(self, object_name:str):
        if object_name in self.objects:
            return self
        
        for child in self.children:
            if child.get_object_parent_recursive(object_name) is not None:
                return child.get_object_parent_recursive(object_name)
    
        return None
    
    def get_collection_element_recursive(self, col_name:str):
        if col_name == self.name:
            return self
        
        for child in self.children:
            if child.get_collection_element_recursive(col_name) is not None:
                return child.get_collection_element_recursive(col_name)
    
        return None
    
    def get_collection_parent_recursive(self, col_name:str):
        if col_name in [c.name for c in self.children]:
            return self
        
        for child in self.children:
            if child.get_collection_parent_recursive(col_name) is not None:
                return child.get_collection_parent_recursive(col_name)
    
        return None
    
    def __repr__(self):
        return f"Collection element named -{self.name}-, with {len(self.children)} children and {len(self.objects)} objects."
    
class FakeCollectionManager:
    def __init__(self):
        self.collection_master = CollectionElement("")
        
    def get_selected_collection(self):
        return self.collection_master.children[0].name
        
    def move_object_to_collection(self, object_name:str, collection_name:str):
        print(f"Moving {object_name} to {collection_name}")
        target_col = self.collection_master.get_collection_element_recursive(collection_name)
        self.collection_master.remove_object_recursive(object_name)

        target_col.objects.append(object_name)

            
    def get_collection_parent(self, collection_name):
        col = self.collection_master.get_collection_parent_recursive(collection_name)

        if col is not None:
            return col.name
        
        return None
        
    def get_collection_object_list(self, collection_name):
        col = self.collection_master.get_collection_element_recursive(collection_name)

        if col is not None:
            return col.objects
        return None

    def get_object_collection_name(self, object_name):
        col = self.collection_master.get_object_parent_recursive(object_name)

        if col is not None:
            return col.name
        
        return None

    def delete_collection(self, collection_name):
        col = self.collection_master.get_collection_parent_recursive(collection_name)

        if col is not None:
            del col.children[collection_name]
    
    def delete_object(self, object_name):
        col = self.collection_master.get_object_parent_recursive(object_name)

        if col is not None:
            col.objects.remove(object_name)

    def clear_unattached_objects(self):
        pass

    def clear_unused_materials(self):
        pass
            
    def exist_collection(self, collection_name):
        return self.collection_master.get_collection_element_recursive(collection_name) is not None
            
    def new_collection(self, collection_name, parent_collection_name, clear = False):
        print(f"Adding collection {collection_name} in {parent_collection_name}")
        col = self.collection_master.get_collection_element_recursive(parent_collection_name)

        if col is not None:
            col.children.append(CollectionElement(collection_name))
        else:
            raise KeyError