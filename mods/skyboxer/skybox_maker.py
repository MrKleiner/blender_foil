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

from ...utils.shared import eval_state

try:
    from bs4 import BeautifulSoup
    from bs4 import Tag, NavigableString
except:
    pass
import asyncio
import socket
import base64
# get the current directory. Just in case
# todo: lmao parent.parent.parent
# replace it with parents[2]
addon_root_dir = Path(__file__).absolute().parent.parent.parent





async def appgui_updater(pngpath, side):
    s = socket.socket()  # Create a socket object
    port = 1337  # Reserve a port for your service every new transfer wants a new port or you must wait.

    s.connect(('localhost', port))
    x = 0

    with open(str(pngpath), 'rb') as readimg:
        b_img = readimg.read()

    test_shit = base64.b64encode(b_img).decode('utf-8', errors='ignore')

    payload = {
        'app_action': 'add_skybox_side',
        'side': side,
        'image': test_shit
    }

    st = json.dumps(payload)
    byt = st.encode()
    s.send(byt)
    # s.send(byt)

    print(x)

    while True:
        data = s.recv(1024)
        if data:
            print(data)
            x += 1
            break

        else:
            print('no data received')


    print('closing')
    s.close()
























# =========================================================
# ---------------------------------------------------------
#                   Base functionality
# ---------------------------------------------------------
# =========================================================



def blfoil_skybox_maker(tgt_scene):

    sk_settings = tgt_scene.blfoil_skyboxer_settings

    this_blend = bpy.path.abspath('//')

    magix = addon_root_dir / 'bins' / 'imgmagick' / 'magick.exe'

    def except_raiser():
        raise Exception('Somethings very wrong')


    # Check if game path exists. If not - stop script execution and throw a warning
    # but first - check if we use SourceOps Game path and if SourceOps is available at all
    # check if we use source ops
    # todo: wtf :(
    if sk_settings.use_sourceops_gpath == True:
        try:
            sky_foil_gpath = tgt_scene.sourceops.game_items[tgt_scene.sourceops.game_index]['game']
        except:
            # self.report({'WARNING'}, 'Unable to locate any SourceOps games. Go drink some tea')
            except_raiser()
    else:
        sky_foil_gpath = bpy.path.abspath(sk_settings.game_path)

    game_path = Path(bpy.path.abspath(sky_foil_gpath))

    # vtex has to be present. Else - can't do shit
    vtex_path = game_path.parent / 'bin' / 'vtex.exe'
    print(str(vtex_path))
    if not vtex_path.is_file():
        # self.report({'WARNING'}, 'Game path invalid, go kys, fucker: Unable to locate vtex.exe')
        except_raiser()



    # important todo: XY size enum
    sky_dimx = sk_settings.size_x
    sky_dimy = sk_settings.size_y


    # Check the destination folder condition: If exists, but overwrite is False - stop and throw error
    dest_folder = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name

    if dest_folder.is_file() and sk_settings.overwrite_shit == False:
        # self.report({'WARNING'}, 'The specified path exists, but overwrite checkbox is tunred off')
        except_raiser()
    else:
        try:
            shutil.rmtree(dest_folder)
        except OSError as e:
            print('Error: %s : %s' % (dest_folder, e.strerror))


    # Run cleanup just in case :
    # important todo: redo this
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
        shutil.rmtree(str(dest_folder))
    except:
        print('materialsrc folder does not exist alr')

    # Overengineering shit again ?!
    destinations = [
        sk_settings.sky_name + '_exr_src',
        sk_settings.sky_name + '_generated_pfm',
        sk_settings.sky_name + '_tga_src'
    ]
    for ds in destinations:
        os.makedirs(str(dest_folder / ds))


    # Save scene settings
    # todo: some stuff is missing
    tgt_scene['blfoil_skyboxer_settings_save'] = {
        # Dimensions
        'res_x': tgt_scene.render.resolution_x,
        'res_y': tgt_scene.render.resolution_y,
        'res_perc': tgt_scene.render.resolution_percentage,
        
        'aspectx': tgt_scene.render.pixel_aspect_x,
        'aspecty': tgt_scene.render.pixel_aspect_y,
        
        'render_region': tgt_scene.render.use_border,
        
        # Output mode
        'render_filepath': tgt_scene.render.filepath,
        'use_file_extension': tgt_scene.render.use_file_extension,
        'use_render_cache': tgt_scene.render.use_render_cache,
        'file_format': tgt_scene.render.image_settings.file_format,
        'color_mode': tgt_scene.render.image_settings.color_mode,
        'use_overwrite': tgt_scene.render.use_overwrite,
        'use_placeholder': tgt_scene.render.use_placeholder,
        'img_color_depth': tgt_scene.render.image_settings.color_depth,
        'exr_codec': tgt_scene.render.image_settings.exr_codec,
        'use_zbuffer': tgt_scene.render.image_settings.use_zbuffer,
        'use_preview': tgt_scene.render.image_settings.use_preview,
        'use_compositing': tgt_scene.render.use_compositing,
        'use_sequencer': tgt_scene.render.use_sequencer,
        'dither_intensity': tgt_scene.render.dither_intensity
        # TODO: MAKE OLD CAMERA ACTIE AGAIN
    }

    # sidez = ['bk:90:0:-90', 'dn:0:0:-180', 'ft:90:0:90', 'lf:90:0:0', 'rt:90:0:-180', 'up:180:0:180']
    sidez = {
        'bk': (90, 0, -90),
        'dn': (0, 0, -180),
        'ft': (90, 0, 90),
        'lf': (90, 0, 0),
        'rt': (90, 0, -180),
        'up': (180, 0, 180)
    }

    # create camera
    sky_camera_data = bpy.data.cameras.new(name='blfoil_skybox_maker_camera_data')
    
    sky_camera_data.type = 'PERSP'
    sky_camera_data.clip_end = 100000.0
    
    # Sweet magic numbers
    sky_camera_data.lens = 64
    sky_camera_data.sensor_width = 128.5
    
    sky_camera_object = bpy.data.objects.new('blfoil_skybox_maker_camera', sky_camera_data)
    tgt_scene.collection.objects.link(sky_camera_object)

    # make this camera active
    tgt_scene.camera = sky_camera_object


    # Render each side into .exr
    for side in sidez:

        csidex = sidez[side][0]
        csidey = sidez[side][1]
        csidez = sidez[side][2]

        sky_camera_object.rotation_euler[0] = math.radians(csidex)
        sky_camera_object.rotation_euler[1] = math.radians(csidey)
        sky_camera_object.rotation_euler[2] = math.radians(csidez)

        # Setup render settings


        # Set render size

        tgt_scene.render.resolution_x = sky_dimx
        tgt_scene.render.resolution_y = sky_dimy

        if sk_settings.nobottom == True and side == 'dn':
            tgt_scene.render.resolution_x = 8
            tgt_scene.render.resolution_y = 8



        # adjust camera if half the size
        if sky_dimy == sky_dimx / 2:
            print('blfoil sky: dimy = dimx/2 (Skybox side is a rectangle)')

            # up and down are always square
            if side == 'dn' or side == 'up':

                sky_camera_data.shift_y = 0
                sky_camera_data.shift_x = 0
                tgt_scene.render.resolution_x = sky_dimx
                tgt_scene.render.resolution_y = sky_dimx
                # print('triggered dn or up side = ' + side + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))
            else:
                sky_camera_data.shift_y = 0.25
                sky_camera_data.shift_x = 0
                tgt_scene.render.resolution_x = sky_dimx
                tgt_scene.render.resolution_y = sky_dimy
                # print('triggered else side = ' + side + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))

            # If sides are rectangular - there could be no bottom
            if side == 'dn':
                tgt_scene.render.resolution_x = 8
                tgt_scene.render.resolution_y = 8
                # print('triggered dn side = ' + side + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))
 
        
        # print('final side = ' + side + ' set to ' + str(bpy.context.scene.render.resolution_y) + ' ' + str(bpy.context.scene.render.resolution_x))

        

        # set output dir per side
        if sk_settings.hdrldr == 'HDR':
            filepathed = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_exr_src') / (sk_settings.sky_name + side + '.exr')
        else:
            # todo: the name "generated_pfms" is also used for LDR src files
            filepathed = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + side + '.tga')
        
        
        tgt_scene.render.filepath = str(filepathed)
        
        # set output prefs
        if sk_settings.hdrldr == 'HDR':
            tgt_scene.render.image_settings.file_format = 'OPEN_EXR'
            tgt_scene.render.image_settings.color_mode = 'RGB'
            tgt_scene.render.image_settings.color_depth = '32'
            tgt_scene.render.image_settings.exr_codec = 'ZIP'
            tgt_scene.render.image_settings.use_zbuffer = False
            tgt_scene.render.image_settings.use_preview = False
        else:
            tgt_scene.render.image_settings.file_format = 'TARGA_RAW'
            tgt_scene.render.image_settings.color_mode = 'RGB'
            
        tgt_scene.render.use_file_extension = True
        tgt_scene.render.use_render_cache = False
        tgt_scene.render.use_overwrite = True
        tgt_scene.render.use_placeholder = False


        # set sequencer to false and dither to 1
        tgt_scene.render.use_sequencer = False
        tgt_scene.render.use_compositing = True
        tgt_scene.render.dither_intensity = 1.0


        # Render
        bpy.ops.render.render(write_still = 1)
        
        
        # if HDR then we need stupid LDR fallbacks
        # fuck them really - downscale them fuckers by a factor of fucking 2
        # todo: finally predefine scene resolution x. or nah ?
        # important todo: DOUBLE RENDER IS HAPPENING. Use imagemagick to convert existing .exr to tga shit
        if sk_settings.hdrldr == 'HDR':
            tgt_scene.render.image_settings.file_format = 'TARGA_RAW'
            tgt_scene.render.image_settings.color_mode = 'RGB'
            tgt_scene.render.filepath = str(game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga'))
            tgt_scene.render.resolution_x = int(tgt_scene.render.resolution_x / 2)
            tgt_scene.render.resolution_y = int(tgt_scene.render.resolution_y / 2)
            bpy.ops.render.render(write_still = 1)

            
            magix_prms = [
                str(magix),
                str(game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga')),
                str(addon_root_dir / 'app' / 'src' / 'tot' / (sk_settings.sky_name + side + '.png'))
            ]

            subprocess.call(magix_prms)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(appgui_updater(magix_prms[2], side))
            
            # appgui_updater(magix_prms)


    # Remove camera once done rendering
    bpy.data.objects.remove(sky_camera_object)

    # Make some paths for later use
    vtex_exe = game_path.parent / 'bin' / 'vtex.exe'
    vtex_outdir = game_path / 'materials' / 'skybox' / sk_settings.sky_name


    #
    # create pfms and text files for vtex.exe
    #

    try:
        shutil.rmtree(vtex_outdir)
    except:
        print('no vtf path alr')
    
    
    for tside in sidez:
        
        # construct pfm output
        # todo: shorten game_path / 'materialsrc' / 'skybox' /
        # or even
        # game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / sk_settings.sky_name
        pfmoutpath = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + '_hdr' + tside + '.pfm')
    
        # construct exr inp path
        exrinpath = game_path / 'materialsrc'/  'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_exr_src') / (sk_settings.sky_name + tside + '.exr')
    
        # path to imgmagick
        
        print(magix)
        if sk_settings.hdrldr == 'HDR':
            # convert with image magick 
            magic_args = [str(magix), exrinpath, '-endian', 'LSB', pfmoutpath]
            subprocess.call(magic_args)
        
        
        
        # write text file

        # important todo: Portal 2 cannot have ignorez 1
        
        text_file_content = [
            'nolod 1',
            'nomip 1',
            'nonice 1'
        ]

        vmt_content = [
            '"sky"',
            '{',
            '',
            '}'
        ]

        ldr_tga_txt = [
            'nolod 1',
            'clamps 1',
            'clampt 1',
            'nomip 1',
            'nonice 1',
            'nocompress 1'
        ]

        # construct text file path and text file
        if sk_settings.hdrldr == 'HDR':
            txtfile_path = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + '_hdr' + tside + '.txt')
            text_file_content.insert(0, 'pfm 1')
            text_file_content.insert(-1, 'pfmscale 1')
            if sk_settings.hdr_compressed == False:
                text_file_content.insert(-1, 'nocompress 1')
        else:
            txtfile_path = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + tside + '.txt')
            text_file_content.insert(-1, 'nocompress 1')

        if sky_dimy == sky_dimx / 2 and tside != 'up' and tside != 'dn':
            text_file_content.insert(-1, 'clamps 1')
            text_file_content.insert(-1, 'clampt 1')


        with open(str(txtfile_path), 'w') as txtfile:
            txtfile.write('\n'.join(text_file_content))


        # write ldr fallbacks
        # important todo: wtf
        with open(str(txtfile_path).replace('_generated_pfm', '_tga_src').replace('_hdr', ''), 'w') as txtfile:
            txtfile.write('\n'.join(ldr_tga_txt))



        # convert to vtf
        # maybe separate this into a separate for loop?
        vtex_args = [str(vtex_exe), '-nopause', '-outdir', vtex_outdir, txtfile_path]
        subprocess.call(vtex_args)
        
        
        # convert ldr vtf
        vtex_args = [str(vtex_exe), '-nopause', '-outdir', vtex_outdir, str(txtfile_path).replace('_generated_pfm', '_tga_src').replace('_hdr', '')]
        subprocess.call(vtex_args)
        
        # Relative path to .vmt
        ldrbasepath = str(Path('skybox') / sk_settings.sky_name / (sk_settings.sky_name + tside))


        # Create VMT

        # is it HDR?
        if sk_settings.hdrldr == 'HDR':
            # If so - .vmt has to have _hdr in its name
            vmtfile_path = game_path / 'materials' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_hdr' + tside + '.vmt')
            # and meaning that .vtf has _hdr too. Make vmt point to _hdr .vtf
            hdrbasepath = str(Path('skybox') / sk_settings.sky_name / (sk_settings.sky_name + '_hdr' + tside))
            
            # Is it compressed 8 bit HDR?
            if sk_settings.hdr_compressed == False:
                vmt_content.insert(-1,'    "$hdrbasetexture" "' + hdrbasepath + '"')
            else:
                vmt_content.insert(-1,'    "$hdrcompressedtexture" "' + hdrbasepath + '"')
            
            # There's always an LDR fallback
            vmt_content.insert(-1,'    "$basetexture" "' + ldrbasepath + '"')

        else:
            vmtfile_path = game_path / 'materials' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + tside + '.vmt')
            vmt_content.insert(-1,'    "$basetexture" "' + ldrbasepath + '"')

        if sky_dimy == sky_dimx / 2 and tside != 'up' and tside != 'dn':
            vmt_content.insert(-1,'   "$basetexturetransform" "center 0 0 scale 1 2 rotate 0 translate 0 0"')


        with open(str(vmtfile_path), 'w') as vmtfile:
            vmtfile.write('\n'.join(vmt_content))















# =========================================================
# ---------------------------------------------------------
#                       Operators
# ---------------------------------------------------------
# =========================================================

# Full skybox export

class OBJECT_OT_blfoil_full_skybox_export(Operator, AddObjectHelper):

    bl_idname = 'mesh.blfoil_full_skybox_export'
    bl_label = 'Compile skybox'
    # bl_options = {'REGISTER'}
    
    def execute(self, context):

        blfoil_skybox_maker(context.scene)

        return {'FINISHED'}





















# =========================================================
# ---------------------------------------------------------
#                       Classes
# ---------------------------------------------------------
# =========================================================


# 
# Dedicated and shared params, like brush material and special entity config, like light/light_spot properties 
#

class blfoil_skyboxer_settings(PropertyGroup):


    # -----------------------------------
    #              Skyboxer
    # -----------------------------------
    game_path : StringProperty(
        name='Path to the game dir. half-life 2/ep2',
        description='Has to point to a valid source engine game setup. half-life 2/ep2, where half-life 2/bin contains stuff like vtex.exe',
        default = 'blfoil_game_path - nil',
        subtype='DIR_PATH'
        )
        
    use_sourceops_gpath: BoolProperty(
        name='Use SourceOps game path',
        description='My dick so big so really big, black holes move towards my huge dick',
        default = False 
        )
        
    sky_name : StringProperty(
        name='The name of the baked skybox',
        description='doctor sex',
        default = 'blfoil_sky_boxname - nil'
        )
        
    size_x : IntProperty(
        name='Skybox X size',
        description='Size of each skybox square on X axis',
        default=1024,
        min=8,
        max=8192,
        soft_max=4096,
        soft_min=128,
        subtype='UNSIGNED'
        )
        
    size_y : IntProperty(
        name='Skybox X size',
        description='Size of each skybox square on X axis',
        default=1024,
        min=8,
        max=8192,
        soft_max=4096,
        soft_min=128,
        subtype='UNSIGNED'
        )

    keep_src_f_exr : BoolProperty(
        name='Whether to keep the src exr files or not',
        description='Disabling this will result into .exr files being deleted',
        default = True
        )
        
    keep_src_f_pfm : BoolProperty(
        name='Whether to keep the src .pfm files or not',
        description='Disabling this will result into .pfm files being deleted',
        default = True
        )
        
    moveto_afterb_path : StringProperty(
        name='Copy compiled stuff here',
        description='Should point to the "materials" folder. Will write to materials/skybox if present and overwrite any existing stuff. This description is redundant',
        default = 'nil',
        subtype='FILE_PATH'
        )
        
    moveto_afterb_movecopy : BoolProperty(
        name='asddw',
        description='Move. Otherwise - copy',
        default = False
        )
        
    hdrldr : EnumProperty(
        items=[
        ('HDR', 'HDR', 'ded2'),
        ('LDR', 'LDR', 'ded2')
        ],
        name='ldr/hdr',
        description='I want to kiss a lizard'
        # default = "nil"
        )
        
    hdr_compressed : BoolProperty(
        name='Compress into 8 bit + alpha',
        # description='Compress the shit like juicy tits',
        description='Lmfao are you serious? Your shit will look rubbish af',
        default = False
        )
        
    projectonly : BoolProperty(
        name='Simple projection',
        description='If set - seimply project whatever is plugged into the world on a cube, avoiding any renders',
        default = False
        )
        
    overwrite_shit : BoolProperty(
        name='Overwrite',
        description='oral',
        default = False 
        )

    nobottom : BoolProperty(
        name='No bottom',
        description='Destroy his ass',
        default = False 
        )
        
    mkenvmap : BoolProperty(
        name='Make envmap',
        description='Pootis',
        default = False 
        )
        
    mkenvmap_only : BoolProperty(
        name='Only envmap',
        description='Pootis',
        default = False 
        )















# =========================================================
# ---------------------------------------------------------
#                          GUI
# ---------------------------------------------------------
# =========================================================

# classes too, but specifically for gui
# and functions too





class VIEW3D_PT_blfoil_skyboxer(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lizards'
    bl_label = 'Sugarplum Gaben'
    # https://youtu.be/sT3joXENOb0

    def draw(self, context):
        layout = self.layout

        sk_settings = context.scene.blfoil_skyboxer_settings


        general_col = layout.column(align=False)
        general_col.label(text='Skybox exporter')
        
        usesrcops = general_col.row()
        # todo: maybe make it disappear if not sourceops? make it disabled if no items in source ops?
        usesrcops.prop(sk_settings, 'use_sourceops_gpath', text='Use SourceOps game path')
        if hasattr(context.scene, 'sourceops'):
            usesrcops.enabled = True
        else:
            usesrcops.enabled = False
        general_col.prop(sk_settings, 'game_path', text='Game path')
        general_col.prop(sk_settings, 'sky_name', text='Skybox name')
        
        
        dimensions_col = layout.column(align=True)
        dimensions_col.use_property_split = True
        dimensions_col.use_property_decorate = False
        
        dimensions_col.prop(sk_settings, 'size_x')
        dimensions_col.prop(sk_settings, 'size_y', text='Skybox Y size')
        
        
        dimensions_col.prop(sk_settings, 'nobottom', text='No bottom')


        leave_src_files = layout.column(align=False)
        if sk_settings.hdrldr == 'HDR': 
            leave_src_files.prop(sk_settings, 'keep_src_f_exr', text='Keep .exr src files')
            leave_src_files.prop(sk_settings, 'keep_src_f_pfm', text='Keep .pfm src files')
        else:
            leave_src_files.prop(sk_settings, 'keep_src_f_exr', text='Keep .tga src files')
            dim_exrsrc = leave_src_files.row()
            dim_exrsrc.enabled = False
            dim_exrsrc.prop(sk_settings, 'keep_src_f_pfm', text='Keep .pfm src files')
            
            
        
        move_vtf_here = layout.column(align=False)
        leave_src_files.prop(sk_settings, 'moveto_afterb_path', text='Move/Copy')
        leave_src_files.prop(sk_settings, 'moveto_afterb_movecopy', text='Move')
        
        mkenvmap_r = layout.column(align=False)
        mkenvmap_r.prop(sk_settings, 'mkenvmap', text='Make envmap')
        
        envmaponlyrow = mkenvmap_r.row()
        if sk_settings.mkenvmap == True:
            envmaponlyrow.enabled = True
        else:
            envmaponlyrow.enabled = False
        envmaponlyrow.prop(sk_settings, 'mkenvmap_only', text='Envmap only')
        
        
        hdrldr = layout.column(align=False)
        hdrldr_switch = hdrldr.row()
        hdrldr_switch.prop(sk_settings, 'hdrldr', expand=True)
        
        compr_sw = hdrldr.row()
        compr_sw.prop(sk_settings, 'hdr_compressed', text='Compressed 8 bit HDR (make it look rubbish)')
        
        # maybe make it appear and disappear ??
        if sk_settings.hdrldr == 'LDR':
            compr_sw.enabled = False
        else:
            compr_sw.enabled = True
        
        overwrite_sh = layout.column(align=False)
        # overwrite_sh.prop(context.scene.blfoil, 'blfoil_sky_projectonly', text='Project only')
        overwrite_sh.prop(sk_settings, 'overwrite_shit', text='Overwrite')

        mabaker_op = layout.column(align=False)
        self.layout.operator('mesh.blfoil_full_skybox_export',
            text='Compile skybox'
        )







