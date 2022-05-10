




# takes client folder path as an input
def gameinfoman_load_gminfo(pl):
	from ....utils.lizard_tail.lizard_tail import lizard_tail
	from pathlib import Path

	clpath = Path(pl['client_path'])

	with open(str(clpath / 'gameinfo.txt'), 'r') as read_gminfo:
		cl_gameinfo = lizard_tail(read_gminfo.read())

	main_keys = cl_gameinfo.base_keys
	main_keys['SteamAppId'] = cl_gameinfo.steam_id

	return main_keys

