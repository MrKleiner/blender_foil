from pathlib import Path
from ...utils.lizard_tail.lizard_tail import lizard_tail
from ...utils.shared import app_command_send, where_addon_root 

addon_root_dir = where_addon_root(__file__)


def skybox_loader_meta_list(pl):
	# first evaluate gameinfo
	cl_gameinfo = lizard_tail(Path(pl['gameinfo_path']).read_text())

	cl_folder = Path(pl['client_folder_path'])

	collected_tgt_vpks = []

	applicable_vpks = []
	# get list of vpks inside current client
	for clvpk in cl_folder.glob('*'):
		if '_dir.vpk' in clvpk.name:
			applicable_vpks.append(clvpk)


	# then - try to collect shit from linked rubbish, if asked

	# Cry about this, you fucking nerd
	# feel so fucking smart?
	# re-write this code and send me an "improved" version: megaadrenaline100@gmail.com
	print(game_info.search_paths)
	# go game_info is a gameinfo class object
	# access search_paths k:v pairs which were parsed from the GameInfo.txt
	# check every single one of them
	for link_entry in game_info.search_paths:
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
							applicable_vpks.append(str(acl) + '/' + str(mp).rstrip('.bsp'))

	# lolololololololol
	return list(filter(None, list(dict.fromkeys(collected_maps))))













