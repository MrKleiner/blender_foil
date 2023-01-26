"""
The license for this rubbish is super simple:
I'd like to see if there's ONE person on earth who would understand this garbage code.
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
	'warning': 'Fuck 3Dmax. RIP Softimage XSI, you will not be forgotten. Praise Maya',
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

import socket, threading, bpy, ctypes, time, atexit, sys
from bpy.app.handlers import persistent


from .mods.vmf_export.vmf_exporter import *
from .mods.skyboxer.skybox_maker import *
from .installer import blfoil_check_pypackages

from time import sleep
from .utils.shared import app_command_send
from .mods.app.modmaker.app_modmaker import *
from .blfoil_appconnect import *
from pathlib import Path

global engine_ref, addon_root
engine_ref = None
addon_root = Path(__file__).parent


# Yes, this room only accepts stuff and doesn't respond with the result within the same connection
# And response is sent as if it was a random command from blender
# It's made this way, because Blender, because of how the custom await system is made in the Foil App
# And it'd be more consistent to send the response that way and not inside the room
def blfoil_socket_room(con, addr):
	print('[blfoil] Room', addr, 'spawned, start listening')

	room_buffer = b''

	# Try is here, because an exception is raised when client closes the connection
	try:
		while True:
			# Try receiving data from the client
			# todo: What's the best amount of bytes to receive at once?
			# todo: It's speculated that 65535 (65kb) is a solid and reliable amount of data to read at once
			data = con.recv(10)
			# If something was received - append to buffer
			if data:
				room_buffer += data
			else:
				print('[blfoil] Empty data from', addr, 'was received, closing connection, proceeding to task evaluation (malfunction?)')
				break

			# important todo: Apparently, not responding to client AFTER EACH READ breaks shit?!
			# PROBABLY the issue is as follows: The socket is closed by the client and not Blender
			# and Blender keeps waiting for new data to come from the client and not closing the connection
			# important todo: YES, this is the issue... and it's literally fatal...
			# Boundaries/content lengths have to be introduced...
			con.send('Thank you for connecting'.encode())
	except Exception as e:
		print('[blfoil]', addr, 'Has closed the connection. Proceeding to task evaluation')

	# Important todo: Additionally, not responding to client after the data read was complete
	# BREAKS SHIT TOO ???
	# todo: This is still a mystery...
	# The loop issue is pretty obvious, but this...
	con.send('Thank you for connecting'.encode())

	# Try evaluating the task
	try:
		appconnect_actions(json.loads(room_buffer))
		print('[blfoil] Evaluated task from', addr)
	except Exception as e:
		print('[blfoil] There was an error while evaluating the task from', addr, str(e))

	print('[blfoil] Room', addr, 'Collapsed')

	# Close the connection
	# important todo: closing the connection before evaluation results into shit breaking
	con.close()


# Listen server for incoming commands
def blfoil_socket_listener():
	# Create the socket object
	socket_server = socket.socket()
	# Bind server to the specified port. 0 = Find the closest free port automatically
	socket_server.bind(('localhost', 0))
	# Basically launch the server
	# The number passed to this function identifies the max amount of simultaneous connections
	# If the amount of connections exceeds this limit - connections become rejected till other ones are resolved (aka closed)
	# 0 = infinite
	# todo: does 0 really mean infinite?
	# todo: What's the best way of making sure that there aren't too many ongoing connections?
	socket_server.listen(1024)
	assigned_port = socket_server.getsockname()[1]
	print('[blfoil] Launched blfoil listener on', assigned_port)

	# Write assigned port to file so that js could read it later
	(addon_root / 'bdsmbind.sex').write_text(str(assigned_port))

	# Enter the main loop
	while True:
		print('[blfoil] awaiting incoming connections...')
		# Try establishing connection, nothing below this line would get executed
		# until server receives a new connection
		conn, address = socket_server.accept()
		print('[blfoil] Got connection, spawning a room. Client info:', address)
		# Once connection was established - spawn a new room
		threading.Thread(target=blfoil_socket_room, args=(conn, address)).start()
		print('[blfoil] Spawned a room, continue accepting new connections')



# do listen
blender_foil_appgui_thread = threading.Thread(target=blfoil_socket_listener, daemon=True)
blender_foil_appgui_thread.start()

# now - check libraries
# it does it on every startup, but it should never take too long even when installing.
# the drive the Blender is installed on should be responsive enough by the time this script is called...
# therefore, checking paths for existance shouldnt take too long
blfoil_check_pypackages()


# super fucking important todo: make it possible to add new menu entries via app gui
# so that you can add weapon entities for your mod
# update: It's dynamically generated from the linked library file



# important todo: Marmoset Toolbag

# todo: Discord reaction images indexer

# important todo: Substance plugin

# important todo: blender image datablock exporter
# downscaled jpegs could be used for previews

# important todo: lights.rad

# important todo: game settings editor outside the engine

# important todo: h++ installer for gmod

# important todo: .pop files for tf2 mvm waves

# important todo: vbsp/vvis switcher

# important todo: js skybox preview from MR. X
	# update: Done

# important todo: propdata maker and other scripts

# important todo: audio waveform generation is easy

# important todo: Easy phong constructor for non-pbr source

# important todo: library maker: unpack vpks, convert mdl to smd, import as asset

# important todo: skybox namer changer. On name change - try to replace all occurances in vmfs

# important todo: Image magick can most likely output data into std

# important todo: would it make any sense for the HDR skybox name to have no _hdr and LDR have no _ldr ?
	# Update: No

# IMPORTANT TODO: easy baker with cool GUI + specificaly for source: bake these to this, to this image and ...

# important todo: Displacement filters!
# custom ones are probably possible

# smart exporter: Soundscape Volume: Create soundscape trigger and soundscape entity from soundscape model

# subprocess.Popen([r'C:\custom\blender_def_otput\bik\ffs.cmd'])
# cd "C:\custom\blender_def_otput\bik"
# radvideo64.exe" bink ... /v100 /d90 /m3.0 /o /l0 /p16 /#

"""
p = subprocess.Popen(cmd)
p.kill()
"""


# mapbase 
# https://www.moddb.com/mods/mapbase/downloads

# visual waves
# https://wavesurfer-js.org/

# wallworm4blender/waveforma/audiowaveform-win64/wv.html

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


	# A tiny list of suggested dev materials
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

