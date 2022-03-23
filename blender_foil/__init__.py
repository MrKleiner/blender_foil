bl_info = {
    'name': 'Blener Foil',
    'author': 'MrKleiner',
    'version': (1, 17),
    'blender': (3, 1, 0),
    'location': '3D Viewport > N menu. Image/UV Editor > N menu',
    'description': 'Aluminium Foil. A set of tools for work with SoS Engeene',
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
                print('Server received', data)

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
blfoil_check_pypackages()

# build_ent_en = threading.Thread(target=r_enum_listd, daemon=True)
# build_ent_en.start()
# sleep(5)


# super fucking important todo: make it possible to add new menu entries via app gui
# so that you can add weapon entities for your mod


# important todo: bd script



"""

class pootis_lol(bpy.types.Operator):

    bl_idname = "blfoil.bhuruthed"
    bl_label = "Observer"
    # socketCount = 0

    def execute(self, context):

        def server_one():
            port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
            s = socket.socket()  # Create a socket object
            host = ""  # Get local machine name
            s.bind(('localhost', port))  # Bind to the port
            s.listen(5)  # Now wait for client connection.

            print('Server listening....')

            x = 0

            while True:
                conn, address = s.accept()  # Establish connection with client.

                while True:
                    try:
                        print('Got connection from', address)
                        data = conn.recv(1024)
                        print('Server 1 received', data)

                        st = 'Thank you for connecting'
                        byt = st.encode()
                        conn.send(byt)

                        x += 1

                    except Exception as e:
                        print(e)
                        print('all good')
                        break

            conn.close()

        s_one = threading.Thread(target=server_one)

        s_one.start()



@persistent
def blfoil_plugin(scene):
    try:
        bpy.ops.blfoil.listen()
    except Exception as e:
        print( "Bridge Plugin Error::Could not start the plugin. Description: ", str(e) )
"""


"""
def register():
    # register_()
    bpy.utils.register_class(pootis_lol)
    # bpy.types.Scene.blfoilvtf = PointerProperty(type=blender_foil_vtf)


def unregister():
    # unregister_()
    bpy.utils.unregister_class(pootis_lol)
    # bpy.utils.unregister_class(blfoilvtf)
"""









# =======================================================
#                       Register
# =======================================================

# register things

rclasses = (
    blender_ents,
    VIEW3D_PT_blender_foil_dn_enum,
    OBJECT_OT_foil_add_ham_entity,
    OBJECT_OT_foil_test_export,
    blender_ents_obj,
    hammer_ents_w_icons,
    OBJECT_OT_foil_add_hwm_ent,
    blfoil_etype_selector_list_prp_col,
    blfoil_etype_selector_panel_itemdraw
)

register_, unregister_ = bpy.utils.register_classes_factory(rclasses)

@persistent
def load_handler(dummy):
    # print("Load Handler:", bpy.data.filepath)

    # stuff to execute after the blend file has been loaded

    # check and resync classnames
    blfoil_ent_classnames_list_builder()

    # get all icons n shit from the blend file
    blfoil_ents_supported_icons(hammer_icons_blend, supported_icons)



def register():
    register_()
    # bpy.utils.register_class(blender_ents)
    bpy.types.Scene.blents = PointerProperty(type=blender_ents)
    
    bpy.types.Object.ent_conf = PointerProperty(type=blender_ents_obj)
    
    bpy.types.VIEW3D_MT_add.append(draw_hwm_presets)
    
    # bpy.types.DATA_PT_modifiers.prepend(ffd_app)

    # bpy.types.Scene.prop_obj = PointerProperty(type=bpy.types.StringProperty)

    bpy.types.Scene.blfoil_etype_selector_list = CollectionProperty(type = blfoil_etype_selector_list_prp_col)
    bpy.types.Scene.blfoil_etype_selector_list_index = IntProperty(name = 'Entity type selector index', default = 0)
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    unregister_()
    # bpy.utils.unregister_class(blender_ents)
    del bpy.types.Scene.blents
    del bpy.types.Object.ent_conf
    
    bpy.types.VIEW3D_MT_light_add.remove(draw_hwm_presets)
    
    # bpy.types.DATA_PT_modifiers.remove(ffd_app)
