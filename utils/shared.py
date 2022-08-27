import asyncio
import socket
import json


# get md5 of a string.
# is not stepped, intended for use with small strings
def eval_m5(st):
	import hashlib
	text = str(st)
	hash_object = hashlib.md5(text.encode())
	md5_hash = hash_object.hexdigest()
	return md5_hash




# takes path to the file as an input
# is stepped. Can process huge files
# returns md5 string
def getfilemd5(filepath):
	import hashlib
	file = str(filepath) # Location of the file (can be set a different way)
	
	# The size of each read from the file
	# BLOCK_SIZE = 65535
	# 23 million
	# BLOCK_SIZE = 23000000
	# 167 million
	BLOCK_SIZE = 167856784
	
	# Create the hash object, can use something other than `.sha256()` if you wish
	# file_hash = hashlib.md5()
	file_hash = hashlib.md5()
	with open(file, 'rb') as f: # Open the file to read it's bytes
		fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		while len(fb) > 0: # While there is still data being read from the file
			file_hash.update(fb) # Update the hash
			fb = f.read(BLOCK_SIZE) # Read the next block from the file

	return(file_hash.hexdigest()) # Get the hexadecimal digest of the hash










# Returns True or False from either a string or int 1/0
def eval_state(state):

	# int to state
	if int(state) == 1:
		return True
	if int(state) == 0:
		return False


	# state to int
	if state == True:
		return 1
	if state == False:
		return 0


	# if state != False and state != True:
	#     return 0

	if int(state) != 1 and int(state) != 0:
		return False



# Returns Object transforms in a format of {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}
# Usage: call this function with an object
# eobject - object selector
# fix90 - 1 to fix the rotation (rotate an object either on Y or other axis)
# axis - axis to apply the rotation to: X, Y or Z
# RETURNS X Y Z
def get_obj_locrot_v1(eobject, fix90, axis, self, context):
	import bpy
	import mathutils
	from mathutils import Matrix
	import math
	
	# get scene scale
	if context.scene.unit_settings.system != 'NONE':
		sce_scale = bpy.context.scene.unit_settings.scale_length
	else:
		sce_scale = 1

	if str(axis).upper() in ['X', 'Y', 'Z', '-X', '-Y', '-Z', '+X', '+Y', '+Z']:
		fl_axis = str(axis).upper().replace('-', '').replace('+', '')
	else:
		fl_axis = 'Y'

	
	# if 'z' in str(axis).lower():
	#     fl_axis = 'Z'
	# else: 
	#     fl_axis = 'Y'

	if '-' in str(axis).lower():
		rfactor = -1
	else:
		rfactor = 1
	
	# hack pentagon
	if int(fix90) == 1:
		# eobject.rotation_euler.rotate_axis(fl_axis, math.radians(-90 * rfactor))
		# bpy.context.view_layer.update()
		
		# rotall = ((eobject.rotation_euler.to_matrix() @ Matrix.Rotation(math.radians(90 * rfactor), 3, 'Y')) @ eobject.matrix_world).to_euler()
		# These two lines is where magic happens
		rot_st = Matrix.Rotation(math.radians(90 * rfactor), 4, fl_axis)
		
		rotall = (eobject.matrix_world @ rot_st).to_euler()
		
		rotx = float(round(math.degrees(rotall[0]), 4))
		roty = float(round(math.degrees(rotall[1]), 4))
		rotz = float(round(math.degrees(rotall[2]), 4))
	else:
		rotx = float(round(math.degrees(eobject.matrix_world.to_euler()[0]), 4))
		roty = float(round(math.degrees(eobject.matrix_world.to_euler()[1]), 4))
		rotz = float(round(math.degrees(eobject.matrix_world.to_euler()[2]), 4))


	# extract locations
	locx = float(round(eobject.matrix_world[0][3], 4) * sce_scale)
	locy = float(round(eobject.matrix_world[1][3], 4) * sce_scale)
	locz = float(round(eobject.matrix_world[2][3], 4) * sce_scale)

	return {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}



# ==========================================
#               App bridge
# ==========================================

# this is CLIENT which SENDS data to javascript
# The server who's a listener is inside __init__

# todo: is async really needed ?
async def appgui_updater(pl):
	try:
		s = socket.socket()  # Create a socket object
		port = 1337  # Reserve a port for your service every new transfer wants a new port or you must wait.

		s.connect(('localhost', port))
		x = 0

		# test_shit = base64.b64encode(b_img).decode('utf-8', errors='ignore')

		"""
		payload = {
			'app_module': 'skyboxer',
			'mod_action': 'add_skybox_side',
			'side': side,
			'image': test_shit
		}
		"""

		st = json.dumps(pl)
		byt = st.encode()
		s.send(byt)
		# s.send(byt)

		print(x)

		collect_data = b''

		no_data_safety = 0

		while True:
			data = s.recv(1024)
			if data:
				print(data)
				collect_data += data
				x += 1
				break

			else:
				print('no data received')
				# important todo: this is an extremely retarded assumption
				# which is there because of the following issue:
				# sometimes it would just get stuck on 'no data received' forever
				# and just spam this message into the console...
				if no_data_safety == 4:
					print('Data Safety Triggered')
					break
				no_data_safety += 1


		print('Closing')
		print('Complete response:', collect_data)
		s.close()
	except Exception as e:
		print('Failed to initialize socket stuff (appgui_updater function failed to start)')
		return {'status': 'error', 'reason': e}


def app_command_send(payload):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	result = loop.run_until_complete(appgui_updater(payload))








# ==========================================
#               Cleanup
# ==========================================

def blfoil_file_cleanup(flushtemp=False, dmark='blfoil_cleanup_todelete'):
	import shutil
	import os
	from pathlib import Path
	import bpy
	
	addon_root_dir = Path(__file__).absolute().parent.parent
	# delete all images
	for cleanup in bpy.data.images:
		if cleanup.get(str(dmark)) == True:
			bpy.data.images.remove(cleanup)
	# delete all materials
	for cleanup in bpy.data.materials:
		if cleanup.get(str(dmark)) == True:
			bpy.data.materials.remove(cleanup)
	# delete all objects
	for cleanup in bpy.data.objects:
		if cleanup.get(str(dmark)) == True:
			bpy.data.objects.remove(cleanup)
	# delete all worlds
	for cleanup in bpy.data.worlds:
		if cleanup.get(str(dmark)) == True:
			bpy.data.worlds.remove(cleanup)
	# delete all meshes
	for cleanup in bpy.data.meshes:
		if cleanup.get(str(dmark)) == True:
			bpy.data.meshes.remove(cleanup)
	# Flush temp folder
	if flushtemp == True:
		shutil.rmtree(str(addon_root_dir / 'tot'), ignore_errors=True)
		os.makedirs(str(addon_root_dir / 'tot'))












# ==========================================
#              Module downloaders
# ==========================================
"""
with open('downloaded.zip', 'wb') as txtfile:
	txtfile.write(data)
"""

# important todo: this function is unfinished
# set beta to True to make it download beta version
def download_mapbase(tmpfolder=None, beta=True):
	# Normally, this should download to tot and extract to bins/mapbase/release OR beta
	import requests, zipfile, shutil, urllib.request, urllib.parse, urllib.error, time
	from pathlib import Path
	from bs4 import BeautifulSoup as jquery
	from bs4 import Tag, NavigableString

	addon_root_dir = Path(__file__).absolute().parent.parent



	#
	# get list of URLs to download from
	#

	# get html page. important todo: Is there a key-free unlimited API for moddb ?
	# important todo: it seems like it finds the fastest url by itself if you remove /all
	# 'https://www.moddb.com/downloads/start/183649'
	# dl links are very simple on moddb: moddb domain + static download ID
	rq_url = 'https://www.moddb.com/downloads/start/' + ('223275' if beta == True else '183649') + '/all'
	url_prms = {
		'Accept': '*/*'
	}
	# I fucking hate it when it's impossible to distinguish which name is built-in into the langauge
	# and which one is a custom one
	# LIKE, headers=headers YES, THAT'S VERY FUCKING NICE
	rq_headers = {
		'Accept': '*/*'
	}
	do_request = requests.get(url=rq_url, params=url_prms, headers=rq_headers)
	urls_html = do_request.content

	# print(data)

	# parse loaded HTML
	lizard = jquery(urls_html.decode(), 'lxml', multi_valued_attributes=None)

	# get all row links
	# todo: review this selector ?
	rowlinks = [rl['href'] for rl in lizard.select('.mirrors .row [href*="downloads/mirror"]')]

	print('Found Mapbase Download Links:')
	for ded in rowlinks:
		print(ded)



	#
	# Find the fastest Link
	#

	# important todo: urllib allows for continuable downloads
	print('Looking for the fastest URL...')
	timings = {}
	for sex in rowlinks:
		# print('Пикаем ссылку тремя метрами данных...')
		start_time = time.time()
		
		request_r = urllib.request.Request('https://www.moddb.com' + sex)
		request_r.add_header('Accept', '*/*')
		# Do websites REALLY think they can protect themselves from me by simply requiring user-agent ????
		request_r.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
		
		ping = urllib.request.urlopen(request_r)
		data = ping.read((1024**2)*3)
		end_time = time.time()
		# todo: do we actually need to close it ?
		ping.close()
		
		tspent = end_time - start_time
		timings[tspent] = sex
		
		print(sex, ':', tspent)

	# set dl link
	fastest_timing = min(timings.keys())
	mb_dl_link = 'https://www.moddb.com' + timings[fastest_timing]
	print('Found The Fastest DL Link:', mb_dl_link)

	# speed dict
	# key means more than
	speed_dict = {
		2: (1024**2)*15,
		8: (1024**2)*6,
		12: (1024**2)*4,
		20: (1024**2)*2
	}
	dl_speed = speed_dict[2]
	# set dl speed
	for speed in speed_dict:
		if fastest_timing > speed:
			dl_speed = speed_dict[speed]

	#
	# Do download
	#

	mapbase_ver = 'beta' if beta == True else 'release'

	ziptmp = 'mapbase_dl_tmp'

	# create temp dir
	# for zip only
	# because why not to take extra safety margins
	dl_to_folder = (Path(tmpfolder) / ziptmp) if tmpfolder != None else (addon_root_dir / 'bins' / 'mapbase' / mapbase_ver / ziptmp)

	# quite a risky operation, but fine... be it...
	dl_to_folder.mkdir(parents=True, exist_ok=True)

	# actually download the mapbase archive
	"""
	dl_url_prms = {
		'Accept': '*/*'
	}
	dl_headerx = {
		'Accept': '*/*',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
	}
	dl_request = requests.get(url=mb_dl_link, params=dl_url_prms, headers=dl_headerx)
	dl_data = dl_request.content
	"""
	
	dl_data = b''
	# create request
	mp_dl_request = urllib.request.Request(mb_dl_link)
	# set headers
	mp_dl_request.add_header('Accept', '*/*')
	mp_dl_request.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
	# open the tunnel
	mp_dl = urllib.request.urlopen(mp_dl_request)

	# get content size
	content_len = int(mp_dl.getheader('Content-Length'))

	# pull data by chunks
	while True:
		pulled = mp_dl.read(dl_speed)
		dl_data += pulled
		# (current / total) * 100
		if len(pulled) <= 0: break
		print('Downloading Mapbase:', round((len(dl_data) / content_len)*100, 2), '%')

	# write downloaded zip data to a temp folder
	with open(str(dl_to_folder / 'mapbase_downloaded.zip'), 'wb') as arc_file:
		arc_file.write(dl_data)

	# write md5 hash because it's the only way to tell whether the download was interrupted or not
	# todo: wat ????
	with open(str(dl_to_folder / 'mapbase_downloaded.m5hash'), 'w') as hash_file:
		hash_file.write(getfilemd5((dl_to_folder / 'mapbase_downloaded.zip')))

	# create tmp folder
	extracted_loc = dl_to_folder.parent / 'mapbase_extracted'
	# delete target folder because pineapple
	if extracted_loc.is_dir():
		shutil.rmtree(str(extracted_loc))
	# spawn it back
	extracted_loc.mkdir(parents=True, exist_ok=True)

	# extract archive either to beta or release in the bins folder
	with zipfile.ZipFile(str(dl_to_folder / 'mapbase_downloaded.zip'),'r') as zip_ref:
		zip_ref.extractall(str(extracted_loc))


	return extracted_loc

















def blfoil_download_hpp(hppver='2013sp', tmpfolder=None):
	import requests, random, zipfile, os
	from pathlib import Path
	from bs4 import BeautifulSoup as jquery
	from bs4 import Tag, NavigableString
	# import distutils
	# from distutils import dir_util

	"""
	valid entries:
		csgo
		tf2
		2013mp
		2013sp
	"""
# https://github.com/ficool2/HammerPlusPlus-Website/releases/download/8862/hammerplusplus_2013mp_build8862.zip
	#
	# get list of downloadables
	#

	# get html page. For now BDSM. todo: Later - ask ficool for a more elegant way
	rq_url = 'https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/main/download.html'
	url_prms = {
		'Accept': '*/*'
	}
	headerz = {
		'Accept': '*/*'
	}
	do_request = requests.get(url=rq_url, params=url_prms, headers=headerz)
	data = do_request.content

	lizard = jquery(data.decode(), 'lxml', multi_valued_attributes=None)

	# full_links = [fl['href'] for fl in lizard.select('[href*="https://github.com/ficool2/HammerPlusPlus-Website/releases/download"]')]
	full_links = [fl['href'] for fl in lizard.select('[href*="github.com/ficool2/HammerPlusPlus-Website/releases/download"]')]
	for ded in full_links:
		print(ded)



	# get the link for the target engine
	dl_url = None
	for tgtlink in full_links:
		if hppver in tgtlink:
			# return tgtlink
			dl_url = tgtlink
			print('Found requested hpp dl link:', dl_link)
			# just how much of a gentleman one should be to break out of a 5 items array loop
			break


	# create temp dir
	if tmpfolder != None:
		dl_to_folder = Path(tmpfolder) / 'hammer_pp_dl_tmp'
	else:
		addon_root_dir = Path(__file__).absolute().parent.parent.parent
		dl_to_folder = addon_root_dir / 'tot' / 'hammer_pp_dl_tmp'

	dl_to_folder.mkdir(parents=True, exist_ok=True)

	#
	# do download
	#
	# dl_url = dl_link
	dl_url_prms = {
		'Accept': '*/*'
	}
	dl_headerz = {
		'Accept': '*/*'
	}
	dl_request = requests.get(url=dl_url, params=dl_url_prms, headers=dl_headerz)
	dl_data = dl_request.content

	# write downloaded data
	with open(str(dl_to_folder / 'hammer_pp_downloaded.zip'), 'wb') as mpb_file:
		mpb_file.write(dl_data)

	# extract archive
	with zipfile.ZipFile(str(dl_to_folder / 'hammer_pp_downloaded.zip'),'r') as zip_ref:
		zip_ref.extractall(str(dl_to_folder / 'hammer_pp'))

	# move stuff to target and overwrite when neccessary

	# first - move bin
	# todo: safety measures
	# important todo: The whole addon still lacks some safety measures
	"""
	distutils.dir_util.copy_tree(
		src=str(dl_to_folder / 'hammer_pp' / os.listdir(dl_to_folder / 'hammer_pp')[0] / 'bin'),
		dst=r'E:\Gamess\steamapps\common\half-life 2\bin'
	)
	"""

	return (dl_to_folder / 'hammer_pp' / os.listdir(dl_to_folder / 'hammer_pp')[0])












# print(blfoil_download_hpp(hppver='2013sp'))



def shared_drinker():
	print(download_mapbase())



# shared_drinker()

