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
# import pathlib
from math import radians
from mathutils import Matrix

from ...utils.shared import eval_state, app_command_send, blfoil_file_cleanup

try:
    from bs4 import BeautifulSoup
    from bs4 import Tag, NavigableString
except:
    pass
import socket
import base64

from ...utils.lizard_scales.lizard_scales import lizard_scales
# get the current directory. Just in case
# todo: lmao parent.parent.parent
# replace it with parents[2]
addon_root_dir = Path(__file__).absolute().parent.parent.parent







# set back everything
def blfoil_skybox_cleanup(defdict, sce):
    tgt_scene = sce

    tgt_scene.render.resolution_x = defdict['res_x']
    tgt_scene.render.resolution_y = defdict['res_y']
    tgt_scene.render.resolution_percentage = defdict['res_perc']

    tgt_scene.render.pixel_aspect_x = defdict['aspectx']
    tgt_scene.render.pixel_aspect_y = defdict['aspecty']

    tgt_scene.render.use_border = defdict['render_region']

    # Colour management
    tgt_scene.display_settings.display_device = defdict['display_device']
    tgt_scene.view_settings.view_transform = defdict['view_transform']
    tgt_scene.view_settings.look = defdict['look']
    tgt_scene.view_settings.exposure = defdict['exposure']
    tgt_scene.view_settings.gamma = defdict['gamma']


    # Output mode
    tgt_scene.render.filepath = defdict['render_filepath']
    tgt_scene.render.use_file_extension = defdict['use_file_extension']
    tgt_scene.render.use_render_cache = defdict['use_render_cache']
    tgt_scene.render.image_settings.file_format = defdict['file_format']
    tgt_scene.render.image_settings.color_mode = defdict['color_mode']
    tgt_scene.render.use_overwrite = defdict['use_overwrite']
    tgt_scene.render.use_placeholder = defdict['use_placeholder']
    tgt_scene.render.image_settings.color_depth = defdict['img_color_depth']
    tgt_scene.render.image_settings.exr_codec = defdict['exr_codec']
    tgt_scene.render.image_settings.use_zbuffer = defdict['use_zbuffer']
    tgt_scene.render.image_settings.use_preview = defdict['use_preview']
    tgt_scene.render.use_compositing = defdict['use_compositing']
    tgt_scene.render.use_sequencer = defdict['use_sequencer']
    tgt_scene.render.dither_intensity = defdict['dither_intensity']

    tgt_scene.camera = defdict['camera']
















# =========================================================
# ---------------------------------------------------------
#                   Base functionality
# ---------------------------------------------------------
# =========================================================



def blfoil_skybox_maker(tgt_scene):

    # exception raiser
    def except_raiser(details=''):
        # self.report({'WARNING'}, 'Game path invalid, go kys, fucker: Unable to locate vtex.exe')
        raise Exception('Somethings very wrong: ' + str(details))


    # Skybox settings
    sk_settings = tgt_scene.blfoil_skyboxer_settings

    # Absolute path to the current blend file
    this_blend = bpy.path.abspath('//')

    # Path to magick.exe image converter
    magix = addon_root_dir / 'bins' / 'imgmagick' / 'magick.exe'


    # Check if game path exists. If not - stop script execution and throw a warning
    # but first - check if we use SourceOps Game path and if SourceOps is available at all
    # check if we use source ops
    # todo: YES, "try:" allows to go straight to the point istead of checking every part of the chain
    # All that matters is if there's a valid game or not, the presence or abscense of SourceOps doesn't say anything 
    if sk_settings.use_sourceops_gpath == True:
        try:
            sky_foil_gpath = tgt_scene.sourceops.game_items[tgt_scene.sourceops.game_index]['game']
        except:
            except_raiser('It was requested to use SourceOps game path, but SourceOps could not be located OR game is invalid')
    else:
        sky_foil_gpath = bpy.path.abspath(sk_settings.game_path)

    # Path to 'Half-Life 2/ep2'
    game_path = Path(bpy.path.abspath(sky_foil_gpath))

    # vtex has to be present. Else - can't do shit
    vtex_path = game_path.parent / 'bin' / 'vtex.exe'
    print(str(vtex_path))
    if not vtex_path.is_file():
        except_raiser('Game path invalid, go kys: Unable to locate vtex.exe')


    sky_is_rect = sk_settings.halfsize

    sky_dimx = int(sk_settings.size)
    sky_dimy = int(sky_dimx / 2 if sky_is_rect else None or sky_dimx)


    # Check the destination folder condition: If exists, but overwrite is False - stop and throw error
    dest_folder = game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name

    if dest_folder.is_dir() and sk_settings.overwrite_shit == False:
        except_raiser('Skybox destination folder exists, but overwrite is set to False')


    # delete materialsrc dir if any
    shutil.rmtree(str(dest_folder), ignore_errors=True)


    # Overengineering shit again ?!
    destinations = [
        sk_settings.sky_name + '_exr_src',
        sk_settings.sky_name + '_generated_pfm',
        sk_settings.sky_name + '_tga_src'
    ]
    for ds in destinations:
        (dest_folder / ds).mkdir(parents=True, exist_ok=True)


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

        # Colour management
        'display_device': tgt_scene.display_settings.display_device,
        'view_transform': tgt_scene.view_settings.view_transform,
        'look': tgt_scene.view_settings.look,
        'exposure': tgt_scene.view_settings.exposure,
        'gamma': tgt_scene.view_settings.gamma,

        
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
        'dither_intensity': tgt_scene.render.dither_intensity,
        
        'camera': tgt_scene.camera
    }

    # sidez = ['bk:90:0:-90', 'dn:0:0:-180', 'ft:90:0:90', 'lf:90:0:0', 'rt:90:0:-180', 'up:180:0:180']
    """
    sidez = {
        'bk': (90, 0, -90),
        'dn': (0, 0, -180),
        'ft': (90, 0, 90),
        'lf': (90, 0, 0),
        'rt': (90, 0, -180),
        'up': (180, 0, 180)
    }
    """

    # sky_is_rect = sky_dimy == sky_dimx / 2
    # sky_is_rect = sk_settings.halfsize
    # sky_dim

    # important: if not square and NOT a proper rectangle - stop
    # firstly - Y cannot be bigger than x
    # secondly - if X Y are not the same, check if triangle is proper
    # if sky_dimy > sky_dimx or (sky_dimy != sky_dimx and not sky_is_rect):
    #     except_raiser('Invalid sky size setup!')
    # Update: Now it cannot be otherwise: There's a set of dimensions you can have on X axis 
    # and a checkbox whether to half it on Y or not

    # better order so that it looks cooler visually in app
    # (the sides are being rendered and processed in this order)
    sidez = {
        'ft': (90, 0, 90),
        'lf': (90, 0, 0),
        'bk': (90, 0, -90),
        'up': (180, 0, 180),
        'rt': (90, 0, -180),
        'dn': (0, 0, -180)
    }

    # size dict
    side_sizes = {
        'ft': (sky_dimx, sky_dimy),
        'lf': (sky_dimx, sky_dimy),
        'bk': (sky_dimx, sky_dimy),
        'up': (sky_dimx, sky_dimx),
        'rt': (sky_dimx, sky_dimy),
        # 8 if nobottom or side is a rect else - defaults
        'dn': (8 if sk_settings.nobottom or sky_is_rect else sky_dimx, 8 if sk_settings.nobottom or sky_is_rect else sky_dimx)
    }

    # cam shift dict
    camshift = {
        'ft': 0.25 if sky_is_rect else 0,
        'lf': 0.25 if sky_is_rect else 0,
        'bk': 0.25 if sky_is_rect else 0,
        'up': 0,
        'rt': 0.25 if sky_is_rect else 0,
        'dn': 0
    }

    # preview path dict
    # preview_paths = {
    #     'HDR': 
    # }



    # create camera
    sky_camera_data = bpy.data.cameras.new(name='blfoil_skybox_maker_camera_data')
    
    sky_camera_data.type = 'PERSP'
    sky_camera_data.clip_end = 100000.0
    
    # Magic numbers
    sky_camera_data.lens = 64
    sky_camera_data.sensor_width = 128.5
    
    sky_camera_object = bpy.data.objects.new('blfoil_skybox_maker_camera', sky_camera_data)
    tgt_scene.collection.objects.link(sky_camera_object)
    # mark for deleteion, just in case
    sky_camera_object['blfoil_cleanup_todelete'] = True

    # make this camera active
    tgt_scene.camera = sky_camera_object

    # Notify the app that blender renders are happening
    app_command_send({
        'app_module': 'skyboxer',
        'mod_action': 'upd_work_status',
        'status': 'Rendering sides in Blender...'
    })

    # Render each side into .exr OR .tga
    for side in sidez:

        # Set camera rotation
        csidex = sidez[side][0]
        csidey = sidez[side][1]
        csidez = sidez[side][2]

        sky_camera_object.rotation_euler[0] = math.radians(csidex)
        sky_camera_object.rotation_euler[1] = math.radians(csidey)
        sky_camera_object.rotation_euler[2] = math.radians(csidez)


        #
        # Setup camera and render settings
        #

        # render size
        tgt_scene.render.resolution_x = side_sizes[side][0]
        tgt_scene.render.resolution_y = side_sizes[side][1]

        # camera shift
        sky_camera_data.shift_y = camshift[side]
        sky_camera_data.shift_x = 0
        
        
        # set output prefs
        if sk_settings.hdrldr == 'HDR':
            tgt_scene.render.filepath = str(dest_folder / (sk_settings.sky_name + '_exr_src') / (sk_settings.sky_name + side + '.exr'))
            tgt_scene.render.image_settings.file_format = 'OPEN_EXR'
            tgt_scene.render.image_settings.color_mode = 'RGB'
            tgt_scene.render.image_settings.color_depth = '32'
            tgt_scene.render.image_settings.exr_codec = 'ZIP'
            tgt_scene.render.image_settings.use_zbuffer = False
            tgt_scene.render.image_settings.use_preview = False
        else:
            tgt_scene.render.filepath = str(dest_folder / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga'))
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


        # Do Render
        bpy.ops.render.render(write_still=1)
        
        

        # AFTER done rendering, check if HDR then we need stupid LDR fallbacks
        # fuck them really - downscale them fuckers by a factor of fucking 2
        # simply re-save it with blender
        # important todo: it seems like the image is not being downscaled when saving as render
        if sk_settings.hdrldr == 'HDR':

            # Set export settings to .png
            tgt_scene.render.image_settings.file_format = 'TARGA_RAW'
            tgt_scene.render.image_settings.color_mode = 'RGB'
            # tgt_scene.render.image_settings.compression = 15

            # half the resolution
            tgt_scene.render.resolution_x = int(tgt_scene.render.resolution_x / 2)
            tgt_scene.render.resolution_y = int(tgt_scene.render.resolution_y / 2)

            # set filepath
            # tgt_scene.render.filepath = str(game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga'))

            # load resulting .exr or
            apply_filmic = bpy.data.images.load(str(dest_folder / (sk_settings.sky_name + '_exr_src') / (sk_settings.sky_name + side + '.exr')))
            apply_filmic['blfoil_cleanup_todelete'] = True

            # export exr with filmic applied
            apply_filmic.save_render(str(dest_folder / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga')))

            # unlink rubbish
            bpy.data.images.remove(apply_filmic)


        # Use magick to convert tga to png (there's always a tga)
        # important todo: magick can output to stdout. Don't litter with temp files and send bytes right away
        # one advantage of temp files is that they can be accessed...
        (addon_root_dir / 'tot' / 'skyboxer').mkdir(parents=True, exist_ok=True)
        magix_prms = [
            str(magix),
            str(dest_folder / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + side + '.tga')),
            # str(addon_root_dir / 'app' / 'src' / 'tot' / (sk_settings.sky_name + side + '.png'))
            # important todo: So, what's the best place to write temp shit to ?
            str(addon_root_dir / 'tot' / 'skyboxer' / (sk_settings.sky_name + side + '.png'))
        ]
        # exec magick
        subprocess.call(magix_prms)
        # read resulting png to base64
        with open(str(magix_prms[2]), 'rb') as b6i:
            img_b64 = base64.b64encode(b6i.read()).decode('utf-8', errors='ignore')

        # Send image to app
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'add_skybox_side',
            'side': side,
            'image': img_b64
        })
        # send update that blender is green
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'upd_side_status',
            'side': side,
            'what': 'blender',
            'status': True
        })




    # Remove camera once done rendering
    bpy.data.objects.remove(sky_camera_object)


    # Make some paths for later use
    vtex_exe = game_path.parent / 'bin' / 'vtex.exe'
    vtex_outdir = game_path / 'materials' / 'skybox' / sk_settings.sky_name


    #
    # create pfms and text files for vtex.exe
    #

    # clean output directory
    shutil.rmtree(str(vtex_outdir), ignore_errors=True)


    # Notify app that VTF conversion is happening
    app_command_send({
        'app_module': 'skyboxer',
        'mod_action': 'upd_work_status',
        'status': 'Converting to VTF...'
    })


    for tside in sidez:
        
        # construct pfm output
        # todo: shorten game_path / 'materialsrc' / 'skybox' /
        # or even
        # game_path / 'materialsrc' / 'skybox' / sk_settings.sky_name / sk_settings.sky_name
        pfmoutpath = dest_folder / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + '_hdr' + tside + '.pfm')
    
        # construct exr inp path
        exrinpath = dest_folder / (sk_settings.sky_name + '_exr_src') / (sk_settings.sky_name + tside + '.exr')
    


        # Literally the heart of this exporter: Converting .exr to PROPER .pfms
        # -endian LSB !!!!!
        print(magix)
        if sk_settings.hdrldr == 'HDR':
            # convert with image magick 
            magic_args = [str(magix), exrinpath, '-endian', 'LSB', pfmoutpath]
            subprocess.call(magic_args)

        # Basically, this should be triggered regardless
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'upd_side_status',
            'side': tside,
            'what': 'pfm',
            'status': True
        })
            
        
        
        # write text file for vtex
        # todo: create a class for vtex manipulations
        # todo: create a class for imgmagick manips

        # important todo: Portal 2 cannot have ignorez 1
        
        # HDR
        # todo: this still lacks common sense
        # just move this inside if HDR ??
        text_file_content = [
            'nolod 1',
            'nomip 1',
            # important todo: wtf is actually nonice ???? What EXACTLY does it do ?
            'nonice 1' if sky_dimx > 256 else '',
            'pfm 1' if sk_settings.hdrldr == 'HDR' else '',
            'pfmscale 1' if sk_settings.hdrldr == 'HDR' else '',
            # Not specifying nocompress 1 automatically means that it will be compressed
            'nocompress 1' if sk_settings.hdrldr == 'HDR' and sk_settings.hdr_compressed == False else '',
            # Rectangle skyboxes should not repeat. Clamp
            'clamps 1' if sky_is_rect and tside != 'up' and tside != 'dn' else '',
            'clampt 1' if sky_is_rect and tside != 'up' and tside != 'dn' else ''
        ]

        # ' '.join(filter(None, strings))

        # vmt_content = [
        #     '"sky"',
        #     '{',
        #     '',
        #     '}'
        # ]

        

        # There are always targas
        # this is static for now
        # (till there's a noz 1 switch)
        ldr_tga_txt = [
            'nolod 1',
            'clamps 1',
            'clampt 1',
            'nomip 1',
            'nonice 1',
            'nocompress 1'
        ]

        vmtbasepath = Path('skybox') / sk_settings.sky_name / sk_settings.sky_name

        # Additional conversions if there's HDR
        if sk_settings.hdrldr == 'HDR':
            txtfile_path = dest_folder / (sk_settings.sky_name + '_generated_pfm') / (sk_settings.sky_name + '_hdr' + tside + '.txt')

            # Write the vtex text file for HDR
            with open(str(txtfile_path), 'w') as txtfile:
                # join in a specific way because there are empty entries
                txtfile.write('\n'.join(filter(None, text_file_content)))

            # convert HDR .pfm to .vtf
            vtex_args = [str(vtex_exe), '-nopause', '-outdir', vtex_outdir, txtfile_path]
            subprocess.call(vtex_args)

            # write VMT

            hdr_vmt = lizard_scales()
            # HDR skybox uses "sky" shader
            hdr_vmt.shader = 'sky'
            hdr_vmt.setparams({
                # LDR fallback
                'basetexture': str(vmtbasepath) + tside,
                # HDR shit
                'hdrcompressedtexture' if sk_settings.hdr_compressed else 'hdrbasetexture': str(vmtbasepath) + '_hdr' + tside,
                # transform. If sky is rectangular and if current side is not down or up
                'basetexturetransform': 'center 0 0 scale 1 2 rotate 0 translate 0 0' if sky_is_rect and tside != 'up' and tside != 'dn' else None 
            })

            # write resulting vmt
            with open(str(vtex_outdir / (sk_settings.sky_name + '_hdr' + tside + '.vmt')), 'w') as vmtfile:
                vmtfile.write(hdr_vmt.to_vmt())




        # write LDR (which should always be there)
        # basically, targas are always there
        txtfile_path = str(dest_folder / (sk_settings.sky_name + '_tga_src') / (sk_settings.sky_name + tside + '.txt'))
        with open(txtfile_path, 'w') as txtfile:
            txtfile.write('\n'.join(filter(None, ldr_tga_txt)))


        # convert Targas tp vtf
        vtex_args = [str(vtex_exe), '-nopause', '-outdir', vtex_outdir, txtfile_path]
        subprocess.call(vtex_args)


        # write LDR VMT

        ldr_vmt = lizard_scales()
        # LDR skies use UnlitGeneric
        ldr_vmt.shader = 'UnlitGeneric'
        ldr_vmt.setparams({
            'nofog': 1,
            # important todo: Portal 2 SHOULD NOT HAVE ignorez
            'ignorez': 1,
            'basetexture': str(vmtbasepath) + tside,
            # transform. If sky is rectangular and if current side is not down or up
            'basetexturetransform': 'center 0 0 scale 1 2 rotate 0 translate 0 0' if sky_is_rect and tside != 'up' and tside != 'dn' else None 
        })

        # write resulting vmt
        with open(str(vtex_outdir / (sk_settings.sky_name + tside + '.vmt')), 'w') as vmtfile:
            vmtfile.write(ldr_vmt.to_vmt())


        # Send status update to the gui app
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'upd_side_status',
            'side': tside,
            'what': 'vtf',
            'status': True
        })



















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
        # Reset skybox in-app
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'reset'
        })

        # Set sky name in-app
        app_command_send({
            'app_module': 'skyboxer',
            'mod_action': 'set_sky_name',
            'skyname': context.scene.blfoil_skyboxer_settings.sky_name
        })

        # Switch to skyboxer
        app_command_send({
            'app_module': 'load_skyboxer_app'
        })

        try:
            # Do export
            blfoil_skybox_maker(context.scene)
            # Revert settings back
            blfoil_skybox_cleanup(context.scene['blfoil_skyboxer_settings_save'], context.scene)
            del context.scene['blfoil_skyboxer_settings_save']

            # Notify the app that compiling is done
            app_command_send({
                'app_module': 'skyboxer',
                'mod_action': 'upd_work_status',
                'status': 'Finished. No errors'
            })

        except Exception as e:
            self.report({'WARNING'}, str(e))

            # Cleanup
            blfoil_file_cleanup()

            # Notify the app that compiling is failed
            app_command_send({
                'app_module': 'skyboxer',
                'mod_action': 'upd_work_status',
                'status': 'Error: ' + str(e)
            })


        # Cleanup the scene regardless
        blfoil_file_cleanup(flushtemp=True)

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
        
    """
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
    """

    size : EnumProperty(
        items=[
        ('8', '8', 'lmfao'),
        ('16', '16', 'wat ??'),
        ('32', '32', 'rly'),
        ('64', '64', 'why'),
        ('128', '128', 'Gaming on consoles be like'),
        ('256', '256', 'As small as your'),
        ('512', '512', 'rubbish'),
        ('1024', '1024', 'Ery noice'),
        ('2048', '2048', 'Giga Chad'),
        ('4096', '4096', """Doesn't work (I'm not kidding)""")
        ],
        name='sizes',
        description='Pro tip: panorama length / 4 = optimal sky square size',
        default = '2048'
        )

    halfsize : BoolProperty(
        name='Half The Size',
        description='Skybox Half Size',
        default = False
        )

    """
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
    """

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
        ('HDR', 'HDR', 'Giga Chad'),
        ('LDR', 'LDR', 'Rubbish')
        ],
        name='ldr/hdr'
        # description='I want to kiss a lizard'
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
        description='Welcom 2 Bottom Gear mates',
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
        
        # dimensions_col.prop(sk_settings, 'size_x')
        # dimensions_col.prop(sk_settings, 'size_x')
        dimensions_col.prop(sk_settings, 'size', text='Skybox size')
        dimensions_col.prop(sk_settings, 'halfsize', text='Half the size')
        
        
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







