

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
	return True


def load_last_app_context(pl):
	import json
	from pathlib import Path
	from ....utils.shared import app_command_send
	addon_rootdir = Path(__file__).absolute().parent.parent.parent.parent
	if (addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json').is_file():
		with open(str(addon_rootdir / 'configs' / 'app' / 'global' / 'last_context.json'), 'r') as lastcont:
			# app_command_send({
			# 	'app_module': 'set_context',
			# 	'mod_action': 'set_context',
			# 	'payload': json.loads(lastcont)
			# })
			return json.loads(lastcont.read())

	return False
