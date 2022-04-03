



def fetch_existing_engines():
	""" this should be only done once """
	import numpy as np
	import os
	import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path
	# "C:\Program Files (x86)\Steam\config\libraryfolders.vdf"

	# C:\Program Files (x86)\Steam\config\libraryfolders.vdf
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
	applicable = {
		'half-life 2': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		'Half-Life 2 Deathmatch': {
			'exe': 'hl2.exe',
			'icton': 'hl2/resource/game.ico'
		},
		'Left 4 Dead 2': {
			'exe': 'left4dead2.exe',
			'icton': 'left4dead2.ico'
		},
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

	return pl_badwater

# MDMA
def modmaker_load_engine_info(engi_exe):
	import numpy as np
	import os
	import math
	from pathlib import Path
	import shutil
	import os.path
	from os import path

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

	return ess_bins




def multImetr():
	print(fetch_existing_engines())





multImetr()