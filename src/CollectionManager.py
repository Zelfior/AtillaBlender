import bpy

class CollectionManager:
    
    def __init__(self):
        pass
        
    def move_object_to_collection(self, object_name, collection_name):
        if bpy.data.objects.get(object_name) == None:
            print("Object "+object_name+" doesn't exist.")
        elif collection_name == "Scene Collection":
            for collection in bpy.data.objects.get(object_name).users_collection:
                collection.objects.unlink(bpy.data.objects.get(object_name))
            bpy.context.scene.collection.objects.link(bpy.data.objects.get(object_name))
        elif bpy.data.collections.get(collection_name) == None:
            print("collection_name "+object_name+" doesn't exist.")
        else:
            for collection in bpy.data.objects.get(object_name).users_collection:
                collection.objects.unlink(bpy.data.objects.get(object_name))
                
            bpy.data.collections.get(collection_name).objects.link(bpy.data.objects.get(object_name))
            
    def get_collection_parent(self, collection_name):
        for collection in bpy.data.collections:
            if collection_name in collection.children:
                return collection.name
        return None
        
    def get_collection_object_list(self, collection_name):
        return [objects.name for objects in bpy.data.collections[collection_name].objects]

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
        print("Deleting object", object_name)
        if object_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects.get(object_name), do_unlink=True)
            self.clear_unattached_objects


    def clear_unattached_objects(self):
        for obj in bpy.data.objects:
            if obj.users_collection == None or len(obj.users_collection) == 0:
                print(obj.name,"removed")
                bpy.data.objects.remove(obj, do_unlink=True)
            
        for obj in bpy.data.lights:
            if obj.library == None or len(obj.library) == 0:
                print(obj.name,"removed")
                bpy.data.lights.remove(obj, do_unlink=True)
            
        for obj in bpy.data.cameras:
            if obj.library == None or len(obj.library) == 0:
                print(obj.name,"removed")
                bpy.data.cameras.remove(obj, do_unlink=True)
                
        for obj in bpy.data.meshes:
            if obj.users == 0:
                print(obj.name,"removed")
                bpy.data.meshes.remove(obj)

    def clear_unused_materials(self):
        for obj in bpy.data.materials:
            if obj.users == 0:
                print(obj.name,"removed")
                bpy.data.materials.remove(obj)
            
    def exist_collection(self, collection_name):
        return not (bpy.data.collections.get(collection_name) == None)
            
    def new_collection(self, collection_name, parent_collection_name, clear = False):

        if clear:
            self.delete_collection(collection_name)
        
        if bpy.data.collections.get(collection_name) == None:
            collection = bpy.data.collections.new(collection_name)

            if parent_collection_name == "":
                bpy.context.scene.collection.children.link(collection)
            else:
                bpy.data.collections.get(parent_collection_name).children.link(collection)