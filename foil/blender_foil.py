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
import random
import bmesh
import mathutils
import os.path
from pathlib import Path
import sys
import shutil
import subprocess



def getfilemd5(filepath):

    file = str(filepath) # Location of the file (can be set a different way)
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.md5() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    return(file_hash.hexdigest()) # Get the hexadecimal digest of the hash



def vmf_export_foil(self, context):

    # grab vmf path
    file_is = 0
    
    sce_vmf_path = str(bpy.path.abspath(bpy.context.scene.blfoil.scene_vmf_path))
    
    if os.path.isfile(sce_vmf_path):
        file_is = 1
    else:
        file_is = 0
        print('vmf path does not exist!')
    

    if '.vmf' in sce_vmf_path and file_is == 1:
        # =================================================
        #
        # Step 1: Delete all liz3 elements from old file
        #
        # =================================================

        # backup the shit 
        copyfile(sce_vmf_path, sce_vmf_path.replace('.vmf', '') + '_backup' + '.vmf')

        # remove current ver
        # os.remove("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf")

        # create empty file to append to
        # fl = open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf", "a")
        # fl.write("")
        # fl.close()




        file = open(sce_vmf_path)

        # create an array of lines out of the input vmf file
        linez = file.readlines()

        list_of_objects = []
        a = 0
        b = 0

        for strnum, linestr in enumerate(linez):
            if re.search('^[a-zA-Z].*', linestr):
                a = strnum
                
            if 'liz3' in linestr:
                b = strnum
                
            if '}\n' == linestr:
                list_of_objects.append([a,b,strnum])
                # print(linez[a-1])
                a = 0
                b = 0
                

        # print (list_of_objects)

        file.close()
        # now remove the old file 
        os.remove(sce_vmf_path)

        for obj in list_of_objects:
            if obj[1] == 0:
                # print(str(obj[0]) + " " + str(obj[1]) + " " + str(obj[2]) )
                # print(linez[obj[0]])
                
                with open(sce_vmf_path, "a") as txt_file:
                    for i in range(obj[0], obj[2] + 1): 
                        txt_file.write(linez[i])
                        # print(linez[i])
                    print("!")





        # =================================================
        #
        # Step 2: Actually export the shit
        #
        # =================================================
        
        
        def float2rgb(float):
            # print(bpy.data.lights["Spot"].color.b)
            if type(float) is int or type(float) is str:
                print('Tthis is int, not a valid object with float. String and hex support coming soon')
                return False
            else:
                if hasattr(float, 'color'):
                    if hasattr(float.color, 'r') and hasattr(float.color, 'g') and hasattr(float.color, 'b'): 
                        print('has color attribute and rgb values')
                        # convert
                        r = round(float.color.r * 255)
                        g = round(float.color.g * 255)
                        b = round(float.color.b * 255)
                        
                        ret = str(r) + ' ' + str(g) + ' ' + str(b)
                        
                        return ret
                    else:
                        print('rgb2hex: given object has color attribute but lacks a color channel !')
                        return False
                else:
                    print('rgb2hex: given object has no color attribute! Most likely not a light!')
                    return False



        hardcoded_prop_static_preset = """
entity
{
    "classname" "prop_static"
    "angles" "ent_tplate_angles"
    "disableselfshadowing" "0"
    "disableshadows" "0"
    "disablevertexlighting" "0"
    "fademaxdist" "0"
    "fademindist" "-1"
    "fadescale" "1"
    "ignorenormals" "0"
    "maxdxlevel" "0"
    "mindxlevel" "0"
    "liz3" "1"
    "model" "ent_tplate_model"
    "screenspacefade" "0"
    "skin" "0"
    "solid" "6"
    "origin" "ent_tplate_pos"
    editor
    {
        "color" "255 255 0"
        "visgroupshown" "1"
        "visgroupautoshown" "1"
        "logicalpos" "[0 0]"
    }
}
        """



        hardcoded_light_spot_preset = """
entity
{
    "id" "13"
    "classname" "light_spot"
    "_cone" "lightdegsize"
    "_constant_attn" "0"
    "_distance" "light_zero_perc_dist"
    "_exponent" "0"
    "_fifty_percent_distance" "light_half_faloff_dist"
    "_hardfalloff" "1"
    "liz3" "1"
    "_inner_cone" "lightdeg_inner_size"
    "_light" "light_light_info"
    "_lightHDR" "-1 -1 -1 1"
    "_lightscaleHDR" "1"
    "_linear_attn" "1"
    "_quadratic_attn" "0"
    "_zero_percent_distance" "light_zero_perc_dist"
    "angles" "ent_tplate_angles"
    "pitch" "lightspot_pitch"
    "spawnflags" "0"
    "style" "0"
    "origin" "ent_tplate_pos"
    editor
    {
        "color" "220 30 220"
        "visgroupautoshown" "1"
        "logicalpos" "[0 0]"
    }
}
        """
        


        # define a place to store the constructed crap
        hammer_ents_constructed = []

        # return a list of all the instances marked for export of models
        hammer_marked_list = [obj for obj in bpy.data.objects if "foil_conf" in obj and len(obj.foil_conf.model_name) > 3]

        # return a list of all the spotlights
        foil_spotlight_list = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.data.type == 'SPOT']
        
        # todo: A button to delete all data
        
        # bpy.context.selected_objects[0].data.type
        # bpy.context.selected_objects[0].type

        #
        # construct an array containing all the constructed ents
        #
        for obj in hammer_marked_list:
            # extract rotations
            rotx = str(round(math.degrees(obj.matrix_world.to_euler()[0]), 4))
            roty = str(round(math.degrees(obj.matrix_world.to_euler()[1]), 4))
            rotz = str(round(math.degrees(obj.matrix_world.to_euler()[2]), 4))
            
            # extract locations
            locx = str(round(obj.matrix_world[0][3], 4))
            locy = str(round(obj.matrix_world[1][3], 4))
            locz = str(round(obj.matrix_world[2][3], 4))

            print('\n'+obj.name+'\n')
            print(obj.foil_conf.model_name)
            
            if len(str(obj.foil_conf.model_name)) > 1:
            
                # write visgroups
                apgroups = hardcoded_prop_static_preset.splitlines(True)
                # 22
                
                if len(obj.foil_conf.object_assigned_vgroups.split(':')) > 0:
                    for vgroup in obj.foil_conf.object_assigned_vgroups.split(':'):
                        if vgroup != '':
                            apgroups.insert(23, '    "visgroupid" "' + vgroup + '"\n')
            
                adde_vgroups = ''.join(apgroups)
            
                hammer_ents_constructed.append(
                adde_vgroups
                .replace('ent_tplate_pos', locx + ' ' + locy + ' ' + locz)
                .replace('ent_tplate_model', obj.foil_conf.model_name)
                .replace('ent_tplate_angles', roty + ' ' + rotz + ' ' + rotx)
                )
                
                print('appended')
            else:
                print('has config, but model name is nil')
            
        #
        # Add Construct lights
        #

        for obj in foil_spotlight_list:
            # extract rotations
            rotx = str(round(math.degrees(obj.matrix_world.to_euler()[0]), 4))
            roty = str(round(math.degrees(obj.matrix_world.to_euler()[1]), 4))
            rotz = str(round(math.degrees(obj.matrix_world.to_euler()[2]), 4))
            
            # extract locations
            locx = str(round(obj.matrix_world[0][3], 4))
            locy = str(round(obj.matrix_world[1][3], 4))
            locz = str(round(obj.matrix_world[2][3], 4))
            
            # calc power
            strength = str(int(obj.data.energy / 18000))
            print('strngth is:' + str(strength))
            
            # make color
            light_color = str(float2rgb(obj.data))
            
            # faloff
            faloff_50 = str(int(obj.data.cutoff_distance / 2))
            faloff_100 = str(int(obj.data.cutoff_distance))
            
            # angles
            outer_angle = str(round(math.degrees(obj.data.spot_size), 2))
            
            inner_angle = str(round(math.degrees(obj.data.spot_blend * obj.data.spot_size), 3))
            print(inner_angle)

            hammer_ents_constructed.append(
            hardcoded_light_spot_preset
            .replace('ent_tplate_pos', locx + ' ' + locy + ' ' + locz)
            .replace('ent_tplate_angles', roty + ' ' + rotz + ' ' + rotx)
            .replace('lightdegsize', outer_angle)
            .replace('light_zero_perc_dist', faloff_100)
            .replace('light_half_faloff_dist', faloff_50)
            .replace('lightdeg_inner_size', inner_angle)
            .replace('light_light_info', str(light_color) + ' ' + str(strength))
            .replace('lightspot_pitch', roty)
            )

        print('Constructed result is: ')
        print(''.join(hammer_ents_constructed))
            




        # open the file
        file = open(sce_vmf_path)

        # create an array of lines out of the input vmf file
        linez = file.readlines()

        # figure out the length of the given array
        nI = len(linez)

        # empty offset for the bracker
        # not functional, in theory, but let it be
        world_bracket_offset = 0

        # empty container for world offset
        # not functional, in theory, but let it be
        world_offset = 0



        def insert_dilator(howdeep):
            linez.insert(howdeep, ''.join(hammer_ents_constructed))
            with open(sce_vmf_path, "w") as txt_file:
                for line in linez:
                    txt_file.write("".join(line))
            # file.close()


        # find cameras
        def find_cams():
            # cam_offset = linez.index("cameras\n")
            cam_offset = list_of_objects[-1][2] + 1
            print('cam offset is:')
            print(cam_offset)
            insert_dilator(cam_offset)
        

        # exec find cams
        find_cams()
        file.close()
    else:
        self.report({"WARNING"}, "This is not a .vmf, stop lying to me, bitch")

test_rad_list = [
    ('nil', 'nil', 'nil')
]

scene_vmf_vgroups = [
    ('nil_ar', 'nil_ar', '1'),
    ('nil1_ar', 'nil2_ar', '0')
]


def unmark_asset(self, context):
    # print('fuck')
    for obj in bpy.context.selected_objects:
        print(obj.foil_conf.model_name)
        if len(str(obj.foil_conf.model_name)) > 1:
            # del obj.foil_conf
            print('pootis shit')
            obj.foil_conf.model_name = ''
        else:
            print('object is not an asset alr')


def setrad_col(self, context):
    if ':' in str(bpy.context.scene.lightsrad.title()):
        make_rgb = bpy.context.scene.lightsrad.title().split(':')[1]
        if len(make_rgb) > 6 and len(make_rgb) < 30 and ' ' in str(make_rgb):
            make_rgb = make_rgb.split(' ')
            mk_r = float(make_rgb[0]) / 255
            mk_g = float(make_rgb[1]) / 255
            mk_b = float(make_rgb[2]) / 255

            bpy.context.scene.rad_color = (mk_r, mk_g, mk_b)
            rewrite_rad_list()
        else:
            print('invalid rad entry color syntax: Color property is invalid')
    else:
        print('invalid rad entry color syntax: No ":" presented')

def rewrite_rad_list():

    # if os.path.isfile(str(bpy.context.scene.blfoil.scene_radlights_path)):
        # pass
    # else:
        # return
    
    rad_path = 'E:\\Gamess\\steamapps\\common\\Half-Life 2\\hl2\\lights.rad'
    # rad_path = str(bpy.context.scene.blfoil.scene_radlights_path)



    checksum = getfilemd5(str(rad_path))

    # if str(checksum) != str(bpy.context.scene.blfoil.lightsradcsum):
        # pass
    # else:
        # return
        # print('files are equal')

    radfile = open(str(rad_path))
    radlines = radfile.readlines()
    print(radlines)

    rad_entries = []

    for radentry in radlines:
        
        if '\t' in radentry:
            par = radentry.split('\t')
            todel = []
            for val_inx, val in enumerate(reversed(par)):
                print(len(val))
                if len(val) < 2:
                    todel.append(val_inx)
            for index in sorted(todel, reverse=True):
                del par[index]
                
            par[1] = str(par[1].replace('\n', ''))
            rad_entries.append(':'.join(par))
        else:
            print('invalid syntax. Skipping for now')

    print(rad_entries)

    full_rad_lis = []
    global test_rad_list
    test_rad_list = [
        ('nil', 'nil', 'nil')
    ]
    for rentry in rad_entries:
        get_name = rentry.split(':')[0]
        test_rad_list.append((rentry, get_name, 'rad entry'))
    # bpy.types.Scene.lightsrad = EnumProperty(items=full_rad_lis, name="Rads", default='nil', update=setrad_col)
    bpy.types.Scene.lightsrad = EnumProperty(items=test_rad_list, name="Rads", default='nil', update=setrad_col)
    # bpy.context.scene.blfoil.lightsradcsum = str(getfilemd5(str(rad_path)))

rewrite_rad_list()

def append_vmf_vgroups(self, context):
    # print('shit')
    
    # grab vmf path
    file_is = 0
    
    sce_vmf_path = str(bpy.path.abspath(bpy.context.scene.blfoil.scene_vmf_path))
    
    if os.path.isfile(sce_vmf_path):
        file_is = 1
    else:
        file_is = 0
        print('vmf path does not exist!')
    

    if '.vmf' in sce_vmf_path and file_is == 1:
        print('append vgroups')
        
        file = open(sce_vmf_path)

        # create an array of lines out of the input vmf file
        linez = file.readlines()
        global scene_vmf_vgroups
        scene_vmf_vgroups = []
        for lineid, lineval in enumerate(linez):
            if '"visgroupid" ' in lineval:
                get_id = linez[lineid].split('" "')[1].replace('"', '').replace('\n', '')
                get_name = linez[lineid - 1].split('name" "')[1].replace('"', '').replace('\n', '')
                get_color = linez[lineid + 1].split('color" "')[1].replace('"', '').replace('\n', '')
                
                # id : color, hammer name, show unassign button (do not use)
                # todo: make 2 panels: 1 - availabe groups, 2 - assigned to
                scene_vmf_vgroups.append((get_id + ':' + get_color, get_name, 0))
        
        print(scene_vmf_vgroups)
        
        
        
        
        
        
    else:
        print('aint no valid vmf, fuckoff')

# append_vmf_vgroups()



def set_arlight_op(self, context):
    # print('fuck')
    # areal_list = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.data.type == 'AREA']
    for obj in bpy.context.selected_objects:
        if obj.type == 'LIGHT' and obj.data.type == 'AREA':
            obj.foil_conf.arlight_config = str(bpy.context.scene.lightsrad)
            rgb = bpy.context.scene.lightsrad.split(':')[1].split(' ')
            ar = int(rgb[0]) / 255
            ag = int(rgb[1]) / 255
            ab = int(rgb[2]) / 255
            for pootis in bpy.context.selected_objects:
                pootis.data.color = (ar, ag, ab)
                pootis.data.energy = int(rgb[3]) * 262144
                


def unset_arlight_exp(self, context):
    for obj in bpy.context.selected_objects:
        obj.foil_conf.arlight_config = ''

def copy_arlight_config(self, context):
    if str(bpy.context.active_object.foil_conf.arlight_config) != '' and str(bpy.context.active_object.foil_conf.arlight_config) != 'nil':
        for obj in bpy.context.selected_objects:
            obj.foil_conf.arlight_config = str(bpy.context.active_object.foil_conf.arlight_config)
    else:
        print('theres no point in copying empty config !')


def upd_area(self, context):
    # print('heavy update')
    if str(bpy.context.active_object.foil_conf.arlight_config) == '' or str(bpy.context.active_object.foil_conf.arlight_config) == 'nil':
        # print('Not a valid config. Dont change intensity')
        pass
    else:
        if ':' in str(bpy.context.active_object.foil_conf.arlight_config):
            rgb = bpy.context.scene.lightsrad.split(':')[1].split(' ')
            intens = bpy.context.active_object.foil_conf.arlight_strength
            ar = int(rgb[0]) / 255
            ag = int(rgb[1]) / 255
            ab = int(rgb[2]) / 255
            # for pootis in bpy.context.selected_objects:
            bpy.context.active_object.data.color = (ar, ag, ab)
            bpy.context.active_object.data.energy = int(rgb[3]) * 262144 * intens

def foil_export_area_lights(self, context):


    sce_vmf_path = str(bpy.path.abspath(bpy.context.scene.blfoil.scene_vmf_path))

    file = open(sce_vmf_path)

    # create an array of lines out of the input vmf file
    linez = file.readlines()

    list_of_brushes = []

    brstart = 0
    brmark = 0
    bigbang = 'nil'

    # find world
    for strnum, linestr in enumerate(linez):
        if linestr == 'world\n':
            print('found world: ' + str(strnum))
            bigbang = strnum


    for strnum, linestr in enumerate(linez):
        # if re.search('^[a-zA-Z].*', linestr):
        if 'solid\n' in linestr:
            print('found solid: ' + str(strnum))
            brstart = strnum
            
        if '"-570425344"' in linestr:
            brmark = strnum
            
        if '\t}\n' == linestr and brstart != 0:
            print('found solid end: ' + str(strnum))
            list_of_brushes.append([brstart,brmark,strnum])
            print(linez[brstart-1])
            brstart = 0
            brmark = 0

    print(list_of_brushes)

    for brushnum, brush in enumerate(reversed(list_of_brushes)):
        if brush[1] != 0:
            del linez[brush[0]:brush[2] + 1]


    lizards_tail = 'nil'
    lizards_head = 0
    for line_num, linetext in enumerate(linez):
        if linetext == 'world\n':
            lizards_head = 1
            
        if lizards_head == 1:
            if linetext == '}\n':
                print('found lizards tail: ' + str(line_num))
                lizards_tail = line_num
                lizards_head = 0

    print(list_of_brushes)

    # linez.insert(lizards_tail, 'azaza' + '\n')

    export_shit = str(''.join(linez))











    all_elights = []

    def write_elight_brushes(what, lightsource, light_intensity, vgroups):
        
        obj = what
        mtr = obj.matrix_world
        visgrouplist = vgroups.split(':')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(visgrouplist)

        solid = 'solid \n{'

        for f_indx, f in enumerate(obj.data.polygons):
            # process face. We are at face
            print(str(f) + ' use smooth is ' + str(f.use_smooth))
            
            # store collected verts here
            vertz = []
            
            plane = '"plane" "('
            hpp_vertz = 'vertices_plus \n    {'
            
            smoothgroup = ''
            
            cuvc = []
            
            # write all verts
            for idx in f.vertices:
                tvert = obj.data.vertices[idx].co
                fixpos = mtr @ tvert
                print('obj pos: ' + str(tvert) + ' world z pos: ' + str(fixpos[2]))
                
                vertz.append(str(round(fixpos[0], 4)) + ' ' + str(round(fixpos[1], 4)) + ' ' + str(round(fixpos[2], 4)))
                cuvc.append((round(fixpos[0], 4), round(fixpos[1], 4), round(fixpos[2], 4)))
                
            vertz.reverse()
            plane = str(plane) + str(vertz[0]) + ') (' + str(vertz[1]) + ') (' + str(vertz[2]) + ')"'
            
            for vertvect in vertz:
                hpp_vertz = str(hpp_vertz) + '\n        "v" "' + str(vertvect) + '"'
                
            hpp_vertz = str(hpp_vertz) + '\n    }'
            
            
            print(hpp_vertz)
            print(plane)
            
            if f.use_smooth:
                smoothgroup = '"smoothing_groups" "1"'
            else:
                smoothgroup = '"smoothing_groups" "16777216"'
            
            """
            for thing in random.sample(vertz,3):
                plane = str(plane) + 
            """
            
            
            #
            # Calculate texture alignment
            #
            
            # calc U
            uwidth_a = cuvc[2][0] - cuvc[1][0]
            uwidth_b = cuvc[2][1] - cuvc[1][1]
            uwidth_c = cuvc[2][2] - cuvc[1][2]
            
            calc_uwidth = math.sqrt(uwidth_a * uwidth_a + uwidth_b * uwidth_b + uwidth_c * uwidth_c)
            
            calc_ux = uwidth_a / calc_uwidth
            calc_uy = uwidth_b / calc_uwidth
            calc_uz = uwidth_c / calc_uwidth
            
            
            # calc V
            vwidth_a = cuvc[0][0] - cuvc[1][0]
            vwidth_b = cuvc[0][1] - cuvc[1][1]
            vwidth_c = cuvc[0][2] - cuvc[1][2]
            
            calc_vwidth = math.sqrt(vwidth_a * vwidth_a + vwidth_b * vwidth_b + vwidth_c * vwidth_c)
            
            calc_vx = vwidth_a / calc_vwidth
            calc_vy = vwidth_b / calc_vwidth
            calc_vz = vwidth_c / calc_vwidth
            
            print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ')
            print(str(calc_vx) + ' ' + str(calc_vy) + ' ' + str(calc_vz))
            print(str(calc_ux) + ' ' + str(calc_uy) + ' ' + str(calc_uz))
            
            construct_u = str(round(calc_ux, 3)) + ' ' + str(round(calc_uy, 3)) + ' ' + str(round(calc_uz, 3))
            construct_v = str(round(calc_vx, 3)) + ' ' + str(round(calc_vy, 3)) + ' ' + str(round(calc_vz, 3))
            
            
            
            # construct face
            
            if f_indx == 4:
                makeface = 'side\n{' + '\n    ' + str(plane) + '\n    ' + str(hpp_vertz) + '\n    ' + '"material" "' + str(lightsource) + '"\n    "uaxis" "[' + str(light_intensity) + ' ' + str(light_intensity) + ' ' + str(light_intensity) + ' 0] 0.25"\n    "vaxis" "[' + str(light_intensity) + ' ' + str(light_intensity) + ' ' + str(light_intensity) + ' 0] 0.25"\n    "rotation" "0"\n    "lightmapscale" "16"\n    "smoothing_groups" "-570425344"\n}'
            else:
                makeface = 'side\n{' + '\n    ' + str(plane) + '\n    ' + str(hpp_vertz) + '\n    ' + '"material" "TOOLS/TOOLSNODRAW"\n    "uaxis" "[' + construct_u + ' 0] 0.25"\n    "vaxis" "[' + construct_v + ' 0] 0.25"\n    "rotation" "0"\n    "lightmapscale" "16"\n    "smoothing_groups" "0"\n}'
            
            solid = str(solid) + '\n' + str(makeface)
            # print(str(makeface))
            
            
        # make visgroups
        my_hat = """
        editor
        {
            "color" "0 181 254"
        """
        
        my_jeans = """
            "visgroupshown" "1"
            "visgroupautoshown" "1"
        }
        """
        if len(visgrouplist) > 0:
            for vgroup in visgrouplist:
                if vgroup != '':
                    my_hat = my_hat + '    "visgroupid" "' + vgroup + '"\n'
        
        my_jeans = my_hat + my_jeans

        solid = str(solid) + '\n' + my_jeans + '\n}'
        all_elights.append('\n' + str(solid))




    areal_list = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.data.type == 'AREA' and len(obj.foil_conf.arlight_config) > 2 and obj.foil_conf.arlight_config != 'nil']
    
    if len(areal_list) < 1:
        print('No lights to export!')
        return
    
    for obje in areal_list:
        
        print('area x: ' + str(obje.matrix_world[0][3]) + ' y: ' + str(obje.matrix_world[1][3]) + ' z: ' + str(obje.matrix_world[2][3]))
        
        aloc_x = obje.matrix_world[0][3]
        aloc_y = obje.matrix_world[1][3]
        aloc_z = obje.matrix_world[2][3]
        
        rotx = obje.matrix_world.to_euler()[0]
        roty = obje.matrix_world.to_euler()[1]
        rotz = obje.matrix_world.to_euler()[2]
        
        scx = obje.matrix_world.to_scale()[0]
        scy = obje.matrix_world.to_scale()[1]
        scz = obje.matrix_world.to_scale()[2]
        
        # create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1)

        # newly created cube will be automatically selected
        cube = bpy.context.selected_objects[0]


        cube.location = (aloc_x, aloc_y, aloc_z)
        cube.rotation_euler = (rotx, roty, rotz)
        cube.scale = (scx, scy, 8)
        cube['foil_elight'] = 1
        
        obj = cube
            
        # one blender unit in x-direction
        distz = mathutils.Vector((0.0, 0.0, 4.0))
        rotationMAT = obj.rotation_euler.to_matrix()
        rotationMAT.invert()
        # project the vector to the world using the rotation matrix
        zVector = distz @ rotationMAT
        obj.location = obj.location + zVector
        
    export_are_light_brushes = [obj for obj in bpy.data.objects if 'foil_elight' in obj]
    print(export_are_light_brushes)
    # export_are_light_brushes.append(1)

    # create a new cube
    bpy.ops.mesh.primitive_cube_add(size=1)

    # newly created cube will be automatically selected
    fuck_python_cube = bpy.context.selected_objects[0]
    fuck_python_cube.name = 'i_want_to_have_bdsm_with_a_lizard'
    export_are_light_brushes.append(fuck_python_cube)

    for aeobj in export_are_light_brushes:
        if 'i_want_to_have_bdsm_with_a_lizard' in aeobj.name:
            print('nen')
        else:
            print(aeobj.matrix_world)
            write_elight_brushes(aeobj, str(obje.foil_conf.arlight_config.split(':')[0]).upper(), obje.foil_conf.arlight_strength, obje.foil_conf.object_assigned_vgroups)

            print(str(obje.foil_conf.arlight_config.split(':')[0]).upper())
    for aelightb in export_are_light_brushes:
        bpy.data.objects.remove(aelightb, do_unlink=True)


    """
    text_file = open('E:\\!!Blend_Projects\\scripts\\wallworm4blender\\qr_test\\map\\fuck_yall.txt', 'w')
    n = text_file.write(str(''.join(all_elights)))
    text_file.close()
    """


    total_export = str(''.join(all_elights))
    cleaned_map = str(''.join(linez))

    linez.insert(lizards_tail, str(total_export) + '\n')

    text_file = open(sce_vmf_path, 'w')
    n = text_file.write(str(''.join(linez)))
    text_file.close()



def assign_to_vgroup(self, context):
    
    # print('fuck')
    print(self.gr_id)
    """
    for obj in bpy.context.selected_objects:
        # print(obj.foil_conf.model_name)
        if len(str(obj.foil_conf.model_name)) > 1:
            # del obj.foil_conf
            print('pootis shit')
            obj.foil_conf.model_name = ''
        else:
            print('object is not an asset alr')
    """
    for obj in bpy.context.selected_objects:
        check_shit = obj.foil_conf.object_assigned_vgroups.split(':')
        
        if self.gr_id in check_shit:
            print(str(self.gr_id) + ' is assigned alr')
            
            pootis = obj.foil_conf.object_assigned_vgroups.split(':')
            pootis.remove(self.gr_id)
            # del bpy.types.Scene.pipe
            obj.foil_conf.object_assigned_vgroups = ':'.join(pootis)
        else:
            pootis = obj.foil_conf.object_assigned_vgroups.split(':')
            pootis.append(self.gr_id)
            # del bpy.types.Scene.pipe
            obj.foil_conf.object_assigned_vgroups = ':'.join(pootis)


def foil_compile_skybox(self, context):
    print('fuck you')
    
    def excep_raiser():
        raise Exception('THIS IS AN ARTIFICIALLY TRIGGERED ERROR. IGNORE THIS!!!!!!!!!!! CHECK THE INFO PANEL!!!!')
    
    
    # Check if game path exists. If not - stop script execution and throw a warning
    # but first - check if we use SourceOps Game path and if SourceOps is available at all
    # check if we use source ops
    if bpy.context.scene.blfoil.blfoil_sky_use_sourceops_gpath == True:
        try:
            sky_foil_gpath = bpy.context.scene.sourceops.game_items[bpy.context.scene.sourceops.game_index]['game']
        except:
            self.report({'WARNING'}, 'Unable to locate any SourceOps games. Go drink some tea')
            # excep_raiser()
            sky_foil_gpath = 'nil'
    else:
        sky_foil_gpath = bpy.path.abspath(bpy.context.scene.blfoil.blfoil_sky_game_path)
    
    
    
    if os.path.isfile(os.path.join(Path(bpy.path.abspath(sky_foil_gpath)).parents[0], 'bin', 'vtex.exe')):
        print('found vtex.exe and game')
    else:
        self.report({'WARNING'}, 'Game path invalid, go kys, fucker. Unable to locate vtex.exe')
        excep_raiser()
    

    # Check if X or Y is higher than 4096 in either dimension. 
    # If so - Stop script execution and throw a warning 
    # Else - proceed with script execution
    
    foil_sky_dimx = bpy.context.scene.blfoil.blfoil_sky_size_x
    foil_sky_dimy = bpy.context.scene.blfoil.blfoil_sky_size_y
    
    if foil_sky_dimx > 4096 or foil_sky_dimy > 4096:
        self.report({'WARNING'}, 'requested texture is bigger than 4096 in either dimension. For now - stop script')
        excep_raiser()
    
    # check if any axis is smaller than 8, throw an error if so and stop execution
    if foil_sky_dimx < 8 or foil_sky_dimy < 8:
        self.report({'WARNING'}, 'Requested texture is smaller than 8 on any axis. Stop execution and fuck you')
        excep_raiser()
        
    # check if not power of two
    if math.log(foil_sky_dimx, 2).is_integer() and math.log(foil_sky_dimy, 2).is_integer():
        print('Is power of 2. Noice COFFEE TABLE')
    else:
        self.report({'WARNING'}, 'Current implementation does not allow values of non-power of two')
        excep_raiser()
    
    
    
    # Check the destination folder condition: If exists, but overwrite is False - stop and throw error
    
    sky_foil_boxname = bpy.context.scene.blfoil.blfoil_sky_boxname
    
    this_blend_file = bpy.path.abspath('//')
    
    
    destination_folder_qcheck = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname)
    print(destination_folder_qcheck)
    
    if os.path.isdir(destination_folder_qcheck) and bpy.context.scene.blfoil.blfoil_sky_overwrite_shit == False:
        print('shite exists')
        self.report({'WARNING'}, 'The specified path exists, but overwrite checkbox is tunred off')
        excep_raiser()
    else:
        try:
            shutil.rmtree(destination_folder_qcheck)
        except OSError as e:
            print("Error: %s : %s" % (destination_folder_qcheck, e.strerror))
    
    
    # Run cleanup just in case :
    def docleanup():
        # delete all images
        for img in bpy.data.images:
            if 'liz3bkproc_delme' in img.name:
                bpy.data.images.remove(bpy.data.images[img.name])
        # delete all mats
        for mat in bpy.data.materials:
            if 'liz3bkproc_delme' in mat.name or 'skybakem_' in mat.name:
                bpy.data.materials.remove(bpy.data.materials[mat.name])
        # delete all objects
        for objc in bpy.data.objects:
            if 'liz3bkproc_delme' in objc.name:
                bpy.data.objects.remove(bpy.data.objects[objc.name])
        # delete all worlds
        for wrld in bpy.data.worlds:
            if 'liz3bkproc_delme' in wrld.name:
                bpy.data.worlds.remove(wrld)
        # delete local temp_dir
        try:
            shutil.rmtree(os.path.join(this_blend_file, 'tmp_folder_liz3bkproc_delme'))
        except:
            print('Local tmp folder does not exists. Dont delete')
        # todo: also delete object data n shit
        


    docleanup()
    # delete src dir if any
    try:
        shutil.rmtree(destination_folder_qcheck)
    except:
        print('materialsrc folder does not exist alr')
        
    
    
    
    # Create destination folders
    create_destination_folders = destination_folder_qcheck
    os.makedirs(os.path.join(create_destination_folders, sky_foil_boxname + '_exr_src'))
    os.makedirs(os.path.join(create_destination_folders, sky_foil_boxname + '_generated_pfm'))
    os.makedirs(os.path.join(create_destination_folders, sky_foil_boxname + '_tga_src'))
    
    
    
    # Since we're gonna mess around with the render settings - save them and bring them back later.
    bpy.context.scene['liz3bkproc_delme_save_r_prefs'] = {
        # Dimensions
        'res_x': bpy.context.scene.render.resolution_x,
        'res_y': bpy.context.scene.render.resolution_y,
        'res_perc': bpy.context.scene.render.resolution_percentage,
        
        'aspectx': bpy.context.scene.render.pixel_aspect_x,
        'aspecty': bpy.context.scene.render.pixel_aspect_y,
        
        'render_region': bpy.context.scene.render.use_border,
        
        # Output mode
        'render_filepath': bpy.context.scene.render.filepath,
        'use_file_extension': bpy.context.scene.render.use_file_extension,
        'use_render_cache': bpy.context.scene.render.use_render_cache,
        'file_format': bpy.context.scene.render.image_settings.file_format,
        'color_mode': bpy.context.scene.render.image_settings.color_mode,
        'use_overwrite': bpy.context.scene.render.use_overwrite,
        'use_placeholder': bpy.context.scene.render.use_placeholder,
        'img_color_depth': bpy.context.scene.render.image_settings.color_depth,
        'exr_codec': bpy.context.scene.render.image_settings.exr_codec,
        'use_zbuffer': bpy.context.scene.render.image_settings.use_zbuffer,
        'use_preview': bpy.context.scene.render.image_settings.use_preview,
        'use_compositing': bpy.context.scene.render.use_compositing,
        'use_sequencer': bpy.context.scene.render.use_sequencer,
        'dither_intensity': bpy.context.scene.render.dither_intensity
        # TODO: MAKE OLD CAMERA ACTIE AGAIN
        
    }
    
    
    
    # Render the shit
    
    sidez = ['bk:90:0:-90', 'dn:0:0:-180', 'ft:90:0:90', 'lf:90:0:0', 'rt:90:0:-180', 'up:180:0:180']
    
    # create camera
    sky_camera_data = bpy.data.cameras.new(name='obj_data_skycam_liz3bkproc_delme')
    
    sky_camera_data.type = 'PERSP'
    sky_camera_data.clip_end = 100000.0
    # sky_camera_data.lens_unit = 'FOV'
    # sky_camera_data.angle = 1.5707963705062866
    sky_camera_data.lens = 64
    sky_camera_data.sensor_width = 128.5
    
    
    
    sky_camera_object = bpy.data.objects.new('skycam_liz3bkproc_delme', sky_camera_data)
    bpy.context.scene.collection.objects.link(sky_camera_object)

    # make this camera active
    bpy.context.scene.camera = sky_camera_object


    
    for side in sidez:
        theside = side.split(':')[0]
    
        csidex = int(side.split(':')[1])
        csidey = int(side.split(':')[2])
        csidez = int(side.split(':')[3])
    
        sky_camera_object.rotation_euler[0] = math.radians(csidex)
        sky_camera_object.rotation_euler[1] = math.radians(csidey)
        sky_camera_object.rotation_euler[2] = math.radians(csidez)
    
        # Setup render settings
        

        # Set render size
        if bpy.context.scene.blfoil.blfoil_sky_nobottom == True:
            if theside == 'dn':
                bpy.context.scene.render.resolution_x = 8
                bpy.context.scene.render.resolution_y = 8
            else:
                bpy.context.scene.render.resolution_x = foil_sky_dimx
                bpy.context.scene.render.resolution_y = foil_sky_dimy
        else:
            bpy.context.scene.render.resolution_x = foil_sky_dimx
            bpy.context.scene.render.resolution_y = foil_sky_dimy
        
        
        
        
        # adjust camera if half the size
        if foil_sky_dimy == foil_sky_dimx / 2:
            print('dimy = dimx/2')
            if theside == 'dn' or theside == 'up':
                
                sky_camera_data.shift_y = 0
                sky_camera_data.shift_x = 0
                bpy.context.scene.render.resolution_x = foil_sky_dimx
                bpy.context.scene.render.resolution_y = foil_sky_dimx
                print('triggered dn or up side = ' + theside + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))
            else:
                sky_camera_data.shift_y = 0.25
                sky_camera_data.shift_x = 0
                bpy.context.scene.render.resolution_x = foil_sky_dimx
                bpy.context.scene.render.resolution_y = foil_sky_dimy
                print('triggered else side = ' + theside + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))

            if theside == 'dn':
                bpy.context.scene.render.resolution_x = 8
                bpy.context.scene.render.resolution_y = 8
                print('triggered dn side = ' + theside + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))
 
        
        print('final side = ' + theside + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))

        
        
        # set output dir per side
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            filepathed = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_exr_src', sky_foil_boxname + theside + '.exr')
        else:
            filepathed = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_generated_pfm', sky_foil_boxname + theside)
        
        
        bpy.context.scene.render.filepath = filepathed
        
        # set output prefs
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
            bpy.context.scene.render.image_settings.color_depth = '32'
            bpy.context.scene.render.image_settings.exr_codec = 'ZIP'
            bpy.context.scene.render.image_settings.use_zbuffer = False
            bpy.context.scene.render.image_settings.use_preview = False
        else:
            bpy.context.scene.render.image_settings.file_format = 'TARGA_RAW'
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
            
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.use_render_cache = False
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_placeholder = False
            
            
        # set sequencer to false and dither to 1
        bpy.context.scene.render.use_sequencer = False
        bpy.context.scene.render.use_compositing = True
        bpy.context.scene.render.dither_intensity = 1.0
        
        
        # Render
        bpy.ops.render.render(write_still = 1)
        
        
        # if HDR then we need stupid LDR fallbacks
        # fuck them really - downscale them fuckers by a factor of fucking 2
        # todo: finally predefine scene resolution x. or nah ?
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            bpy.context.scene.render.image_settings.file_format = 'TARGA_RAW'
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
            bpy.context.scene.render.filepath = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_tga_src', sky_foil_boxname + theside)
            bpy.context.scene.render.resolution_x = bpy.context.scene.render.resolution_x / 2
            bpy.context.scene.render.resolution_y = bpy.context.scene.render.resolution_y / 2
            bpy.ops.render.render(write_still = 1)
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    # Remove camera once done rendering
    bpy.data.objects.remove(sky_camera_object)

    
    # Make some paths for later use
    vtex_exe = os.path.join(Path(sky_foil_gpath).parents[0], 'bin', 'vtex.exe')
    vtex_outdir = os.path.join(sky_foil_gpath, 'materials', 'skybox', sky_foil_boxname)
    
    
    
    
    # create pfms and text files for vtex.exe
    
    try:
        shutil.rmtree(vtex_outdir)
    except:
        print('no vtf path alr')
    
    
    for tside in sidez:

        current_side = tside.split(':')[0]
        
        # construct pfm output 
        pfmoutpath = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_generated_pfm', sky_foil_boxname + '_hdr' + current_side + '.pfm')
    
        # construct exr inp path
        exrinpath = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_exr_src', sky_foil_boxname + current_side + '.exr')
    
        # img magick path
        hl2deathmatch = 'E:\\!!Blend_Projects\\env_baker\\util\\pfm2exr\\magick.exe'
    
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            # convert with image magick 
            magic_args = [hl2deathmatch, exrinpath, '-endian', 'LSB', pfmoutpath]
            subprocess.call(magic_args)
        
        
        
        # write text file 
        
        text_file_content = """nolod 1
nomip 1
nonice 1"""

        vmt_content = """"sky"
{

}"""

        ldr_tga_txt = """nolod 1
nomip 1
nonice 1
nocompress 1"""

        write_text_file_content = text_file_content.splitlines()
        write_vmt_content = vmt_content.splitlines()

        # construct text file path and text file
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            txtfile_path = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_generated_pfm', sky_foil_boxname + '_hdr' + current_side + '.txt')
            write_text_file_content.insert(0, 'pfm 1')
            write_text_file_content.insert(-1, 'pfmscale 1')
            if bpy.context.scene.blfoil.blfoil_sky_hdr_compressed == False:
                write_text_file_content.insert(-1, 'nocompress 1')
        else:
            txtfile_path = os.path.join(sky_foil_gpath, 'materialsrc', 'skybox', sky_foil_boxname, sky_foil_boxname + '_generated_pfm', sky_foil_boxname + current_side + '.txt')
            write_text_file_content.insert(-1, 'nocompress 1')

        if foil_sky_dimy == foil_sky_dimx / 2 and current_side != 'up' and current_side != 'dn':
            write_text_file_content.insert(-1, 'clamps 1')
            write_text_file_content.insert(-1, 'clampt 1')

        assrod = open(txtfile_path,'w')
        assrod.write('\n'.join(write_text_file_content))
        assrod.close()
        
        # write ldr fallbacks
        assrod_tga = open(txtfile_path.replace('_generated_pfm', '_tga_src').replace('_hdr', ''),'w')
        assrod_tga.write(ldr_tga_txt)
        assrod_tga.close()
        
        # convert to vtf
        # maybe separate this into a separate for loop?
        vtex_args = [vtex_exe, '-nopause', '-outdir', vtex_outdir, txtfile_path]
        subprocess.call(vtex_args)
        
        
        # convert ldr vtf
        vtex_args = [vtex_exe, '-nopause', '-outdir', vtex_outdir, txtfile_path.replace('_generated_pfm', '_tga_src').replace('_hdr', '')]
        subprocess.call(vtex_args)
        
        # write vmt
        ldrbasepath = os.path.join('skybox', sky_foil_boxname, sky_foil_boxname + current_side)
        if bpy.context.scene.blfoil.blfoil_sky_hdrldr == 'HDR':
            vmtfile_path = os.path.join(sky_foil_gpath, 'materials', 'skybox', sky_foil_boxname, sky_foil_boxname + '_hdr' + current_side + '.vmt')
            hdrbasepath = os.path.join('skybox', sky_foil_boxname, sky_foil_boxname + '_hdr' + current_side)
            
            if bpy.context.scene.blfoil.blfoil_sky_hdr_compressed == False:
                write_vmt_content.insert(-1,'    "$hdrbasetexture" "' + hdrbasepath + '"')
            else:
                write_vmt_content.insert(-1,'    "$hdrcompressedtexture" "' + hdrbasepath + '"')
                
            write_vmt_content.insert(-1,'    "$basetexture" "' + ldrbasepath + '"')
      
        else:
            vmtfile_path = os.path.join(sky_foil_gpath, 'materials', 'skybox', sky_foil_boxname, sky_foil_boxname + current_side + '.vmt')
            write_vmt_content.insert(-1,'    "$basetexture" "' + ldrbasepath + '"')
        
        if foil_sky_dimy == foil_sky_dimx / 2 and current_side != 'up' and current_side != 'dn':
            write_vmt_content.insert(-1,'	"$basetexturetransform" "center 0 0 scale 1 2 rotate 0 translate 0 0"')
        
        # write vmt file 
        urethral_dilator = open(vmtfile_path,'w')
        urethral_dilator.write('\n'.join(write_vmt_content))
        urethral_dilator.close()
        
        

        
        
        
        
        
    


# =========================================================
#----------------------------------------------------------
#                   Classes
#----------------------------------------------------------
# =========================================================


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
        name="Enable or Disable",
        description="A bool property",
        default = False
        )
        
    scene_vmf_path : StringProperty(
        name="Path to vmf",
        description="lizards are sexy",
        default = "nil",
        subtype="FILE_PATH",
        update=append_vmf_vgroups
        )
        
    lightsradcsum : StringProperty(
        name="checksum",
        description="I want a lizard to put her tongue in my urethra",
        default = "nil",
        )

    foil_export_area_lights : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    foil_export_props : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )
        
        # EnumProperty(items=test_rad_list, name="Rads", default='nil', update=setrad_col)
        
    scene_radlights_path : StringProperty(
        name="Path to .rad",
        description="I like bread",
        default = "nil",
        subtype="FILE_PATH"
        )
        
    scene_vmf_visgroups : EnumProperty(
        items=scene_vmf_vgroups,
        name="all visgroups",
        description="I like bread"
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


#
# View Panel
#

class VIEW3D_PT_blender_foil(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "foil"
    bl_label = "Aluminium"
    
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
        col.prop(context.scene.blfoil, "all_lights", text="Export all lights")
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

def unmark_asset_button(self, context):
    self.layout.operator(
        OBJECT_OT_unmark_asset.bl_idname,
        text="Add Object",
        icon='PLUGIN')




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
    bpy.types.VIEW3D_MT_mesh_add.append(unmark_asset_button)
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
    bpy.types.VIEW3D_MT_mesh_add.remove(unmark_asset_button)
