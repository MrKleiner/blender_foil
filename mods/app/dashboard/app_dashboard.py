

# takes full config as an input
# important todo: Mod Kill button does not work
def dboard_launch_mod(cfg):
	from ....utils.shared import app_command_send
	import subprocess
	from pathlib import Path

	global engine_ref
	engine_ref = None
	try:
		varstate = True if engine_ref == None else False
	except:
		varstate = True

	if varstate:
		ldmap = ['+map', '"' + cfg.get('map') + '"'] if cfg.get('map') != None else []
		with open(str(Path(cfg['client_name']).parent / 'bl_foil_launcher.cmd'), 'w') as launcher:
			# todo: does it really has to be human readable ?
			launcher.write(' '.join(['"' + cfg['engine'] + '"'] + ['-game', '"' + cfg['client_name'] + '"'] + ldmap + cfg['params']))

		# print(ldmap)
		# engine_ref = subprocess.Popen([cfg['engine']] + ['-game', cfg['client_name']] + ldmap + cfg['params'])
		# print(' '.join([cfg['engine']] + ['-game', cfg['client_name']] + ldmap + cfg['params']))
		engine_ref = subprocess.Popen(str(Path(cfg['client_name']).parent / 'bl_foil_launcher.cmd'))

		return 'Launched Mod'
	else:
		return 'Mod is running already. Kill it before launching a new instance'



# takes full config as an input
def dboard_kill_mod(pl):
	from ....utils.shared import app_command_send
	import subprocess
	global engine_ref

	try:
		varstate = True if engine_ref != None else False
	except:
		varstate = False

	if varstate:	
		engine_ref.kill()
		engine_ref = None

		return 'Killed Mod'
	else:
		return 'Mod is not running'







# takes path to gameinfo to read from
def dboard_get_suggested_maps(pl):
	from pathlib import Path
	import os
	from ....utils.lizard_tail.lizard_tail import lizard_tail

	gameinfo_path = Path(pl['gminfo_path'])
	# root of the client folder
	cl_folder = gameinfo_path.parent

	# evaluate game info
	with open(str(gameinfo_path), 'r') as gm:
		game_info = lizard_tail(gm.read())


	collected_maps = []

	# first - collect maps from the current maps folder, if any
	if (cl_folder / 'maps').is_dir():
		# I fucking swear if you start the holywar on oneliners vs readable shit - I'll fucking feed you to my home xenomorph
		# collected_maps += [local_map.rstrip('.bsp') if local_map.endswith('.bsp') else '' for local_map in os.listdir(str(cl_folder / 'maps'))]
		collected_maps += [str(local_map.relative_to(cl_folder / 'maps').as_posix()).rstrip('.bsp') for local_map in (cl_folder / 'maps').rglob('*') if (local_map.suffix.lower() == '.bsp')]
		# for local_map in os.listdir(str(cl_folder / 'maps')):
		# 	if local_map.endswith('.bsp'):
		# 		collected_maps.append()


	applicable_clients = []
	# get list of clients
	# unreliable, but maps/ + entries only with .bsp should serve as a good filter
	for cl in os.listdir(cl_folder.parent):
		if (cl_folder.parent / cl / 'maps').is_dir():
			applicable_clients.append(cl)


	# then - try to collect shit from linked rubbish, if asked
	# todo: is this slow ?
	# the loop lenght would never even exceed 20 ...

	# Cry about this, you fucking nerd
	# feel so fucking smart?
	# re-write this code and send me an "improved" version: megaadrenaline100@gmail.com
	if len(applicable_clients) > 0 and pl.get('suggest_linked') == True:
		print(game_info.search_paths)
		# go game_info is a gameinfo class object
		# access search_paths k:v pairs which were parsed from the GameInfo.txt
		# check every single one of them
		for link_entry in game_info.search_paths:
			# if link_entry['key'].lower() != 'gamebin' and any(ext in link_entry['value'].lower() for ext in applicable_clients):
			
			# since the checking pattern is like anything:anything + everywhere + doesnt matter
			# try to avoind gamebin at all
			if link_entry['key'].lower() != 'gamebin':
				# see if any client is in the value
				for acl in applicable_clients:
					if acl in link_entry['value'].lower():
						# actually find maps in the client that matched the query
						# (applicable client means that it has the maps folder)
						for mp in os.listdir(cl_folder.parent / acl / 'maps'):
							if mp.endswith('.bsp'):
								collected_maps.append(str(acl) + '/' + str(mp).rstrip('.bsp'))

	# lolololololololol
	return list(filter(None, list(dict.fromkeys(collected_maps))))






























# ==========================================
#               Context Manager
# ==========================================

# for now it's here, in the Dashboard module, because it's pretty much a dashboard task...

def save_last_app_context(pl):
	import json
	from pathlib import Path
	from ....utils.shared import where_addon_root

	addon_rootdir = where_addon_root(__file__)
	with open(str(addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json'), 'w') as lastcont:
		# todo: does it really has to be human readable ?
		lastcont.write(json.dumps(pl, indent=4, sort_keys=True))
	return {'Saved global last context': pl}




# takes index context and quick config as an input
# is additive
def save_app_quick_config(pl):
	import json
	from pathlib import Path
	from ....utils.shared import where_addon_root


	addon_rootdir = where_addon_root(__file__)
	jpath = (addon_rootdir / 'configs' / 'app' / 'projects' / str(pl['project_index']) / 'fast_config.json')

	addition = {}

	if jpath.is_file():
		with open(str(jpath), 'r') as quickconf:
			addition = json.loads(quickconf.read())

	for ad in pl['quick_config']:
		addition[ad] = pl['quick_config'][ad]

	with open(str(jpath), 'w') as quickconf:
		quickconf.write(json.dumps(addition, indent=4, sort_keys=True))
	return {'Saved Project Quick Config': addition}





# loadquick context by project index
def load_context_by_index(pl):
	import json
	from pathlib import Path
	from ....utils.shared import app_command_send, where_addon_root
	addon_rootdir = where_addon_root(__file__)
	print('Blender got asked to load context from id', pl['project_index'])

	pr_index = pl['project_index']

	if (addon_rootdir / 'configs' / 'app' / 'projects' / str(pr_index) / 'fast_config.json').is_file():
		with open(str(addon_rootdir / 'configs' / 'app' / 'projects' / str(pr_index) / 'fast_config.json'), 'r') as lastcont:
			print('Returning fast config')
			return json.loads(lastcont.read())
	else:
		print('Fast config under specified index', pr_index, 'does not exist')
		stats = {
			'status': 'fail',
			'reason': 'Fast config under specified index does not exist',
			'details': str(addon_rootdir / 'configs' / 'app' / 'projects' / str(pr_index) / 'fast_config.json')
		}
		return stats



# loads quick config
def load_last_app_context(pl):
	import json
	from pathlib import Path
	from ....utils.shared import where_addon_root


	addon_rootdir = where_addon_root(__file__)

	print('Blender got asked to give last used fast config')

	# read file containing last used project index
	with open(str(addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json'), 'r') as prindex:
		lastcont = json.loads(prindex.read())['project_index']

	return load_context_by_index({'project_index': lastcont})