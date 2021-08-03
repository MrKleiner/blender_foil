bl_info = {
    'name': 'dynamic enum',
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


addon_root_dir = Path(__file__).absolute().parent



# =========================================================
#----------------------------------------------------------
#                   Enum returners SIMPLY KEEP THE DEFAULT AT THE TOP IN JSON LOOOL
#----------------------------------------------------------
# =========================================================



def enum_returner_1(self, context):

    shit_number = 1

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)
        
        
        
        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)



        
        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []
        
        
        
        
        # for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4]):
            # obj.ent_conf['pr_str_' + str(str_j_idx + 1)] = prop_ents[cent_type][0][str_pr].split(':-:')[1]
            
        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            # lizard_sex.append(('enum_entry', prop_ents[cent_type][4][indexed_ballsack[0]][0][enum_ballsack], 'enum_entry'))
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))
        
        
        
        return lizard_sex

    else:
        return []



def enum_returner_2(self, context):

    shit_number = 2

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_3(self, context):

    shit_number = 3

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_4(self, context):

    shit_number = 4

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_5(self, context):

    shit_number = 5

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_6(self, context):

    shit_number = 6

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_7(self, context):

    shit_number = 7

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_8(self, context):

    shit_number = 8

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_9(self, context):

    shit_number = 9

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_10(self, context):

    shit_number = 10

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_11(self, context):

    shit_number = 11

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_12(self, context):

    shit_number = 12

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_13(self, context):

    shit_number = 13

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_14(self, context):

    shit_number = 14

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_15(self, context):

    shit_number = 15

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_16(self, context):

    shit_number = 16

    cent_type = context.active_object.ent_conf.obj_ent_type
    this_obj = bpy.context.active_object

    if cent_type != 'nil':
        current_enum = shit_number - 1
        radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
        entfile = open(radpath)
        entjson = entfile.read()
        
        # all possible ents
        prop_ents = json.loads(entjson)

        # index all the enum ballsacks
        indexed_ballsack = []
        
        # make list of all enums:
        for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
            indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(prop_ents[cent_type][4][indexed_ballsack[current_enum]][0]):
            lizard_sex.append((prop_ents[cent_type][4][indexed_ballsack[current_enum]][0][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []




















# =========================================================
#----------------------------------------------------------
#                   Base functionality
#----------------------------------------------------------
# =========================================================


def r_enum_list(self, context):
    current_time = datetime.datetime.now()
    radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
    # print(radpath.stat().st_mtime)
    
    if context is None:
        return []
    

    print('rebuild enum list ' + str(current_time))
    # scene_vmf_vgroups = []
    entfile = open(radpath)
    entjson = entfile.read()
    prop_ents = json.loads(entjson)
    
    # dev print
    # for thl in radlines:
        # print(thl)
    
    
    # so here we read and overwrite everyhing

    re_scene_ents = []
    for ent in prop_ents:
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
    

def set_obj_ent(self, context):

    radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
    entfile = open(radpath)
    entjson = entfile.read()
    
    # all possible ents
    prop_ents = json.loads(entjson)
    
    # current entity type
    cent_type = bpy.context.scene.blents.dnenum
    
    # TODO: DEFAULT ALL THE PARAMS BEFOREHAND. Not possible for enums. This comment is irrelevant
    
    
    
    # index all the enum ballsacks
    indexed_ballsack = []
    
    # make list of all enums:
    for enum_ind, enum_name in enumerate(prop_ents[cent_type][4]):
        indexed_ballsack.append(enum_name)
    
    
    # set to default
    for obj in bpy.context.selected_objects:
        print('set entity')
        obj.ent_conf.obj_ent_type = bpy.context.scene.blents.dnenum
        
        
        
        # set strings to default
        for str_j_idx, str_pr in enumerate(prop_ents[cent_type][0]):
            obj.ent_conf['pr_str_' + str(str_j_idx + 1)] = prop_ents[cent_type][0][str_pr].split(':-:')[1]
            
            # dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_j_idx + 1), text=str_pr)
            
        # set ints to default
        for ind_j_idx, ind_pr in enumerate(prop_ents[cent_type][1]):
            obj.ent_conf['pr_int_' + str(ind_j_idx + 1)] = int(prop_ents[cent_type][1][ind_pr].split(':-:')[1])
        
        # set floats to default
        for float_j_idx, float_pr in enumerate(prop_ents[cent_type][2]):
            obj.ent_conf['pr_float_' + str(float_j_idx + 1)] = float(prop_ents[cent_type][2][float_pr].split(':-:')[1])


        # set enums to default.
        for enum_j_idx, enum_pr in enumerate(prop_ents[cent_type][4]):
            obj.ent_conf['pr_enum_' + str(enum_j_idx + 1)] = enum_pr.split(':-:')[1]










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




    # =================================================
    #                  Shared Enums
    # =================================================
    




class blender_ents_obj(PropertyGroup):

    # =================================================
    #                       Shared
    # =================================================
    obj_ent_type : StringProperty(
        name='Entity type',
        description='lizards are sexy',
        default = 'nil'
        )
    
    
    
    
    

    
    
    
    
    
    # =================================================
    #                       Strings
    # =================================================
    pr_str_1 : StringProperty(
        name='str1',
        description='lizards are sexy',
        default = 'str1'
        )
        
    pr_str_2 : StringProperty(
        name='str2',
        description='lizards are sexy',
        default = 'str2'
        )
        
    pr_str_3 : StringProperty(
        name='str3',
        description='lizards are sexy',
        default = 'str3'
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


    # =================================================
    #                     Enum targets
    # =================================================
    
    pr_enum_1 : EnumProperty(
        items=enum_returner_1,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_2 : EnumProperty(
        items=enum_returner_2,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_3 : EnumProperty(
        items=enum_returner_3,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_4 : EnumProperty(
        items=enum_returner_4,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_5 : EnumProperty(
        items=enum_returner_5,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_6 : EnumProperty(
        items=enum_returner_6,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_7 : EnumProperty(
        items=enum_returner_7,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_8 : EnumProperty(
        items=enum_returner_8,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_9 : EnumProperty(
        items=enum_returner_9,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_10 : EnumProperty(
        items=enum_returner_10,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_11 : EnumProperty(
        items=enum_returner_11,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_12 : EnumProperty(
        items=enum_returner_12,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_13 : EnumProperty(
        items=enum_returner_13,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_14 : EnumProperty(
        items=enum_returner_14,
        name='Entity',
        description='I like bread'
        )
        
    pr_enum_15 : EnumProperty(
        items=enum_returner_15,
        name='Entity',
        description='I like bread',
        )
        
    pr_enum_16 : EnumProperty(
        items=enum_returner_16,
        name='Entity',
        description='I like bread'
        )







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
        
        
        # raw json test
        # if context.object != None:
            # for str_indx, str_prm in enumerate(prop_ents[bpy.context.scene.blents.dnenum][0]):
                # dumpster.label(text=str(str_indx) + ': ' + str_prm + ' - ' + prop_ents[bpy.context.scene.blents.dnenum][0][str_prm].split(':-:')[-1] )



        
        if context.object != None and context.object.ent_conf.obj_ent_type != 'nil':
        
            radpath = pathlib.Path(bpy.context.scene.blents.dn_str)
            entfile = open(radpath)
            entjson = entfile.read()
            
            # all possible ents
            prop_ents = json.loads(entjson)
            
            
            
            cur_object = context.active_object
            cent_type = context.active_object.ent_conf.obj_ent_type
            
        
        
            dumpster.label(text=bpy.context.active_object.ent_conf.obj_ent_type)
            
            
            # show because why not
            for str_indx, str_prm in enumerate(prop_ents[cent_type][0]):
                dumpster.label(text=str(str_indx) + ': ' + str_prm + ' - ' + prop_ents[cent_type][0][str_prm].split(':-:')[-1] )
            
            
            #
            # FOR IN RANGE LENGTH OF TOTAL NUMBER OF THE JSON ENTRIES
            #
            
            
        
            # show strings
            # for str_pr in range(len(prop_ents[cent_type][0])):
                # dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_pr + 1), text=prop_ents[cent_type][0][])
            
            # show strings
            for str_j_idx, str_pr in enumerate(prop_ents[cent_type][0]):
                dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_j_idx + 1), text=str_pr)

            
            # show ints
            for int_j_idx, int_pr in enumerate(prop_ents[cent_type][1]):
                dumpster.prop(context.object.ent_conf, 'pr_int_' + str(int_j_idx + 1), text=int_pr)


            # show floats
            for float_j_idx, float_pr in enumerate(prop_ents[cent_type][2]):
                dumpster.prop(context.object.ent_conf, 'pr_float_' + str(float_j_idx + 1), text=float_pr)
                
                
            # show enums
            for enum_j_idx, enum_pr in enumerate(prop_ents[cent_type][4]):
                dumpster.prop(context.object.ent_conf, 'pr_enum_' + str(enum_j_idx + 1), text=enum_pr.split(':-:')[0])
                
                
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





def register():
    bpy.utils.register_class(blender_ents)
    bpy.types.Scene.blents = PointerProperty(type=blender_ents)
    bpy.utils.register_class(VIEW3D_PT_blender_foil_dn_enum)
    bpy.utils.register_class(OBJECT_OT_vmf_export_foil)
    
    bpy.utils.register_class(blender_ents_obj)
    bpy.types.Object.ent_conf = PointerProperty(type=blender_ents_obj)


def unregister():
    bpy.utils.unregister_class(blender_ents)
    bpy.utils.unregister_class(blender_ents_obj)
    bpy.utils.unregister_class(VIEW3D_PT_blender_foil_dn_enum)
    bpy.utils.unregister_class(OBJECT_OT_vmf_export_foil)
    del bpy.types.Scene.blents
    del bpy.types.Object.ent_conf

