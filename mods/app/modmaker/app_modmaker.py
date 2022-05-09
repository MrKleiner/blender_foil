


# important: function has to always accept a payload

def fetch_existing_engines(pl):
	""" this should be only done once """
	import numpy as np
	import os
	import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	import json
	# "C:\Program Files (x86)\Steam\config\libraryfolders.vdf"

	# C:\Program Files (x86)\Steam\config\libraryfolders.vdf
	# Fuck Linux users
	with open(r'C:\Program Files (x86)\Steam\config\libraryfolders.vdf', 'r') as libfile:
		rlines = libfile.readlines()

	libpaths = []

	# get libs
	# important todo: KV parser is actually there
	# gameinfo parser could easily be adapted
	for ln in rlines:
		if '"path"' in ln:
			libpaths.append(Path(''.join(ln.split('"path"')).strip().replace('"', '').replace('\\\\', '\\')))

	print(libpaths)

	# applicable
	# wtf
	# fucking pre-include these stupid icons
	# gmod is not moddable. Create addons instead
	applicable = {
		# hl2, ep1 and ep2 use the same engine
		'half-life 2': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		'Half-Life 2 Deathmatch': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		# Because what's the fucking point of modding l4d 1
		'Left 4 Dead 2': {
			'exe': 'left4dead2.exe',
			'icton': 'left4dead2.ico'
		},
		# Because what's the fucking point of modding p1
		'Portal 2': {
			'exe': 'portal2.exe',
			'icton': 'portal2.ico'
		},
		'Source SDK Base 2013 Multiplayer': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		'Source SDK Base 2013 Singleplayer': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		# Seriously, this is valve's habit: *release a "game"* --> *release a "game 2" which is literally "game 1" + "game 2"*
		'Alien Swarm Reactive Drop': {
			'exe': 'reactivedrop.exe',
			'icton': 'reactivedrop.ico'
		},
		'Counter-Strike Global Offensive': {
			'exe': 'csgo.exe',
			'icton': 'csgo/resource/game.ico'
		},
		'day of defeat source': {
			'exe': 'hl2.exe',
			'icton': 'dod/resource/game.ico'
		},
		'Black Mesa': {
			'exe': 'bms.exe',
			'icton': 'hl2/resource/game.ico'
		},
		'Team Fortress 2': {
			'exe': 'hl2.exe',
			'icton': 'tf/resource/game.ico'
		},
		'Counter-Strike Source': {
			'exe': 'hl2.exe',
			'icton': 'cstrike/resource/game.ico'
		}
	}

	# scan libs
	libmatches = []
	for gamelib in libpaths:
		for gmpath in os.listdir(str(gamelib / 'steamapps' / 'common')):
			# print(gmpath)
			if gmpath in applicable:
				print(gamelib / 'steamapps' / 'common' / gmpath)
				libmatches.append(gamelib / 'steamapps' / 'common' / gmpath)

	# create return payload
	libmatches = list(dict.fromkeys(libmatches))
	pl_badwater = [
		{
			'engine_path': str(ep / applicable[ep.name]['exe']), 
			'engine_name': ep.name,
			'icon': str(ep / applicable[ep.name]['icton'])
		} for ep in libmatches
	]

	# C:\Users\DrHax\AppData\Roaming\Blender Foundation\Blender\3.1\scripts\addons\blender_foil\configs\app\engines
	# important todo: some paths should be pre-defined
	config_loc = Path(__file__).absolute().parent.parent.parent.parent / 'configs' / 'app' / 'engines' / 'engines_info.json'
	epayload = {}
	# todo: md5 of a path ?
	for en in pl_badwater:
		epayload[en['engine_path']] = {
			'engine_path': en['engine_path'], 
			'engine_name': en['engine_name'],
			'icon': en['icon']
		}

	with open(str(config_loc), 'w') as jsonfile:
		jsonfile.write(json.dumps(epayload, indent=4, sort_keys=False))

	return pl_badwater



# MDMA
def modmaker_load_engine_info(pl):
	# import numpy as np
	import os
	import math
	from pathlib import Path
	import shutil
	import base64
	# import os.path
	# from os import path
	import subprocess
	import json
	from ....utils.lizard_tail.lizard_tail import lizard_tail

	engi_exe = pl['engine_exe']

	engine_dir = Path(engi_exe).parent

	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent

	# todo: it gets re-ordered in-app anyway...
	# but like, the amount of .is_file() operation will remain the same...
	ess_bins = {
		'engine.dll': (engine_dir / 'bin' / 'engine.dll').is_file(),
		'datacache.dll': (engine_dir / 'bin' / 'datacache.dll').is_file(),
		'inputsystem.dll': (engine_dir / 'bin' / 'inputsystem.dll').is_file(),
		'launcher.dll': (engine_dir / 'bin' / 'launcher.dll').is_file(),
		'mdllib.dll': (engine_dir / 'bin' / 'mdllib.dll').is_file(),
		'tier0.dll': (engine_dir / 'bin' / 'tier0.dll').is_file(),
		'vgui2.dll': (engine_dir / 'bin' / 'vgui2.dll').is_file(),
		'vphysics.dll': (engine_dir / 'bin' / 'vphysics.dll').is_file(),
		'vstdlib.dll': (engine_dir / 'bin' / 'vstdlib.dll').is_file(),
		'vguimatsurface.dll': (engine_dir / 'bin' / 'vguimatsurface.dll').is_file(),
		'unitlib.dll': (engine_dir / 'bin' / 'unitlib.dll').is_file(),
		'soundsystem.dll': (engine_dir / 'bin' / 'soundsystem.dll').is_file()
	}

	sdk_bins = {
		'vrad exe/dll': ((engine_dir / 'bin' / 'vrad.exe').is_file(), (engine_dir / 'bin' / 'vrad_dll.dll').is_file()),
		'hammer exe/dll': ((engine_dir / 'bin' / 'hammer.exe').is_file(), (engine_dir / 'bin' / 'hammer_dll.dll').is_file()),
		'vtex exe/dll': ((engine_dir / 'bin' / 'vtex.exe').is_file(), (engine_dir / 'bin' / 'vtex_dll.dll').is_file()),
		'vvis exe/dll': ((engine_dir / 'bin' / 'vvis.exe').is_file(), (engine_dir / 'bin' / 'vvis_dll.dll').is_file()),
		'vrad exe/dll': ((engine_dir / 'bin' / 'vrad.exe').is_file(), (engine_dir / 'bin' / 'vrad_dll.dll').is_file()),
		'hlmv.exe': [(engine_dir / 'bin' / 'hlmv.exe').is_file(), (engine_dir / 'bin' / 'hlmv.exe').is_file()],
		'studiomdl.exe': [(engine_dir / 'bin' / 'studiomdl.exe').is_file(), (engine_dir / 'bin' / 'studiomdl.exe').is_file()],
		'hlfaceposer.exe': [(engine_dir / 'bin' / 'hlfaceposer.exe').is_file(), (engine_dir / 'bin' / 'hlfaceposer.exe').is_file()],
		'height2ssbump.exe': [(engine_dir / 'bin' / 'height2ssbump.exe').is_file(), (engine_dir / 'bin' / 'height2ssbump.exe').is_file()],
		'vpk.exe': [(engine_dir / 'bin' / 'vpk.exe').is_file(), (engine_dir / 'bin' / 'vpk.exe').is_file()]
	}


	#
	# Get clients
	#

	# separate function ?
	identifier = [
		'bin',
		'maps',
		'gameinfo.txt',
		'sound',
		'resource',
		'materials',
		'models',
		'materialsrc'
		'modelsrc',
		# todo: questionable
		'scripts'
	]

	config_loc = addon_rootdir / 'configs' / 'app' / 'engines' / 'engines_info.json'
	with open(str(config_loc), 'r') as jsonfile:
		jfile = json.loads(jsonfile.read())

	allowed_clients = []

	for gc in os.listdir(engine_dir):
		tgt_dir = engine_dir / gc
		# there are a few folder names that should be omitted, like bin and mapbase binaries
		noscan = [
			'bin',
			'mapbase_shared',
			'mapbase_episodic',
			'mapbase_hl2'
		]
		if tgt_dir.is_dir() and not gc in noscan:
			# this chains ensures that an actual client is being tested
			if set(os.listdir(tgt_dir)) & set(identifier):
				# allowed_clients.append(gc)
				clpl = {
					'folder_name': gc,
					'client_name': 'NONE/BASE',
					# Points to a base since if there's gameinfo
					# then the icon will at least be re-marked as no-icon and not as base
					'client_icon': 'assets/cleint_isbase.svg',
					'hasdll': True if (tgt_dir / 'bin' / 'client.dll').is_file() and (tgt_dir / 'bin' / 'server.dll').is_file() else False
				}
				# it's шиndows - a folder cannot contain duplicate names
				if (tgt_dir / 'gameinfo.txt').is_file():

					# read gameinfo
					with open(str(tgt_dir / 'gameinfo.txt'), 'r') as gminfofile:
						gminfo = lizard_tail(gminfofile.read())

					clpl['client_name'] = gminfo.game_name

					# this will either return False or an absolute Path to the icon
					# exception safe
					icon_order = (
						(tgt_dir / (gminfo.game_icon + '.ico')) if gminfo.game_icon != '' and (tgt_dir / (gminfo.game_icon + '.ico')).is_file() else False
						or
						(tgt_dir / (gminfo.game_icon + '.tga')) if gminfo.game_icon != '' and (tgt_dir / (gminfo.game_icon + '.tga')).is_file() else False
						or
						(tgt_dir / (gminfo.game_icon + '.bmp')) if gminfo.game_icon != '' and (tgt_dir / (gminfo.game_icon + '.bmp')).is_file() else False
						or
						(tgt_dir / 'resource' / 'game.ico') if (tgt_dir / 'resource' / 'game.ico').is_file() else False
						or
						(tgt_dir / 'resource' / 'game.tga') if (tgt_dir / 'resource' / 'game.tga').is_file() else False
						or
						(tgt_dir / 'resource' / 'game.bmp') if (tgt_dir / 'resource' / 'game.bmp').is_file() else False
					)

					# formats supported by chromium
					# todo: this has to be in a shared place
					supported_imf = [
						'apng',
						'avif',
						'gif',
						'jpg',
						'jpeg',
						'jfif',
						'pjpeg',
						'pjp',
						'png',
						'svg',
						# it appears that the webp rubbish is "performant" and "recommended" for use in web rubbish
						'webp',
						'bmp',
						'ico',
						'cur',
						'tif',
						'tiff'
					]

					rdyicon = 'assets/icon_default.svg'

					# only do conversions if file exists AND it's not in the list of supported formats
					# todo: Who cares about supported chromium formats when it could appear that
					# source only supports bmp, tga, ico and pur ?
					if icon_order != False and not icon_order.suffix.replace('.', '') in supported_imf:
						print('icon order:', icon_order)

						(addon_rootdir / 'tot' / 'tmpico.png').unlink(missing_ok=True)

						print(str(addon_rootdir / 'bins' / 'imgmagick' / 'magick.exe'))
						magic_args = [
							str(addon_rootdir / 'bins' / 'imgmagick' / 'magick.exe'),
							str(icon_order),
							'-auto-orient',
							addon_rootdir / 'tot' / 'tmpico.png'
						]
						subprocess.call(magic_args)

						# nobody knows what could go wrong with magick conversion
						if (addon_rootdir / 'tot' / 'tmpico.png').is_file():
							with open(str(addon_rootdir / 'tot' / 'tmpico.png'), 'rb') as b6i:
								rdyicon = 'data:image/png;base64,' + base64.b64encode(b6i.read()).decode('utf-8', errors='ignore')
					else:
						# todo: this logic could be better
						rdyicon = str(icon_order or 'assets/icon_default.svg')
					
					clpl['client_icon'] = rdyicon

				allowed_clients.append(clpl)

	# Get clients' names
	# for acl in allowed_clients:






	# get other engine info


	# get icon and name
	# for engine_info in jfile:


	return {'exe': engi_exe, 'ess_bins': ess_bins, 'sdk_bins': sdk_bins, 'icon': jfile[engi_exe]['icon'], 'engine_name': jfile[engi_exe]['engine_name'], 'clients': allowed_clients}



def modmaker_check_engine_bins(engi_exe):
	import numpy as np
	import os
	import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	import json

	# todo: reuse this. Avoid duplicates
	ess_bins = {
		'engine.dll': (Path(engi_exe).parent / 'bin' / 'engine.dll').is_file(),
		'datacache.dll': (Path(engi_exe).parent / 'bin' / 'datacache.dll').is_file(),
		'inputsystem.dll': (Path(engi_exe).parent / 'bin' / 'inputsystem.dll').is_file(),
		'launcher.dll': (Path(engi_exe).parent / 'bin' / 'launcher.dll').is_file(),
		'mdllib.dll': (Path(engi_exe).parent / 'bin' / 'mdllib.dll').is_file(),
		'tier0.dll': (Path(engi_exe).parent / 'bin' / 'tier0.dll').is_file(),
		'vgui2.dll': (Path(engi_exe).parent / 'bin' / 'vgui2.dll').is_file(),
		'vphysics.dll': (Path(engi_exe).parent / 'bin' / 'vphysics.dll').is_file(),
		'vstdlib.dll': (Path(engi_exe).parent / 'bin' / 'vstdlib.dll').is_file(),
		'vguimatsurface.dll': (Path(engi_exe).parent / 'bin' / 'vguimatsurface.dll').is_file(),
		'unitlib.dll': (Path(engi_exe).parent / 'bin' / 'unitlib.dll').is_file(),
		'soundsystem.dll': (Path(engi_exe).parent / 'bin' / 'soundsystem.dll').is_file()
	}

	sdk_bins = {
		'vrad exe/dll': ((Path(engi_exe).parent / 'bin' / 'vrad.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'vrad_dll.dll').is_file()),
		'hammer exe/dll': ((Path(engi_exe).parent / 'bin' / 'hammer.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'hammer_dll.dll').is_file()),
		'vtex exe/dll': ((Path(engi_exe).parent / 'bin' / 'vtex.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'vtex_dll.dll').is_file()),
		'vvis exe/dll': ((Path(engi_exe).parent / 'bin' / 'vvis.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'vvis_dll.dll').is_file()),
		'vrad exe/dll': ((Path(engi_exe).parent / 'bin' / 'vrad.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'vrad_dll.dll').is_file()),
		'hlmv.exe': [(Path(engi_exe).parent / 'bin' / 'hlmv.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'hlmv.exe').is_file()],
		'studiomdl.exe': [(Path(engi_exe).parent / 'bin' / 'studiomdl.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'studiomdl.exe').is_file()],
		'hlfaceposer.exe': [(Path(engi_exe).parent / 'bin' / 'hlfaceposer.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'hlfaceposer.exe').is_file()],
		'height2ssbump.exe': [(Path(engi_exe).parent / 'bin' / 'height2ssbump.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'height2ssbump.exe').is_file()],
		'vpk.exe': [(Path(engi_exe).parent / 'bin' / 'vpk.exe').is_file(), (Path(engi_exe).parent / 'bin' / 'vpk.exe').is_file()]
	}


	return {'exe': engi_exe, 'ess_bins': ess_bins, 'sdk_bins': sdk_bins}



def modmaker_save_engine_info(pl):
	# import numpy as np
	import os
	# import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	import json

	config_loc = Path(__file__).absolute().parent.parent.parent.parent / 'configs' / 'app' / 'engines' / 'engines_info.json'
	with open(str(config_loc), 'r') as jsonfile:
		jfile = json.loads(jsonfile.read())

	jfile[eng_info['engine_exe']] = {
		'engine_path': eng_info['engine_exe'],
		'engine_name': eng_info['engine_name'],
		'icon': eng_info['icon']
	}

	with open(str(config_loc), 'w') as jsonfile:
		jsonfile.write(json.dumps(jfile, indent=4, sort_keys=False))


def modmaker_load_saved_engines(pl):
	# import numpy as np
	import os
	# import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	import json


	config_loc = Path(__file__).absolute().parent.parent.parent.parent / 'configs' / 'app' / 'engines' / 'engines_info.json'
	with open(str(config_loc), 'r') as jsonfile:
		jfile = json.loads(jsonfile.read())

	pl_badwater = [
		{
			'engine_path': jfile[ep]['engine_path'], 
			'engine_name': jfile[ep]['engine_name'],
			'icon': jfile[ep]['icon']
		} for ep in jfile
	]

	return pl_badwater


# delete engine from config
def modmaker_kill_engine(pl):
	from pathlib import Path
	import json

	eng = pl['engine']

	config_loc = Path(__file__).absolute().parent.parent.parent.parent / 'configs' / 'app' / 'engines' / 'engines_info.json'
	with open(str(config_loc), 'r') as jsonfile:
		jfile = json.loads(jsonfile.read())

	try:
		del jfile[eng]
	except:
		# todo: handle exception
		print('Tried to delete engine', eng, 'but it cannot be found in the config')
		pass

	with open(str(config_loc), 'w') as jsonfile:
		jsonfile.write(json.dumps(jfile, indent=4, sort_keys=False))








#
# Spawns a new engine. The final step when creating a mod.
#

# takes a dict, where:

# mapbase: true/false - whether it's mapbase or not
# pbr: true/false - include PBR or not
# link_content: an array of folder names to link in gameinfo
# link_binaries: true/false - link or copy client/server .dll
# binpath: path to client/server .dll folder (relative to engine)
# cl_name: folder name of the client
# game_name: name of the game (any)
# engine_exe: path to engine .exe
# default_dll: 2013_mp/2013_sp_hl2/2013_sp_episodic/dont


# important todo: each engine HAS to have a platform folder
# todo: just in case, strip all " from key/values
def modmaker_spawn_new_client(einf):
	import os
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	import json
	from ....utils.shared import download_mapbase, app_command_send
	from ....utils.lizard_tail.lizard_tail import lizard_tail

	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent


	# if mapbase then check if mapbase is present and download it if necessary

	# Have 3 pre-defined mapbase folders
	# create empty folder next to engine.exe
	# create gameinfo, which should at least:
	# 	point to cl/sv .dll (could be linked or copied)
	#	point to content source
	#	have game name
	#	have game title
	#	have SteamAppId


	#
	# setup some paths
	#

	# engine executable, like Team Fortress 2\hl2.exe
	engine_exe = Path(einf['engine_exe'])
	# folder in which the engine executable is
	engine_folder = engine_exe.parent
	# Client folder is where gameinfo, materials, models go
	# Like, Team Fortress 2\tf(client folder)\materials
	# (should not exist at first)
	client_folder = engine_folder / einf['cl_name']


	#
	# First - create the target client folder and some default folders
	#

	# delete dest folder, if any
	if client_folder.is_dir():
		shutil.rmtree(str(client_folder))

	# create target client folder
	# this is where gameinfo, materials, models go
	# Like, Team Fortress 2\tf(client folder)\materials
	client_folder.mkdir(parents=True, exist_ok=True)

	# create some default folders
	st_folders = [
		'bin',
		'cfg',
		'custom',
		'maps',
		'scripts',
		'materials',
		'models',
		'resource',
		'sound'
	]
	for dff in st_folders:
		(client_folder / dff).mkdir(parents=True, exist_ok=True)


	# then, create gameinfo
	cl_gameinfo = lizard_tail(True)
	# set appid
	cl_gameinfo.steam_id = 243730
	# set game name
	cl_gameinfo.game_name = einf['game_name']




	#
	# Mapbase
	#
	if (einf['mapbase'] == True):
		# important todo: for now - always download mapbase
		# later - check if downloaded and hash matches and simply re-extract if ok
		mapbase_dl = download_mapbase()
		# print(mapbase_dl)

		#
		# set search paths for gameinfo
		#

		# Essential shit like binaries and game root
		info_search_paths = [
			{
				'key': 'Game+Mod+Default_Write_Path',
				'value': '|GameInfo_Path|.'
			},
			{
				'key': 'GameBin',
				'value': '|gameinfo_path|bin'
			},


			# Mapbase
			{
				'key': 'GameBin',
				'value': '|gameinfo_path|../mapbase_episodic/bin'
			},
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|../mapbase_episodic'
			},
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|../mapbase_episodic/content/*'
			},
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|../mapbase_hl2'
			},
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|../mapbase_hl2/content/*'
			},
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|../mapbase_shared/*'
			},
			{
				'key': 'GameBin',
				'value': '|gameinfo_path|../mapbase_shared/shared_misc/bin'
			},
			# d

			# There's always platform
			# {
			# 	'key': 'platform',
			# 	'value': '|All_Source_Engine_Paths|platform'
			# }
		]

		
		#
		# add mounted content
		#

		# important: vpks have to be mounted fucking one by one
		# FIRST, mount vpks and THEN, add directory as "game"
		# weird af

		# mount vpks
		# important todo: ensure there's platform
		for mount in einf['link_content']:
			for mvpk in os.listdir(str(engine_folder / mount)):
				if '_dir.vpk' in mvpk:
					info_search_paths.append({
						'key': 'platform' if mount == 'platform' else 'Game',
						'value': '|All_Source_Engine_Paths|' + mount + '/' + mvpk.replace('_dir.vpk', '.vpk')
					})

		# THEN mount folders
		for mount in einf['link_content']:
			info_search_paths.append({
				'key': 'platform' if mount == 'platform' else 'Game',
				'value': '|All_Source_Engine_Paths|' + mount
			})


		#
		# gameinfo done, now copy mapbase binaries to engine folder (enforce, ensure)
		#
		mapbase_copier = [
			'mapbase_episodic',
			'mapbase_hl2',
			'mapbase_shared'
		]
		# todo: for now - don't bother verifying integrity n shit
		# simply overwrite this rubbish
		for mp_bin in mapbase_copier:
			copy_tgt = (engine_folder / mp_bin)
			if copy_tgt.is_dir():
				# important todo: own shutil, but better
				# fileman
				shutil.rmtree(str(copy_tgt))
			# copy_tgt.mkdir(parents=True, exist_ok=True)
			# copy tree reuires the directory to be absent
			shutil.copytree(mapbase_dl / mp_bin, engine_folder / mp_bin)

		#
		# Mapbase bins are there, populate client with some defaults
		#
		
		# funny todo: if game name field blank - pick random name

		# copy chapters script and discord rpc
		populate_defaults = {
			'chapters.txt': 'scripts',
			'discord-rpc.dll': 'bin',
			'mapbase_rpc.txt': 'scripts',
			'mapbase_demo02.bsp': 'maps'
		}
		for pd in populate_defaults:
			# todo: are brackets actually needed ?
			shutil.copy((addon_rootdir / 'bins' / 'mapbase' / 'common' / pd), (client_folder / populate_defaults[pd]))

		# copy common things
		populate_common = {
			'chapter1.cfg': 'cfg',
			'config.cfg': 'cfg'
		}
		for pc in populate_common:
			# todo: are brackets actually needed ?
			shutil.copy((addon_rootdir / 'bins' / 'source_sdk' / 'common' / pc), (client_folder / populate_common[pc]))





	#
	# Other/SDK
	#
	if einf['mapbase'] != True:


		#
		# set search paths for gameinfo
		#

		# Essential shit like binaries and game root
		info_search_paths = [
			{
				'key': 'Game+Mod+Default_Write_Path',
				'value': '|GameInfo_Path|.'
			},
			{
				'key': 'GameBin',
				'value': '|gameinfo_path|bin' if einf['link_binaries'] == False or (einf['default_dll'] != None and einf['default_dll'] != 'dont') else '|All_Source_Engine_Paths|' + str(einf['binpath'])
			}

			# There's always platform
			# {
			# 	'key': 'platform',
			# 	'value': '|All_Source_Engine_Paths|platform'
			# }
		]


		#
		# add mounted content
		#

		# important: vpks have to be mounted fucking one by one
		# FIRST, mount vpks and THEN, add directory as "game"
		# weird af

		# mount vpks
		# important todo: ensure there's platform
		for mount in einf['link_content']:
			for mvpk in os.listdir(str(engine_folder / mount)):
				if '_dir.vpk' in mvpk:
					info_search_paths.append({
						'key': 'platform' if mount == 'platform' else 'Game',
						'value': '|All_Source_Engine_Paths|' + mount + '/' + mvpk.replace('_dir.vpk', '.vpk')
					})

		# THEN mount folders
		for mount in einf['link_content']:
			info_search_paths.append({
				'key': 'platform' if mount == 'platform' else 'Game',
				'value': '|All_Source_Engine_Paths|' + mount
			})

		#
		# Do predefined SDk 2013 binaries, if asked
		#

		# todo: those are precompiled, compile own or even better - compile on a go
		if einf['default_dll'] != None and einf['default_dll'] != 'dont':
			sdk_bins_paths = {
				'2013_mp': 'mp_bin',
				'2013_sp_hl2': 'sp_bin_hl2',
				'2013_sp_episodic': 'sp_bin'
			}

			# copy cl/sv dlls
			# todo: copytree instead ?
			# todo: overengineering is nice: 'client.dll' is a predefined word, bad ?
			# todo: as could be observed - this logic is not the best
			shutil.copy((addon_rootdir / 'bins' / 'source_sdk' / sdk_bins_paths[einf['default_dll']] / 'client.dll'), (client_folder / 'bin' / 'client.dll'))
			shutil.copy((addon_rootdir / 'bins' / 'source_sdk' / sdk_bins_paths[einf['default_dll']] / 'server.dll'), (client_folder / 'bin' / 'server.dll'))
		else:
			# else - there have to be predefined place to link/copy bins from 
			# important todo: safety measures
			if einf['link_binaries'] != True:
				shutil.copy((engine_folder / einf['binpath'] / 'bin' / 'client.dll'), (client_folder / 'bin' / 'client.dll'))
				shutil.copy((engine_folder / einf['binpath'] / 'bin' / 'server.dll'), (client_folder / 'bin' / 'server.dll'))


	#
	# include PBR, if asked to
	#

	# todo: this is a shared action
	if einf['pbr'] == True:
		pbr_bins = [
			'game_shader_dx9.dll',
			'game_shader_dx9.pdb'
		]
		for pb in pbr_bins:
			shutil.copy((addon_rootdir / 'bins' / 'pbr_sh' / 'bin' / pb), (client_folder / 'bin' / pb))
		shutil.copytree((addon_rootdir / 'bins' / 'pbr_sh' / 'shaders'), (client_folder / 'shaders'))


	#
	# Write gameinfo
	#

	# set paths back to lizard class
	cl_gameinfo.search_paths = info_search_paths

	# write gameinfo to the client folder
	with open(str(client_folder / 'gameinfo.txt'), 'w') as infofile:
		infofile.write(cl_gameinfo.tofile())




	#
	# Create game config dir and write defaults there
	#

	# get free folder name
	taken_names = []
	for fn in os.listdir(addon_rootdir / 'configs' / 'app' / 'projects'):
		try:
			taken_names.append(int(fn))
		except:
			pass

	# available name
	av_name = str(max(taken_names if len(taken_names) > 0 else [0]) + 1)
	pr_folder = addon_rootdir / 'configs' / 'app' / 'projects' / av_name

	# create project folder
	pr_folder.mkdir()

	# write default json
	default_settings = {
		'fullscreen': False,
		'intro_vid': False,
		'loadtools': False,
		'maps_from_linked_gminfo': True,
		'start_from_map': False,
		'use_add_options': True,
		'starting_map': '',
		'add_start_opts': '',
		'project_index': str(av_name),
		'project_name': 'My Rubbish Mod Which I Will Never Finish',
		'client_folder_path': str(client_folder),
		'client_folder_name': str(client_folder.name),
		'full_game_name': str(cl_gameinfo.game_name),
		'engine_executable': str(engine_exe)
	}

	with open(str(pr_folder / 'fast_config.json'), 'w') as project_quick_settings:
		# todo: does it really has to be human readable ?
		project_quick_settings.write(json.dumps(default_settings, indent=4, sort_keys=True))

	# trigger engine load
	app_command_send({
		'app_module': 'modmaker',
		'mod_action': 'load_resulting_engine',
		'payload': default_settings
	})



































def mdma_multImetr():
	# print(fetch_existing_engines())
	modmaker_spawn_new_engine({'mapbase': True})





# mdma_multImetr()
















