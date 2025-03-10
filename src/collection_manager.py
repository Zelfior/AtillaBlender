from typing import Union
import bpy

class CollectionManager:
    
    def __init__(self):
        self.debug = False
        pass
        
    def get_selected_collection(self):
        return bpy.context.collection.name

    def rename_object(self, 
                            o:Union[bpy.types.Object, bpy.types.Collection], 
                            name:str):
        """
            Please do not ask why this heresy for it is the work of Melkor
        """
        if self.debug:
            print(f"Renaming {o} to {name} of length {len(name)}")
        o.name = name
        
    def move_object_to_collection(self, object_name, collection_name):
        if isinstance(object_name, bpy.types.Object):
            object_name = object_name.name
        if bpy.data.objects.get(object_name) == None:
            if self.debug:
                print("Object "+object_name+" doesn't exist.")
        elif collection_name == "Scene Collection":
            for collection in bpy.data.objects.get(object_name).users_collection:
                collection.objects.unlink(bpy.data.objects.get(object_name))
            bpy.context.scene.collection.objects.link(bpy.data.objects[object_name])
        elif bpy.data.collections.get(collection_name) == None:
            if self.debug:
                print("Collection named "+object_name+" doesn't exist.")
        else:
            for collection in bpy.data.objects.get(object_name).users_collection:
                collection.objects.unlink(bpy.data.objects[object_name])
                
            bpy.data.collections.get(collection_name).objects.link(bpy.data.objects.get(object_name))
            
    def get_collection_parent(self, collection_name):
        for collection in bpy.data.collections:
            if collection_name in collection.children:
                return collection.name
        return None
        
    def get_collection_children(self, collection_name):
        return [c.name for c in bpy.data.collections.get(collection_name).children]
        
    def get_collection_object_list(self, collection_name):
        col:bpy.types.Collection = bpy.data.collections.get(collection_name)

        if col is None:
            return []
        else:
            return [obj.name for obj in bpy.data.collections.get(collection_name).objects]

    def get_collection_parent_path(self, collection_name, current_path):
        if self.get_collection_parent(collection_name) == None:
            return collection_name
        else:
            return self.get_collection_parent_path(self.get_collection_parent(collection_name),current_path)+"/"+collection_name

    def get_object_collection_name(self, object_name):
        return bpy.data.objects.get(object_name).users_collection

    def delete_collection(self, collection_name):
        collection = bpy.data.collections.get(collection_name)
        
        if not collection == None:
            for collect in collection.children:
                if not collect == None:
                    self.delete_collection(collect.name)
            
            for obj in collection.objects:
                if not obj == None:
                    bpy.data.objects.remove(obj, do_unlink=True)
                
            bpy.data.collections.remove(collection)

    def delete_object(self, object_name):
        if self.debug:
            print("Deleting object", object_name)
        if object_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects.get(object_name), do_unlink=True)
            self.clear_unattached_objects()

    def clear_unattached_objects(self):
        for obj in bpy.data.objects:
            if obj.users_collection == None or len(obj.users_collection) == 0:
                if self.debug:
                    print(obj.name,"removed")
                bpy.data.objects.remove(obj, do_unlink=True)
            
        for obj in bpy.data.lights:
            if obj.library == None or len(obj.library) == 0:
                if self.debug:
                    print(obj.name,"removed")
                bpy.data.lights.remove(obj, do_unlink=True)
            
        for obj in bpy.data.cameras:
            if obj.library == None or len(obj.library) == 0:
                if self.debug:
                    print(obj.name,"removed")
                bpy.data.cameras.remove(obj, do_unlink=True)
                
        for obj in bpy.data.meshes:
            if obj.users == 0:
                if self.debug:
                    print(obj.name,"removed")
                bpy.data.meshes.remove(obj)

    def clear_unused_materials(self):
        for obj in bpy.data.materials:
            if obj.users == 0:
                if self.debug:
                    print(obj.name,"removed")
                bpy.data.materials.remove(obj)

    def reset(self):
        """
            Clears the blender model
        """
        for object in bpy.data.objects:
            bpy.data.objects.remove(object, do_unlink=True)

        for obj in bpy.data.lights:
            bpy.data.lights.remove(obj, do_unlink=True)
            
        for obj in bpy.data.cameras:
            bpy.data.cameras.remove(obj, do_unlink=True)
                
        for obj in bpy.data.meshes:
            bpy.data.meshes.remove(obj)

        for collection in bpy.data.collections:
            bpy.data.collections.remove(collection)
        
            
    def exist_collection(self, collection_name):
        return not (bpy.data.collections.get(collection_name) == None)
            
    def new_collection(self, collection_name, parent_collection_name, clear = False):

        if self.debug:
            print(f"Making collection {collection_name} in {parent_collection_name}")

        if clear:
            self.delete_collection(collection_name)
        
        if bpy.data.collections.get(collection_name) == None:
            collection = bpy.data.collections.new(collection_name)

            self.rename_object(collection, collection_name)

            if parent_collection_name == "":
                bpy.context.scene.collection.children.link(collection)
            else:
                if self.debug:
                    print(f"getting collection -{parent_collection_name}- children haha")
                bpy.data.collections[parent_collection_name].children.link(collection)