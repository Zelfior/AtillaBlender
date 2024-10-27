
bl_info = {
    # required
    'name': 'TotalWarAtillaCS2Exporter',
    'blender': (3,4,1),
    'category': 'Object',
    "location": "View3D > Sidebar > Atilla",
    # optional
    'version': (0, 1, 0),
    'author': 'Zelfior',
    'description': 'Exports Atilla Totalwar .cs2.parsed files.',
}

import bpy
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty

from src.cs2_parsed_io import Cs2File
from src.cs2_to_blender import Cs2ToBlender
from src.io_elementary import IOOperation, UnknownData

# == GLOBAL VARIABLES
PROPS = [
    ('input_file', bpy.props.StringProperty(name='.cs2.parsed input file', default='//TBD')),
    ('input_message', bpy.props.StringProperty(name='input message', default='')),
    ('input_error', bpy.props.BoolProperty(name='input error', default=False)),
    ('cs2_object', None),
]


# == PANELS
class ATILLA_HT_panel(bpy.types.Panel):
    
    bl_idname = 'ATILLA_HT_panel'
    bl_label = 'Atilla import/export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Atilla" 
    
    def draw(self, context:bpy.types.Context):
        layout = self.layout
        layout.label(text="Totalwar Atilla input files import/export.")

# == PANELS
class IMPORT_PT_panel(bpy.types.Panel):
    
    bl_parent_id = "ATILLA_HT_panel"
    bl_idname = 'IMPORT_PT_panel'
    bl_label = 'Atilla .cs2.parsed file'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context:bpy.types.Context):
        col = self.layout.column()
        row = col.row()
        split = row.split(factor=0.9)
        col1 = split.column()
        col2 = split.column()


        col1.prop(context.scene,'input_file')
        col2.operator("explorer_file.import", icon="FILEBROWSER")

        col.operator("file_loader.import", text="Load .cs2.parsed file")

        if context.scene.input_message != "":
            if context.scene.input_error:
                col.label(text=context.scene.input_message, icon='ERROR')

            else:
                col.label(text=context.scene.input_message)

            


# == OPERATORS

class EXPLORER_OT_import(Operator, ImportHelper):
    bl_idname = 'explorer_file.import'
    bl_label = 'File loader'
    bl_options = {'PRESET', 'UNDO'}
    
    filter_glob:bpy.props.StringProperty = bpy.props.StringProperty(
        default='*',
        options={'HIDDEN'},
    )

    def execute(self, context:bpy.types.Context):
        print('imported file: ', self.filepath)
        context.scene.input_file = self.filepath

        return {'FINISHED'}


class file_loader_OT_input(bpy.types.Operator):
    bl_idname = 'file_loader.import'
    bl_label = 'File loader'
 
    def execute(self, context:bpy.types.Context):
        print('imported file: ', context.scene.input_file)

        cs2_object = Cs2File.new_cs2file()
        try:
            cs2_object.read_write_file(context.scene.input_file, IOOperation.READ, has_vfx=True)
            context.scene.input_message = "Loaded file with VFX objects."
            context.scene.input_error = False
        except UnknownData:
            try:
                cs2_object.read_write_file(context.scene.input_file, IOOperation.READ, has_vfx=False)
                context.scene.input_message = "Loaded file without VFX objects."
                context.scene.input_error = False
            except UnknownData:
                context.scene.input_message = "File can't be read, please contact the extension author."
                context.scene.input_error = True
                return {'FINISHED'}

        if not context.scene.input_error:
            setattr(bpy.types.Scene, 'cs2_object', cs2_object)

            c2b = Cs2ToBlender()
            c2b.make_cs2(context.scene.cs2_object, "cs2_parsed")


        return {'FINISHED'}

# == MAIN ROUTINE
CLASSES = [
    ATILLA_HT_panel,
    IMPORT_PT_panel,
    EXPLORER_OT_import,
    file_loader_OT_input,
]

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == '__main__':
    register()