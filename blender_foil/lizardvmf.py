
"""
import io


class lizardvmf:
	"Simple, but flexible vmf parser"
	# anything that is specified becomes defaults. Useful
	id = 10
	name = 'Anderson'
	def __init__(self, pootis):
		from pathlib import Path
		self.pootis = Path(pootis)

	def display(self):
		print(self.pootis.parent)
	
	def settler(self, wat):
		self.id = wat



lizard = lizardvmf(r'C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\screenshots\engi_bucket')

# lizard.display()

# lizard.settler(43)


lizard.display()
lizard.display()
# print(lizard.id)
"""

"""
	@property
	def temperature(self):
		print("Getting value...")
		return self._temperature

	@temperature.setter
	def temperature(self, value):
		print("Setting value...")
		if value < -273.15:
			raise ValueError("Temperature below -273 is not possible")
		self._temperature = value
"""




class lizardvmf_visgroup:
	"""visgroup"""

	# todo: Some defaults ??
	def __init__(self, rt, ct):

		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs
		self.name = ct['name']
		self.visgroupid = ct['visgroupid']



	@property
	def name(self):
		return self.ctag['name']
	
	@name.setter
	def name(self, newname):
		if str(newname).strip() != '' and newname != None:
			self.ctag['name'] = str(newname)
			return True
		else:
			return False


	# get a free id for a visgroup
	def vgetfreeid(self):
		lizard = self.lizard

		# collect all ids here
		taken_ids = []

		# groups share id pool with ents and solids
		for vgid in lizard.select('map visgroups visgroup'):
			if vgid.get('visgroupid') != None:
				taken_ids.append(int(vgid['visgroupid']))

		# store free ids here
		free_ids = None

		# basis
		basis = 4

		# todo: very reliable but slow
		while free_ids == None:
			# basically test all the ids until we find the suitable one
			basis += 1
			if not basis in taken_ids:
				free_ids = basis
				# There should always be enough free ids
				return basis


	# create a new visgroup
	# important todo: Make this function accept custom ids ?
	def add_new(self, vname=None):
		if str(vname).strip() != '' and vname != None:
			lizard = self.lizard
			vgtag = lizard.new_tag('visgroup', visgroupid=str(self.vgetfreeid()), color='202 246 72')
			vgtag['name'] = str(vname)

			self.ctag.append(vgtag)

			return lizardvmf_visgroup(lizard, vgtag)
		else:
			return False


	# properly remove visgroup
	def kill(self):
		lizard = self.lizard
		# first - remove all references to it from solids and ents
		# important todo: it's possible to select multiple things at once with ,
		for ref in lizard.select('map solid editor[visgroupid="' + str(self.ctag['visgroupid']) + '"], map entity editor[visgroupid="' + str(self.ctag['visgroupid']) + '"]'):
			del ref['visgroupid']

		# and finally - commit self die
		self.ctag.decompose()
		return True






class lizardvmf_cordon:
	"""Cordon box"""

	box = None

	# returns box center and scales
	# takes strings as an input...
	# todo: take tuple as an input ?
	def cordon_to_blender(self, mins, maxs):
		import math
		minsplit = mins.replace('(', '').replace(')', '').split(' ')
		maxsplit = maxs.replace('(', '').replace(')', '').split(' ')

		min = (float(minsplit[0]), float(minsplit[1]), float(minsplit[2]))
		max = (float(maxsplit[0]), float(maxsplit[1]), float(maxsplit[2]))

		# x y z
		p1 = (min[0], min[1], max[2])
		p2 = (max[0], min[1], max[2])
		p3 = (max[0], min[1], min[2])
		p4 = (min[0], min[1], min[2])
		p5 = (min[0], max[1], max[2])
		p6 = (max[0], max[1], max[2])
		p7 = (max[0], max[1], min[2])
		p8 = (min[0], max[1], min[2])

		# get distance
		def distance(x1, y1, z1, x2, y2, z2):
			  
			d = math.sqrt(math.pow(x2 - x1, 2) +
						math.pow(y2 - y1, 2) +
						math.pow(z2 - z1, 2)* 1.0)
			return d

		# get 3D modpoint
		def midpoint(n1, n2):
			cx = (n1[0] + n2[0]) / 2
			cy = (n1[1] + n2[1]) / 2
			cz = (n1[2] + n2[2]) / 2
			return (cx, cy, cz)

		oct = (midpoint(p1, p2)[0], midpoint(p4, p8)[1], midpoint(p1, p4)[2])

		obs_x = distance(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2]) / 2
		obs_y = distance(p1[0], p1[1], p1[2], p5[0], p5[1], p5[2]) / 2
		obs_z = distance(p1[0], p1[1], p1[2], p4[0], p4[1], p4[2]) / 2

		pl_badwater = {
			'center': (oct[0], oct[1], oct[2]),
			'scale': (obs_x, obs_y, obs_z),
			'points': [p1, p2, p3, p4, p5, p6, p7, p8]
		}

		return pl_badwater


	# todo: Some defaults ??
	def __init__(self, rt, ct):

		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs
		self.name = ct['name']
		self.active = ct['active']
		# todo: what if box not found ? skip this cordon ?
		self.boxart = ct.select('box')[0]
		# mins and maxs
		# todo: make it also accept cubes ?
		self.box_z = None
		self.box_x = None
		# a cooler way to return box
		# self.box = ((0, 0, 0), (1024, 1024, 1024))


	# takes location and scale tupe, returns mins and maxs
	# important todo: this function was duplicated into the lizardvmf
	# either make these 2 functions external or place them better
	def blender_to_cordon(self, eloc, escale):
		cent = (eloc[0], eloc[1], eloc[2])
		scl = (escale[0], escale[1], escale[2])

		min_x = cent[0] - (scl[0] / 2)
		min_y = cent[1] - (scl[1] / 2)
		min_z = cent[2] - (scl[2] / 2)

		max_x = cent[0] + (scl[0] / 2)
		max_y = cent[1] + (scl[1] / 2)
		max_z = cent[2] + (scl[2] / 2)

		# print(min_x, min_y, min_z)
		# print(max_x, max_y, max_z)

		ret = {
			'mins': (min_x, min_y, min_z),
			'maxs': (max_x, max_y, max_z)
		}
		return ret



	@property
	def active(self):
		if self.ctag['active'] == '1':
			return True
		if self.ctag['active'] == '0':
			return False
	
	@active.setter
	def active(self, cstate):
		if cstate == True:
			self.ctag['active'] = '1'

		if cstate == False:
			self.ctag['active'] = '0'


	@property
	def name(self):
		return self.ctag['name']
	
	@name.setter
	def name(self, newname):
		if str(newname).strip() != '' and newname != None:
			self.ctag['name'] = str(newname)
			return True
		else:
			return False



	@property
	def box(self):
		return self.cordon_to_blender(self.boxart['mins'], self.boxart['maxs'])


	# for now, takes a tuple of two tuples: location, scale, ORDER IS IMPORTANT
	# YES, scale, NOT dimensions
	# made specifically to accept raw params from empty cube objects
	@box.setter
	def box(self, obtr):
		# todo: check if proper syntax was passed

		# mins
		self.boxart['mins'] = ''
		self.boxart['mins'] += '('
		self.boxart['mins'] += str(self.blender_to_cordon(obtr[0], obtr[1])['mins'][0])
		self.boxart['mins'] += ' '
		self.boxart['mins'] += str(self.blender_to_cordon(obtr[0], obtr[1])['mins'][1])
		self.boxart['mins'] += ' '
		self.boxart['mins'] += str(self.blender_to_cordon(obtr[0], obtr[1])['mins'][2])
		self.boxart['mins'] += ')'

		# maxs
		self.boxart['maxs'] = ''
		self.boxart['maxs'] += '('
		self.boxart['maxs'] += str(self.blender_to_cordon(obtr[0], obtr[1])['maxs'][0])
		self.boxart['maxs'] += ' '
		self.boxart['maxs'] += str(self.blender_to_cordon(obtr[0], obtr[1])['maxs'][1])
		self.boxart['maxs'] += ' '
		self.boxart['maxs'] += str(self.blender_to_cordon(obtr[0], obtr[1])['maxs'][2])
		self.boxart['maxs'] += ')'


	# removes the cordon
	def kill(self):
		self.ctag.decompose()
		return True










class lizardvmf_solid_side:
	"""Side of a solid"""

	def __init__(self, rt, ct):
		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs


	# removes the side. Why ??????
	def kill(self):
		self.ctag.decompose()
		return True


	# returns all vertices+, if any
	# lmfao why
	def verts(self):
		all_vp = []
		for vp in self.ctag.select('vertices_plus v'):
			stepstring = vp.string.split(' ')
			all_vp.append((stepstring[0], stepstring[1], stepstring[2]))

		return all_vp







# todo: redundant ?
class lizardvmf_cordons:
	"""A collection of cordons, if any"""

	def __init__(self, rt, ct):
		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs






# takes global map root tag and solid tag as an input
class lizardvmf_solid:
	'Solid (brush) object of the lizard vmf'

	# -(base taken from entity class)-

	# takes bs4 tag and root tag as an input

	lizard = None
	# groupid - redundant?
	# update: For now - yes. This has to be done via @property
	# groupid = None

	# this stores all the attributes
	# yes, it's possible to simply do whatever.prms['whatever'] and whatever.prms['whatever'] = something
	# just like regular bs4 tag
	# todo: Solid doesn't has them (it only has id)
	prms = None

	# bs4 also provides us with the attribute dictionary. Make this available with distinctive name
	# todo: Solid doesn't has them (it only has id)
	prmsdict = None

	# important todo: simply create a variable with editor on init?
	# so that it's possible to access its params as usual...

	# rt - root tag (whole map)
	# ct - current tag
	def __init__(self, rt, ct):
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs
		# self.groupid = ''
		# this has to be pre-declared
		self.visgroup = ''
		self.group = None
		# self.visgroupid = ''
		# self.visgroupshown = ''

	
	# I actually like this variant more than @property fuckery

	def prmquery(self, k, v):
		# self.ctag[k] = v
		
		# if both key and value are present - set it and return true as a confirmation
		if k != None and v != None:
			self.ctag[k] = v
			return True

		# if key is none and val is specified - return key with the following value
		if k == None and v != None:
			return [ke for ke, va in self.prmsdict.items() if va == v]



	# todo: this still could be a function. Just make the function return a value based on a query...
	# update: todo: make this a function too, since keyvalues are functions as well...
	# if no query is passed - return group name and id
	# if set visgroup - return id and name
	@property
	def visgroup(self):
		# print('Getting value...')
		try:
			# todo: don't use try, check if it has visgroupid or not via attribute check
			vgroupid = self.ctag.select('editor')[0]['visgroupid']
			parrot = {
				'id': int(vgroupid),
				'name': self.lizard.select('visgroup[visgroupid="' + vgroupid + '"]')[0]['name']
			}
		except:
			parrot = {'id':'','name':''}
		return parrot


	@visgroup.setter
	def visgroup(self, query):
		# -(copied from entity class)-

		# todo: what if the name of the group is a number too ?
		if len(self.lizard.select('visgroup[visgroupid="' + str(query) + '"]')) > 0 or len(self.lizard.select('visgroup[name="' + str(query) + '"]')):
			if isinstance(query, int):
				# qselector = self.lizard.select('visgroup[visgroupid="' + query + '"]')
				self.ctag.select('editor')[0]['visgroupid'] = str(query)
			else:
				# else - assume that it's a string...
				qselector = self.lizard.select('visgroup[name="' + query + '"]')
				self.ctag.select('editor')[0]['visgroupid'] = qselector[0]['visgroupid']


	# simple groups (id groups n stuff)

	# the @ parametrical shit is kinda obsolete

	# @property
	def group_z(self):
		""" If this entity is in a group - returns group id """
		# print('Getting value...')
		try:
			# todo: don't use try, check if it has visgroupid or not via attribute check
			vgroupid = self.ctag.select('editor')[0]['groupid']
		except:
			vgroupid = None
		return vgroupid


	# @group.setter
	def group_z(self, grpid :int):
		""" Takes either string or an integer as an input, it has """
		# -(partially copied from entity class)-

		# check if we can even do anything
		# todo: regexp???
		try:
			groupid_int = int(grpid)
		except:
			return False

		# if this group exists...
		# todo: check if id exceeds max int ??
		if len(self.lizard.select('map world group[id="' + str(query) + '"]')) > 0:
			# todo: a solid/entity could have no editor
			# create if neccessary ? or skip ?
			self.ctag.select('editor')[0]['groupid'] = str(query)


	# todo: why use properties ?
	# todo: trim stuff, just in case ?
	# if nothing given - returns the group id if any
	# if anything was specified - it'll try to find a group with the given id and assign the entity to it
	def group(self, grpid=None):
		# if groupid is specified then try to set
		if grpid != None:
			# if something was pecified - it mans that we need to try to set shit

			# check if we can even do anything
			try:
				groupid_int = int(grpid)
			except:
				return False

			# if this group exists...
			# todo: check if id exceeds max int ??
			if len(self.lizard.select('map world group[id="' + str(query) + '"]')) > 0:
				# todo: a solid/entity could have no editor
				# create if neccessary ? or skip ?
				self.ctag.select('editor')[0]['groupid'] = str(query)
		else:
			# if None - means we don't need to set anything and just return group id if any

			try:
				# todo: don't use try, check if it has visgroupid or not via attribute check
				vgroupid = self.ctag.select('editor')[0]['groupid']
			except:
				vgroupid = None
			return vgroupid



	# removes the solid
	def kill(self):
		self.ctag.decompose()
		return True


	# removes solid from entity and moves it to world
	def toworld(self):
		lizard = self.lizard
		# csolid = self.ctag

		solid_extracted = self.ctag.extract()
		lizard.select('map world')[0].append(solid_extracted)


	# moves solid to an entity if it's not a displacement
	# either takes a lizard entity or entity id as an input
	def toent(self, tgt_ent):
		lizard = self.lizard

		# cannot be a displacement...
		for sd in self.ctag.select('side'):
			# todo: is it possible to do sd.dispinfo ?
			if len(sd.select('dispinfo')) > 0:
				return False

		# todo: check if current tag has id ??

		# by entity class
		if isinstance(tgt_ent, lizardvmf_entity):
			# tgt_ent.add_solid(self.ctag['id'])
			extracted_solid = self.ctag.extract()
			lizard.select('map entity[id="' + str(self.ctag['id']) + '"]')[0].append(extracted_solid)
			return True

		# by entity id
		if isinstance(tgt_ent, int):
			# tgt_ent.add_solid(self.ctag['id'])
			extracted_solid = self.ctag.extract()
			lizard.select('map entity[id="' + str(tgt_ent) + '"]')[0].append(extracted_solid)
			return True

		# important todo: There should be a centralized system of returning success or whatever??
		# todo: should it return the solid? Would be pretty useful when id was passed...
		

	# returns all the sides of a solid
	def sides(self):
		colsides = []
		for sol_side in self.ct.select('side'):
			colsides.append(lizardvmf_solid_side(self.lizard, self.ct))
		return colsides




# a collection of connections
# todo: make them all attributes ????
# todo: make this also accept a dict to overwrite current shit
class lizardvmf_connection:
	"""Connection"""

	def __init__(self, rt, ct):
		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs


		# set defaults
		# self.tgt_ents = ''
		# self.action = ''
		# self.params = ''
		# self.delay = ''
		# self.refire_limit = ''


	# todo: check if there are enough commas
	@property
	def tgt_ents(self):
		return self.ctag.string.split(',')[0]

	@tgt_ents.setter
	def tgt_ents(self, newtgt):
		val_set = self.ctag.string.split(',')
		val_set[0] = str(newtgt)
		self.ctag.string = ','.join(val_set)
		# todo: return dict instead
		return ','.join(val_set)


	@property
	def action(self):
		return self.ctag.string.split(',')[1]

	@action.setter
	def action(self, newact):
		val_set = self.ctag.string.split(',')
		val_set[1] = str(newact)
		self.ctag.string = ','.join(val_set)
		# todo: return dict instead
		return ','.join(val_set)


	@property
	def params(self):
		return self.ctag.string.split(',')[2]

	@params.setter
	def params(self, newprm):
		val_set = self.ctag.string.split(',')
		val_set[2] = str(newprm)
		self.ctag.string = ','.join(val_set)
		# todo: return dict instead
		return ','.join(val_set)

	
	@property
	def delay(self):
		try:
			proper = float(self.ctag.string.split(',')[3])
		except:
			proper = str(self.ctag.string.split(',')[3])

		return proper

	@delay.setter
	def delay(self, newdl):
		val_set = self.ctag.string.split(',')
		val_set[3] = str(newdl)
		self.ctag.string = ','.join(val_set)
		# todo: return dict instead
		return ','.join(val_set)


	@property
	def refire_limit(self):
		try:
			proper = float(self.ctag.string.split(',')[4])
		except:
			proper = str(self.ctag.string.split(',')[4])
		
		return proper

	@refire_limit.setter
	def refire_limit(self, newrefire):
		val_set = self.ctag.string.split(',')
		val_set[4] = str(newrefire)
		self.ctag.string = ','.join(val_set)
		# todo: return dict instead
		return ','.join(val_set)


	@property
	def output_name(self):
		return self.ctag.name

	@output_name.setter
	def output_name(self, newtgname):
		if newtgname != None:
			self.ctag.name = str(newtgname)
			return True
		else:
			return False


		







# a collection of connections
class lizardvmf_connections:
	"""connection collection"""

	def __init__(self, rt, ct):
		# super(lizardvmf_solid_side, self).__init__()
		# self.material = arg
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs


	@property
	def items(self):
		allchilds = []
		for cnt in self.ctag.children:
			allchilds.append(lizardvmf_connection(self.lizard, cnt))

		return allchilds

	# add a connection
	def add(self, ctype=None, actiondict=None):
		"""
		Expects following params either in order or named:

		ctype - input type (My output named), like "OnPressed"

		actiondict - a dictionary of the actions where:
			tgt_ents - Target entities named
			action - Via this input
			params - With a parameter override of
			delay - Fire after delay in seconds of (accepts ints and floats)
			refire_limit - Limit to this many fires (-1 = infinite) (accepts ints and floats)

		"""

		if ctype != None and actiondict != None:
			lizard = self.lizard
			# todo: for now - silently delete spaces
			newc = lizard.new_tag(str(ctype).replace(' ', ''))

			# todo: is it possible to use += with .string ?
			gm_construct = ''

			gm_construct += actiondict['tgt_ents']
			gm_construct += ','
			gm_construct += actiondict['action']
			gm_construct += ','
			gm_construct += actiondict['params']
			gm_construct += ','
			gm_construct += str(actiondict['delay'])
			gm_construct += ','
			gm_construct += str(actiondict['refire_limit'])

			newc.string = gm_construct

			self.ctag.append(newc)

			return lizardvmf_connection(lizard, newc)





# todo: don't forget that entity could have a solid
class lizardvmf_entity:
	'Entity object of the lizard vmf'
	# A little easier acces of k:v
	# An ability to distinguish editor k:v and base k:v
	# takes bs4 tag and root tag as an input

	lizard = None
	# redundant?
	# update: For now - yes. This has to be done via @property
	# groupid = None
	# this stores all the attributes
	# yes, it's possible to simply do whatever.prms['whatever'] and whatever.prms['whatever'] = something
	# just like regular bs4 tag
	prms = None

	# bs4 also provides us with the attribute dictionary. Make this available with distinctive name
	prmsdict = None

	# important todo: simply create a variable with editor on init?
	# so that it's possible to access its params as usual...

	# rt - root tag (whole map)
	# ct - current tag
	def __init__(self, rt, ct):
		# (root tag)
		self.lizard = rt
		# it's possible to access the bs4 object via this variable (this is a bs4 tag object)
		self.ctag = ct
		# since it's a pointer it will work just fine. Same as ctag, but with a different name for consistency
		self.prms = ct
		# same as .prms, but it's a dict. Is it settable?? Should be...
		self.prmsdict = ct.attrs
		# self.groupid = ''
		# this has to be pre-declared
		self.visgroup = ''
		# self.visgroupid = ''
		# self.visgroupshown = ''

	
	# I actually like this variant more than @property fuckery

	def prmquery(self, k, v):
		# self.ctag[k] = v
		
		# if both key and value are present - set it and return true as a confirmation
		if k != None and v != None:
			self.ctag[k] = v
			return True

		# if key is none and val is specified - return key with the following value
		if k == None and v != None:
			return [ke for ke, va in self.prmsdict.items() if va == v]



	"""
	def editor_z(self, key, value):
		self.ctag.select('editor')[0][key] = value

	def tovisgroup(self, vgname):
		lizard = self.lizard
		found_id = lizard.select('visgroup[name="' + vgname + '"]')[0]['id']
	"""


	# todo: this still could be a function. Just make the function return a value based on a query...
	# update: todo: make this a function too?? since keyvalues are functions as well...
	# if no query is passed - return group name and id
	# if set visgroup - return id and name
	@property
	def visgroup(self):
		# print('Getting value...')
		try:
			# todo: don't use try, check if it has visgroupid or not via attribute check
			vgroupid = self.ctag.select('editor')[0]['visgroupid']
			parrot = {
				'id': int(vgroupid),
				'name': self.lizard.select('visgroup[visgroupid="' + vgroupid + '"]')[0]['name']
			}
		except:
			parrot = {'id':'','name':''}
		return parrot


	@visgroup.setter
	def visgroup(self, query):
		"""
		Either takes int or a string
		If string - look for visgroup with the name
		If int - look for visgroup with id
		"""

		# print('Setting value...')
		"""
		if value < -273.15:
			raise ValueError("Temperature below -273 is not possible")
		self._temperature = value
		"""

		# first - decide if we want to search by id or name
		# main task is to get a valid visgroupid and then add it to the editor of the current tag
		# logic is simple: If no valid visgroup is found - just don't do anything because fuck you
		"""
		if isinstance(query, int):
			qselector = self.lizard.select('visgroup[visgroupid="' + query + '"]')
			qtype = 'visgroupid'
		else:
			# else - assume that it's a string...
			qselector = self.lizard.select('visgroup[name="' + query + '"]')
			qtype = 'name'

		# only do shit if query has returned anything
		if len(qselector) > 0:
			pass
		"""

		# todo: what if the name of the group is a number too ?
		if len(self.lizard.select('visgroup[visgroupid="' + str(query) + '"]')) > 0 or len(self.lizard.select('visgroup[name="' + str(query) + '"]')):
			if isinstance(query, int):
				# qselector = self.lizard.select('visgroup[visgroupid="' + query + '"]')
				self.ctag.select('editor')[0]['visgroupid'] = str(query)
			else:
				# else - assume that it's a string...
				qselector = self.lizard.select('visgroup[name="' + query + '"]')
				self.ctag.select('editor')[0]['visgroupid'] = qselector[0]['visgroupid']


	# todo: why use properties ?
	# if nothing given - returns the group id if any
	# if anything was specified - it'll try to find a group with the given id and assign the entity to it
	def group(self, grpid=None):
		# if groupid is specified then try to set
		if grpid != None:
			# if something was pecified - it mans that we need to try to set shit

			# check if we can even do anything
			try:
				groupid_int = int(grpid)
			except:
				return False

			# if this group exists...
			# todo: check if id exceeds max int ??
			if len(self.lizard.select('map world group[id="' + str(query) + '"]')) > 0:
				# todo: a solid/entity could have no editor
				# create if neccessary ? or skip ?
				self.ctag.select('editor')[0]['groupid'] = str(query)
		else:
			# if None - means we don't need to set anything and just return group id if any

			try:
				# todo: don't use try, check if it has visgroupid or not via attribute check
				vgroupid = self.ctag.select('editor')[0]['groupid']
			except:
				vgroupid = None
			return vgroupid



	# removes the entity
	def kill(self):
		self.ctag.decompose()
		return True


	# adds solid to the entity if it's not a displacement
	# takes either solid id or solid class as an input
	# todo: what if solid has no id ? add one ?
	def add_solid(self, tgt_solid):
		# -(base copied from lizard solid toent)-

		lizard = self.lizard

		extracted_solid = None

		# by solid class
		if isinstance(tgt_solid, lizardvmf_solid):
			extracted_solid = lizard.select('map solid[id="' + tgt_solid.prms['id'] + '"]')[0].extract()

		# by solid id
		if isinstance(tgt_solid, int):
			# tgt_solid.add_solid(self.ctag['id'])
			extracted_solid = lizard.select('map solid[id="' + str(tgt_solid) + '"]')[0].extract()
			
		# check if we got any solids
		if extracted_solid == None:
			return False

		# cannot be a displacement...
		for sd in self.ctag.select('side'):
			# todo: is it possible to do sd.dispinfo ?
			if len(sd.select('dispinfo')) > 0:
				return False

		# if passed checks - append
		self.ctag.append(extracted_solid)
		return True


	# returns a collection of solids of the current entity
	# todo: make a property again ?
	# @property
	def solids(self):
		solid_collection = []
		for sl in self.ctag.select('solid'):
			solid_collection.append(lizardvmf_solid(self.lizard, sl))
		return solid_collection


	# return connections, if any
	# returns False if no connections for this entity
	# todo: return empty array ?
	# important todo: create if none? Not too big of a deal anyway...
	@property
	def connections(self):
		if len(self.ctag.select('connections')) > 0:
			return(lizardvmf_connections(self.lizard, self.ctag.select('connections')[0]))
		else:
			return False

	# if passed true - adds connection param
	# if passed false - kills everything
	# todo: "kills everything" should also be a function of the connections class
	@connections.setter
	def connections(self, yesno):
		if yesno == True:
			mk_connections = self.lizard.new_tag('connections')
			self.ctag.append(mk_connections)

		if yesno == False:
			# important todo: finally use .find, it returns none if nothing was found
			get_connections = self.ctag.select('connections')
			if len(get_connections) > 0:
				get_connections.decompose()













# you can add (and store) variables to class with internal functions via self.whatever
# you can also have this name pre-defined and then overwrite it.
# All imports should happen in init. It will be reusable in all the other functions.
# todo: make all spawners round shit if neccessary and basically do some fixups
# todo: pyvmf-like spawner: .Child('whatever', {}) n shit
# todo: int's kinda possible to specify data type like int: whatever

# important todo: apparently, solid or entity could belong to mulptiple visgroups
class lizardvmf:
	'Simple, but flexible vmf parser, read more at https://mrkleiner.github.io/source_tricks/?lt=b50a2cad'
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

	# The beautiful soup object. None by default
	# This is a refined vmf xml bs4 object for manipulations and modifications
	lizard = None

	# The result of reconstructed vmf, None by default
	# Gotta be careful since this could give outdated results
	# exists because what if you'd need to access this multiple times ?
	# Let this be a little secret feature
	readyvmfstr = None




	#
	# Functionality
	#



	# Supposedly, the parse should happen when the class is being created...
	# important todo: with all respect, this has to be an external function...
	# as well as reconstructor
	def __init__(self, pootis):
		from bs4 import BeautifulSoup, Tag, NavigableString
		import io
		import base64

		# confirmed to work with
		# Half Life 2 and Episodes

		# kind of confirmed to work with
		# Gmod
		# CS GO
		# TF 2
		# CS Source
		# Portal, Portal 2
		# Left 4 Dead, l4d2
		# DOD

		# important todo: it appears that this class has a serious weakness:
		# creating a map from scratch is fucking hard
		# for now just use the base from gmod
		# pro tip: Fuck notepad++ b64 encoder...
		newdefault = """
			dmVyc2lvbmluZm8KewoJImVkaXRvcnZlcnNpb24iICI0MDAiCgkibWFwdmVyc2lvbiIgIjAiCgkiZm9ybWF0dmVyc2l
			vbiIgIjEwMCIKCSJwcmVmYWIiICIwIgp9CnZpZXdzZXR0aW5ncwp7CgkiYlNuYXBUb0dyaWQiICIxIgoJImJTaG93R3
			JpZCIgIjEiCgkiYlNob3dMb2dpY2FsR3JpZCIgIjAiCgkibkdyaWRTcGFjaW5nIiAiNjQiCgkiYlNob3czREdyaWQiI
			CIwIgp9CndvcmxkCnsKCSJpZCIgIjEiCgkibWFwdmVyc2lvbiIgIjEiCgkiY2xhc3NuYW1lIiAid29ybGRzcGF3biIK
			CSJza3luYW1lIiAic2t5X2RheTAxXzAxIgoJIm1heHByb3BzY3JlZW53aWR0aCIgIi0xIgoJImRldGFpbHZic3AiICJ
			kZXRhaWwudmJzcCIKCSJkZXRhaWxtYXRlcmlhbCIgImRldGFpbC9kZXRhaWxzcHJpdGVzIgp9CmNhbWVyYXMKewoJIm
			FjdGl2ZWNhbWVyYSIgIi0xIgp9CmNvcmRvbnMKewoJImFjdGl2ZSIgIjAiCn0K
		"""

		# pass True to the class instead of vmf to create a new vmf
		if pootis == True:
			inpstr = io.StringIO(base64.b64decode(newdefault.replace('\n', '').replace(' ', '').encode('utf-8')).decode('utf-8'))
		else:
			# Since we're not dealing with files anymore (at least for now) - we cannot just do .readlines()
			# gotta use io module
			inpstr = io.StringIO(pootis)

		# so that we have access to .readlines() again
		maplines = inpstr.readlines()

		# print(maplines)

		# we no longer create a file, we store processed raw vmf in a variable
		# this stores super raw unrefined xml
		rawvmf = ''

		# open xml root
		rawvmf += ('<map>' + '\n')

		for mpindex, mapline in enumerate(maplines):
			# try, because invalid index appears when we reach the very last line of the string
			try:
				if '{\n' in maplines[mpindex + 1]:
					rawvmf += (mapline.replace(maplines[mpindex].strip(), '').replace('\n', '') + '<item type="' + maplines[mpindex].strip() + '">' + '\n')
					maplines[mpindex] = ''
					# print(maplines[mpindex])
			except:
				pass

			if '}\n' in mapline:
				rawvmf += (mapline.replace('}\n', '') + '</item>' + '\n')


			if not '}\n' in mapline and not '{\n' in mapline:
				rawvmf += (maplines[mpindex])

		rawvmf += ('</map>')



		#
		# refinery
		#

		# This will be a bs4 xml object
		# It will be modified (refined)
		lizard = BeautifulSoup(rawvmf, 'html.parser', multi_valued_attributes=None)

		# print(lizard.select('map item[type="entity"]')[13].next_element)
		# print(lizard.select('map item[type="world"]')[0].next_element)



		# rename tags to their corresponding namez
		# todo: name them the proper way right away ?
		for etname in lizard.select('map item'):
			etname.name = etname['type']
			del etname['type']




		# no quickhide support yet
		# todo: hide afterwards by entity id ??
		for sas in lizard.select('map hidden'):
			sas.unwrap()
		try:
			lizard.select('map quickhide')[0].decompose()
		except:
			pass


		# format version info
		"""
		vsinfo = lizard.select('map item[type="versioninfo"]')[0]
		for ses in vsinfo.next_element.strip().split('\n'):
			print(ses.strip())
			vsinfo[ses.strip().split('" "')[0].replace('"', '')] = ses.strip().split('" "')[1].replace('"', '')
		vsinfo.next_element.extract()
		# print(dir(vsinfo.next_element))
		# print(vsinfo.contents[0].string)
		print(vsinfo)
		"""


		# format visgroups
		visgroups = lizard.select('map visgroup')

		for vgr in visgroups:
			for ses in vgr.next_element.strip().split('\n'):
				print(ses.strip())
				vgr[ses.strip().split('" "')[0].replace('"', '')] = ses.strip().split('" "')[1].replace('"', '')

			vgr.next_element.extract()

		print(visgroups)



		# todo: why is this commented out
		# format viewsettings
		"""
		viewsettings = lizard.select('map item[type="viewsettings"]')[0]
		for vst in viewsettings.next_element.strip().split('\n'):
			print(vst.strip())
			viewsettings[vst.strip().split('" "')[0].replace('"', '')] = vst.strip().split('" "')[1].replace('"', '')

		viewsettings.next_element.extract()
		print(viewsettings)
		"""


		# todo: add parent name to the element name for more precise hierarchy ?
		# update: which parent ?

		# format type "move exposed key-values to group name"
		forma = ['versioninfo', 'viewsettings', 'world', 'editor', 'entity', 'side', 'solid', 'dispinfo', 'cordons', 'cordon', 'box', 'cameras', 'camera', 'group']

		for fm in forma:
			select_frm = lizard.select('map ' + fm)
			# for every element that matched a query
			for sks in select_frm:
				# sexy red strings
				collected_strings = []
				# for every direct child check if it's a string. If so - collect it
				for dch in sks.children:
					# isinstance
					if isinstance(dch, NavigableString):
						collected_strings.append(dch)
				
				# then, do shit with them
				for vst in '\n'.join(collected_strings).strip().split('\n'):
					if vst.strip() != '':
						print(vst.strip())
						sks[vst.strip().split('" "')[0].replace('"', '')] = vst.strip().split('" "')[1].replace('"', '')

				# after that - remove these strings from the fucking shit
				for rmstring in collected_strings:
					rmstring.extract()
			# print(select_frm)





		# format type "convert exposed key-values to tag"
		kv2tag = ['normals', 'distances', 'offsets', 'offset_normals', 'alphas', 'triangle_tags', 'vertices_plus', 'connections', 'multiblend', 'alphablend', 'multiblend_color_0', 'multiblend_color_1', 'multiblend_color_2', 'multiblend_color_3']
		for kvt in kv2tag:
			select_kv2tags = lizard.select('map ' + kvt)
			for sgw in select_kv2tags:
				raw_data = sgw.next_element
				# todo: no next element. Do collection
				sgw.next_element.extract()
				for vhs in raw_data.strip().split('\n'):
					print(vhs.strip())
					# such a beautiful one-liner went terribly wrong
					# sgw.append(lizard.new_tag(vhs.strip().split('" "')[0].replace('"', '')).append(NavigableString(vhs.strip().split('" "')[1].replace('"', ''))))
					# print('tag name:' + vhs.strip().split('" "')[0].replace('"', ''))
					# print('tag value:' + vhs.strip().split('" "')[1].replace('"', ''))

					# Only if there are children
					if len(raw_data.strip()) > 0:
						mktg = lizard.new_tag(vhs.strip().split('" "')[0].replace('"', ''))
						try:
							# important todo: Replace them stupid bytes right away in the very beginning of parsing the whole thing?
							mktg.string = vhs.strip().split('" "')[1].replace('"', '').replace('', ',')
						except:
							mktg.string = vhs.strip() + 'FIXME EXCEPTION FFS. Children size:' + str(len(raw_data.strip()))
						print(mktg)
						sgw.append(mktg)
					# print(mktg.name)


				
			# print(select_frm)





		# end refinery
		# save back
		self.lizard = lizard


	# Reconstructor. The coolest part. Kind of
	# This will convert xml to a valid .vmf string
	# and store it in class
	# Theoretically, this should NOT do anything with the xml
	# important todo: with all respect, this has to be an external function...
	# as well as init :(
	def tovmf(self):
		#
		# reconstruct
		#


		# - define some reusables -


		# wrap into quotation marks
		def wap(ste):
			return '"' + str(ste) + '"'

		# takes key name, object, wether to insert line break or not and number of tabs, returns reconstruct string
		# converts given attribute name of a tag to .vmf standard key - value
		def wapr(itr, ob, brk, tabs):
			mktabs = ''
			for iguana in range(int(tabs)):
				mktabs += '\t'
			
			if int(brk) == 1:
				return mktabs + wap(itr) + ' ' + wap(ob[itr]) + '\n'
			else:
				return mktabs + wap(itr) + ' ' + wap(ob[itr])

		# takes tag as an input and number of tabs, returns unwrap
		def unwapr(tg, nt):
			mktabs = ''
			for iguana in range(int(nt)):
				mktabs += '\t'
			return mktabs + wap(tg.name) + ' ' + wap(tg.string) + '\n'

		# open block with tabs and opening bracket
		def op(tgname, ntc):
			mktabs = ''
			for iguana in range(int(ntc)):
				mktabs += '\t'
			return mktabs + tgname + '\n' + mktabs + '{\n'

		# close block
		def cl(tabz):
			mktabs = ''
			for iguana in range(int(tabz)):
				mktabs += '\t'
			return mktabs + '}\n'



		# - start reconstruction -


		# first, grab the bs object from the class
		lizard = self.lizard

		# again, we no longer use files (for now at least)
		# define a variable to write the reconstruct to.
		# then, write it to class and return the reconstruct
		rcf = ''


		# reconstruct versioninfo and viewsettings, if any
		if len(lizard.select('versioninfo')) > 0 or len(lizard.select('viewsettings')) > 0:
			common_pre_world = ['versioninfo', 'viewsettings']
			for kingdom_cum in common_pre_world:
				# check if current selection exists
				if len(lizard.select('map ' + kingdom_cum)) > 0:
					rcf += (op(kingdom_cum, 0))
					# for every versioninfo k:v of the current map
					for cum_kv in lizard.find(kingdom_cum).attrs:
					   rcf += (wapr(cum_kv, lizard.find(kingdom_cum).attrs, 1, 1))
					rcf += (cl(0))



		#
		# start construct visgroups, if any
		#
		if len(lizard.select('map visgroups')) > 0:
			print(lizard.select('map visgroups')[0].prettify())
			# for every visgroup in the map visgroups group
			for vgr_kv in lizard.select('map visgroups visgroup'):
				# collect tag attributes into a string and delete them afterwards
				gecko = []
				# for every k:v (from attr) of the current visgroup
				for vs_kv in vgr_kv.attrs:
					# collect attributes to delete
					gecko.append(vs_kv)
					# del vgr_kv[vs_kv]
					smart_shit = lizard.new_tag('lmfao')
					smart_shit.string = wapr(vs_kv, vgr_kv.attrs, 0, 0)
					vgr_kv.append(smart_shit)
				# delete attributes
				for rmattr in gecko:
					del vgr_kv[rmattr]


			print(lizard.select('map visgroups')[0].prettify())
			constructed_vgroups = lizard.select('map visgroups')[0].prettify().split('\n')

			for indegz, fuck in enumerate(constructed_vgroups):
				# print(fuck)
				writeshit = fuck
				# get indentation
				startwhites = fuck[:len(fuck)-len(fuck.lstrip())]
				if '<visgroup' in fuck:
					# rcf += (startwhites + 'visgroup\n' + startwhites + '{\n')
					writeshit = startwhites + 'visgroup\n' + startwhites + '{\n'
				if '</visgroup>' in fuck: 
					writeshit = startwhites + '}\n'
				if '<lmfao>' in fuck or '</lmfao>' in fuck:
					writeshit = '\n'

				if '<visgroups' in fuck:
					writeshit = 'visgroups\n{\n'
				if '</visgroups>' in fuck:
					writeshit = '}\n'
				# write result
				rcf += (writeshit)

			#
			# end construct visgroups
			#





		#
		# reconstruct world
		#
		rcf += (op('world', 0))
		world_attrs = lizard.select('map world')[0].attrs
		for wattr in world_attrs:
			rcf += (wapr(wattr, world_attrs, 1, 1))



		# construct world solids
		# for every solid of the current map
		for wrsolid in lizard.select('world solid'):
			# open solid
			rcf += (op('solid', 1))
			rcf += (wapr('id', wrsolid, 1, 2))
			# construct sides
			# get all current sides
			csides = wrsolid.find_all('side')
			# for every side of a current solid
			for wrside in csides:
				# open side
				rcf += (op('side', 2))
				# for every keyvalue of a current side
				for cside_kv in wrside.attrs:
					rcf += (wapr(cside_kv, wrside.attrs, 1, 3))

				# reconstruct hammer vertices plus
				# todo: for now - require hammer++
				# done. hammer++ not required
				if len(wrside.select('vertices_plus')) > 0:
					rcf += (op('vertices_plus', 3))
					# for every vert+ (tag) in the current side, if any
					for vplus in wrside.find('vertices_plus'):
						rcf += (unwapr(vplus, 4))
					rcf += (cl(3))


				# a side COULD have displacement
				# print(len(wrside.select('dispinfo ' + 'normals')))
				if len(wrside.select('dispinfo')) > 0:
					# write disp info k-v
					# open disp info
					rcf += (op('dispinfo', 3))
					# for every k-v of the current disp info
					for dsp_kv in wrside.select('dispinfo')[0].attrs:
						rcf += (wapr(dsp_kv, wrside.select('dispinfo')[0].attrs, 1, 4))

					# by far not always a displacement has all the components
					disp_info = ['normals', 'distances', 'offsets', 'offset_normals', 'alphas', 'triangle_tags', 'multiblend', 'alphablend', 'multiblend_color_0', 'multiblend_color_1', 'multiblend_color_2', 'multiblend_color_3']
					# for every possible info of the current side disp info
					for dsinfo in disp_info:
						# if this info exists - do shit
						if len(wrside.select('dispinfo ' + dsinfo)) > 0:
							rcf += (op(dsinfo, 4))
							# for every keyvalue (tag) of the current block
							for dsinfo_kv in wrside.select('dispinfo ' + dsinfo)[0].children:
								rcf += (unwapr(dsinfo_kv, 5))
							rcf += (cl(4))

					# write allowed verts
					# wtf does it mean even
					# does every displacement has it ??????
					if len(wrside.select('dispinfo allowed_verts')) > 0: 
						rcf += (op('allowed_verts', 4))
						rcf += ('\t\t\t\t\t' + wrside.select('dispinfo allowed_verts')[0].string.strip() + '\n')
						rcf += (cl(4))

					# close disp info
					rcf += (cl(3))

				# close side
				rcf += (cl(2))
			
			# reconstruct editor, IF ANY
			if len(wrsolid.select('editor')) > 0:
				rcf += (op('editor', 2))
				# for every editor k:v of the current solid
				for editor_kv in wrsolid.find('editor').attrs:
				   rcf += (wapr(editor_kv, wrsolid.find('editor'), 1, 3))
				# close editor
				rcf += (cl(2))

			# close solid
			rcf += (cl(1))



		# reconstruct groups, if any
		if len(lizard.select('world group')) > 0:
			# for every group in the current world
			for wrgroup in lizard.select('world group'):
				# open group
				rcf += (op('group', 1))
				# current group k:v
				for cgrp_kv in wrgroup.attrs:
					rcf += (wapr(cgrp_kv, wrgroup.attrs, 1, 2))

				# group editor, IF ANY
				if len(wrgroup.select('editor')) > 0:
					rcf += (op('editor', 2))
					# for every editor k:v of the current group
					for cum_kv in wrgroup.find('editor').attrs:
					   rcf += (wapr(cum_kv, wrgroup.find('editor').attrs, 1, 3))
					# close editor
					rcf += (cl(2))

				# close group
				rcf += (cl(1))

		# close world
		#
		rcf += (cl(0))





		# reconstruct entities, IF ANY
		# for every entity on a map
		if len(lizard.select('map entity')) > 0:
			for wrent in lizard.select('map entity'):
				# open entity
				rcf += (op('entity', 0))
				# current entity k:v
				for cent_kv in wrent.attrs:
					rcf += (wapr(cent_kv, wrent.attrs, 1, 1))

				# Write connections if any
				if len(wrent.select('connections')) > 0:
					# open connections
					rcf += (op('connections', 1))
					for cnt in wrent.select('connections')[0].children:
						rcf += (unwapr(cnt, 2))
					rcf += (cl(1))


				# write solids, if any
				if len(wrent.select('solid')) > 0:
					# for every solid in the current entity
					for esolid in wrent.select('solid'):
						# open solid
						rcf += (op('solid', 1))
						rcf += (wapr('id', esolid, 1, 2))
						# construct sides
						# get all current sides
						csides = esolid.find_all('side')
						# for every side of a current solid
						for wrside in csides:
							# open side
							rcf += (op('side', 2))
							# for every keyvalue of a current side
							for cside_kv in wrside.attrs:
								rcf += (wapr(cside_kv, wrside.attrs, 1, 3))

							# reconstruct hammer vertices plus, IF ANY
							# todo: for now - require hammer++
							# Done. No hammer++ required
							if len(wrside.select('vertices_plus')) > 0:
								rcf += (op('vertices_plus', 3))
								# for every vert+ (tag) in the current side
								for vplus in wrside.find('vertices_plus'):
									rcf += (unwapr(vplus, 4))
								# close v+
								rcf += (cl(3))
							# close side
							rcf += (cl(2))
						# close solid
						rcf += (cl(1))



				# write editor, IF ANY
				if len(wrent.select('editor')) > 0:
					rcf += (op('editor', 1))
					# for every editor k:v of the current entity
					for cent_ed_kv in wrent.find('editor').attrs:
					   rcf += (wapr(cent_ed_kv, wrent.find('editor').attrs, 1, 2))
					# close editor
					rcf += (cl(1))

				# close entity
				rcf += (cl(0))

		# end reconstructing entities


		# reconstruct cameras
		# write global cameras k:v
		rcf += (op('cameras', 0))
		# for every gl camera k:v of the map
		for glcam_kv in lizard.select('map cameras')[0].attrs:
		   rcf += (wapr(glcam_kv, lizard.select('map cameras')[0].attrs, 1, 1))

		# write actual cameras
		# for every childcam k:v of the map
		for chcam in lizard.select('map cameras camera'):
			# open camera
			rcf += (op('camera', 1))
			# for every ch camera k:v of the map
			for chcam_kv in chcam.attrs:
			   rcf += (wapr(chcam_kv, chcam.attrs, 1, 2))
			# close camera
			rcf += (cl(1))

		# close global cameras
		rcf += (cl(0))



		# reconstruct cordons, IF ANY
		# keep in mind that sometimes in old map files we only have one cordon
		if len(lizard.select('cordons cordon')) > 0:
			# write global cordons k:v
			rcf += (op('cordons', 0))
			# for every gl cordons k:v of the map
			for glcor_kv in lizard.select('map cordons')[0].attrs:
			   rcf += (wapr(glcor_kv, lizard.select('map cordons')[0].attrs, 1, 1))

			# write actual cordons
			# for every childcam k:v of the map
			for chcor in lizard.select('map cordons cordon'):
				# open cordon
				rcf += (op('cordon', 1))
				# for every current camera k:v of the map
				for chcor_kv in chcor.attrs:
				   rcf += (wapr(chcor_kv, chcor.attrs, 1, 2))

				# write cordon box
				rcf += (op('box', 2))
				# for every box k:v of the current entity, IF ANY
				for cent_box_kv in chcor.find('box').attrs:
				   rcf += (wapr(cent_box_kv, chcor.find('box').attrs, 1, 3))
				# close box
				rcf += (cl(2))

				# close cordon
				rcf += (cl(1))

			# close global cordons
			rcf += (cl(0))
		else:
			# try to locate the one-box cordon
			# todo: drop support for this retarded shit, force users to use h++ and convert parsed old vmfs to new format
			# if on refinery onebox cordon detected - create cordons and append that box there
			cordonlocate = lizard.select('map > cordon')
			if len(cordonlocate) > 0:
				rcf += (op('cordon', 0))
				# for every versioninfo k:v of the current map
				for cum_kv in cordonlocate[0].attrs:
				   rcf += (wapr(cum_kv, cordonlocate[0].attrs, 1, 1))
				rcf += (cl(0))


		# finally, write reconstruct back and return the string
		self.readyvmf = rcf
		return rcf


	# Returns a dict of basic stats
	def vmfstats(self):
		stats = {}

		lizard= self.lizard

		# basic info



		# -- number of entities --

		# static props do not count
		allowance_ents = {
			'hl2': 4096,
			'tf2': 4096,
			'portal2': 8192,
			'csgo': 8192,
			'gmod': 16384
		}

		ent_edict = 0
		notcount = ['prop_static', 'sprite_clientside', 'prop_detail']

		for ent in lizard.select('map entity'):
			if not ent['classname'] in notcount:
				ent_edict += 1

		stats['ents_enum_edict'] = ent_edict
		stats['ents_total'] = len(lizard.select('map entity'))



		# -- brushes and faces stats --

		# nodraws do not count
		# 128 faces max per single brush
		# 32768 faces overall (it's a plane limit, each face uses 2 planes. 65536‬)
		allowance_brush = {
			'hl2': 8192,
			'tf2': 8192,
			'portal2': 8192,
			'csgo': 8192,
			'gmod': 16384
		}
		faces_edict = 0
		for side in lizard.select('map solid side'):
			if not 'toolsnodraw' in side['material'].lower():
				faces_edict += 1

		stats['faces_enum_edict'] = faces_edict
		stats['faces_total'] = len(lizard.select('map solid side'))
		stats['brushes_edict'] = len(lizard.select('map solid'))



		# -- face limit per brush. 128 --
		anybad = False
		badstats = {}
		for tside in lizard.select('map solid'):
			if len(tside.select('side')) > 127:
				anybad = True
				badstats[tside['id']] = len(tside.select('side'))

		if anybad == True:
			# write badsolids anyway? For consistency?
			stats['badsolids'] = True
			stats['bad_info'] = badstats

		return stats


	# append point entity
	# def add_ent(self, prmdict, mkid):


	# return matches
	def vmfquery(self, qr):
		lizard = self.lizard
		selector = ''
		
		# todo: repeating code
		# todo: query itself could contain special symbols. Temp solution: only look at the very first character?

		# Since ids are PRESUMABLY unique, here we should only return the first match...
		if '#' in qr:
			selector = 'map entity[id="' + qr.split('#')[-1] + '"]'
			if len(lizard.select(selector)) > 0:
				return lizardvmf_entity(lizard, lizard.select(selector)[0])
			else:
				return None

		# select solids by id
		# todo: use something else than ^, % for example
		if '^' in qr:
			selector = 'map solid[id="' + qr.split('^')[-1] + '"]'
			if len(lizard.select(selector)) > 0:
				return lizardvmf_solid(lizard, lizard.select(selector)[0])
			else:
				return None



		# select by targetname (name)
		if '$' in qr:
			# construct selector by targtname which will probably return many entries
			selector = 'map entity[targetname="' + qr.split('$')[-1] + '"]'
			# if selector returns anything - create an array of returned results
			# in a form of lizardvmf_entity
			if len(lizard.select(selector)) > 0:
				qresults = []
				for q in lizard.select(selector):
					qresults.append(lizardvmf_entity(lizard, q))
				return qresults
			else:
				return None


		# any keyvalue query
		# example: ~fogMaxDensity=1
		# todo: make this accept something smarter than that
		if '~' in qr:
			parts = qr.split('~')[-1].split('=')
			selector = 'map entity[' + parts[0] + '="' + parts[-1] + '"]'
			if len(lizard.select(selector)) > 0:
				qresults = []
				for q in lizard.select(selector):
					qresults.append(lizardvmf_entity(lizard, q))
				return qresults
			else:
				# todo (also applies to selectors above): return empty array if nothing found ?
				return None


		# any custom query
		# raw bs4 css query
		# returns lizard entity
		# anything beyond that should be done via direct xml access
		"""
		if '%' in qr:
			selector = str(qr)[1:]
			if len(lizard.select(selector)) > 0:
				qresults = []
				for q in lizard.select(selector):
					qresults.append(lizardvmf_entity(lizard, q))
				return qresults
			else:
				return None
		"""


	# returns all entities
	def ents(self):
		all_ents = []
		for en in self.lizard.select('map entity'):
			all_ents.append(lizardvmf_entity(self.lizard, en))
		return all_ents


	# returns map properties
	# simply because I don't want to add self.mapsettings to the end of the init parser
	@property
	def mapsettings(self):
		return self.lizard.select('map world')[0]


	# get a bunch of free ids
	def getfreeid(self, amount, doside=False):

		# check that integer has been passed since it's a required parameter
		# todo: make it accept True and whatever and spit a single id ???
		# why ??????
		if isinstance(amount, int):
			pass
		else:
			raise ValueError('Amount can only be an integer. No bigger than 2,147,483,646 and not negative')

		lizard = self.lizard

		# todo: there are many other ways of getting free ids
		# like cycling through existing ones and finding gaps. Do these gaps actually matter ??
		# also other ways may result in way more readable ids

		# collect all ids here
		taken_ids = []

		# important todo: it's possible to select multiple things at once with ,
		if doside == True:
			for soid in lizard.select('map solid side'):
				if soid.get('id') != None:
					taken_ids.append(int(soid['id']))
		else:
			# get all solid ids
			# todo: the int() thing is very unreliable here
			for soid in lizard.select('map solid'):
				if soid.get('id') != None:
					taken_ids.append(int(soid['id']))

			# get all entity ids
			for eid in lizard.select('map entity'):
				if eid.get('id') != None:
					taken_ids.append(int(eid['id']))

			# groups share id pool with ents and solids
			for eid in lizard.select('map world group'):
				if eid.get('id') != None:
					taken_ids.append(int(eid['id']))

		# sort ids out
		# update: not needed anymore
		# taken_ids.sort()

		# store free ids here
		free_ids = []

		# lowest id possible
		# 2,147,483,646
		basis = -2147483640

		# margin. A safety margin of around a few thousand ids
		margin = 65535

		basis += margin

		# todo: very reliable but slow
		while len(free_ids) < amount:
			# basically test all the ids until we find the suitable one
			basis += 1
			if not basis in taken_ids:
				free_ids.append(basis)

		# There should always be enough free ids
		return free_ids

	# create entity
	# todo: specify classname more easily ??
	# todo: also assign own id like md5 ????
	# todo: the defaults for loc, rot could be (0, 0, 0)
	def mk_ent(self, params, loc=None, rot=None, idstate=None):
		
		"""
		Creates an entity and returns lizard entity.
		It expects following parameters in a following order:

		A dictionary of key-values ("angles" and "origin" are always overwritten)
		Location (loc), if None or not passed - 0 0 0
		Rotation (rot), if None or not passed - this parameter is not being set
		Id (idstate) - if nothing or none - id is assigned automatically. If int - sets passed int as id

		Location, rotation and id are keyword arguments
		meaning that the only positional argument that matters is the k:v dictionary (always has to be the first argument)

		Don't forget that dictionary should always have "classname" specified
		"""
		


		lizard = self.lizard

		# todo: do nothing if params are undefined
		newent = lizard.new_tag('entity')

		# append editor
		# todo: should editor always be there or create when neccessary ?
		edtr = lizard.new_tag('editor', color='202 246 72', visgroupshown='1', visgroupautoshown='1', logicalpos='[0 500]')
		newent.append(edtr)

		# populate attributes (parameters)
		for pr in params:
			newent[pr] = params[pr]

		# set id if told to
		# ffs, False is an int...
		if isinstance(idstate, int) and idstate != None and idstate != False and idstate != True:
			# you cannot have ids bigger than biggest int
			if idstate < 2147483640 and idstate > -2147483640:
				newent['id'] = idstate
			else:
				raise ValueError('id cannot be bigger than max int (2147483640)')
		else:
			newent['id'] = self.getfreeid(1)[0]

		# Location and Rotation
		# takes tuples with 3 values
		# todo: only accept vectors ?
		if loc != None and isinstance(loc, tuple):
			newent['origin'] = str(loc[0]) + ' ' + str(loc[1]) + ' ' + str(loc[2])
		else:
			newent['origin'] = '0 0 0'

		# it's impossible to guess which entity should have angles and which not
		# therefore, assume that if not passed - entity doesn't has angles
		if rot != None and isinstance(loc, tuple):
			newent['angles'] = str(rot[0]) + ' ' + str(rot[1]) + ' ' + str(rot[2])

		# finally, append constructed tag to map
		lizard.select('map world')[0].insert_after(newent)

		# and return the lizard entity
		return lizardvmf_entity(lizard, newent)


	# for now displacements are not possible
	# todo: some defaults ?
	def mk_solid(self, sides, idstate=None):
		"""
		It expects following parameters in the following order:
		An array of side dicts the solid has.
		Wether to generate id or not.

		Dictionary of the side is as follows. Accepts ints and floats (for now all params are mandatory):

		material: path to vmt
		rotation: texture rotation
		lightmapscale: lightmapscale
		smoothing_groups: shitty 3dmax-like smoothing groups (an int)

		3verts: 3 verts of the face in the right order - ((LocVector), (LocVector), (LocVector))
		uaxis/vaxis: ((u/vVector), (Shift, Scale)), for example ((0 1 0), (-22, 0.5))
		allverts: an array of all verts of the face (optional) - [LocVector, LocVector ...]
		"""

		lizard = self.lizard

		# keep in mind that a solid cannot have more than 128 faces
		# todo: all these functions can receive a lot of malformed data
		# raise error or skip?
		if len(sides) > 127:
			raise ValueError('A solid cannot have more than 127 faces, while current one has ' + str(len(sides)))
			return

		# create base tag
		solidtag = lizard.new_tag('solid')

		# add sides
		for sid in sides:
			# create side tag
			sidetag = lizard.new_tag('side')
			
			# do attributes (parameters)

			# plane
			# ((LocVector), (LocVector), (LocVector))
			# ordered !
			sidetag['plane'] = ''
			# 1
			sidetag['plane'] += '(' + str(sid['3verts'][0][0]) + ' ' + str(sid['3verts'][0][1]) + ' ' + str(sid['3verts'][0][2]) + ')'
			# 2
			sidetag['plane'] += '(' + str(sid['3verts'][1][0]) + ' ' + str(sid['3verts'][1][1]) + ' ' + str(sid['3verts'][1][2]) + ')'
			# 3
			sidetag['plane'] += '(' + str(sid['3verts'][2][0]) + ' ' + str(sid['3verts'][2][1]) + ' ' + str(sid['3verts'][2][2]) + ')'

			# do uppercase ?
			sidetag['material'] = str(sid['material'])

			sidetag['rotation'] = str(sid['rotation'])
			sidetag['lightmapscale'] = str(sid['lightmapscale'])
			sidetag['smoothing_groups'] = str(sid['smoothing_groups'])

			
			# ((0 1 0), (-22, 0.5))
			# ((Vector), (Shift, Scale))

			# U
			sidetag['uaxis'] = ''
			sidetag['uaxis'] += '[' + str(sid['uaxis'][0][0]) + ' ' + str(sid['uaxis'][0][1]) + ' ' + str(sid['uaxis'][0][2]) + str(sid['uaxis'][1][0]) + ']'
			sidetag['uaxis'] += ' '
			sidetag['uaxis'] += str(sid['uaxis'][1][1])

			# V
			sidetag['vaxis'] = ''
			sidetag['vaxis'] += '[' + str(sid['vaxis'][0][0]) + ' ' + str(sid['vaxis'][0][1]) + ' ' + str(sid['vaxis'][0][2]) + str(sid['vaxis'][1][0]) + ']'
			sidetag['vaxis'] += ' '
			sidetag['vaxis'] += str(sid['vaxis'][1][1])


			# vertices plus IF PRESENT
			if 'allverts' in sid:
				# create verts plus tag
				vtplus = lizard.new_tag('vertices_plus')
				# add actual verts to that tag
				for vrt in sid['allverts']:
					vertag = lizard.new_tag('v')
					vertag.string = str(vrt[0]) + ' ' + str(vrt[1]) + ' ' + str(vrt[2])
					vtplus.append(vertag)

				# after done adding verts - append the verts plus to the side
				sidetag.append(vtplus)

			# assign id to the side
			# todo: get required amount of ids in advance?
			sidetag['id'] = getfreeid(1, True)[0]

			# append side to solid
			solidtag.append(sidetag)


		# Once done with all the sides - assign id to the solid
		# todo: finally come up with smarter logic for detecting good ints
		if idstate != True and idstate != False and idstate != None and isinstance(idstate, int):
			solidtag['id'] = str(idstate)
		else:
			solidtag['id'] = getfreeid(1)[0]

		# Also add editor, we try to keep it present everywhere...
		edtr = lizard.new_tag('editor', color='202 246 72', visgroupshown='1', visgroupautoshown='1', logicalpos='[0 500]')
		solidtag.append(edtr)

		# Finally, append to world and return lizard solid because fuck you
		# todo: things like 'map world' are probably better done with lizard.map.world
		lizard.select('map world')[0].append(solidtag)

		return lizardvmf_solid(lizard, solidtag)


	# creates a group
	# it looks like groups share same id pool as solids n stuff
	# todo: A pool of ids occupied by some of the spawners?
	# because, is it possible for something to exist with an id and yet not exist in the xml tree????
	# todo: should it inherit visgroup options (hidden/visible) since there are parameters like visgroupshown ???
	# todo: separate class for groups ???
	def mk_group(self):
		lizard = self.lizard
		# create the group itself
		grp = lizard.new_tag('group')
		# and append editor into it
		edtr = lizard.new_tag('editor', color='202 246 72', visgroupshown='1', visgroupautoshown='1')
		grp.append(edtr)

		# now, create an id for it and assign it
		mk_id = self.getfreeid(1)[0]
		grp['id'] = mk_id

		# once done - append to world
		lizard.select('map world')[0].append(grp)

		return mk_id


	# set cordon state, accepts true or false, none to return status
	def cordonstate(self, state):
		lizard = self.lizard
		cords = lizard.select('map > cordons')
		onecord = lizard.select('map > cordon')

		# prioritize cordons...
		# todo: the fucking returns
		if len(cords) > 0:
			if state == True:
				cords[0]['active'] = '1'

			if state == False:
				cords[0]['active'] = '0'

			return 'new'
		elif len(onecord) > 0:
			# check for old-ass cordon method, where you can only have one
			if state == True:
				onecord[0]['active'] = '1'

			if state == False:
				onecord[0]['active'] = '0'

			return 'old'
		else:
			return False



	# returns a collection of cordons IF ANY
	# todo: old single-cordon is not supported yet
	# update: this now supports queries
	# meaning that you can select cordons by name righ away
	def cordons(self, cquery=None):
		lizard = self.lizard
		crd = []
		if cquery != None:
			for cor in lizard.select('cordons cordon[name="' + str(cquery) + '"]'):
				crd.append(lizardvmf_cordon(lizard, cor))
		else:
			for cor in lizard.select('cordons cordon'):
				crd.append(lizardvmf_cordon(lizard, cor))

		return crd


	# todo: duplicated from the cordon class
	def blender_to_cordon(self, eloc, escale):
		cent = (eloc[0], eloc[1], eloc[2])
		scl = (escale[0], escale[1], escale[2])

		min_x = cent[0] - (scl[0] / 2)
		min_y = cent[1] - (scl[1] / 2)
		min_z = cent[2] - (scl[2] / 2)

		max_x = cent[0] + (scl[0] / 2)
		max_y = cent[1] + (scl[1] / 2)
		max_z = cent[2] + (scl[2] / 2)

		# print(min_x, min_y, min_z)
		# print(max_x, max_y, max_z)

		ret = {
			'mins': (min_x, min_y, min_z),
			'maxs': (max_x, max_y, max_z)
		}
		return ret



	# add cordon to map. Make it part of cordons and make cordons a class?
	# todo: old single-cordon is not supported yet
	# for now, takes a tuple of two tuples: location, scale, ORDER IS IMPORTANT
	def new_cordon(self, corname, corbox):
		lizard = self.lizard
		if corname != None and str(corname).strip() != '':

			cordtag = lizard.new_tag('cordon', active='1')
			cordtag['name'] = str(corname)
			convertbox = self.blender_to_cordon(corbox)
			min_s = '(' + str(convertbox['mins'][0]) + ' ' + str(convertbox['mins'][1]) + ' ' + str(convertbox['mins'][2]) + ')'
			max_s = '(' + str(convertbox['maxs'][0]) + ' ' + str(convertbox['maxs'][1]) + ' ' + str(convertbox['maxs'][2]) + ')'
			boxtag = lizard.new_tag('box', mins=min_s, maxs=max_s)
			cordtag.append(boxtag)

			lizard.select('map cordons').append(cordtag)

			return lizardvmf_cordon(lizard, cordtag)


	# important todo: this is the second duplicate of such kind
	# always returns an array because apparently, you can have mutiple visgroups with the same name
	def visgroups(self, vname=None):
		allvis = []

		if vname != None and vname != '':
			for vi in self.lizard.select('map visgroups visgroup[name="' + str(vname) + '"]'):
				allvis.append(lizardvmf_visgroup(self.lizard, vi))
		else:
			for vi in self.lizard.select('map visgroups visgroup'):
				allvis.append(lizardvmf_visgroup(self.lizard, vi))
		return allvis



	# get a free id for a visgroup
	def vgetfreeid(self):
		lizard = self.lizard

		# collect all ids here
		taken_ids = []

		# groups share id pool with ents and solids
		for vgid in lizard.select('map visgroups visgroup'):
			# important todo: WHAT ???
			if vgid.get('visgroupid') != None:
				# print(vgid['an'] == 'None')
				# print(vgid['name'])
				taken_ids.append(int(vgid['visgroupid']))

		# store free ids here
		free_ids = None

		# basis
		basis = 4

		# todo: very reliable but slow
		while free_ids == None:
			# basically test all the ids until we find the suitable one
			basis += 1
			if not basis in taken_ids:
				free_ids = basis
				# There should always be enough free ids
				return basis


	# create a new visgroup
	# important todo: Make this function accept custom ids ?
	# important todo: Fuck visgroups with the same names, disallow the creation of visgroups with duplicate names
	# simply return an existing one
	def new_visgroup(self, vname=None):
		if str(vname).strip() != '' and vname != None:
			lizard = self.lizard
			# vgtag = lizard.new_tag('visgroup', name=str(vname), visgroupid=str(self.vgetfreeid()), color='202 246 72')
			vgtag = lizard.new_tag('visgroup', visgroupid=str(self.vgetfreeid()), color='202 246 72')
			vgtag['name'] = str(vname)

			lizard.select('map visgroups')[0].append(vgtag)

			return lizardvmf_visgroup(lizard, vgtag)
		else:
			return False


	# todo: add cameras (the ones created with the camera tool in hammer)




# test
fr = open(r'E:\!!Blend_Projects\scripts\map_parser\example_map_src.vmf', 'r').read()
# fr = open(r'E:\!!Blend_Projects\scripts\map_parser\tmp\tmp_empty_gmod.vmf', 'r').read()
# fr = open(r'E:\!!!!!opforce2\reverse\bms\maps\src\bms_map_src\2331428357\Singleplayer\C4A3-Interloper\bm_c4a3d.vmf', 'r').read()

lol = lizardvmf(fr)
# lol = lizardvmf(True)

# lol.vmfquery('#273')['classname'] = 'prop_ass'

"""
print(lol.vmfquery('#273').visgroup)
print(lol.vmfquery('#273').visgroup['name'])
print(lol.vmfquery('#273').visgroup['id'])
print(lol.vmfquery('#273').prms['classname'])
lol.vmfquery('#273').prms['classname'] = 'dicks'
print(lol.vmfquery('#273').prms['classname'])
"""

print(lol.mapsettings['skyname'])
print(len(lol.ents()))
lol.mapsettings['skyname'] = 'tits'
print(lol.mapsettings['skyname'])
print(lol.getfreeid(7))
prmdict = {
	'classname': 'prop_physics',
	'model': 'models/props_junk/plasticbucket001a.mdl',
	'spawnflags': '256',
	'modelscale': '1'
}
ne = lol.mk_ent(prmdict, (0, 12 , 33), (0, 0, 0))
print(lol.getfreeid(7))
print(ne.prms['model'])
print(len(lol.ents()))
ne.kill()
print(lol.getfreeid(7))
print(lol.mk_group())
print(lol.mk_group())
print(lol.mk_group())
print(lol.mk_group())
print(lol.mk_group())

print(lol.cordonstate(True))
print(lol.cordons()[1].box)
print(lol.cordons()[2].box)
print(lol.cordons()[0].box)

print(len(lol.visgroups()))

newis = lol.new_visgroup('fuck pingas')

print(newis.name)
newis.name = 'tits dick'
print(newis.name)
print(len(lol.visgroups()))

another_vis = newis.add_new('pills here')
print(another_vis.name)
another_vis.name = 'pills there'
print(another_vis.name)

ent_w_cnts = lol.vmfquery('#742')
print(ent_w_cnts)
print(ent_w_cnts.connections)
print(ent_w_cnts.connections.items)
print(ent_w_cnts.connections.items[0])
print(ent_w_cnts.connections.items[0].output_name)
print(ent_w_cnts.connections.items[0].tgt_ents)
print(ent_w_cnts.connections.items[0].action)
print(ent_w_cnts.connections.items[0].params)
print(ent_w_cnts.connections.items[0].delay)
print(ent_w_cnts.connections.items[0].refire_limit)
print(ent_w_cnts.connections.items[0].ctag.string)

ent_w_cnts.connections.items[0].tgt_ents = 'botle*'

print(ent_w_cnts.connections.items[0].ctag.string)

mkconnection = {
	'tgt_ents': 'everyone',
	'action': 'kill',
	'params': '',
	'delay': 2.73,
	'refire_limit': -1
}

ent_w_cnts.connections.add('OnDamaged', mkconnection)
print(ent_w_cnts.connections.items[-1].ctag.string)

print(len(lol.ents()))

# print()
# print(lol.tovmf())
# print(str(lol.lizard))


# print(lol.tovmf())
# print(lol.mk_ent.__doc__)





# print(lol.vmfquery('#272').visgroup)

# lol.vmfquery('#273').visgroup = 'sideramp'

# print(lol.vmfquery('#273').visgroup)