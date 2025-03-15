
from typing import Any, Dict, List, Tuple, Union
from src.cs2_parsed_io import Vec3d, Face, TransformMatrix

debug = True
"""
    FakeMeshEditor to test the blender interface
"""
class FakeMeshEditor:
    
    def __init__(self, cm = None):
        if cm is not None:
            self.cm = cm

        self.objects_data:Dict[str, Tuple[List[Vec3d], List[Tuple[int, int]], List[Face]]] = {}
        self.objects_transform:Dict[str, TransformMatrix] = {}

        self.empty:Dict[str, TransformMatrix] = {}

        self.objects_normal:Dict[str, List[Vec3d]] = {}
        
        
    def apply_transform_matrix(self, object_name:str, matrix:TransformMatrix):
        self.objects_transform[object_name] = matrix

    def read_transform_matrix(self, object_name:str):
        if object_name in self.objects_transform:
            return self.objects_transform[object_name]
        elif object_name in self.empty:
            return self.empty[object_name]
        else:
            raise KeyError(f"Requested {object_name}, found {list(self.objects_transform.keys())} and {list(self.empty.keys())}")
    
    def make_py_data(self, 
                        object_name:str,
                        swap_yz = True):
        vertex_list, edge_list, face_list = self.objects_data[object_name]

        v_list = vertex_list.copy()
        e_list = edge_list.copy()
        f_list = face_list.copy()

        for v in range(len(v_list)):
            if isinstance(v_list[v], list):
                v_list[v] = Vec3d(*v)

        if swap_yz:
            for i in range(len(v_list)):
                v_list[i] = Vec3d(v_list[i].x, v_list[i].z, v_list[i].y)

        if object_name in self.objects_normal:
            n_list = self.objects_normal[object_name]
        else:
            n_list = []

        return v_list, e_list, f_list, n_list


    def make_object_from_data(self, 
                              object_name:str, 
                              vertex_list:List[Union[Tuple[float, float, float], Vec3d]], 
                              edge_list:List[Tuple[int, int]], 
                              face_list:List[Face],
                              swap_yz = True,
                              normals = []):
        if debug:
            print(f"Making object {object_name}")
        name = object_name
        if name in self.objects_data:
            i = 1
            name = f"{object_name}.{i:03}"
            while name in self.objects_data:
                i += 1
                name = f"{object_name}.{i:03}"
            if debug:
                print(f"Renaming {object_name} to {name}")

        v_list = [v if isinstance(v, Vec3d) else Vec3d(*v)  for v in vertex_list]
        f_list = face_list

        if swap_yz:
            for i in range(len(v_list)):
                v_list[i] = Vec3d(v_list[i].x, v_list[i].z, v_list[i].y)

        self.objects_data[name] = (v_list, edge_list, f_list)

        if not normals == []:
            self.objects_normal[name] = normals

        return name

    def make_empty(self, empty_name:str, matrix):
        name = empty_name
        if name in self.empty:
            i = 1
            name = f"{empty_name}.{i:03}"
            while name in self.empty:
                i += 1
                name = f"{empty_name}.{i:03}"
            print(f"Renaming {empty_name} to {name}")

        self.empty[name] = matrix

        return name

    def make_cylinder(self, radius:float, height:float, name:str, collection_name:str, node_transform:TransformMatrix):
        new_name = name
        if new_name in self.objects_data:
            i = 1
            new_name = f"{name}.{i:03}"
            while new_name in self.objects_data:
                i += 1
                new_name = f"{name}.{i:03}"
            print(f"Renaming {name} to {new_name}")

        matrix = node_transform.to_matrix()
        center_coordinates = (matrix[0][3], matrix[1][3], matrix[2][3])

        self.make_object_from_data(new_name, [
            [center_coordinates[0]-radius, center_coordinates[1]-radius, center_coordinates[2]-height/2],
            [center_coordinates[0]+radius, center_coordinates[1]+radius, center_coordinates[2]+height/2]
        ], [], [], swap_yz=False)

        nt = node_transform.copy()
        nt.row1_col3 += height/2

        self.cm.move_object_to_collection(new_name, collection_name)
        self.objects_transform[new_name] = nt

    def swap_y_z_matrix(self, mat:List[List[float]]):
        col_save = mat[1].copy()
        mat[1] = mat[2].copy()
        mat[2] = col_save.copy()

        for i in range(4):
            e_save = float(mat[i][1])
            mat[i][1] = float(mat[i][2])
            mat[i][2] = e_save

        return mat

    def get_object_matrix_transform(self, object_name:str, swap_yz:bool = True) -> TransformMatrix:
        matrix = [list(row) for row in self.read_transform_matrix(object_name).to_matrix(transpose=True)]

        # if not swap_yz:
        #     matrix = self.swap_y_z_matrix(matrix)

        list_matrix = []
        for row in matrix:
            list_matrix += row
            
        return TransformMatrix(*list_matrix)
    
    
    def update(self,):
        pass

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
        if debug:
            print(f"Moving {object_name} to {collection_name}")

        target_col = self.collection_master.get_collection_element_recursive(collection_name)
        self.collection_master.remove_object_recursive(object_name)
        
        target_col.objects.append(object_name)

            
    def get_collection_children(self, collection_name):
        col = self.collection_master.get_collection_element_recursive(collection_name)

        if col is not None:
            return [c.name for c in col.children]
        
        return None
    
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
            
    def reset(self):
        self.collection_master = CollectionElement("")

    def exist_collection(self, collection_name):
        return self.collection_master.get_collection_element_recursive(collection_name) is not None
            
    def new_collection(self, collection_name, parent_collection_name, clear = False):
        if debug:
            print(f"Adding collection {collection_name} in {parent_collection_name}")
        col = self.collection_master.get_collection_element_recursive(parent_collection_name)

        if col is not None:
            col.children.append(CollectionElement(collection_name))
        else:
            raise KeyError