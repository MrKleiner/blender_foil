bl_info = {
    'name': 'Blender Foil',
    'author': 'MrKleiner',
    'version': (1, 0),
    'blender': (2, 93, 1),
    'location': 'N menu',
    'description': '',
    'warning': '',
    'doc_url': '',
    'category': 'Add Mesh',
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import re
from shutil import copyfile
import os
import json
from re import search
import math
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import hashlib
import mathutils
import os.path
from pathlib import Path
import sys
import shutil

from .logic import *
from .ui import *




class OBJECT_OT_add_to_vgroup(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_to_vgroup"
    bl_label = "Add Mesh Object"
    # bl_options = {'REGISTER'}
    
    # gr_id = StringProperty(default='nil')
    gr_id: bpy.props.StringProperty(
        name = 'gr_id',
        default = 'asd'
    )

    # @classmethod
    
    def execute(self, context):
        # print(self.gr_id)
        assign_to_vgroup(self, context)

        return {'FINISHED'}


class OBJECT_OT_unmark_asset(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.unmark_asset"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER'}

    def execute(self, context):

        unmark_asset(self, context)

        return {'FINISHED'}


class OBJECT_OT_vmf_export_foil(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.vmf_export_foil"
    bl_label = "Export to vmf"
    bl_options = {'REGISTER'}

    def execute(self, context):

        vmf_export_foil(self, context)

        return {'FINISHED'}


# scene config storage
class blender_foil(PropertyGroup):

    all_lights : BoolProperty(
        name='Enable or Disable',
        description='A bool property',
        default = False
        )
        
    scene_vmf_path : StringProperty(
        name='Path to vmf',
        description='lizards are sexy',
        default = 'nil',
        subtype='FILE_PATH',
        update=append_vmf_vgroups
        )
        
    lightsradcsum : StringProperty(
        name='checksum',
        description='I want a lizard to put her tongue in my urethra',
        default = 'nil',
        )

    foil_export_area_lights : BoolProperty(
        name='Enable or Disable',
        description='A bool property',
        default = False
        )

    foil_export_props : BoolProperty(
        name='Enable or Disable',
        description='A bool property',
        default = False
        )
        
        # EnumProperty(items=test_rad_list, name="Rads", default='nil', update=setrad_col)
        
    scene_radlights_path : StringProperty(
        name='Path to .rad',
        description='I like bread',
        default = 'nil',
        subtype='FILE_PATH'
        )
        
    scene_vmf_visgroups : EnumProperty(
        items=scene_vmf_vgroups,
        name='all visgroups',
        description='I like bread'
        # default = "nil"
        )
        
        
        
        # --------
        # Skyboxer
        # --------
    blfoil_sky_game_path : StringProperty(
        name='Path to the game dir. half-life 2/ep2',
        description='Has to point to a valid source engine game setup. half-life 2/ep2, where half-life 2/bin contains stuff like vtex.exe',
        default = 'blfoil_game_path - nil',
        subtype='DIR_PATH'
        )
        
    blfoil_sky_use_sourceops_gpath: BoolProperty(
        name='Use SourceOps game path',
        description='My dick so big so really big, black holes move towards my huge dick',
        default = False 
        )
        
    blfoil_sky_boxname : StringProperty(
        name='The name of the baked skybox',
        description='doctor sex',
        default = 'blfoil_sky_boxname - nil'
        )
        
    blfoil_sky_size_x : IntProperty(
        name='Skybox X size',
        description='Size of each skybox square on X axis',
        default=1024,
        min=8,
        max=8192,
        soft_max=4096,
        soft_min=128,
        subtype='UNSIGNED'
        )
        
    blfoil_sky_size_y : IntProperty(
        name='Skybox X size',
        description='Size of each skybox square on X axis',
        default=1024,
        min=8,
        max=8192,
        soft_max=4096,
        soft_min=128,
        subtype='UNSIGNED'
        )

    blfoil_sky_keep_src_f_exr : BoolProperty(
        name='Whether to keep the src exr files or not',
        description='Disabling this will result into .exr files being deleted',
        default = True
        )
        
    blfoil_sky_keep_src_f_pfm : BoolProperty(
        name='Whether to keep the src .pfm files or not',
        description='Disabling this will result into .pfm files being deleted',
        default = True
        )
        
    blfoil_sky_moveto_afterb_path : StringProperty(
        name='Copy compiled stuff here',
        description='Should point to the "materials" folder. Will write to materials/skybox if present and overwrite any existing stuff. This description is redundant',
        default = 'nil',
        subtype='FILE_PATH'
        )
        
    blfoil_sky_moveto_afterb_movecopy : BoolProperty(
        name='asddw',
        description='Move. Otherwise - copy',
        default = False
        )
        
    blfoil_sky_hdrldr : EnumProperty(
        items=[
        ('HDR', 'HDR', 'ded2'),
        ('LDR', 'LDR', 'ded2')
        ],
        name='ldr/hdr',
        description='I want to kiss a lizard'
        # default = "nil"
        )
        
    blfoil_sky_hdr_compressed : BoolProperty(
        name='Compress into 8 bit + alpha',
        # description='Compress the shit like juicy tits',
        description='Lmfao are you serious? Your shit will look rubbish af',
        default = False
        )
        
    blfoil_sky_projectonly : BoolProperty(
        name='Simple projection',
        description='If set - seimply project whatever is plugged into the world on a cube, avoiding any renders',
        default = False
        )
        
    blfoil_sky_overwrite_shit : BoolProperty(
        name='Overwrite',
        description='oral',
        default = False 
        )
        
    # blfoil_sky_maxsize : BoolProperty(
        # name='Molest source engine',
        # description='Insert a 1 cm silicone rod into his urethra',
        # default = False 
        # )
        
    blfoil_sky_nobottom : BoolProperty(
        name='No bottom',
        description='Destroy his ass',
        default = False 
        )
        
    blfoil_sky_mkenvmap : BoolProperty(
        name='Make envmap',
        description='Pootis',
        default = False 
        )
        
    blfoil_sky_mkenvmap_only : BoolProperty(
        name='Only envmap',
        description='Pootis',
        default = False 
        )


# shared object config 
class foil_obj_settings(PropertyGroup):

    ignore : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    model_name : StringProperty(
        name="Model Name",
        description="i want to fuck a lizard",
        default = ""
        )
        
    arlight_config : StringProperty(
        name="Area Light Config",
        description="i want to fuck an Alien",
        default = ""
        )
    arlight_strength : FloatProperty(
        name="arlightstrength",
        description="nen",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=3,
        update=upd_area
        )
    object_assigned_vgroups : StringProperty(
        default='',
        name='assigned_visgroups',
        )
        

class OBJECT_OT_set_arlight(Operator, AddObjectHelper):
    """Set area light"""
    bl_idname = "mesh.set_arlight_op"
    bl_label = "Set area light"
    bl_options = {'REGISTER'}

    def execute(self, context):

        set_arlight_op(self, context)

        return {'FINISHED'}

class OBJECT_OT_unset_arlight(Operator, AddObjectHelper):
    """UNset area light"""
    bl_idname = "mesh.unset_arlight_conf"
    bl_label = "Set area light"
    bl_options = {'REGISTER'}

    def execute(self, context):

        unset_arlight_exp(self, context)
        return {'FINISHED'}

class OBJECT_OT_copy_arlight_conf(Operator, AddObjectHelper):
    """UNset area light"""
    bl_idname = "mesh.copy_arlight_config"
    bl_label = "Set area light"
    bl_options = {'REGISTER'}

    def execute(self, context):

        copy_arlight_config(self, context)
        return {'FINISHED'}

class OBJECT_OT_export_arlights_vmf(Operator, AddObjectHelper):
    """UNset area light"""
    bl_idname = "mesh.export_arlights_vmf"
    bl_label = "Export arlights vmf"
    bl_options = {'REGISTER'}

    def execute(self, context):

        foil_export_area_lights(self, context)
        return {'FINISHED'}

class OBJECT_OT_blfoil_bake_skybox_opr(Operator, AddObjectHelper):
    bl_idname = 'mesh.blfoil_bake_skybox_opr'
    bl_label = 'Compile skybox'
    bl_options = {'REGISTER'}

    def execute(self, context):

        foil_compile_skybox(self, context)
        return {'FINISHED'}



def register():
    
    # bpy.types.WindowManager.my_operator_toggle = bpy.props.BoolProperty()
    
    bpy.utils.register_class(blender_foil)
    bpy.types.Scene.blfoil = PointerProperty(type=blender_foil)
    
    
    bpy.utils.register_class(OBJECT_OT_unmark_asset)
    bpy.utils.register_class(OBJECT_OT_add_to_vgroup)
    bpy.utils.register_class(OBJECT_OT_set_arlight)
    bpy.utils.register_class(OBJECT_OT_unset_arlight)
    bpy.utils.register_class(OBJECT_OT_copy_arlight_conf)
    
    bpy.utils.register_class(foil_obj_settings)
    bpy.utils.register_class(OBJECT_OT_vmf_export_foil)
    bpy.utils.register_class(VIEW3D_PT_blender_foil)
    bpy.utils.register_class(VIEW3D_PT_blender_foil_visgroups)
    bpy.utils.register_class(VIEW3D_PT_blender_foil_skyboxer)
    bpy.utils.register_class(OBJECT_OT_export_arlights_vmf)
    bpy.utils.register_class(OBJECT_OT_blfoil_bake_skybox_opr)
    # bpy.utils.register_manual_map(unmark_asset_manual_map)
    # bpy.types.VIEW3D_MT_mesh_add.append(unmark_asset_button)
    # bpy.types.Scene.my_tool = PointerProperty(type=MySettings)
    
    bpy.types.Object.foil_conf = PointerProperty(type=foil_obj_settings)
    bpy.types.Scene.lightsrad = EnumProperty(items=test_rad_list, name="Rads", default='nil', update=setrad_col)
    
    bpy.types.Scene.rad_color = bpy.props.FloatVectorProperty(subtype='COLOR')


def unregister():
    # del bpy.types.Scene.mass_import_path
    bpy.utils.unregister_class(OBJECT_OT_unmark_asset)
    bpy.utils.unregister_class(OBJECT_OT_add_to_vgroup)
    bpy.utils.unregister_class(blender_foil)
    bpy.utils.unregister_class(foil_obj_settings)
    bpy.utils.unregister_class(OBJECT_OT_vmf_export_foil)
    bpy.utils.unregister_class(VIEW3D_PT_blender_foil)
    bpy.utils.unregister_class(VIEW3D_PT_blender_foil_visgroups)
    bpy.utils.unregister_class(VIEW3D_PT_blender_foil_skyboxer)
    bpy.utils.unregister_class(OBJECT_OT_unset_arlight)
    bpy.utils.unregister_class(OBJECT_OT_set_arlight)
    bpy.utils.unregister_class(OBJECT_OT_export_arlights_vmf)
    bpy.utils.unregister_class(OBJECT_OT_blfoil_bake_skybox_opr)
    bpy.utils.unregister_class(OBJECT_OT_copy_arlight_conf)
    # bpy.utils.unregister_manual_map(unmark_asset_manual_map)
    # bpy.types.VIEW3D_MT_mesh_add.remove(unmark_asset_button)
    
    del bpy.types.Object.foil_conf
    del bpy.types.Scene.blfoil
    del bpy.types.Scene.lightsrad
    del bpy.types.Scene.rad_color