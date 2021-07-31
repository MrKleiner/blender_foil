import bpy



#
# View Panel
#

class VIEW3D_PT_blender_foil(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'foil'
    bl_label = 'Aluminium'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.blfoil, 'scene_vmf_path')
        col.prop(context.scene.blfoil, 'scene_radlights_path')
        
        col = layout.column(align=True)
        # print(context.object.type)
        if context.object:
            if context.object.type != 'LIGHT':
                col.prop(context.object.foil_conf, 'model_name')
            else:
                col.label(text='nein')
        else:
            col.label(text='nein')
        
        # create unmark asset
        self.layout.operator('mesh.unmark_asset',
            text='Unmark hammer model'
        )
        
        self.layout.operator('mesh.vmf_export_foil',
            text='Export to vmf'
        )
        
        self.layout.operator('mesh.export_arlights_vmf',
            text='Export area lights to given vmf'
        )
        
        # create all lights are hammer checkbox
        col.prop(context.scene.blfoil, 'all_lights', text='Export all lights')
        # print('triggered')
        if context.object:
            if context.object.type == 'LIGHT' and context.object.data.type == 'AREA':
                teacup = layout.box()
                teabag = teacup.row()
                sugar = teacup.row()
                # spoon = teacup.row()
                
                melt_dead_space = teacup.column(align=True)
                
                # wheel = teacup.row()
                urethral_dilator = teacup.row()
                fleshlight = teacup.row()
                handbrake = teacup.row()
                bumper_cars = teacup.row()
                
                teabag.label(text='Area Light Config')

                sugar.prop(context.scene, 'lightsrad')
                melt_dead_space.prop(context.scene, 'rad_color', text='')
                # sugar.prop(context.scene, 'rad_color', text='Rad Color')
                
                melt_dead_space.prop(context.object.foil_conf, 'arlight_strength', slider=True, text='Strength')
                
                urethral_dilator.operator('mesh.set_arlight_op',
                    text='Set Area Light config'
                )
                
                fleshlight.operator('mesh.unset_arlight_conf',
                    text='Unset Area Light config'
                )
                
                handbrake.operator('mesh.copy_arlight_config',
                    text='Copy Area Light config to selected'
                )
                
                

                bumper_cars.label(text=str(context.object.foil_conf.arlight_config.split(':')[0]))
                
            else:
                col.label(text='nein')
        else:
            col.label(text='nein')


class VIEW3D_PT_blender_foil_visgroups(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "foil"
    bl_label = "Visgroups"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
        
        col.label(text='nein')
        
        if not bpy.context.active_object == None:
            if '.vmf' in str(bpy.path.abspath(bpy.context.scene.blfoil.scene_vmf_path)):
                for item in scene_vmf_vgroups:
                    if item[0].split(':')[0] in bpy.context.active_object.foil_conf.object_assigned_vgroups.split(':'):
                        fuck = col.row()
                        ded_l = fuck.column()
                        ded_l.operator('mesh.add_to_vgroup',
                            text=item[1],
                            # active=True
                        ).gr_id = item[0].split(':')[0]
                        
                        ded_r = fuck.column()
                        ded_r.scale_x = 0.5
                        
                        ded_r.operator('mesh.add_to_vgroup',
                            text='Unset',
                            # active=True
                        ).gr_id = item[0].split(':')[0]
                    else:
                        col.operator('mesh.add_to_vgroup',
                            text=item[1],
                            # active=True
                        ).gr_id = item[0].split(':')[0]
            else:
                info = layout.column(align=False)
                info.label(text='no vmf')


class VIEW3D_PT_blender_foil_skyboxer(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "foil"
    bl_label = 'Sugarplum Gaben'
    # https://youtu.be/sT3joXENOb0
    
    def draw(self, context):
        layout = self.layout
        
        
        general_col = layout.column(align=False)
        general_col.label(text='Skybox exporter')
        
        usesrcops = general_col.row()
        # todo: maybe make it disappear if not sourceops? make it disabled if no items in source ops?
        usesrcops.prop(context.scene.blfoil, 'blfoil_sky_use_sourceops_gpath', text='Use SourceOps game path')
        if hasattr(context.scene, 'sourceops'):
            usesrcops.enabled = True
        else:
            usesrcops.enabled = False
        general_col.prop(context.scene.blfoil, 'blfoil_sky_game_path', text='Game path')
        general_col.prop(context.scene.blfoil, 'blfoil_sky_boxname', text='Skybox name')
        
        
        dimensions_col = layout.column(align=True)
        dimensions_col.use_property_split = True
        dimensions_col.use_property_decorate = False
        
        dimensions_col.prop(context.scene.blfoil, 'blfoil_sky_size_x')
        dimensions_col.prop(context.scene.blfoil, 'blfoil_sky_size_y', text='Skybox Y size')
        
        
        dimensions_col.prop(context.scene.blfoil, 'blfoil_sky_nobottom', text='No bottom')
        
        
        leave_src_files = layout.column(align=False)
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR': 
            leave_src_files.prop(context.scene.blfoil, 'blfoil_sky_keep_src_f_exr', text='Keep .exr src files')
            leave_src_files.prop(context.scene.blfoil, 'blfoil_sky_keep_src_f_pfm', text='Keep .pfm src files')
        else:
            leave_src_files.prop(context.scene.blfoil, 'blfoil_sky_keep_src_f_exr', text='Keep .tga src files')
            dim_exrsrc = leave_src_files.row()
            dim_exrsrc.enabled = False
            dim_exrsrc.prop(context.scene.blfoil, 'blfoil_sky_keep_src_f_pfm', text='Keep .pfm src files')
            
            
        
        move_vtf_here = layout.column(align=False)
        leave_src_files.prop(context.scene.blfoil, 'blfoil_sky_moveto_afterb_path', text='Move/Copy')
        leave_src_files.prop(context.scene.blfoil, 'blfoil_sky_moveto_afterb_movecopy', text='Move')
        
        mkenvmap_r = layout.column(align=False)
        mkenvmap_r.prop(context.scene.blfoil, 'blfoil_sky_mkenvmap', text='Make envmap')
        
        envmaponlyrow = mkenvmap_r.row()
        if context.scene.blfoil.blfoil_sky_mkenvmap == True:
            envmaponlyrow.enabled = True
        else:
            envmaponlyrow.enabled = False
        envmaponlyrow.prop(context.scene.blfoil, 'blfoil_sky_mkenvmap_only', text='Envmap only')
        
        
        hdrldr = layout.column(align=False)
        hdrldr_switch = hdrldr.row()
        hdrldr_switch.prop(context.scene.blfoil, 'blfoil_sky_hdrldr', expand=True)
        
        compr_sw = hdrldr.row()
        compr_sw.prop(context.scene.blfoil, 'blfoil_sky_hdr_compressed', text='Compressed 8 bit HDR (make it look rubbish)')
        
        # maybe make it appear and disappear ??
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'LDR':
            compr_sw.enabled = False
        else:
            compr_sw.enabled = True
        
        
        overwrite_sh = layout.column(align=False)
        # overwrite_sh.prop(context.scene.blfoil, 'blfoil_sky_projectonly', text='Project only')
        overwrite_sh.prop(context.scene.blfoil, 'blfoil_sky_overwrite_shit', text='Overwrite')

        mabaker_op = layout.column(align=False)
        self.layout.operator('mesh.blfoil_bake_skybox_opr',
            text='Compile skybox'
        )
# Registration

