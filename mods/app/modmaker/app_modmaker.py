



def fetch_existing_engines():
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
def modmaker_load_engine_info(engi_exe):
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
		if tgt_dir.is_dir() and gc != 'bin':
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
						# it appears that the webp rubbish is "performant"
						'webp',
						'bmp',
						'ico',
						'cur',
						'tif',
						'tiff'
					]

					rdyicon = str(icon_order)

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
						rdyicon = 'assets/icon_default.svg'
					
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



def modmaker_save_engine_info(eng_info):
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


def modmaker_load_saved_engines():
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
def modmaker_kill_engine(eng):
	from pathlib import Path
	import json

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



def modmaker_spawn_new_engine(einf):















def mdma_multImetr():
	print(fetch_existing_engines())





# mdma_multImetr()
















