

# takes full config as an input
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





def save_last_app_context(pl):
	import json
	from pathlib import Path
	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent
	with open(str(addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json'), 'w') as lastcont:
		# todo: does it really has to be human readable ?
		lastcont.write(json.dumps(pl, indent=4, sort_keys=True))
	return {'Saved global last context': pl}


# loads quick config
def load_last_app_context(pl):
	import json
	from pathlib import Path
	from ....utils.shared import app_command_send
	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent
	print('Blender got asked to give away fast config')
	if pl.get('last_used') == True:
		print('Fast config has to be based from last used context')
		with open(str(addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json'), 'r') as prindex:
			lastcont = json.loads(prindex.read())['project_index']
	else:
		print('Fast config has to be based from requested index')
		lastcont = pl['project_index']

	if (addon_rootdir / 'configs' / 'app' / 'projects' / str(lastcont) / 'fast_config.json').is_file():
		with open(str(addon_rootdir / 'configs' / 'app' / 'projects' / str(lastcont) / 'fast_config.json'), 'r') as lastcont:
			# app_command_send({
			# 	'app_module': 'set_context',
			# 	'mod_action': 'set_context',
			# 	'payload': json.loads(lastcont)
			# })
			print('Returning fast config')
			return json.loads(lastcont.read())
	else:
		print('Fast config under specified index does not exist')
		return {'load_last_app_context': 'Fast config under specified index does not exist'}



# takes index context and quick config as an input
# is additive
def save_app_quick_config(pl):
	import json
	from pathlib import Path
	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent
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



# takes path to gameinfo to read from
def dboard_get_suggested_maps(pl):
	from pathlib import Path
	import os
	from ....utils.lizard_tail.lizard_tail import lizard_tail

	gameinfo_path = Path(pl['gminfo_path'])
	cl_folder = gameinfo_path.parent

	with open(str(gameinfo_path), 'r') as gm:
		game_info = lizard_tail(gm.read())

	# search_paths

	collected_maps = []

	# first - collect maps from the current maps folder, if any
	if (cl_folder / 'maps').is_dir():
		# I fucking swear if you start the holywar on oneliners vs readable shit - I'll fucking feed you to my home alien
		collected_maps += [local_map.rstrip('.bsp') if local_map.endswith('.bsp') else '' for local_map in os.listdir(str(cl_folder / 'maps'))]
		# for local_map in os.listdir(str(cl_folder / 'maps')):
		# 	if local_map.endswith('.bsp'):
		# 		collected_maps.append()


	applicable_clients = []
	# get list of clients
	# unreliable, but maps/ + entries only with .bsp should serve as a good filter
	for cl in os.listdir(cl_folder.parent):
		if (cl_folder.parent / cl / 'maps').is_dir():
			applicable_clients.append(cl)


	# then - try to collect shit from linked rubbish
	# todo: is this slow ?
	# the loop lenght would never even exceed 20 ...

	# Cry about this, you fucking nerd
	# feel so fucking smart?
	# re-write this code and send me an "improved" version: megaadrenaline100@gmail.com
	if len(applicable_clients) > 0:
		print(game_info.search_paths)
		for link_entry in game_info.search_paths:
			# if link_entry['key'].lower() != 'gamebin' and any(ext in link_entry['value'].lower() for ext in applicable_clients):
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






















