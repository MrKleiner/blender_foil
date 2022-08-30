




# pass True to make a new gameinfo
# pass gameinfo string to parse existing gameinfo
class lizard_tail:
	""" super simple gameinfo maker. Takes gameinfo as an input """
	# anything that is specified becomes defaults. Useful
	# Create a string at the very top of the class to make it a documentation
	# variables inside functions HAVE NO CONNECTION to the class variables no matter what
	# to access/write stored variables use self.whatever

	# all the additional functionality is quite optional
	# main purpose of this class is the init function which parses the shit
	# and tovmf function which converts it back to vmf string


	#
	# Defaults
	#

	# pootis = None



	#
	# Functionality
	#



	def __init__(self, pootis=True):
		import io
		import base64
		from .parser import gameinfoparser
		from .reconstructor import gameinfo_rebuilder

		self.gameinfo_r = None

		# It should be possible to create blank gameinfo
		if pootis == True:
			defblank = """
			IkdhbWVJbmZvIgp7CgkiZ2FtZSIJCSJBbGllbiBTd2FybTogUmVhY3RpdmUgRHJvcCIKCSJ0aXRsZSIJCSJBU1ciCS8vIGFzdyAtIGxl
			YXZlIHRoaXMgYmxhbmsgYXMgd2UgaGF2ZSBhIHRleHR1cmUgbG9nbwoJInR5cGUiCQkic2luZ2xlcGxheWVyX29ubHkiCglHYW1lRGF0
			YQkicmVhY3RpdmVkcm9wLmZnZCIKCWljb24JCSJyZXNvdXJjZS9pY29uMSIKCS8vIEluc3RhbmNlUGF0aCAidGlsZWdlbi9pbnN0YW5j
			ZXMvIgoJIlN1cHBvcnRzVlIiICIxIgoJIk5vTW9kZWxzIiAiMSIKCSJOb0hJTW9kZWwiICIxIgoJIkhhc1BvcnRhbHMiICIwIgoJIkFk
			dkNyb3NzaGFpciIgIjAiCgkiTm9EaWZmaWN1bHR5IiAiMCIKCQoJU3VwcG9ydHNEWDggICAgIDAKCQoJIkZpbGVTeXN0ZW0iCgl7CgkJ
			IlN0ZWFtQXBwSWQiCSI1NjM1NjAiCgkJLy8gIlRvb2xzQXBwSWQiCSIyMTEiCgkJCgkJIlNlYXJjaFBhdGhzIgoJCXsKCQkJIkdhbWUi
			CSJ8Z2FtZWluZm9fcGF0aHwuIgoJCQkiR2FtZSIJInBsYXRmb3JtIgoJCX0KCX0KfQo=
			"""
			mkinput = base64.b64decode(defblank.replace('\n', '').replace(' ', '').encode('utf-8')).decode('utf-8')
		else:
			mkinput = pootis


		# There are three reserved characters in xml
		bad_piggies = {
			'<': '&lt;',
			'>': '&gt;',
			'&': '&amp;'
		}
		for pg in bad_piggies:
			str_toparse = mkinput.replace(pg, bad_piggies[pg])
			mkinput = mkinput.replace(pg, bad_piggies[pg])

		inpstr = io.StringIO(str_toparse).readlines()

		gminfo = gameinfoparser(inpstr)

		self.gameinfo_r = gminfo

		# self.game_name = None


	@property
	def game_name(self):
		return self.gameinfo_r.select('GameInfo > kv[keyname="game"]')[0].gval.string

	@game_name.setter
	def game_name(self, newname):
		self.gameinfo_r.select('GameInfo > kv[keyname="game"]')[0].gval.string = str(newname)


	@property
	def game_title(self):
		return self.gameinfo_r.select('GameInfo > kv[keyname="title"]')[0].gval.string

	@game_title.setter
	def game_title(self, newtitle):
		self.gameinfo_r.select('GameInfo > kv[keyname="title"]')[0].gval.string = str(newtitle)


	# get a dict of all the base keys
	@property
	def base_keys(self):
		basekeys = {}
		for bkey in self.gameinfo_r.select('GameInfo > kv'):
			if bkey['keyname'].lower() != 'filesystem':
				basekeys[bkey['keyname']] = bkey.gval.string

		return basekeys


	@property
	def game_icon(self):
		iconselect = self.gameinfo_r.select('GameInfo > kv[keyname="icon"]')
		if len(iconselect) > 0:
			return iconselect[0].gval.string
		else:
			return ''

	@game_icon.setter
	def game_icon(self, newicon):
		self.gameinfo_r.select('GameInfo > kv[keyname="icon"]')[0].gval.string = str(newicon)

	# (key, value) tuple
	def set_basekey(self, bk, additive=False):
		older = self.gameinfo_r.select('GameInfo > kv[keyname="' + bk[0] + '"]')
		if len(older) > 0:
			older[0].decompose()

		newer = self.gameinfo_r.new_tag('kv', keyname=str(bk[0]))
		keyt = self.gameinfo_r.new_tag('gkey')
		keyt.string = str(bk[0])
		newer.append(keyt)
		valt = self.gameinfo_r.new_tag('gval')
		valt.string = str(bk[1])
		newer.append(valt)

		self.gameinfo_r.select('GameInfo')[0].append(newer)

		return True



	@property
	def steam_id(self):
		return self.gameinfo_r.select('GameInfo > FileSystem kv[keyname="SteamAppId"]')[0].gval.string

	@steam_id.setter
	def steam_id(self, newicon):
		self.gameinfo_r.select('GameInfo > FileSystem kv[keyname="SteamAppId"]')[0].gval.string = str(newicon)


	# important todo: this was done by a principle "as fast as posibble because lazyness"

	@property
	def search_paths(self):
		# todo: generator ?
		spaths = []
		for sp in self.gameinfo_r.select('GameInfo > FileSystem > SearchPaths > kv'):
			path_payload = {}
			path_payload['key'] = sp.gkey.string
			path_payload['value'] = sp.gval.string
			spaths.append(path_payload)
		return spaths



	@search_paths.setter
	def search_paths(self, pairs):
		"""
		[
			{
				'key': 'keyname',
				'value': 'value'
			},
			{
				'key': 'keyname',
				'value': 'value'
			},
		]
		"""
		self.gameinfo_r.select('GameInfo > FileSystem > SearchPaths')[0].clear()
		for kvp in pairs:
			keyvtag = self.gameinfo_r.new_tag('kv', keyname=kvp['key'])
			keyt = self.gameinfo_r.new_tag('gkey')
			keyt.string = kvp['key']
			keyvtag.append(keyt)

			valt = self.gameinfo_r.new_tag('gval')
			valt.string = kvp['value']
			keyvtag.append(valt)
			self.gameinfo_r.select('GameInfo > FileSystem > SearchPaths')[0].append(keyvtag)


	def tofile(self):
		from .reconstructor import gameinfo_rebuilder
		return gameinfo_rebuilder(self.gameinfo_r)



	"""
	@property
	def shader(self):
		return self.main_vmt['shader']


	@shader.setter
	def shader(self, newshade):
		self.main_vmt['shader'] = str(newshade)

	@property
	def params(self):
		return self.main_vmt['params']

	"""


def multImetr():
	from parser import gameinfoparser
	from reconstructor import gameinfo_rebuilder
	import io


	# with open(r'E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer\mapbase_episodic_template\gameinfo.txt', 'r') as readf:
	with open(r'E:\Gamess\steamapps\common\Alien Swarm Reactive Drop\reactivedrop\gameinfo.txt', 'r') as readf:
	# with open(r'E:\Gamess\steamapps\common\Counter-Strike Global Offensive\csgo\gameinfo.txt', 'r') as readf:
		nen = readf.read()

	bad_piggies = {
		'<': '&lt;',
		'>': '&gt;',
		'>': '&amp;'
	}
	for pg in bad_piggies:
		nen = nen.replace(pg, bad_piggies[pg])

	inpstr = io.StringIO(nen).readlines()

	rst = gameinfoparser(inpstr)

	"""
	# raw
	with open('rawshit.xml', 'w') as txtfile:
		txtfile.write(rst)
		# txtfile.write(gameinfoparser(inpstr))
	"""

	
	# gameinfoparser().prettify()
	with open('rc.xml', 'w') as txtfile:
		txtfile.write(rst.prettify())
		# txtfile.write(gameinfoparser(inpstr))

	# gameinfoparser().prettify()
	with open('gameinfo.txt', 'w') as txtfile:
		txtfile.write(gameinfo_rebuilder(rst))
	

def multImetrs():

	fuck_you = lizard_tail(True)

	print(fuck_you.gameinfo_r.GameInfo)
	print(fuck_you.game_name)
	fuck_you.game_name = 'Alien Swarm Toilet Drop'
	print(fuck_you.game_name)
	print(fuck_you.gameinfo_r.select('GameInfo kv[keyname="game"]')[0].gval.string)
	print(fuck_you.steam_id)
	fuck_you.steam_id = 1337
	print(fuck_you.steam_id)
	print(fuck_you.search_paths)
	fuck_you.search_paths = [
			{
				'key': 'game+mod',
				'value': '|gameinfo_path|.'
			},
			{
				'key': 'game',
				'value': 'platforma'
			},
		]
	# tofile
	with open('gameinfo.txt', 'w') as txtfile:
		txtfile.write(fuck_you.tofile())

# multImetrs()