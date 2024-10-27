import bpy

# == PANELS
class GEOMETRY_HT_panel(bpy.types.Panel):
    
    bl_idname = 'GEOMETRY_HT_panel'
    bl_label = 'Geometry definition'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tripoli" 
    
    def draw(self, context:bpy.types.Context):
        layout = self.layout
        layout.label(text="Geometry building from Tripoli file.")

# == PANELS
class JDD_PT_panel(bpy.types.Panel):
    
    bl_parent_id = "GEOMETRY_HT_panel"
    bl_idname = 'JDD_PT_panel'
    bl_label = 'Tripoli geometry file'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context:bpy.types.Context):
        col = self.layout.column()
        row = col.row()
        split = row.split(factor=0.9)
        col1 = split.column()
        col2 = split.column()


        col1.prop(context.scene,'Tripoli_JDD')
        col2.operator("EXPLORER_JDD.import", icon="FILEBROWSER")

        col.operator("file_loader.import", text="Load TRIPOLI file")

        if context.scene.TJDD != None:
            self.layout.label(text="Surfaces count : "+str(context.scene.surf_count), icon = 'INFO')
            self.layout.label(text="Fictive count : "+str(context.scene.fictive_count), icon = 'INFO')
            self.layout.label(text="Volumes count : "+str(context.scene.vol_count), icon = 'INFO')
            self.layout.label(text="Composition count : "+str(context.scene.compo_count), icon = 'INFO')

# == PANELS
class VOLUMES_PT_panel(bpy.types.Panel):
    
    bl_parent_id = "GEOMETRY_HT_panel"
    bl_idname = 'VOLUMES_PT_panel'
    bl_label = 'Volumes'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context:bpy.types.Context):
        if context.scene.TJDD is None:
            self.layout.label(text="Please load a Tripoli input file first.", icon="ERROR")
        else:
            if bpy.data.filepath == "":
                self.layout.label(text="Please save your Blender file first.", icon="ERROR")
            else:
                col = self.layout.column()
                # row = col.row()
                # split = row.split(factor=0.9)
                # col1 = split.column()
                # col2 = split.column()
                
                col.prop(context.scene,'volume_x_min')
                col.prop(context.scene,'volume_x_max')
                col.prop(context.scene,'volume_y_min')
                col.prop(context.scene,'volume_y_max')
                col.prop(context.scene,'volume_z_min')
                col.prop(context.scene,'volume_z_max')

                col.operator('volume.create', text='Create volumes')
                # col.prop(context.scene,'vol_visible')

                
                col.prop(context.scene,'del_vol')

                if context.scene.del_vol:
                    col.operator('clean.volumes', text='Delete volumes')


            
class MATERIALS_PT_panel(bpy.types.Panel):
    
    bl_parent_id = "GEOMETRY_HT_panel"
    bl_idname = 'MATERIALS_PT_panel'
    bl_label = 'Materials'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context:bpy.types.Context):
        if context.scene.TJDD is None:
            self.layout.label(text="Please load a Tripoli input file first.")
        else:
            if not context.scene.vol_created:
                self.layout.label(text="Please create the volumes first.", icon="ERROR")
            else:

                col = self.layout.column()
                row = col.row()
                split = row.split(factor=0.9)
                col1 = split.column()
                col2 = split.column()

                col.operator('material.create', text='Create materials')
                col.prop(context.scene,'mat_visible')
        