import bpy
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
                       CollectionProperty
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       bpy_prop_collection
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

from .do_export import blfoil_vmf_exporter
from ...utils.shared import eval_state

try:
    from bs4 import BeautifulSoup
    from bs4 import Tag, NavigableString
except:
    pass

# todo: Separate actions into functions as often as possible
# important todo: transfer blpe to xml.
# update: No. Json forever

# important todo: at some point there could be way too many items with icon support.
# (epsecially considering the fact that it's very easy to add custom ones)
# the genius solution would be to check if currently selected entity class in the entity class selector is available as "icon"
# and display a button which sez "append as icon"
# menus and submenus are also possible, but the "append as icon" is way more rational

# get the current directory. Just in case
addon_root_dir = Path(__file__).absolute().parent.parent.parent

# vp_radpath = pathlib.Path(bpy.context.scene.blents.dn_str)

# get path to the entity definition json
vp_blpe_path = addon_root_dir / 'configs' / 'blpe_main.json'


# a blend file with hammer icons traced with curves
# should also be in a subdir on release
# may also contain other things like player scale ref ?
hammer_icons_blend = pathlib.Path('E:\\!!Blend_Projects\\hammer_icons\\hammer_icons_01a.blend')

print('read and rebuild json')

# parse json and therefore obtain the list of all the entities and their params
vp_blpe_ents = None
with open(str(vp_blpe_path), 'r') as ec_json:
    vp_blpe_ents = json.loads(ec_json.read())
    print(len(vp_blpe_ents))


# define names of the supported icons
# a json should have a corresponding entry
# important todo: better organize the icon/asset blend file 
supported_icons = {}


# expects pathlib path and a variable to append to
# important todo: do NOT do this in the asset file itself !!!!!!!
# simply check if it's this file or not...
def blfoil_ents_supported_icons(from_file, tovar):
    print (bpy.path.abspath('//'), str(from_file))
    # return


    # Don't do this in the source file...
    if bpy.data.filepath == str(from_file):
        return


    with bpy.data.libraries.load(str(from_file)) as (data_from, data_to):
        data_to.collections = ['entity_icons']

    obj = data_to.collections[0]

    print(obj.children_recursive)

    for all_coll in obj.children_recursive:
        for col_obj in all_coll.objects:
            if col_obj.ent_conf.get('obj_ent_type') != None:
                supported_icons[col_obj.ent_conf['obj_ent_type']] = col_obj.name
                col_obj.data['blfoil_cdel'] = '1'
            bpy.data.objects.remove(col_obj)
        bpy.data.collections.remove(all_coll)

    bpy.data.collections.remove(bpy.data.collections['entity_icons'])

    for curvedel in bpy.data.curves:
        if curvedel.get('blfoil_cdel') == '1':
            bpy.data.curves.remove(curvedel)





# =========================================================
#----------------------------------------------------------
#                       Enums START
#----------------------------------------------------------
# =========================================================

def enum_re(number, cte):

    # cte = current entity name
    if cte != 'nil':
        current_enum = number - 1

        # index all the enum ballsacks
        # indexed_ballsack = []

        # because fuck it...
        this_enum = vp_blpe_ents[cte][4]
        
        # make list of all enums:
        # for enum_ind, enum_name in enumerate(this_enum):
        #     indexed_ballsack.append(enum_name)

        # append all enums for this entity type, delete the selected one and prepend it in the beginning of the array
        lizard_sex = []

        for enum_item, enum_ballsack in enumerate(this_enum[current_enum]['eitems']):
            lizard_sex.append((this_enum[current_enum]['eitems'][enum_ballsack], enum_ballsack, 'enum_entry'))

        return lizard_sex
        
    else:
        return []



def enum_returner_1(self, context):
    shit_number = 1
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_2(self, context):
    shit_number = 2
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_3(self, context):
    shit_number = 3
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_4(self, context):
    shit_number = 4
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_5(self, context):
    shit_number = 5
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_6(self, context):
    shit_number = 6
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_7(self, context):
    shit_number = 7
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_8(self, context):
    shit_number = 8
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_9(self, context):
    shit_number = 9
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_9(self, context):
    shit_number = 9
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_10(self, context):
    shit_number = 10
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_11(self, context):
    shit_number = 11
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_12(self, context):
    shit_number = 12
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_13(self, context):
    shit_number = 13
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_14(self, context):
    shit_number = 14
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_15(self, context):
    shit_number = 15
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_16(self, context):
    shit_number = 16
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_17(self, context):
    shit_number = 17
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_18(self, context):
    shit_number = 18
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_19(self, context):
    shit_number = 19
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_20(self, context):
    shit_number = 20
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_21(self, context):
    shit_number = 21
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_22(self, context):
    shit_number = 22
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_23(self, context):
    shit_number = 23
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_24(self, context):
    shit_number = 24
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_25(self, context):
    shit_number = 25
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_26(self, context):
    shit_number = 26
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_27(self, context):
    shit_number = 27
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_28(self, context):
    shit_number = 28
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_29(self, context):
    shit_number = 29
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_30(self, context):
    shit_number = 30
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_31(self, context):
    shit_number = 31
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)

def enum_returner_32(self, context):
    shit_number = 32
    cent_type = context.active_object.ent_conf.obj_ent_type
    return enum_re(shit_number, cent_type)



#
# Targets
#

# since all the enums are reusable slots - we have to trasfer the chosen value to the static config of the object on change
# (means that gui slots and actual slots are different things)
# every object has predefined slots for all possible kinds of data
# important todo: All the properties including floats, ints, etc could be stored in the scene types, not object
# Although this may not work as expected
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

def enum_tgt_17(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_17'] = bpy.context.active_object.ent_conf.pr_enum_17

def enum_tgt_18(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_18'] = bpy.context.active_object.ent_conf.pr_enum_18

def enum_tgt_19(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_19'] = bpy.context.active_object.ent_conf.pr_enum_19

def enum_tgt_20(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_20'] = bpy.context.active_object.ent_conf.pr_enum_20

def enum_tgt_21(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_21'] = bpy.context.active_object.ent_conf.pr_enum_21

def enum_tgt_22(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_22'] = bpy.context.active_object.ent_conf.pr_enum_22

def enum_tgt_23(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_23'] = bpy.context.active_object.ent_conf.pr_enum_23

def enum_tgt_24(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_24'] = bpy.context.active_object.ent_conf.pr_enum_24

def enum_tgt_25(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_25'] = bpy.context.active_object.ent_conf.pr_enum_25

def enum_tgt_26(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_26'] = bpy.context.active_object.ent_conf.pr_enum_26

def enum_tgt_27(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_27'] = bpy.context.active_object.ent_conf.pr_enum_27

def enum_tgt_28(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_28'] = bpy.context.active_object.ent_conf.pr_enum_28

def enum_tgt_29(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_29'] = bpy.context.active_object.ent_conf.pr_enum_29

def enum_tgt_30(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_30'] = bpy.context.active_object.ent_conf.pr_enum_30

def enum_tgt_31(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_31'] = bpy.context.active_object.ent_conf.pr_enum_31

def enum_tgt_32(self, context):
    bpy.context.active_object.ent_conf['ob_enum_tgt_32'] = bpy.context.active_object.ent_conf.pr_enum_32

# =========================================================
#----------------------------------------------------------
#                       Enums END
#----------------------------------------------------------
# =========================================================












# =========================================================
# ---------------------------------------------------------
#                   Base functionality
# ---------------------------------------------------------
# =========================================================


#
# Base reusable functions
#

# link all the curves used to visualize an entity to a single datablock
# so that there are no excess verts and other data in the scene
def cdata_cleanup(self, context):
    # todo: revisit
    return


# This takes all the currently selected objects and re-evaluates their spawnflags
# todo: make this function accept object input
# update: done. Now takes object input

# triggered on value change
def eval_spawnflags_auto(self, context):

    print('auto eval spawnflags')

    # quite stupid, but less logic required
    # if vp_blpe_ents.get(obj.ent_conf.obj_ent_type) != None:
    #     return

    for obj in bpy.context.selected_objects:
        if vp_blpe_ents.get(obj.ent_conf.obj_ent_type) != None:
            print('calc spawnflags')
            cur_obj_ent_type = obj.ent_conf.obj_ent_type
            obj.ent_conf['l3_ent_sflags'] = 0
            
            calculated_bytes = 0
            
            for sflag_index, sflag in enumerate(vp_blpe_ents[cur_obj_ent_type][6]):
                
                if obj.ent_conf['pr_sflags_' + str(sflag_index + 1)] == True:
                    calculated_bytes += int(sflag['byte'])
            
            obj.ent_conf['l3_ent_sflags'] = calculated_bytes
            print('calculated flags are: ' + str(calculated_bytes))

    print('end eval spawnflags')

# callable
# takes object as an input
def eval_spawnflags(blfoil_obj):
    print('blfoil: eval spawnflags for', blfoil_obj.name)
    cur_obj_ent_type = blfoil_obj.ent_conf.obj_ent_type
    blfoil_obj.ent_conf['l3_ent_sflags'] = 0
    
    calculated_bytes = 0
    
    for sflag_index, sflag in enumerate(vp_blpe_ents[cur_obj_ent_type][6]):
        if blfoil_obj.ent_conf['pr_sflags_' + str(sflag_index + 1)] == True:
            # in case some retard creates malformed bytes
            try:
                calculated_bytes += int(sflag['byte'])
            except:
                calculated_bytes += 0
    
    blfoil_obj.ent_conf['l3_ent_sflags'] = calculated_bytes
    print('blfoil: Calculated flags are: ', calculated_bytes)

    print('blfoil: Done evaluating spawnflags for', blfoil_obj.name)


# --------------------------------------------------
# --------------------------------------------------


# every entity is an entry






# dynamically build supported entities enum list (from blpe_main.json)
# On blender startup - we read and parse the blpe json in the very beginning of the script
# and then reuse it, for example here.
# todo: Only do this once ?

"""
def r_enum_list(self, context):
    current_time = datetime.datetime.now()
    
    if context is None:
        return []
    
    print('rebuild enum list ' + str(current_time))

    re_scene_ents = []
    for ent in vp_blpe_ents:
        re_scene_ents.append((ent, ent, 'bl_ent'))
        

    # print(re_scene_ents)
    return re_scene_ents
"""

def blfoil_entity_classnames_resync(scen, blpe):

    # first - delete existing
    for dle in range(len(scen.blfoil_etype_selector_list)):
        scen.blfoil_etype_selector_list.remove(0)

    d = 0
    for ent in blpe:
        scen.blfoil_etype_selector_list.add()
        scen.blfoil_etype_selector_list[-1].name = ent
        # print(bpy.data.scenes[0].blfoil_etype_selector_list[-1].name)
        d += 1
        print(d, len(blpe))


def blfoil_suggested_mats_builder():
    
    # todo: make it read this from config
    # todo: make icons for this
    # 'tools/toolsnodraw': 'nodraw_icon'
    # if not specified - default icon

    # todo MAYBE: make it a enum with cool icon previews?
    
    dev_textures_json = None
    with open(str(addon_root_dir/ 'configs' / 'dev_texture_list.json'), 'r') as dev_json:
        dev_textures_json = json.loads(dev_json.read())

    # wait for global context to become available
    # todo: We no longer have to wait. This function is called with a cool handler
    print('blfoil Rebuild suggested mats list')
    # if available - do shit and break out of the loop when done
    if bpy.context != None:
        # YAAAY, it appears that once it's added and saved - it stays there !
        # check if every scene has classnames and if the amount is the same
        for allsc in bpy.data.scenes:
            # if this scene doesn't has the same amount of ents - resync. Otherwise - pass
            if len(dev_textures_json) != len(allsc.blfoil_common_brush_materials):

                # first - delete existing
                # todo: make it a while loop
                for dle in range(len(allsc.blfoil_common_brush_materials)):
                    allsc.blfoil_common_brush_materials.remove(0)

                d = 0
                for sg_mat in dev_textures_json:
                    allsc.blfoil_common_brush_materials.add()
                    allsc.blfoil_common_brush_materials[-1].name = sg_mat
                    d += 1
                    print(d, len(dev_textures_json))

    return

"""
# awaits for context
def blfoil_ent_classnames_list_builder():
    # from time import sleep
    fu = True
    # sleep(1)
    
    # wait for global context to become available
    # todo: We no longer have to wait. This function is called with a cool handler
    while fu:
        print('trying')
        # if available - do shit and break out of the loop when done
        if bpy.context != None:
            
            # YAAAY, it appears that once it's added and saved - it stays there !
            # check if every scene has classnames and if the amount is the same
            for allsc in bpy.data.scenes:
                # if this scene doesn't has the same amount of ents - resync. Otherwise - pass
                if len(vp_blpe_ents) != len(allsc.blfoil_etype_selector_list):
                    blfoil_entity_classnames_resync(allsc, vp_blpe_ents)

            # break out of the while loop
            fu = False
            break
    return


    # build_ent_en.join()
"""

# expects context to be available when called
def blfoil_ent_classnames_list_builder():
    
    # wait for global context to become available
    # todo: We no longer have to wait. This function is called with a cool handler
    print('blfoil Rebuild entity classname list')
    # if available - do shit and break out of the loop when done
    if bpy.context != None:
        # YAAAY, it appears that once it's added and saved - it stays there !
        # check if every scene has classnames and if the amount is the same
        for allsc in bpy.data.scenes:
            # if this scene doesn't has the same amount of ents - resync. Otherwise - pass
            if len(vp_blpe_ents) != len(allsc.blfoil_etype_selector_list):
                blfoil_entity_classnames_resync(allsc, vp_blpe_ents)
    return

"""
# unused function to parse lights.rad
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


# unused function to parse lights.rad v2
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
"""

# mark currently selected object as an entity
# and clean all the data which was probably left from the previous entity
# todo: the context is pretty much useless here...
# just make it accept objects.
# afterall, the execute function can handle simple pre-process steps like collecting objects
def set_obj_ent(self, context):
    
    # current entity type
    # points to a "dynamic enum" enum list which stores all the supported entities
    cent_type = context.scene.blfoil_etype_selector_list[context.scene.blfoil_etype_selector_list_index].name

    # set everything to default
    # for every currently selected object
    for obj in context.selected_objects:
        print('set entity')
        obj.ent_conf.obj_ent_type = cent_type
        obj.ent_conf['l3_ent_sflags'] = 0


        # set strings to default
        for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
            obj.ent_conf['pr_str_' + str(str_j_idx + 1)] = str_pr['default']


        # important todo: try/except is shit...
        # set ints to default
        for ind_j_idx, ind_pr in enumerate(vp_blpe_ents[cent_type][1]):
            try:
                obj.ent_conf['pr_int_' + str(ind_j_idx + 1)] = int(ind_pr['default'])
            except:
                obj.ent_conf['pr_int_' + str(ind_j_idx + 1)] = 0

        # set floats to default
        for float_j_idx, float_pr in enumerate(vp_blpe_ents[cent_type][2]):
            try:
                obj.ent_conf['pr_float_' + str(float_j_idx + 1)] = float(float_pr['default'])
            except:
                obj.ent_conf['pr_float_' + str(float_j_idx + 1)] = 0.0

        # set enums to default.
        for enum_j_idx, enum_pr in enumerate(vp_blpe_ents[cent_type][4]):
            # set target (not gui)
            # todo: set default in definition file by idname and not gui ?

            # in some absolutely absurd cases, the default is not in the dict and it's the first item in the dict...
            if enum_pr['eitems'].get(enum_pr['default']) == None:
                # so, set the first occurance in the dict...
                empty_default = next(iter(enum_pr['eitems']))
                gui_default = empty_default
            else:
                empty_default = enum_pr['eitems'][enum_pr['default']]
                gui_default = empty_default

            obj.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)] = empty_default
            # set gui
            obj.ent_conf['pr_enum_' + str(enum_j_idx + 1)] = gui_default
            # print('set def idx ' + str(enum_j_idx) + ' enum to: ' + '"' + str(vp_blpe_ents[cent_type][4][enum_pr][0][enum_pr.split(':-:')[1]]) + '"')


        # set enum bools to default.
        for enum_bool_j_idx, enum_bool_pr in enumerate(vp_blpe_ents[cent_type][5]):
            obj.ent_conf['pr_enum_bool_' + str(enum_bool_j_idx + 1)] = eval_state(enum_bool_pr['default'])
            
            
        # set Spawn Flags to default
        for sflags_j_idx, sflags_pr in enumerate(vp_blpe_ents[cent_type][6]):
            obj.ent_conf['pr_sflags_' + str(sflags_j_idx + 1)] = eval_state(sflags_pr['default'])

        # set Colors to default
        for color_j_idx, color_pr in enumerate(vp_blpe_ents[cent_type][3]):
        
            jrgb = color_pr['default'].split(' ')
            try:
                ar = float(int(jrgb[0]) / 255)
                ag = float(int(jrgb[1]) / 255)
                ab = float(int(jrgb[2]) / 255)
            except:
                ar, ag, ab = 255.0, 255.0, 255.0

            obj.ent_conf['pr_color_' + str(color_j_idx + 1)] = (ar, ag, ab)

        # evaluate spawnflags for the current object. This is kind of an unnecessary since it should happen on data retreive...
        eval_spawnflags(obj)

        # and unmark it from world brush
        obj.blfoil_ent_specials.is_world_brush = False
    


# Export entities to a given vmf
# todo: Also do preparational steps in the execute function of the operator...
def blfoil_full_vmf_export(self, context):
    import time

    full_exp = int(round(time.time() * 1000))
    # TESTING
    pootisd = open('E:\\map\\export_test\\wow.vmf', 'r').read()

    towrite = blfoil_vmf_exporter(self, context, vp_blpe_ents, pootisd)
    pootis_ded = open('E:\\map\\export_test\\wow.vmf', 'w')
    pootis_ded.write(towrite)
    print('Full export took', int(round(time.time() * 1000)) - full_exp)
    return




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


def blfoil_add_hwm_entity(self, context):
    
    inner_path = 'Object'
    # object_name = self.icon_ent_type + '_curve'
    object_name = supported_icons[self.icon_ent_type]
    print(object_name)

    lnk_file = hammer_icons_blend.absolute().name
    
    with bpy.data.libraries.load(str(hammer_icons_blend)) as (data_from, data_to):
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
    if obj.get('blfoil_entity_icon_iscube') == '1' or obj.get('blfoil_entity_icon_iscube') == 1:
        bpy.context.view_layer.update()
        obj.dimensions[0] = 16
        bpy.context.view_layer.update()
        obj.dimensions[1] = 16
        bpy.context.view_layer.update()
        obj.dimensions[2] = 16
    
    context.view_layer.objects.active = obj
    bpy.data.libraries.remove(bpy.data.libraries[lnk_file])
    
    
    # gud for helth
    # todo: fix this fucking shit
    # cdata_cleanup(self, context)
    # I want 2 die
    




# =========================================================
# ---------------------------------------------------------
#                       Operators
# ---------------------------------------------------------
# =========================================================

# Things that get triggered when a button is being pressed
# Shift + A menu counts too
# Basically operators that you can call from gui or whatever

# Set object entity
class OBJECT_OT_blfoil_set_obj_ent_class(Operator, AddObjectHelper):
    bl_idname = 'mesh.set_ent_type'
    bl_label = 'Set entity type'
    bl_options = {'REGISTER'}

    def execute(self, context):
        set_obj_ent(self, context)
        return {'FINISHED'}


# Export vmf
class OBJECT_OT_blfoil_vmf_export(Operator, AddObjectHelper):
    bl_idname = 'mesh.blfoil_export_vmf'
    bl_label = 'Blender Foil VMF export'
    bl_options = {'REGISTER'}

    def execute(self, context):
        blfoil_full_vmf_export(self, context)
        return {'FINISHED'}


# Add a hammer entity from the Shift + A menu
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
        blfoil_add_hwm_entity(self, context)

        return {'FINISHED'}


# Set suggested material
class OBJECT_OT_blfoil_set_suggested_mat(Operator, AddObjectHelper):

    bl_idname = 'mesh.blfoil_set_suggested_mat'
    bl_label = 'Set material'
    # bl_options = {'REGISTER'}
    
    def execute(self, context):

        sce = context.scene

        for objs in context.selected_objects:
            objs.blfoil_ent_specials.brush_material_name = sce.blfoil_common_brush_materials[sce.blfoil_common_brush_materials_index].name

        return {'FINISHED'}

# Mark object as a world brush
class OBJECT_OT_blfoil_mark_as_world_brush(Operator, AddObjectHelper):

    bl_idname = 'mesh.blfoil_mark_as_world_brush'
    bl_label = 'Set material'
    # bl_options = {'REGISTER'}
    
    def execute(self, context):

        sce = context.scene

        for objs in context.selected_objects:
            objs.blfoil_ent_specials.is_world_brush = True

        return {'FINISHED'}





















"""
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
"""


# =========================================================
# ---------------------------------------------------------
#                       Classes
# ---------------------------------------------------------
# =========================================================

# Property specific things




#
# Rubbish
#

class blender_ents(PropertyGroup):
    """
    dnenum : EnumProperty(
        items=r_enum_list,
        name='Entity',
        description='I like bread'
        # default = "nil"
        )
    
    last_mod_time : StringProperty(
        name='last mod time',
        description='lizards are sexy',
        default = 'nil'
        )
    """
        
        
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






# 
# Dedicated and shared params, like brush material and special entity config, like light/light_spot properties 
#

class blfoil_ents_dedicated_params(PropertyGroup):

    # ----------------------------------
    #              Brushes
    # ----------------------------------

    brush_material_name : StringProperty(
        name='Material path',
        description='Path to the material .vmt, like tools/toolsnodraw',
        default = 'brick/brickfloor001a'
        )

    lightmap_scale : IntProperty(
        name='Lightmap scale',
        default=16,
        min=1,
        max=128,
        soft_max=64,
        soft_min=1
        )

    texture_scale : FloatProperty(
        name='Texture scale',
        default=0.25,
        min=-65535.0,
        max=65535.0,
        precision=3
        )

    is_world_brush : BoolProperty(
        name='Object is a world brush',
        description='Cannot contain multiple islands',
        default = False 
        )






#
# Suggested materials
#

# property
class blfoil_common_brush_materials(PropertyGroup):

    material_name : StringProperty(
        name='Material path',
        description='Path to the material .vmt, like tools/toolsnodraw',
        default = 'brick/brickfloor001a'
        )

# drawing
class blfoil_common_brush_materials_item_draw(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        ma = item
        self.use_filter_show = True
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if ma:
                layout.label(text=ma.name, icon='NODE_TEXTURE', translate=False)
            else:
                layout.label(text='', translate=False, icon='SHAPEKEY_DATA')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'









#
# Predefined parameter slots: strings, ints, enums, whatever
#

# important todo: move shared shit from blender_ents_obj to wherever
# IF POSSIBLE

# etype - eNTITY type
# strings, ints, enums, whatever
class blfoil_predefined_entity_prop_slots(PropertyGroup):

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
    pr_str_33 : StringProperty(
        name='pr_str_33',
        description='lizards are sexy',
        default = 'pr_str_33'
        )
    pr_str_34 : StringProperty(
        name='pr_str_34',
        description='lizards are sexy',
        default = 'pr_str_34'
        )
    pr_str_35 : StringProperty(
        name='pr_str_35',
        description='lizards are sexy',
        default = 'pr_str_35'
        )
    pr_str_36 : StringProperty(
        name='pr_str_36',
        description='lizards are sexy',
        default = 'pr_str_36'
        )
    pr_str_37 : StringProperty(
        name='pr_str_37',
        description='lizards are sexy',
        default = 'pr_str_37'
        )
    pr_str_38 : StringProperty(
        name='pr_str_38',
        description='lizards are sexy',
        default = 'pr_str_38'
        )
    pr_str_39 : StringProperty(
        name='pr_str_39',
        description='lizards are sexy',
        default = 'pr_str_39'
        )
    pr_str_40 : StringProperty(
        name='pr_str_40',
        description='lizards are sexy',
        default = 'pr_str_40'
        )
    pr_str_41 : StringProperty(
        name='pr_str_41',
        description='lizards are sexy',
        default = 'pr_str_41'
        )
    pr_str_42 : StringProperty(
        name='pr_str_42',
        description='lizards are sexy',
        default = 'pr_str_42'
        )
    pr_str_43 : StringProperty(
        name='pr_str_43',
        description='lizards are sexy',
        default = 'pr_str_43'
        )
    pr_str_44 : StringProperty(
        name='pr_str_44',
        description='lizards are sexy',
        default = 'pr_str_44'
        )
    pr_str_45 : StringProperty(
        name='pr_str_45',
        description='lizards are sexy',
        default = 'pr_str_45'
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
    
    pr_enum_17 : EnumProperty(
        items=enum_returner_17,
        name='Entity',
        description='I like bread',
        update=enum_tgt_17
        )

    pr_enum_18 : EnumProperty(
        items=enum_returner_18,
        name='Entity',
        description='I like bread',
        update=enum_tgt_18
        )

    pr_enum_19 : EnumProperty(
        items=enum_returner_19,
        name='Entity',
        description='I like bread',
        update=enum_tgt_19
        )

    pr_enum_20 : EnumProperty(
        items=enum_returner_20,
        name='Entity',
        description='I like bread',
        update=enum_tgt_20
        )

    pr_enum_21 : EnumProperty(
        items=enum_returner_21,
        name='Entity',
        description='I like bread',
        update=enum_tgt_21
        )

    pr_enum_22 : EnumProperty(
        items=enum_returner_22,
        name='Entity',
        description='I like bread',
        update=enum_tgt_22
        )

    pr_enum_23 : EnumProperty(
        items=enum_returner_23,
        name='Entity',
        description='I like bread',
        update=enum_tgt_23
        )

    pr_enum_24 : EnumProperty(
        items=enum_returner_24,
        name='Entity',
        description='I like bread',
        update=enum_tgt_24
        )

    pr_enum_25 : EnumProperty(
        items=enum_returner_25,
        name='Entity',
        description='I like bread',
        update=enum_tgt_25
        )

    pr_enum_26 : EnumProperty(
        items=enum_returner_26,
        name='Entity',
        description='I like bread',
        update=enum_tgt_26
        )

    pr_enum_27 : EnumProperty(
        items=enum_returner_27,
        name='Entity',
        description='I like bread',
        update=enum_tgt_27
        )

    pr_enum_28 : EnumProperty(
        items=enum_returner_28,
        name='Entity',
        description='I like bread',
        update=enum_tgt_28
        )

    pr_enum_29 : EnumProperty(
        items=enum_returner_29,
        name='Entity',
        description='I like bread',
        update=enum_tgt_29
        )

    pr_enum_30 : EnumProperty(
        items=enum_returner_30,
        name='Entity',
        description='I like bread',
        update=enum_tgt_30
        )

    pr_enum_31 : EnumProperty(
        items=enum_returner_31,
        name='Entity',
        description='I like bread',
        update=enum_tgt_31
        )

    pr_enum_32 : EnumProperty(
        items=enum_returner_32,
        name='Entity',
        description='I like bread',
        update=enum_tgt_32
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
        update=eval_spawnflags_auto
        )
        
    pr_sflags_2 : BoolProperty(
        name='pr_sflags_2',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_3 : BoolProperty(
        name='pr_sflags_3',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_4 : BoolProperty(
        name='pr_sflags_4',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )

    pr_sflags_5 : BoolProperty(
        name='pr_sflags_5',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_6 : BoolProperty(
        name='pr_sflags_6',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_7 : BoolProperty(
        name='pr_sflags_7',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_8 : BoolProperty(
        name='pr_sflags_8',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_9 : BoolProperty(
        name='pr_sflags_9',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_10 : BoolProperty(
        name='pr_sflags_10',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_11 : BoolProperty(
        name='pr_sflags_11',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
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
        update=eval_spawnflags_auto
        )
        
    pr_sflags_14 : BoolProperty(
        name='pr_sflags_14',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_15 : BoolProperty(
        name='pr_sflags_15',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_16 : BoolProperty(
        name='pr_sflags_16',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )

    pr_sflags_17 : BoolProperty(
        name='pr_sflags_17',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_18 : BoolProperty(
        name='pr_sflags_18',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_19 : BoolProperty(
        name='pr_sflags_19',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_20 : BoolProperty(
        name='pr_sflags_20',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )

    pr_sflags_21 : BoolProperty(
        name='pr_sflags_21',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_22 : BoolProperty(
        name='pr_sflags_22',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_23 : BoolProperty(
        name='pr_sflags_23',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_24 : BoolProperty(
        name='pr_sflags_24',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_25 : BoolProperty(
        name='pr_sflags_25',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_26 : BoolProperty(
        name='pr_sflags_26',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_27 : BoolProperty(
        name='pr_sflags_27',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_28 : BoolProperty(
        name='pr_sflags_28',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_29 : BoolProperty(
        name='pr_sflags_29',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_30 : BoolProperty(
        name='pr_sflags_30',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_31 : BoolProperty(
        name='pr_sflags_31',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
        )
        
    pr_sflags_32 : BoolProperty(
        name='pr_sflags_32',
        description='Pootis',
        default = False,
        update=eval_spawnflags_auto
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
# list of all possible entities
#
class blfoil_etype_selector_list_prp_col(PropertyGroup):
    """Group of properties representing an item in the list."""

    blfoil_etype_selector_list_item : StringProperty(
        name='ent_classname',
        description='Entity classname from .fgd',
        default = 'nil'
        )

# list of all possible entities item draw
class blfoil_etype_selector_panel_itemdraw(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        ma = item
        self.use_filter_show = True
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if ma:
                # layout.prop(ma, "name", text="fuck", emboss=False, icon='SHAPEKEY_DATA')
                if vp_blpe_ents[ma.name][9]['brush_ent'] == '1':
                    z_icon = 'SHAPEKEY_DATA'
                else:
                    z_icon = 'PROP_ON'
                # layout.prop(ma, 'name', text='', emboss=False, icon=z_icon)
                layout.label(text=ma.name, icon=z_icon, translate=False)
                # pass
            else:
                layout.label(text="", translate=False, icon='SHAPEKEY_DATA')
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'







# =========================================================
# ---------------------------------------------------------
#                           GUI
# ---------------------------------------------------------
# =========================================================

# classes too, but specifically for gui
# and functions too


# create a submenu in the hammer ents subcategory
class hammer_ents_w_icons(bpy.types.Menu):
    bl_idname = 'OBJECT_MT_hammer_ents_w_icons'
    bl_label = 'Hammer Ents'
    def draw(self, context):
        for supported_icon in supported_icons:
            self.layout.operator(
                'mesh.foil_add_hwm_ent',
                text=supported_icon
            ).icon_ent_type = supported_icon




# append submenu with hammer entities to the Shift + A menu
# Those just hammer icons traced with curves with entity type set beforehand
def draw_hwm_presets(self, context):
    self.layout.separator()
    self.layout.menu('OBJECT_MT_hammer_ents_w_icons', icon='LIGHT')




#
# Entity or Brush assignment and configuration
#
class VIEW3D_PT_blender_foil_vmf_gui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lizards'
    bl_label = 'Iguana'
    # https://youtu.be/sT3joXENOb0
    
    def draw(self, context):
        layout = self.layout
        
        
        dumpster = layout.column(align=False)
        dumpster.use_property_split = True
        dumpster.use_property_decorate = False

        # dumpster.prop(context.scene.blents, 'dnenum')
        the_filter = dumpster.template_list('blfoil_etype_selector_panel_itemdraw', '', context.scene, 'blfoil_etype_selector_list', context.scene, 'blfoil_etype_selector_list_index')

        dumpster.operator('mesh.set_ent_type', text='Mark entity')
        dumpster.operator('mesh.blfoil_mark_as_world_brush', text='Mark brush')
        
        dumpster.operator('mesh.blfoil_export_vmf', text='Export vmf')


        # todo: performance ??????
        # todo: check if current entity type is in the dict or not
        # if context.object != None and context.object.ent_conf.obj_ent_type != 'nil':
        if context.object != None and context.object.ent_conf.obj_ent_type != 'nil':
             
            cur_object = context.active_object
            # important todo: all cent_types are actually redundant. Just do vp_blpe_ents[cent_type] right away...
            cent_type = vp_blpe_ents[context.active_object.ent_conf.obj_ent_type]
            cent_name = context.active_object.ent_conf.obj_ent_type

            dumpster.label(text=bpy.context.active_object.ent_conf.obj_ent_type)

            # show because why not
            for str_indx, str_prm in enumerate(cent_type[0]):
                dumpster.label(text=str(str_indx) + ': ' + str_prm['guiname'] + ' - ' + str_prm['descr'])


            # todo: Yes, this is smarter, but what abour performance ?
            # todo: Safety measures
            # Overengineering ?
            ent_prop_types = {
                'pr_str_': 0,
                'pr_int_': 1,
                'pr_float_': 2,
                'pr_enum_': 4,
                'pr_enum_bool_': 5,
                'pr_color_': 3,
                'pr_sflags_': 6
            }

            ent_prop_separators = {
                'pr_sflags_': 'Spawnflags'
            }

            # ecl - Entity CLass
            for ecl_prop_type in ent_prop_types:
                if ent_prop_separators.get(ecl_prop_type) != None:
                    dumpster.label(text=ent_prop_separators[ecl_prop_type])

                for ecl_prop_index, ecl_prop in enumerate(cent_type[ent_prop_types[ecl_prop_type]]):
                    dumpster.prop(context.object.ent_conf, ecl_prop_type + str(ecl_prop_index + 1), text=ecl_prop['guiname'])


            """
            # Old method (other entries were deleted): 
            # show strings
            for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
                dumpster.prop(context.object.ent_conf, 'pr_str_' + str(str_j_idx + 1), text=str_pr['guiname'])
            """






#
# Brush parameters manager
#

# Brush parameters manager dev textures list
class VIEW3D_PT_blfoil_brush_config_dev_texture_picker_menu(bpy.types.Panel):
    bl_category = 'Lizards'
    # bl_context = '.objectmode'  # dot on purpose (access from topbar)
    bl_label = 'Dev Textures'
    bl_parent_id = 'VIEW3D_PT_blender_foil_brush_config_gui'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        dumpster = layout.column(align=False)
        dumpster.use_property_split = True
        dumpster.use_property_decorate = False

        dumpster.template_list('blfoil_common_brush_materials_item_draw', '', context.scene, 'blfoil_common_brush_materials', context.scene, 'blfoil_common_brush_materials_index')
        dumpster.operator('mesh.blfoil_set_suggested_mat', text='Set Material')

# Brush parameters manager brush params
class VIEW3D_PT_blender_foil_brush_config_gui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lizards'
    bl_label = 'Tegu'
    # https://youtu.be/6tCz-M66_vo

    def draw(self, context):
        layout = self.layout
        
        
        dumpster = layout.column(align=False)
        dumpster.use_property_split = True
        dumpster.use_property_decorate = False

        # dumpster.prop(context.scene.blents, 'dnenum')
        # the_filter = dumpster.template_list('blfoil_etype_selector_panel_itemdraw', '', context.scene, 'blfoil_etype_selector_list', context.scene, 'blfoil_etype_selector_list_index')

        # dumpster.operator('mesh.set_ent_type', text='Mark entity')
        
        # dumpster.operator('mesh.blfoil_export_vmf', text='Export vmf')
        #

        if context.object != None:
            cent_type = context.object.ent_conf.obj_ent_type
            isbrush = context.object.blfoil_ent_specials.is_world_brush

            brush_config_show = False

            if vp_blpe_ents.get(cent_type) != None:
                brush_config_show = True

            if brush_config_show:
                if vp_blpe_ents[cent_type][9]['brush_ent'] == '1':
                    brush_config_show = True
                else:
                    brush_config_show = False

            if isbrush:
                brush_config_show = True



            if brush_config_show:

                # dumpster.template_list('blfoil_common_brush_materials_item_draw', '', context.scene, 'blfoil_common_brush_materials', context.scene, 'blfoil_common_brush_materials_index')
                # dumpster.operator('mesh.blfoil_set_suggested_mat', text='Set Material')

                dumpster.prop(context.object.blfoil_ent_specials, 'brush_material_name')
                dumpster.prop(context.object.blfoil_ent_specials, 'lightmap_scale')
                dumpster.prop(context.object.blfoil_ent_specials, 'texture_scale')





