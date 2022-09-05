




# takes client folder path as an input
def gameinfoman_load_gminfo(pl):
	from ....utils.lizard_tail.lizard_tail import lizard_tail
	from pathlib import Path

	clpath = Path(pl['client_path'])

	with open(str(clpath / 'gameinfo.txt'), 'r') as read_gminfo:
		cl_gameinfo = lizard_tail(read_gminfo.read())

	main_keys = cl_gameinfo.base_keys
	main_keys['SteamAppId'] = cl_gameinfo.steam_id
	main_keys['content_mount'] = cl_gameinfo.search_paths

	return main_keys



def gameinfo_save_back(pl):
	from ....utils.lizard_tail.lizard_tail import lizard_tail
	from pathlib import Path
	import json

	gpath = Path(pl['gminfo_path'])

	with open(str(gpath), 'r') as read_gminfo:
		cl_gameinfo = lizard_tail(read_gminfo.read())

	for bskey in pl['base_keys']:
		cl_gameinfo.set_basekey((bskey, pl['base_keys'][bskey]))

	# app id
	cl_gameinfo.steam_id = pl['app_id']

	with open(str(gpath), 'w') as write_gminfo:
		write_gminfo.write(cl_gameinfo.tofile())

	return 'saved gmi'


def gameinfo_save_back_mounts(pl):
	from ....utils.lizard_tail.lizard_tail import lizard_tail
	from pathlib import Path
	import json

	gpath = Path(pl['gminfo_path'])

	# eval gameinfo
	cl_gameinfo = lizard_tail(gpath.read_text())

	cl_gameinfo.search_paths = pl['search_paths']

	gpath.write_text(cl_gameinfo.tofile())

	return 'saved gmi mount'


# important todo: important shit like magix has to be as a module or smth
# like a class or something
# for easier calls
def gminfo_icon_vis_feedback(pl):
	from pathlib import Path
	import json
	import base64
	import subprocess

	addon_root_dir = Path(__file__).absolute().parent.parent.parent.parent

	clpath = Path(pl['client_path'])
	iconpath = Path(pl['icon_path'])

	# if icon path is absolute - don't join
	# if relative - join
	if not clpath.is_absolute():
		realpath = clpath / iconpath
	else:
		realpath = iconpath

	# if icon file does not exist - dont do shit and cry about it
	if not realpath.is_file():
		return {'conversion_success': False}

	magix = addon_root_dir / 'bins' / 'imgmagick' / 'magick.exe'

	magix_prms = [
		# magick exe
		str(magix),
		# magick input
		str(realpath) + '[0]',
		# psuedo output
		str('png:')
	]
	# exec magick
	# fuck webp and especially jfif, but here's literally no way to see which image format is used
	# so use webp, because it appears that it's very performant
	# if the output is specified like " png: ", then magick will output the resulting bytes into stdout
	# todo: stderr ??
	webp = subprocess.run(magix_prms, capture_output=True)
	# convert result to base64
	webp_b64 = base64.b64encode(webp.stdout)
	print('converted gameinfo icon to base64:', len(webp_b64))
	# send result back
	return {'icon_exists': True, 'conversion_success': True, 'format': 'webp', 'img_base64': webp_b64.decode()}














