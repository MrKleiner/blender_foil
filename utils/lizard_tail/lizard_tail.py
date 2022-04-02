











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



	def __init__(self, pootis=False):
		import io

		self.gameinfo = {}


	@property
	def shader(self):
		return self.main_vmt['shader']


	@shader.setter
	def shader(self, newshade):
		self.main_vmt['shader'] = str(newshade)

	@property
	def params(self):
		return self.main_vmt['params']

	# reconstruct to vmt
	def to_vmt(self):

		def wr(st, pr=False):
			if pr == True:
				return '"$' + str(st) + '"'
			else:
				return '"' + str(st) + '"'

		vbase = self.main_vmt

		# begin vmt
		vmt_str = ''

		# write shader
		vmt_str += wr(vbase['shader'])

		# open brackets
		vmt_str += '\n'
		vmt_str += '{'

		# skipper = [False, True, None, '']
		# APPARENTLY, 1 == True !!!!!
		skipper = [None, '']

		# write params
		for prm in vbase['params']:
			# Do not write empty shit
			# todo: better logic pls
			if prm.strip() in skipper or str(vbase['params'][prm]).strip() in skipper or vbase['params'][prm] in skipper:
				continue

			vmt_str += '\n\t'
			# write key
			vmt_str += wr(prm, True)
			vmt_str += ' '

			# tuples are supported
			write_val = ''
			if isinstance(vbase['params'][prm], tuple):
				# open vector
				write_val += '['

				# write all values
				for tpv in vbase['params'][prm]:
					write_val += str(tpv)
					write_val += ' '

				# close vector
				write_val += ']'
				# todo: lmfao wtf
				write_val.replace(' ]', ']')
			else:
				write_val += str(vbase['params'][prm])

			vmt_str += wr(write_val)

		# close params
		vmt_str += '\n'
		vmt_str += '}'

		return vmt_str


	# add a dict of params
	def add_params(self, moredict):
		for pr in moredict:
			self.main_vmt[str(pr)] = moredict[pr]

	def setparams(self, pdict):
		self.main_vmt['params'] = pdict





def multImetr():
	from parser import gameinfoparser
	from reconstructor import gameinfo_rebuilder
	import io


	with open(r'E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer\mapbase_episodic_template\gameinfo.txt', 'r') as readf:
		nen = readf.read()

	inpstr = io.StringIO(nen).readlines()

	rst = gameinfoparser(inpstr)

	# gameinfoparser().prettify()
	with open('rc.xml', 'w') as txtfile:
		txtfile.write(rst.prettify())
		# txtfile.write(gameinfoparser(inpstr))

	# gameinfoparser().prettify()
	with open('gameinfo.txt', 'w') as txtfile:
		txtfile.write(gameinfo_rebuilder(rst))



multImetr()