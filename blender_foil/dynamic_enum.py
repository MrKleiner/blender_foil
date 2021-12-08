bl_info = {
    'name': 'BlenderFoil',
    'author': 'MrKleiner',
    'version': (1, 0),
    'blender': (3, 0, 0),
    'location': 'N menu',
    'description': 'Export shit from blender to source engine. Also, I like bread',
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
import random
import bmesh
import mathutils
import os.path, time
from pathlib import Path
import sys
import shutil
import subprocess
import datetime
import pathlib
from math import radians
from mathutils import Matrix

# figure out a way of loading this from a subfodler, if possible
from bs4 import BeautifulSoup
from bs4 import Tag, NavigableString


# todo: Separate actions into functions as often as possible



# get the current directory. Just in case
addon_root_dir = Path(__file__).absolute().parent

# vp_radpath = pathlib.Path(bpy.context.scene.blents.dn_str)

# get path to the entity definition json
# should be in the subdir of this file on release
vp_blpe_path = pathlib.Path('E:\\!!Blend_Projects\\scripts\\wallworm4blender\\blender_foil\\blender_foil\\blpe_main.json')

print('rebuild json')

# parse json and therefore obtain the list of all the entities and their params
vp_blpe_ents = json.loads(open(vp_blpe_path).read())



# define names of the supported icons
# gui_name:real_ent_name
# a json should have a corresponding entry
supported_icons = [
    ('logic_case', 'nein'),
    ('env_cubemap', 'nicht'),
    ('logic_relay', 'nicht'),
    ('filter_activator_name', 'nicht')
    
]







# =========================================================
#----------------------------------------------------------
#                           Enums
#----------------------------------------------------------
# =========================================================


def enum_returner_1(self, context):

    shit_number = 1

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)
        
        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []
        
        # for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4]):
            # obj.ent_conf['pr_str_' + str(str_j_idx + 1)] = vp_blpe_ents[cent_type][0][str_pr].split(':-:')[1]
            
        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            # lizard_sex.append(('enum_entry', vp_blpe_ents[cent_type][4][indexed_ballsack[0]][0][enum_ballsack], 'enum_entry'))
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))
        
        
        
        return lizard_sex

    else:
        return []


def enum_returner_2(self, context):

    shit_number = 2

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_3(self, context):

    shit_number = 3

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_4(self, context):

    shit_number = 4

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_5(self, context):

    shit_number = 5

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_6(self, context):

    shit_number = 6

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_7(self, context):

    shit_number = 7

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_8(self, context):

    shit_number = 8

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_9(self, context):

    shit_number = 9

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_10(self, context):

    shit_number = 10

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_11(self, context):

    shit_number = 11

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_12(self, context):

    shit_number = 12

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_13(self, context):

    shit_number = 13

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_14(self, context):

    shit_number = 14

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_15(self, context):

    shit_number = 15

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []


def enum_returner_16(self, context):

    shit_number = 16

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((vp_blpe_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



#
# Targets
#

# since all the enums are reusable slots - we have to trasfer the chosen value to the static config of the object
# every object has predefined slots for all possible kinds of data
def enum_tgt_1(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_1'] = bpy.context.active_object.ent_conf.pr_enum_1

def enum_tgt_2(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_2'] = bpy.context.active_object.ent_conf.pr_enum_2

def enum_tgt_3(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_3'] = bpy.context.active_object.ent_conf.pr_enum_3

def enum_tgt_4(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_4'] = bpy.context.active_object.ent_conf.pr_enum_4

def enum_tgt_5(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_5'] = bpy.context.active_object.ent_conf.pr_enum_5

def enum_tgt_6(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_6'] = bpy.context.active_object.ent_conf.pr_enum_6

def enum_tgt_7(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_7'] = bpy.context.active_object.ent_conf.pr_enum_7

def enum_tgt_8(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_8'] = bpy.context.active_object.ent_conf.pr_enum_8

def enum_tgt_9(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_9'] = bpy.context.active_object.ent_conf.pr_enum_9

def enum_tgt_10(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_10'] = bpy.context.active_object.ent_conf.pr_enum_10

def enum_tgt_11(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_11'] = bpy.context.active_object.ent_conf.pr_enum_11

def enum_tgt_12(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_12'] = bpy.context.active_object.ent_conf.pr_enum_12

def enum_tgt_13(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_13'] = bpy.context.active_object.ent_conf.pr_enum_13

def enum_tgt_14(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_14'] = bpy.context.active_object.ent_conf.pr_enum_14

def enum_tgt_15(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_15'] = bpy.context.active_object.ent_conf.pr_enum_15

def enum_tgt_16(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_16'] = bpy.context.active_object.ent_conf.pr_enum_16







# =========================================================
#----------------------------------------------------------
#                   Base functionality
#----------------------------------------------------------
# =========================================================


#
# Base reusable functions
#

# Returns Object transforms in a format of {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}
# Usage: call this function with an object
# eobject - object selector
# fix90 - 1 to fix the rotation (rotate an object either on Y or other axis)
# axis - axis to apply the rotation to: X, Y or Z
def get_obj_locrot_v1(eobject, fix90, axis, self, context):

    # extract rotations
    
    # get scene scale
    if context.scene.unit_settings.system != 'NONE':
        sce_scale = bpy.context.scene.unit_settings.scale_length
    else:
        sce_scale = 1
    
    if 'z' in str(axis).lower():
        fl_axis = 'Z'
    else: 
        fl_axis = 'Y'
        
    if '-' in str(axis).lower():
        rfactor = -1
    else:
        rfactor = 1
    
    # hack pentagon
    if int(fix90) == 1:
        # eobject.rotation_euler.rotate_axis(fl_axis, math.radians(-90 * rfactor))
        # bpy.context.view_layer.update()
        
        # rotall = ((eobject.rotation_euler.to_matrix() @ Matrix.Rotation(radians(90 * rfactor), 3, 'Y')) @ eobject.matrix_world).to_euler()
        rot_st = Matrix.Rotation(radians(90), 4, 'Y')
        
        rotall = (eobject.matrix_world @ rot_st).to_euler()
        
        rotx = float(round(math.degrees(rotall[0]), 4))
        roty = float(round(math.degrees(rotall[1]), 4))
        rotz = float(round(math.degrees(rotall[2]), 4))
    else:
        rotx = float(round(math.degrees(eobject.matrix_world.to_euler()[0]), 4))
        roty = float(round(math.degrees(eobject.matrix_world.to_euler()[1]), 4))
        rotz = float(round(math.degrees(eobject.matrix_world.to_euler()[2]), 4))
    

    
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print(eobject.rotation_euler[2])
    
    # hack pentagon
    # if int(fix90) == 1:
        # eobject.rotation_euler.rotate_axis(fl_axis, math.radians(+90 * rfactor))
        # bpy.context.view_layer.update()

    # extract locations
    locx = float(round(eobject.matrix_world[0][3], 4) * sce_scale)
    locy = float(round(eobject.matrix_world[1][3], 4) * sce_scale)
    locz = float(round(eobject.matrix_world[2][3], 4) * sce_scale)

    return {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}


# link all the curves used to visualize an entity
# so that there are no excess verts
def cdata_cleanup(self, context):
    for existing_icon in supported_icons:
        all_fuckdata = []
        
        for foil_obj in bpy.data.objects:
            if foil_obj.type == 'CURVE':
                if existing_icon[0] + '_curve_data' in foil_obj.data.name:
                    all_fuckdata.append(foil_obj.data)

        if len(all_fuckdata) > 1:
            for foil_obj in bpy.data.objects:
                if existing_icon[0] + '_curve_data' in foil_obj.data.name:
                    foil_obj.data = all_fuckdata[0]
            
            for ded_data in bpy.data.curves:
                if existing_icon[0] + '_curve_data' in ded_data.name:
                    if ded_data != all_fuckdata[0]:
                        bpy.data.curves.remove(ded_data)
















# dynamically build supported entities enum list (from blpe_main.json)
# On blender startup - we read and parse the blpe json in the very beginning of the script
# and then reuse it, for example here.
def r_enum_list(self, context):
    # current_time = datetime.datetime.now()
    
    if context is None:
        return []
    
    print('rebuild enum list ' + str(current_time))
    
    # dev print
    # for thl in radlines:
        # print(thl)
    
    
    # so here we read and overwrite everyhing

    re_scene_ents = []
    for ent in vp_blpe_ents:
        re_scene_ents.append((ent, ent, 'ent'))
        

    # print(re_scene_ents)
    return re_scene_ents
    

def r_enum_list_rads(self, context):
    current_time = datetime.datetime.now()
    radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
    # print(radpath.stat().st_mtime)
    
    if context is None:
        return []
    

    print('rebuild enum list ' + str(current_time))
    # scene_vmf_vgroups = []
    radfile = open(radpath)
    radlines = radfile.readlines()
    
    # dev print
    # for thl in radlines:
        # print(thl)
    
    
    # so here we read and overwrite everyhing

    re_scene_vmf_vgroups = []
    for rline in radlines:
        rlinetweak = rline.replace('\t', ' ').replace('\n', '').strip().split(' ')
        if len(rline) > 10:
            path = rlinetweak[0]
            zvalue = str(rlinetweak[-1]) + ' ' + str(rlinetweak[-2]) + ' ' + str(rlinetweak[-3]) + ' ' + str(rlinetweak[-4])
            # print(path + ':::' + zvalue)

            # construct the return list
            re_scene_vmf_vgroups.append(('rad_entry', path, 'rad_entry'))
        

    # print(re_scene_vmf_vgroups)
    return re_scene_vmf_vgroups
    

def r_enum_list_v1(self, context):
    current_time = datetime.datetime.now()
    radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
    print(radpath.stat().st_mtime)
    
    if context is None:
        return []
    
    # if the mod date doesnt match - rebuild list. If it does - return old value recorded in scene
    if str(bpy.context.scene.blents.last_mod_time) != str(radpath.stat().st_mtime):
        bpy.context.scene.blents.last_mod_time = str(radpath.stat().st_mtime)
        print('rebuild enum list')
        # scene_vmf_vgroups = []
        radfile = open(radpath)
        radlines = radfile.readlines()
        
        # dev print
        for thl in radlines:
            print(thl)
        
        
        # so here we read and overwrite everyhing
        app_rad_list = []
        re_scene_vmf_vgroups = []
        for rline in radlines:
            rlinetweak = rline.replace('\t', ' ').replace('\n', '').strip().split(' ')
            if len(rline) > 10:
                path = rlinetweak[0]
                zvalue = str(rlinetweak[-1]) + ' ' + str(rlinetweak[-2]) + ' ' + str(rlinetweak[-3]) + ' ' + str(rlinetweak[-4])
                print(path + ':::' + zvalue)
                app_rad_list.append((path, zvalue))
                
                # construct the return list
                re_scene_vmf_vgroups.append(('rad_entry', path, 'rad_entry'))
        
        # record parsed value to scene for later reuse
        # bpy.context.scene.blents['blfoil_parsed_radlist'] = app_rad_list
        
        # record enum to return later if file hasnt changed
        # bpy.context.scene.blents['blfoil_enum_radlist'] = re_scene_vmf_vgroups
        print(re_scene_vmf_vgroups)
        return re_scene_vmf_vgroups
    
    else:
        print('dont rebuild enum list')
        fixed_enum = []
        for fix_entry in bpy.context.scene.blents['blfoil_enum_radlist']:
            fuck = (fix_entry[0], fix_entry[1], fix_entry[2])
            fixed_enum.append(fuck)
        print(fixed_enum)
        return fixed_enum
    
# call this function with object selected to evaluate its spawnflags
# todo: make this function accept object input
def eval_spawnflags(self, context):

    print('eval spawnflags')

    # evaluate
    for obj in bpy.context.selected_objects:
        print('calc spawnflags')
        cur_obj_ent_type = obj.ent_conf.obj_ent_type
        obj.ent_conf['l3_ent_sflags'] = 0
        
        calculated_bytes = 0
        
        for sflag_index, sflag in enumerate(vp_blpe_ents[cur_obj_ent_type][6]):
            
            if obj.ent_conf['pr_sflags_' + str(sflag_index + 1)] == True:
                calculated_bytes += int(sflag)
        
        obj.ent_conf['l3_ent_sflags'] = calculated_bytes
        print('calculated flags are: ' + str(calculated_bytes))
    
        
# mark currently selected object as an entity
# and clean all the data which was probably left from the previous entity
def set_obj_ent(self, context):

    def eval_state(state):
        if int(state) == 1:
            return True
        if int(state) == 0:
            return False
        if int(state) != 1 and int(state) != 0:
            return False

    
    # current entity type
    cent_type = bpy.context.scene.blents.dnenum
    
    # index all the enum ballsacks
    indexed_ballsack = []
    
    # make list of all enums:
    for enum_ind, enum_name in enumerate(vp_blpe_ents[cent_type][4]):
        indexed_ballsack.append(enum_name)
    
    
    # set to default
    for obj in bpy.context.selected_objects:
        print('set entity')
        obj.ent_conf.obj_ent_type = bpy.context.scene.blents.dnenum
        obj.ent_conf['l3_ent_sflags'] = 0
        
        
        # set strings to default
        for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
            obj.ent_conf['pr_str_' + str(str_j_idx + 1)] = vp_blpe_ents[cent_type][0][str_pr].split(':-:')[1]
            
            # dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_j_idx + 1), text=str_pr)
            
        # set ints to default
        for ind_j_idx, ind_pr in enumerate(vp_blpe_ents[cent_type][1]):
            obj.ent_conf['pr_int_' + str(ind_j_idx + 1)] = int(vp_blpe_ents[cent_type][1][ind_pr].split(':-:')[1])
        
        # set floats to default
        for float_j_idx, float_pr in enumerate(vp_blpe_ents[cent_type][2]):
            obj.ent_conf['pr_float_' + str(float_j_idx + 1)] = float(vp_blpe_ents[cent_type][2][float_pr].split(':-:')[1])


        # set enums to default.
        for enum_j_idx, enum_pr in enumerate(vp_blpe_ents[cent_type][4]):
            # obj.ent_conf['pr_enum_' + str(enum_j_idx + 1)] = enum_pr.split(':-:')[1]
            obj.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)] = vp_blpe_ents[cent_type][4][enum_pr][0][enum_pr.split(':-:')[1]]
            obj.ent_conf['pr_enum_' + str(enum_j_idx + 1)] = vp_blpe_ents[cent_type][4][enum_pr][0][enum_pr.split(':-:')[1]]
            # print('set def idx ' + str(enum_j_idx) + ' enum to: ' + '"' + str(vp_blpe_ents[cent_type][4][enum_pr][0][enum_pr.split(':-:')[1]]) + '"')
        

        # set enum bools to default.
        for enum_bool_j_idx, enum_bool_pr in enumerate(vp_blpe_ents[cent_type][5]):
            obj.ent_conf['pr_enum_bool_' + str(enum_bool_j_idx + 1)] = eval_state(vp_blpe_ents[cent_type][5][enum_bool_pr].split(':-:')[1])
            
            
        # set Spawn Flags to default
        for sflags_j_idx, sflags_pr in enumerate(vp_blpe_ents[cent_type][6]):
            obj.ent_conf['pr_sflags_' + str(sflags_j_idx + 1)] = eval_state(vp_blpe_ents[cent_type][6][sflags_pr].split(':-:')[0])
            
            
        # set Colors to default
        for color_j_idx, color_pr in enumerate(vp_blpe_ents[cent_type][3]):
        
            jrgb = vp_blpe_ents[cent_type][3][color_pr].split(':-:')[1].split(' ')
        
            ar = int(jrgb[0]) / 255
            ag = int(jrgb[1]) / 255
            ab = int(jrgb[2]) / 255

            obj.ent_conf['pr_color_' + str(color_j_idx + 1)] = (ar, ag, ab)
            
    eval_spawnflags(self, context)





# Export entities to a given vmf
def test_export_v1(self, context):
    print('exec')
    
    cdata_cleanup(self, context)
    
    def return_1_0(state):
        if state == True:
            return 1
        if state == False:
            return 0
        if state != False and state != True:
            return 0
            
    
    cdata_cleanup(self, context)
    # ===================================
    #               Cleanup
    # ===================================
    sce_vmf_path = str('E:\\!!Blend_Projects\\scripts\\entity_exporter\\ents.vmf')

    file = open(sce_vmf_path)

    # create an array of lines out of the input vmf file
    linez = file.readlines()
    
    brstart = 0
    brmark = 0
    bigcum = 'nil'
    current_indent = 0

    delete_ents = []

 
    # scan all ents
    for strnum, linestr in enumerate(linez):
        # if re.search('^[a-zA-Z].*', linestr):
        if 'entity\n' in linestr:
            print('found ent: ' + str(strnum))
            brstart = strnum
            current_indent = len(linestr) - len(linestr.lstrip())
            print('ent indent ' + str(current_indent))
            
        if '"liz3"' in linestr and '"1"' in linestr:
            brmark = strnum
            
        if '}\n' in linestr and brstart != 0 and len(linestr) - len(linestr.lstrip()) == current_indent:
            print('found ent end: ' + str(strnum))
            delete_ents.append([brstart,brmark,strnum])
            print(linez[brstart-1])
            brstart = 0
            brmark = 0
            current_indent = 0
    
    # delete ents which have mark on them
    print(delete_ents)
    
    for entnum, del_ent in enumerate(reversed(delete_ents)):
        if del_ent[1] != 0:
            del linez[del_ent[0]:del_ent[2] + 1]
    
    # find camera
    for zstrnum, zlinestr in enumerate(linez):
        if 'cameras\n' in zlinestr:
            print('found camera: ' + str(zstrnum))
            bigcum = zstrnum
    
    print(linez)
    file.close()
    # TEST WRITE


    
    
    
    
    radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
    entfile = open(radpath)
    entjson = entfile.read()
    
    # all possible ents
    prop_ents = json.loads(entjson)
    
    
    # we export spotlights separately
    cbt_victim = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type != 'light_spot']
    
    
    
    print(cbt_victim)
    
    # spotlights
    monitor_lizard = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type == 'light_spot' and obj.type == 'LIGHT' and obj.data.type == 'SPOT']
    # monitor_lizard = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type == 'light_spot']
    
    constructed_ents = []
    
    
    # -----------
    #   Write
    # -----------
    for cbt in cbt_victim:
        mk_ent = []
        
        print('processing object: ' + str(cbt))
        
        cent_type = cbt.ent_conf.obj_ent_type
        
        # get transforms from blender
        obj_locrot = get_obj_locrot_v1(cbt, 1, 'z', self, context)
        
        
        #
        # write shared
        #
        
        # write opening
        mk_ent.append('entity\n{\n')
        mk_ent.append('\t' + '"classname" "' + cent_type + '"\n')
        mk_ent.append('\t' + '"liz3" "1"\n')    
        
        # any entity should have an origin - write origin (loc)
        mk_ent.append('\t' + '"origin" "' + str(obj_locrot['loc'][0]) + ' ' + str(obj_locrot['loc'][1]) + ' ' + str(obj_locrot['loc'][2]) + '"\n')
        
        # if it's stated in the blender config json block that this entity should have angles - write anlges
        if int(prop_ents[cent_type][9]['angles_enabled']) == 1:
            
            mk_ent.append('\t' + '"angles" "' + str(obj_locrot['rot'][1]) + ' ' + str(obj_locrot['rot'][2]) + ' ' + str(obj_locrot['rot'][0]) + '"\n')
        
        
        # write strings
        for str_j_idx, str_pr in enumerate(prop_ents[cent_type][0]):
            # strings are never empty, unless you take them off
            if cbt.ent_conf['pr_str_' + str(str_j_idx + 1)] != ' ':
                mk_ent.append('\t' + '"' + prop_ents[cent_type][0][str_pr].split(':-:')[0] + '" "' + cbt.ent_conf['pr_str_' + str(str_j_idx + 1)] + '"\n')


        # write ints
        for int_j_idx, int_pr in enumerate(prop_ents[cent_type][1]):
            mk_ent.append('\t' + '"' + prop_ents[cent_type][1][int_pr].split(':-:')[0] + '" "' + str(cbt.ent_conf['pr_int_' + str(int_j_idx + 1)]) + '"\n')
        
        
        # write floats
        for float_j_idx, float_pr in enumerate(prop_ents[cent_type][2]):
            mk_ent.append('\t' + '"' + prop_ents[cent_type][2][float_pr].split(':-:')[0] + '" "' + str(round(cbt.ent_conf['pr_float_' + str(float_j_idx + 1)], 4)) + '"\n')


        # write colors
        for color_j_idx, color_pr in enumerate(prop_ents[cent_type][3]):
            rgb = str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][0] * 255)) + ' ' + str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][1] * 255)) + ' ' + str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][2] * 255))
            mk_ent.append('\t' + '"' + prop_ents[cent_type][3][color_pr].split(':-:')[0] + '" "' + rgb + '"\n')


        # write enums
        for enum_j_idx, enum_pr in enumerate(prop_ents[cent_type][4]):
            mk_ent.append('\t' + '"' + cbt.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)].split(':-:')[0] + '" "' + cbt.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)].split(':-:')[1] + '"\n')
            # print(cbt.ent_conf['pr_enum_1'])

            
            
        """
        j_enum_amount = len(prop_ents[cent_type][4])
        
        if 1 <= j_enum_amount:
            en1v = cbt.ent_conf.pr_enum_1.split(':-:')
            mk_ent.append('\t' + '"' + en1v[0] + '" "' + en1v[1] + '"\n')

        if 2 <= j_enum_amount:
            print('pootis: ' + str(cbt.ent_conf.pr_enum_2))
            en2v = cbt.ent_conf.pr_enum_2.split(':-:')
            print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ')
            print(en2v)
            mk_ent.append('\t' + '"' + en2v[0] + '" "' + en2v[1] + '"\n')

        if 3 <= j_enum_amount:
            en3v = cbt.ent_conf.pr_enum_3.split(':-:')
            mk_ent.append('\t' + '"' + en3v[0] + '" "' + en3v[1] + '"\n')

        if 4 <= j_enum_amount:
            en4v = cbt.ent_conf.pr_enum_4.split(':-:')
            mk_ent.append('\t' + '"' + en4v[0] + '" "' + en4v[1] + '"\n')

        if 5 <= j_enum_amount:
            en5v = cbt.ent_conf.pr_enum_5.split(':-:')
            mk_ent.append('\t' + '"' + en5v[0] + '" "' + en5v[1] + '"\n')

        if 6 <= j_enum_amount:
            en6v = cbt.ent_conf.pr_enum_6.split(':-:')
            mk_ent.append('\t' + '"' + en6v[0] + '" "' + en6v[1] + '"\n')

        if 7 <= j_enum_amount:
            en7v = cbt.ent_conf.pr_enum_7.split(':-:')
            mk_ent.append('\t' + '"' + en7v[0] + '" "' + en7v[1] + '"\n')

        if 8 <= j_enum_amount:
            en8v = cbt.ent_conf.pr_enum_8.split(':-:')
            mk_ent.append('\t' + '"' + en8v[0] + '" "' + en8v[1] + '"\n')

        if 9 <= j_enum_amount:
            en9v = cbt.ent_conf.pr_enum_9.split(':-:')
            mk_ent.append('\t' + '"' + en9v[0] + '" "' + en9v[1] + '"\n')

        if 10 <= j_enum_amount:
            en10v = cbt.ent_conf.pr_enum_10.split(':-:')
            mk_ent.append('\t' + '"' + en10v[0] + '" "' + en10v[1] + '"\n')

        if 11 <= j_enum_amount:
            en11v = cbt.ent_conf.pr_enum_11.split(':-:')
            mk_ent.append('\t' + '"' + en11v[0] + '" "' + en11v[1] + '"\n')

        if 12 <= j_enum_amount:
            en12v = cbt.ent_conf.pr_enum_12.split(':-:')
            mk_ent.append('\t' + '"' + en12v[0] + '" "' + en12v[1] + '"\n')

        if 13 <= j_enum_amount:
            en13v = cbt.ent_conf.pr_enum_13.split(':-:')
            mk_ent.append('\t' + '"' + en13v[0] + '" "' + en13v[1] + '"\n')

        if 14 <= j_enum_amount:
            en14v = cbt.ent_conf.pr_enum_14.split(':-:')
            mk_ent.append('\t' + '"' + en14v[0] + '" "' + en14v[1] + '"\n')

        if 15 <= j_enum_amount:
            en15v = cbt.ent_conf.pr_enum_15.split(':-:')
            mk_ent.append('\t' + '"' + en15v[0] + '" "' + en15v[1] + '"\n')

        if 16 <= j_enum_amount:
            en16v = cbt.ent_conf.pr_enum_16.split(':-:')
            mk_ent.append('\t' + '"' + en16v[0] + '" "' + en16v[1] + '"\n')
        """

        # write enum booleans
        for bool_enum_j_idx, bool_enum_pr in enumerate(prop_ents[cent_type][5]):
            mk_ent.append('\t' + '"' + prop_ents[cent_type][5][bool_enum_pr].split(':-:')[0] + '" "' + str(int(cbt.ent_conf['pr_enum_bool_' + str(bool_enum_j_idx + 1)])) + '"\n')

        # write sflags
        # If there are no flags - don't write the spawnflags at all
        if len(prop_ents[cent_type][6]) > 0:
            mk_ent.append('\t' + '"spawnflags" "' + str(cbt.ent_conf['l3_ent_sflags']) + '"\n')

        
        # write closing        
        mk_ent.append('}\n')

        # write constructed ent
        constructed_ents.append(''.join(mk_ent))
    
    
    
    
    
    
    
    constructed_spotlights = []
    # write spotlights
    for lizard in monitor_lizard:
        mkspot = []
        
        print('processing object: ' + str(lizard))
        
        cent_type = lizard.ent_conf.obj_ent_type
        
        # get transforms from blender
        obj_locrot = get_obj_locrot_v1(lizard, 1, '-y', self, context)
        
        
        #
        # write shared
        #
        
        # write opening
        mkspot.append('entity\n{\n')
        mkspot.append('\t' + '"classname" "' + cent_type + '"\n')
        mkspot.append('\t' + '"liz3" "1"\n')  
    
        # any entity should have an origin - write origin (loc)
        mkspot.append('\t' + '"origin" "' + str(obj_locrot['loc'][0]) + ' ' + str(obj_locrot['loc'][1]) + ' ' + str(obj_locrot['loc'][2]) + '"\n')
        corrected_y = obj_locrot['rot'][1] * -1
        # ma
        # if obj_locrot['rot'][1] > 0:
            # corrected_y = obj_locrot['rot'][1] - 90
        # if obj_locrot['rot'][1] < 0:
            # corrected_y = obj_locrot['rot'][1] + 90
        # if obj_locrot['rot'][1] == 0:
            # corrected_y = 0

        mkspot.append('\t' + '"angles" "' + str(corrected_y) + ' ' + str(obj_locrot['rot'][2]) + ' ' + str(obj_locrot['rot'][0]) + '"\n')
        mkspot.append('\t' + '"pitch" "' + str(corrected_y) + '"\n')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(obj_locrot['rot'])
        
        
        # write strings
        for str_j_idx, str_pr in enumerate(prop_ents[cent_type][0]):
            # strings are never empty, unless you take them off
            if lizard.ent_conf['pr_str_' + str(str_j_idx + 1)] != ' ':
                mkspot.append('\t' + '"' + prop_ents[cent_type][0][str_pr].split(':-:')[0] + '" "' + lizard.ent_conf['pr_str_' + str(str_j_idx + 1)] + '"\n')
        
        # write ints
        for int_j_idx, int_pr in enumerate(prop_ents[cent_type][1]):
            mkspot.append('\t' + '"' + prop_ents[cent_type][1][int_pr].split(':-:')[0] + '" "' + str(lizard.ent_conf['pr_int_' + str(int_j_idx + 1)]) + '"\n')
        
        
        # write floats
        for float_j_idx, float_pr in enumerate(prop_ents[cent_type][2]):
            mkspot.append('\t' + '"' + prop_ents[cent_type][2][float_pr].split(':-:')[0] + '" "' + str(round(lizard.ent_conf['pr_float_' + str(float_j_idx + 1)], 4)) + '"\n')

        
        
        # write colors
        # sorry, but your shit cannot have negative values. For now
        
        for color_j_idx, color_pr in enumerate(prop_ents[cent_type][3]):
            rgb = str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][0] * 255)) + ' ' + str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][1] * 255)) + ' ' + str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][2] * 255))
            if '-' in str(rgb):
                mkspot.append('\t' + '"' + prop_ents[cent_type][3][color_pr].split(':-:')[0] + '" "-1 -1 -1 1"\n')
            else:
                mkspot.append('\t' + '"' + prop_ents[cent_type][3][color_pr].split(':-:')[0] + '" "' + rgb + '"\n')
        
        
        
        # write sflags
        # If there are no flags - don't write the spawnflags at all
        if len(prop_ents[cent_type][6]) > 0:
            mkspot.append('\t' + '"spawnflags" "' + str(lizard.ent_conf['l3_ent_sflags']) + '"\n')

        
        # write closing        
        mkspot.append('}\n')

        # write constructed ent
        constructed_ents.append(''.join(mkspot))
    
    
    
    
    
    
    
    
    
    
    print(constructed_ents)
    
    linez.insert(int(bigcum), str(''.join(constructed_ents)))

    # fed = open('E:\\!!Blend_Projects\\scripts\\entity_exporter\\fuck.txt', 'w')
    # fed.write(''.join(constructed_ents))
    # fed.close()

    TEST_fed = open('E:\\!!Blend_Projects\\scripts\\entity_exporter\\ents.vmf', 'w')
    TEST_fed.write(''.join(linez))
    TEST_fed.close()



#
# IO
#



def build_suggest_ent_outp(self, context):
    # return []

    # vp_blpe_ents
    
    sg_build = []
    
    cent_type = context.active_object.ent_conf.obj_ent_type
    # print(vp_blpe_ents[cent_type][7])
    for prm_indx, psb_outp in enumerate(vp_blpe_ents[cent_type][7]):
        sg_build.append((psb_outp, psb_outp, 'output'))
    # print(sg_build)
    return sg_build


def apply_loutp_suggestion(self, context):
    print('triggered')
    get_tgt_ind = context.active_object.list_index

    get_suggestion = context.scene.blents.suggest_outp

    context.active_object.my_list[get_tgt_ind].name = get_suggestion


# def try_set_suggestion(self, context):
    # get_tgt_ind = context.active_object.list_index

    # get_current_outp = context.active_object.my_list[get_tgt_ind].name

    # try:
        # context.scene.blents.suggest_outp = get_current_outp
    # except:
        # pass


def build_suggest_ent_inpt(self, context):
    
    print('build inp suggestions')
    # make a list of eligible entites for scene
    tgt_searchlist = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil']
    print(tgt_searchlist)
    # this will append all the possible results from all the objects with matched name
    matched_inputs = []
    
    # get requested tgt name
    get_cur_ind = context.active_object.list_index
    rq_tgt_name = context.active_object.my_list[get_cur_ind].random_prop
    print('requested tgt name: ' + str(rq_tgt_name))
    
    for sc_obj in tgt_searchlist:
        # get name index and see if an entity has name at all
        # name is always in string
        cent_type = sc_obj.ent_conf.obj_ent_type
        print('scanning ' + str(sc_obj.name) + ' with ent type ' + str(cent_type))
        for ngui_idx, keyname in enumerate(vp_blpe_ents[cent_type][0]):
            # Todo: make it look for "targetname"
            if keyname.lower() == 'name':
                print('Name presented in ' + str(sc_obj.name))

                if sc_obj.ent_conf['pr_str_' + str(ngui_idx + 1)] == rq_tgt_name:
                    # get matched ent type
                    print('matched name!!')
                    matched_ent_type = vp_blpe_ents[sc_obj.ent_conf['obj_ent_type']][8]
                    for found_input in matched_ent_type:
                        matched_inputs.append((found_input, found_input, 'input'))
    
    
    return list(dict.fromkeys(matched_inputs))


def add_hwm_entity(self, context):
    #
    # Todo: make it NOT use bpy.ops !!!!!!!!!!!!!!
    #
    
    file_path = 'E:\\!!Blend_Projects\\hammer_icons\\hammer_icons_01a.blend'
    inner_path = 'Object'
    object_name = self.icon_ent_type + '_curve'
    """
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name,
        autoselect=True,
        link=False,
        instance_object_data=False
        )
    """
    lnk_file = Path(file_path).absolute().name
    
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        data_to.objects = [object_name]
    
    obj = data_to.objects[0]
    bpy.context.collection.objects.link(obj)
    obj.location = context.scene.cursor.location
    # for obj in data_to.objects:
        # if obj.name == object_name:
            # bpy.context.collection.objects.link(obj)
    
    for selected_ob in bpy.data.objects:
        selected_ob.select_set(False)
    
    
    obj.select_set(True)
    context.view_layer.objects.active = obj
    bpy.data.libraries.remove(bpy.data.libraries[lnk_file])
    
    
    # gut for helth
    # todo: make a separate function ?
    cdata_cleanup(self, context)
    # I want 2 die
    




# =========================================================
#----------------------------------------------------------
#                   Operators
#----------------------------------------------------------
# =========================================================


class OBJECT_OT_vmf_export_foil(Operator, AddObjectHelper):
    bl_idname = 'mesh.set_ent_type'
    bl_label = 'Set entity type'
    bl_options = {'REGISTER'}

    def execute(self, context):
        set_obj_ent(self, context)
        return {'FINISHED'}



class OBJECT_OT_foil_test_export(Operator, AddObjectHelper):
    bl_idname = 'mesh.foil_ent_export'
    bl_label = 'Test export entities'
    bl_options = {'REGISTER'}

    def execute(self, context):
        test_export_v1(self, context)
        return {'FINISHED'}


    
class OBJECT_OT_foil_add_hwm_ent(Operator, AddObjectHelper):

    bl_idname = 'mesh.foil_add_hwm_ent'
    bl_label = 'Add object'
    # bl_options = {'REGISTER'}
    
    # gr_id = StringProperty(default='nil')
    icon_ent_type: bpy.props.StringProperty(
        name = 'icon_ent_type',
        default = 'nil'
    )

    # @classmethod
    
    def execute(self, context):
        # print(self.gr_id)
        add_hwm_entity(self, context)

        return {'FINISHED'}




# test
def apply_qffd_n(self, context):

    print('abandoned_fucntion')
    
    
    
    
class OBJECT_OT_apply_qffd(Operator, AddObjectHelper):
    bl_idname = 'mesh.apply_qffd'
    bl_label = 'Apply qffd'
    bl_options = {'REGISTER'}

    def execute(self, context):
        apply_qffd_n(self, context)
        return {'FINISHED'}
        


# =========================================================
#----------------------------------------------------------
#                   Classes
#----------------------------------------------------------
# =========================================================



class blender_ents(PropertyGroup):
    dnenum : EnumProperty(
        items=r_enum_list,
        name='Entity',
        description='I like bread'
        # default = "nil"
        )
        
    dn_str : StringProperty(
        name='some string idk',
        description='lizards are sexy',
        default = 'C:\\Users\\DrHax\\AppData\\Roaming\\Blender Foundation\\Blender\\2.93\\scripts\\addons\\blender_foil\\bl_point_ents\\blpe_main.json'
        # subtype="FILE_PATH",
        # update=append_vmf_vgroups
        )
        
    last_mod_time : StringProperty(
        name='last mod time',
        description='lizards are sexy',
        default = 'nil'
        )
        
        
        
    # ---------
    #  IO sys
    # ---------
        
    suggest_outp : EnumProperty(
        items=build_suggest_ent_outp,
        name='Output',
        description='I like bread',
        update=apply_loutp_suggestion
        # default = "nil"
        )

    suggest_inp : EnumProperty(
        items=build_suggest_ent_inpt,
        name='tgt input',
        description='I like bread'
        # update=apply_loutp_suggestion
        # default = "nil"
        )




class blender_ents_obj(PropertyGroup):

    # =================================================
    #                       Shared
    # =================================================
    obj_ent_type : StringProperty(
        name='Entity type',
        description='lizards are sexy',
        default = 'nil'
        )
    
    obj_ent_sflags : StringProperty(
        name='Entity Spawn Flags',
        description='lizards are sexy',
        default = 'nil'
        )    
    
    

    # =====================================================================
    # TODO: EVERYTHING BESIDES ENUMS COULD EASILY BE DONE WITH FOR LOOPS
    # =====================================================================
    
    
    
    
    # =================================================
    #                       Strings
    # =================================================
    pr_str_1 : StringProperty(
        name='pr_str_1',
        description='lizards are sexy',
        default = 'pr_str_1'
        )
    pr_str_2 : StringProperty(
        name='pr_str_2',
        description='lizards are sexy',
        default = 'pr_str_2'
        )
    pr_str_3 : StringProperty(
        name='pr_str_3',
        description='lizards are sexy',
        default = 'pr_str_3'
        )
    pr_str_4 : StringProperty(
        name='pr_str_4',
        description='lizards are sexy',
        default = 'pr_str_4'
        )
    pr_str_5 : StringProperty(
        name='pr_str_5',
        description='lizards are sexy',
        default = 'pr_str_5'
        )
    pr_str_6 : StringProperty(
        name='pr_str_6',
        description='lizards are sexy',
        default = 'pr_str_6'
        )
    pr_str_7 : StringProperty(
        name='pr_str_7',
        description='lizards are sexy',
        default = 'pr_str_7'
        )
    pr_str_8 : StringProperty(
        name='pr_str_8',
        description='lizards are sexy',
        default = 'pr_str_8'
        )
    pr_str_9 : StringProperty(
        name='pr_str_9',
        description='lizards are sexy',
        default = 'pr_str_9'
        )
    pr_str_10 : StringProperty(
        name='pr_str_10',
        description='lizards are sexy',
        default = 'pr_str_10'
        )
    pr_str_11 : StringProperty(
        name='pr_str_11',
        description='lizards are sexy',
        default = 'pr_str_11'
        )
    pr_str_12 : StringProperty(
        name='pr_str_12',
        description='lizards are sexy',
        default = 'pr_str_12'
        )
    pr_str_13 : StringProperty(
        name='pr_str_13',
        description='lizards are sexy',
        default = 'pr_str_13'
        )
    pr_str_14 : StringProperty(
        name='pr_str_14',
        description='lizards are sexy',
        default = 'pr_str_14'
        )
    pr_str_15 : StringProperty(
        name='pr_str_15',
        description='lizards are sexy',
        default = 'pr_str_15'
        )
    pr_str_16 : StringProperty(
        name='pr_str_16',
        description='lizards are sexy',
        default = 'pr_str_16'
        )
    pr_str_17 : StringProperty(
        name='pr_str_17',
        description='lizards are sexy',
        default = 'pr_str_17'
        )
    pr_str_18 : StringProperty(
        name='pr_str_18',
        description='lizards are sexy',
        default = 'pr_str_18'
        )
    pr_str_19 : StringProperty(
        name='pr_str_19',
        description='lizards are sexy',
        default = 'pr_str_19'
        )
    pr_str_20 : StringProperty(
        name='pr_str_20',
        description='lizards are sexy',
        default = 'pr_str_20'
        )
    pr_str_21 : StringProperty(
        name='pr_str_21',
        description='lizards are sexy',
        default = 'pr_str_21'
        )
    pr_str_22 : StringProperty(
        name='pr_str_22',
        description='lizards are sexy',
        default = 'pr_str_22'
        )
    pr_str_23 : StringProperty(
        name='pr_str_23',
        description='lizards are sexy',
        default = 'pr_str_23'
        )
    pr_str_24 : StringProperty(
        name='pr_str_24',
        description='lizards are sexy',
        default = 'pr_str_24'
        )
    pr_str_25 : StringProperty(
        name='pr_str_25',
        description='lizards are sexy',
        default = 'pr_str_25'
        )
    pr_str_26 : StringProperty(
        name='pr_str_26',
        description='lizards are sexy',
        default = 'pr_str_26'
        )
    pr_str_27 : StringProperty(
        name='pr_str_27',
        description='lizards are sexy',
        default = 'pr_str_27'
        )
    pr_str_28 : StringProperty(
        name='pr_str_28',
        description='lizards are sexy',
        default = 'pr_str_28'
        )
    pr_str_29 : StringProperty(
        name='pr_str_29',
        description='lizards are sexy',
        default = 'pr_str_29'
        )
    pr_str_30 : StringProperty(
        name='pr_str_30',
        description='lizards are sexy',
        default = 'pr_str_30'
        )
    pr_str_31 : StringProperty(
        name='pr_str_31',
        description='lizards are sexy',
        default = 'pr_str_31'
        )
    pr_str_32 : StringProperty(
        name='pr_str_32',
        description='lizards are sexy',
        default = 'pr_str_32'
        )
        
    # =================================================
    #                       Ints
    # =================================================


    pr_int_1 : IntProperty(
        name='pr_int_1',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_2 : IntProperty(
        name='pr_int_2',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_3 : IntProperty(
        name='pr_int_3',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_4 : IntProperty(
        name='pr_int_4',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_5 : IntProperty(
        name='pr_int_5',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_6 : IntProperty(
        name='pr_int_6',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_7 : IntProperty(
        name='pr_int_7',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_8 : IntProperty(
        name='pr_int_8',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_9 : IntProperty(
        name='pr_int_9',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_10 : IntProperty(
        name='pr_int_10',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_11 : IntProperty(
        name='pr_int_11',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_12 : IntProperty(
        name='pr_int_12',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_13 : IntProperty(
        name='pr_int_13',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_14 : IntProperty(
        name='pr_int_14',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_15 : IntProperty(
        name='pr_int_15',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_16 : IntProperty(
        name='pr_int_16',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_17 : IntProperty(
        name='pr_int_17',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_18 : IntProperty(
        name='pr_int_18',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_19 : IntProperty(
        name='pr_int_19',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_20 : IntProperty(
        name='pr_int_20',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_21 : IntProperty(
        name='pr_int_21',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_22 : IntProperty(
        name='pr_int_22',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_23 : IntProperty(
        name='pr_int_23',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_24 : IntProperty(
        name='pr_int_24',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_25 : IntProperty(
        name='pr_int_25',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_26 : IntProperty(
        name='pr_int_26',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_27 : IntProperty(
        name='pr_int_27',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_28 : IntProperty(
        name='pr_int_28',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_29 : IntProperty(
        name='pr_int_29',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_30 : IntProperty(
        name='pr_int_30',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_31 : IntProperty(
        name='pr_int_31',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )
    pr_int_32 : IntProperty(
        name='pr_int_32',
        default=65565,
        min=-999999,
        max=999999,
        soft_max=4096,
        soft_min=0,
        subtype='UNSIGNED'
        )

    # =================================================
    #                       Floats
    # =================================================


    pr_float_1 : FloatProperty(
        name='pr_float_1',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_2 : FloatProperty(
        name='pr_float_2',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_3 : FloatProperty(
        name='pr_float_3',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_4 : FloatProperty(
        name='pr_float_4',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_5 : FloatProperty(
        name='pr_float_5',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_6 : FloatProperty(
        name='pr_float_6',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_7 : FloatProperty(
        name='pr_float_7',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_8 : FloatProperty(
        name='pr_float_8',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_9 : FloatProperty(
        name='pr_float_9',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_10 : FloatProperty(
        name='pr_float_10',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_11 : FloatProperty(
        name='pr_float_11',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_12 : FloatProperty(
        name='pr_float_12',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_13 : FloatProperty(
        name='pr_float_13',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_14 : FloatProperty(
        name='pr_float_14',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_15 : FloatProperty(
        name='pr_float_15',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_16 : FloatProperty(
        name='pr_float_16',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_17 : FloatProperty(
        name='pr_float_17',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_18 : FloatProperty(
        name='pr_float_18',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_19 : FloatProperty(
        name='pr_float_19',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_20 : FloatProperty(
        name='pr_float_20',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_21 : FloatProperty(
        name='pr_float_21',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_22 : FloatProperty(
        name='pr_float_22',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_23 : FloatProperty(
        name='pr_float_23',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_24 : FloatProperty(
        name='pr_float_24',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_25 : FloatProperty(
        name='pr_float_25',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_26 : FloatProperty(
        name='pr_float_26',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_27 : FloatProperty(
        name='pr_float_27',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_28 : FloatProperty(
        name='pr_float_28',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_29 : FloatProperty(
        name='pr_float_29',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_30 : FloatProperty(
        name='pr_float_30',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_31 : FloatProperty(
        name='pr_float_31',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )
    pr_float_32 : FloatProperty(
        name='pr_float_32',
        default=65565.0,
        min=-99999.0,
        max=99999.0,
        precision=4
        )


    # =================================================
    #                     Enum targets
    # =================================================
    
    pr_enum_1 : EnumProperty(
        items=enum_returner_1,
        name='Entity',
        description='I like bread',
        update=enum_tgt_1
        )
        
    pr_enum_2 : EnumProperty(
        items=enum_returner_2,
        name='Entity',
        description='I like bread',
        update=enum_tgt_2
        )
        
    pr_enum_3 : EnumProperty(
        items=enum_returner_3,
        name='Entity',
        description='I like bread',
        update=enum_tgt_3
        )
        
    pr_enum_4 : EnumProperty(
        items=enum_returner_4,
        name='Entity',
        description='I like bread',
        update=enum_tgt_4
        )
        
    pr_enum_5 : EnumProperty(
        items=enum_returner_5,
        name='Entity',
        description='I like bread',
        update=enum_tgt_5
        )
        
    pr_enum_6 : EnumProperty(
        items=enum_returner_6,
        name='Entity',
        description='I like bread',
        update=enum_tgt_6
        )
        
    pr_enum_7 : EnumProperty(
        items=enum_returner_7,
        name='Entity',
        description='I like bread',
        update=enum_tgt_7
        )
        
    pr_enum_8 : EnumProperty(
        items=enum_returner_8,
        name='Entity',
        description='I like bread',
        update=enum_tgt_8
        )
        
    pr_enum_9 : EnumProperty(
        items=enum_returner_9,
        name='Entity',
        description='I like bread',
        update=enum_tgt_9
        )
        
    pr_enum_10 : EnumProperty(
        items=enum_returner_10,
        name='Entity',
        description='I like bread',
        update=enum_tgt_10
        )
        
    pr_enum_11 : EnumProperty(
        items=enum_returner_11,
        name='Entity',
        description='I like bread',
        update=enum_tgt_11
        )
        
    pr_enum_12 : EnumProperty(
        items=enum_returner_12,
        name='Entity',
        description='I like bread',
        update=enum_tgt_12
        )
        
    pr_enum_13 : EnumProperty(
        items=enum_returner_13,
        name='Entity',
        description='I like bread',
        update=enum_tgt_13
        )
        
    pr_enum_14 : EnumProperty(
        items=enum_returner_14,
        name='Entity',
        description='I like bread',
        update=enum_tgt_14
        )
        
    pr_enum_15 : EnumProperty(
        items=enum_returner_15,
        name='Entity',
        description='I like bread',
        update=enum_tgt_15
        )
        
    pr_enum_16 : EnumProperty(
        items=enum_returner_16,
        name='Entity',
        description='I like bread',
        update=enum_tgt_16
        )
    
    
    
    
    
    # =================================================
    #                  Enum Booleans
    # =================================================

    pr_enum_bool_1 : BoolProperty(
        name='pr_enum_bool_1',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_2 : BoolProperty(
        name='pr_enum_bool_2',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_3 : BoolProperty(
        name='pr_enum_bool_3',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_4 : BoolProperty(
        name='pr_enum_bool_4',
        description='Pootis',
        default = False 
        )

    pr_enum_bool_5 : BoolProperty(
        name='pr_enum_bool_5',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_6 : BoolProperty(
        name='pr_enum_bool_6',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_7 : BoolProperty(
        name='pr_enum_bool_7',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_8 : BoolProperty(
        name='pr_enum_bool_8',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_9 : BoolProperty(
        name='pr_enum_bool_9',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_10 : BoolProperty(
        name='pr_enum_bool_10',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_11 : BoolProperty(
        name='pr_enum_bool_11',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_12 : BoolProperty(
        name='pr_enum_bool_12',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_13 : BoolProperty(
        name='pr_enum_bool_13',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_14 : BoolProperty(
        name='pr_enum_bool_14',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_15 : BoolProperty(
        name='pr_enum_bool_15',
        description='Pootis',
        default = False 
        )
        
    pr_enum_bool_16 : BoolProperty(
        name='pr_enum_bool_16',
        description='Pootis',
        default = False 
        )




    # =================================================
    #                  SpawnFlags
    # =================================================

    pr_sflags_1 : BoolProperty(
        name='pr_sflags_1',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_2 : BoolProperty(
        name='pr_sflags_2',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_3 : BoolProperty(
        name='pr_sflags_3',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_4 : BoolProperty(
        name='pr_sflags_4',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )

    pr_sflags_5 : BoolProperty(
        name='pr_sflags_5',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_6 : BoolProperty(
        name='pr_sflags_6',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_7 : BoolProperty(
        name='pr_sflags_7',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_8 : BoolProperty(
        name='pr_sflags_8',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_9 : BoolProperty(
        name='pr_sflags_9',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_10 : BoolProperty(
        name='pr_sflags_10',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_11 : BoolProperty(
        name='pr_sflags_11',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_12 : BoolProperty(
        name='pr_sflags_12',
        description='Pootis',
        default = False 
        )
        
    pr_sflags_13 : BoolProperty(
        name='pr_sflags_13',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_14 : BoolProperty(
        name='pr_sflags_14',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_15 : BoolProperty(
        name='pr_sflags_15',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_16 : BoolProperty(
        name='pr_sflags_16',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )

    pr_sflags_17 : BoolProperty(
        name='pr_sflags_17',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_18 : BoolProperty(
        name='pr_sflags_18',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_19 : BoolProperty(
        name='pr_sflags_19',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_20 : BoolProperty(
        name='pr_sflags_20',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )

    pr_sflags_21 : BoolProperty(
        name='pr_sflags_21',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_22 : BoolProperty(
        name='pr_sflags_22',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_23 : BoolProperty(
        name='pr_sflags_23',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_24 : BoolProperty(
        name='pr_sflags_24',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_25 : BoolProperty(
        name='pr_sflags_25',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_26 : BoolProperty(
        name='pr_sflags_26',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_27 : BoolProperty(
        name='pr_sflags_27',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_28 : BoolProperty(
        name='pr_sflags_28',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_29 : BoolProperty(
        name='pr_sflags_29',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_30 : BoolProperty(
        name='pr_sflags_30',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_31 : BoolProperty(
        name='pr_sflags_31',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )
        
    pr_sflags_32 : BoolProperty(
        name='pr_sflags_32',
        description='Pootis',
        default = False,
        update=eval_spawnflags
        )





    # =================================================
    #                   Color props
    # =================================================


    pr_color_1 : FloatVectorProperty(subtype='COLOR')
    pr_color_2 : FloatVectorProperty(subtype='COLOR')
    pr_color_3 : FloatVectorProperty(subtype='COLOR')
    pr_color_4 : FloatVectorProperty(subtype='COLOR')
    pr_color_5 : FloatVectorProperty(subtype='COLOR')
    pr_color_6 : FloatVectorProperty(subtype='COLOR')
    pr_color_7 : FloatVectorProperty(subtype='COLOR')
    pr_color_8 : FloatVectorProperty(subtype='COLOR')











#
# hwm append Menu mechanism
#




# create a submenu in the hammer ents subcategory
class hammer_ents_w_icons(bpy.types.Menu):
    bl_idname = 'OBJECT_MT_hammer_ents_w_icons'
    bl_label = 'Hammer Ents'
    def draw(self, context):
        for supported_icon in supported_icons:
            self.layout.operator(
                'mesh.foil_add_hwm_ent',
                text=supported_icon[0]
            ).icon_ent_type = supported_icon[0]







# append submenu with hammer entities
# just hammer icons traced with curves with entity type set beforehand
def draw_hwm_presets(self, context):
    self.layout.separator()
    self.layout.menu('OBJECT_MT_hammer_ents_w_icons', icon='LIGHT')







#
# Viewpanel
#


class VIEW3D_PT_blender_foil_dn_enum(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'shitfuck'
    bl_label = 'Iguana'
    # https://youtu.be/sT3joXENOb0
    
    def draw(self, context):
        layout = self.layout
        
        
        dumpster = layout.column(align=False)
        dumpster.use_property_split = True
        dumpster.use_property_decorate = False
        
        dumpster.prop(bpy.context.scene.blents, 'dnenum')
        

        dumpster.operator('mesh.set_ent_type',
            text='Mark entity'
        )
        
        dumpster.operator('mesh.foil_ent_export',
            text='Test export'
        )
        
        
        # raw json test
        # if context.object != None:
            # for str_indx, str_prm in enumerate(prop_ents[bpy.context.scene.blents.dnenum][0]):
                # dumpster.label(text=str(str_indx) + ': ' + str_prm + ' - ' + prop_ents[bpy.context.scene.blents.dnenum][0][str_prm].split(':-:')[-1] )



        
        if context.object != None and context.object.ent_conf.obj_ent_type != 'nil':
             
            cur_object = context.active_object
            cent_type = context.active_object.ent_conf.obj_ent_type
            
        
        
            dumpster.label(text=bpy.context.active_object.ent_conf.obj_ent_type)
            
            
            # show because why not
            for str_indx, str_prm in enumerate(vp_blpe_ents[cent_type][0]):
                dumpster.label(text=str(str_indx) + ': ' + str_prm + ' - ' + vp_blpe_ents[cent_type][0][str_prm].split(':-:')[-1] )
            
            
            #
            # FOR IN RANGE LENGTH OF TOTAL NUMBER OF THE JSON ENTRIES
            #
            
            
        
            # show strings
            # for str_pr in range(len(vp_blpe_ents[cent_type][0])):
                # dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_pr + 1), text=vp_blpe_ents[cent_type][0][])
            
            # show strings
            for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
                dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_j_idx + 1), text=str_pr)

            
            # show ints
            for int_j_idx, int_pr in enumerate(vp_blpe_ents[cent_type][1]):
                dumpster.prop(context.object.ent_conf, 'pr_int_' + str(int_j_idx + 1), text=int_pr)


            # show floats
            for float_j_idx, float_pr in enumerate(vp_blpe_ents[cent_type][2]):
                dumpster.prop(context.object.ent_conf, 'pr_float_' + str(float_j_idx + 1), text=float_pr)
                
                
            # show enums
            for enum_j_idx, enum_pr in enumerate(vp_blpe_ents[cent_type][4]):
                dumpster.prop(context.object.ent_conf, 'pr_enum_' + str(enum_j_idx + 1), text=enum_pr.split(':-:')[0])
                
                
            # show enum booleans
            for enum_bool_j_idx, enum_bool_pr in enumerate(vp_blpe_ents[cent_type][5]):
                dumpster.prop(context.object.ent_conf, 'pr_enum_bool_' + str(enum_bool_j_idx + 1), text=enum_bool_pr.split(':-:')[0])
                
                
            # show colors
            for color_j_idx, color_pr in enumerate(vp_blpe_ents[cent_type][3]):
                dumpster.prop(context.object.ent_conf, 'pr_color_' + str(color_j_idx + 1), text=color_pr)
                
                
            # Flags separator
            dumpster.label(text='Spawnflags')
            
            
            # show spawnflags
            for sfalgs_j_idx, sfalgs_pr in enumerate(vp_blpe_ents[cent_type][6]):
                dumpster.prop(context.object.ent_conf, 'pr_sflags_' + str(sfalgs_j_idx + 1), text=vp_blpe_ents[cent_type][6][sfalgs_pr].split(':-:')[1])
                
                
                
            """
            # show ints
            for int_pr in range(16):
                # print('make ' + ' pr_int_' + str(int_pr + 1) )
                dumpster.prop(context.object.ent_conf, 'pr_int_' + str(int_pr + 1))


            # show floats
            for float_pr in range(16):
                # print('make ' + ' pr_int_' + str(int_pr + 1) )
                dumpster.prop(context.object.ent_conf, 'pr_float_' + str(float_pr + 1))
            """


def ffd_app(self, context):
    if (context.active_object):
        if (len(context.active_object.modifiers)):
            col = self.layout.column(align=True)

            row = col.row(align=True)
            # row.label(text='Spawnflags')






#
# RegEdit
#



rclasses = (
    blender_ents,
    VIEW3D_PT_blender_foil_dn_enum,
    OBJECT_OT_vmf_export_foil,
    OBJECT_OT_foil_test_export,
    blender_ents_obj,
    hammer_ents_w_icons,
    OBJECT_OT_foil_add_hwm_ent
)

register_, unregister_ = bpy.utils.register_classes_factory(rclasses)


def register():
    register_()
    # bpy.utils.register_class(blender_ents)
    bpy.types.Scene.blents = PointerProperty(type=blender_ents)
    # bpy.utils.register_class(VIEW3D_PT_blender_foil_dn_enum)
    # bpy.utils.register_class(OBJECT_OT_vmf_export_foil)
    # bpy.utils.register_class(OBJECT_OT_foil_test_export)
    
    # bpy.utils.register_class(blender_ents_obj)
    bpy.types.Object.ent_conf = PointerProperty(type=blender_ents_obj)
    
    bpy.types.VIEW3D_MT_add.append(draw_hwm_presets)
    
    bpy.types.DATA_PT_modifiers.prepend(ffd_app)


def unregister():
    unregister_()
    # bpy.utils.unregister_class(blender_ents)
    # bpy.utils.unregister_class(blender_ents_obj)
    # bpy.utils.unregister_class(VIEW3D_PT_blender_foil_dn_enum)
    # bpy.utils.unregister_class(OBJECT_OT_vmf_export_foil)
    # bpy.utils.unregister_class(OBJECT_OT_foil_test_export)
    del bpy.types.Scene.blents
    del bpy.types.Object.ent_conf
    
    bpy.types.VIEW3D_MT_light_add.remove(draw_hwm_presets)
    
    bpy.types.DATA_PT_modifiers.remove(ffd_app)
