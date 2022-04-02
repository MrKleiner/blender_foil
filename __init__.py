"""
The license for this rubbish is super simple:
I'd like to see if there's ONE person on earth who would understand this junk code.
Also, everything that is not mine is labeled as such.
ATTENTION: Thank you for your attention.
"""


bl_info = {
    'name': 'Blener Foil',
    'author': 'MrKleiner',
    'version': (1, 17),
    'blender': (3, 1, 0),
    'location': '3D Viewport > N menu. Image/UV Editor > N menu',
    'description': 'Aluminium Foil. A set of tools for work with SooS Engeene',
    'warning': 'Fuck 3Dmax. RIP Softimage XSI, you will not be forgotten',
    'doc_url': '',
    'category': '3D View',
}

"""
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
"""

import socket
import threading
import bpy
from bpy.app.handlers import persistent
import ctypes
import time
import atexit
import sys

from .mods.vmf_export.vmf_exporter import *
from .mods.skyboxer.skybox_maker import *
from .installer import blfoil_check_pypackages

from time import sleep

# The faster we start listening for shit - the better
# this is a port listener so that it's possible to connect an app with blender
def blender_foil_guiappconnect():
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ''  # Get local machine name
    s.bind(('localhost', port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    while True:
        conn, address = s.accept()  # Establish connection with client.
        while True:
            try:
                # get shit
                print('Got connection from', address)
                data = conn.recv(1024)
                if data != b'':
                    print('Server received', data)
                else:
                    print('Server received shit, but its fucking empty')
                # respond to the sender
                response = 'Thank you for connecting'
                byt = response.encode()
                conn.send(byt)

            except Exception as e:
                print(e)
                print('all good')
                break

    conn.close()

# do listen
blender_foil_appgui_thread = threading.Thread(target=blender_foil_guiappconnect, daemon=True)
blender_foil_appgui_thread.start()

# now - check libraries
# it does it on every startup, but it should never take too long even when installing
# the drive the Blender is installed on should be responsive enough by the time this script is called...
# therefore, checking paths for existance shouldnt take too long
blfoil_check_pypackages()

# build_ent_en = threading.Thread(target=r_enum_listd, daemon=True)
# build_ent_en.start()
# sleep(5)


# super fucking important todo: make it possible to add new menu entries via app gui
# so that you can add weapon entities for your mod
# update: It's dynamically generated from the linked library file


# important todo: bd script

# important todo: Marmoset Toolbag

# todo: Discord reaction images indexer

# important todo: Substance plugin


# =======================================================
#                       Register
# =======================================================

# register things

rclasses = (
    blender_ents,
    VIEW3D_PT_blender_foil_vmf_gui,
    OBJECT_OT_blfoil_set_obj_ent_class,
    OBJECT_OT_blfoil_vmf_export,
    blfoil_predefined_entity_prop_slots,
    hammer_ents_w_icons,
    OBJECT_OT_foil_add_hwm_ent,
    blfoil_etype_selector_list_prp_col,
    blfoil_etype_selector_panel_itemdraw,
    blfoil_ents_dedicated_params,
    VIEW3D_PT_blender_foil_brush_config_gui,
    blfoil_common_brush_materials,
    blfoil_common_brush_materials_item_draw,
    VIEW3D_PT_blfoil_brush_config_dev_texture_picker_menu,
    OBJECT_OT_blfoil_set_suggested_mat,
    OBJECT_OT_blfoil_mark_as_world_brush,
    VIEW3D_PT_blfoil_skyboxer,
    blfoil_skyboxer_settings,
    OBJECT_OT_blfoil_full_skybox_export
)

register_, unregister_ = bpy.utils.register_classes_factory(rclasses)

@persistent
def load_handler(dummy):
    # print("Load Handler:", bpy.data.filepath)

    # Stuff to execute after the blend file was loaded

    # Check and resync classnames
    blfoil_ent_classnames_list_builder()

    # Check and resync suggested materials
    blfoil_suggested_mats_builder()

    # Get all icons n shit from the blend file
    # Accessing and reading files is probably a costly operation. Avoid doing that at random points in time
    # do it on load
    blfoil_ents_supported_icons(hammer_icons_blend, supported_icons)


# How to create UIList:
# Create a class containing any amount of properties
# register bpy.types.Scene.WHATEVER_LIST = CollectionProperty(type=CLASS_WITH_PROPERTIES)
# and also register bpy.types.Scene.WHATEVER_LIST_INDEX = IntProperty(name='LIST_INDEX', default = 0)
# Then, create a class responsible for list item drawing
# After that - populate the thing with bpy.types.Scene.WHATEVER_LIST.add()
# Finally, 
# .template_list(
# 'DRAWING_CLASS', 
# '', 
# whatever was specified in bpy.types.Scene (context.scene), 
# 'WHATEVER_LIST(AS REGISTERED - NOT CLASS)', 
# context.scene, 
# 'WHATEVER_LIST_INDEX(AS REGISTERED - NOT CLASS)'
# )


def register():
    register_()
    # bpy.utils.register_class(blender_ents)


    # rubbish
    bpy.types.Scene.blents = PointerProperty(type=blender_ents)
    
    bpy.types.Object.ent_conf = PointerProperty(type=blfoil_predefined_entity_prop_slots)
    bpy.types.Object.blfoil_ent_specials = PointerProperty(type=blfoil_ents_dedicated_params)
    
    bpy.types.VIEW3D_MT_add.append(draw_hwm_presets)
    
    # bpy.types.DATA_PT_modifiers.prepend(ffd_app)

    # bpy.types.Scene.prop_obj = PointerProperty(type=bpy.types.StringProperty)


    # Huge list of all the supported entities
    bpy.types.Scene.blfoil_etype_selector_list = CollectionProperty(type=blfoil_etype_selector_list_prp_col)
    bpy.types.Scene.blfoil_etype_selector_list_index = IntProperty(name='Entity type selector index', default = 0)


    # A small list of suggested dev materials
    bpy.types.Scene.blfoil_common_brush_materials = CollectionProperty(type=blfoil_common_brush_materials)
    bpy.types.Scene.blfoil_common_brush_materials_index = IntProperty(name='Suggested materials index', default = 0)


    # Skyboxer settings
    bpy.types.Scene.blfoil_skyboxer_settings = PointerProperty(type=blfoil_skyboxer_settings)



    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    unregister_()
    # bpy.utils.unregister_class(blender_ents)
    del bpy.types.Scene.blents
    del bpy.types.Object.ent_conf
    del bpy.types.Object.blfoil_ent_specials
    
    bpy.types.VIEW3D_MT_light_add.remove(draw_hwm_presets)
    
    # bpy.types.DATA_PT_modifiers.remove(ffd_app)
