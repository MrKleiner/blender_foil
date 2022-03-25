
# island iterator

"""
import bpy
import bmesh

def walk_island(vert):
	''' walk all un-tagged linked verts '''    
	vert.tag = True
	yield(vert)
	linked_verts = [e.other_vert(vert) for e in vert.link_edges
			if not e.other_vert(vert).tag]

	for v in linked_verts:
		if v.tag:
			continue
		yield from walk_island(v)

def get_islands(bm, verts=[]):
	def tag(verts, switch):
		for v in verts:
			v.tag = switch
	tag(bm.verts, True)
	tag(verts, False)
	ret = {'islands' : []}
	verts = set(verts)
	while verts:
		v = verts.pop()
		verts.add(v)
		island = set(walk_island(v))
		ret['islands'].append(list(island))
		tag(island, False) # remove tag = True
		verts -= island
	return ret
"""

#
# Better iterator
#
import bpy
import bmesh

def blfoil_get_island_facepair(ob):
	# obj = bpy.context.active_object
	obj = ob
	mesh = obj.data
	paths={v.index:set() for v in mesh.vertices}
	for e in mesh.edges:
		paths[e.vertices[0]].add(e.vertices[1])
		paths[e.vertices[1]].add(e.vertices[0])
	lparts=[]
	while True:
		try:
			i=next(iter(paths.keys()))
		except StopIteration:
			break
		lpart={i}
		cur={i}
		while True:
			eligible={sc for sc in cur if sc in paths}
			if not eligible:
				break
			cur={ve for sc in eligible for ve in paths[sc]}
			lpart.update(cur)
			for key in eligible: paths.pop(key)
		lparts.append(lpart)

	print(lparts)


	# isle_pairs = {}
	isle_pairs = []

	for num, super_isle in enumerate(lparts):
		match_faces = []
		for nad in ob.data.polygons:
			for hah in nad.vertices:
				if hah in super_isle:
					match_faces.append(nad)
		matched_faces_to = list(dict.fromkeys(match_faces))
		# isle_pairs[num] = matched_faces_to
		isle_pairs.append(matched_faces_to)
		print(num, 'matched faces:', matched_faces_to)
		
		for vev in matched_faces_to:
			for rer_vert in vev.vertices:
				print(rer_vert)

	return isle_pairs

	"""
	print(isle_pairs)

	print('br')
	for solid in isle_pairs:
		print('island number:', solid)
		print(isle_pairs[solid])
	print(isle_pairs[0][1].index)
	"""

def rotation_matrix(axis, theta):
	"""
	Return the rotation matrix associated with counterclockwise rotation about
	the given axis by theta radians.
	"""
	import numpy as np
	import math

	axis = np.asarray(axis)
	axis = axis / math.sqrt(np.dot(axis, axis))
	a = math.cos(theta / 2.0)
	b, c, d = -axis * math.sin(theta / 2.0)
	aa, bb, cc, dd = a * a, b * b, c * c, d * d
	bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
	return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
					[2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
					[2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])



def vert_uv_math(tverts):
	"""
	Expects a tuple of three vert location vectors: (Vector, Vector, Vector)
	IMPORTANT: VERT LOCATIONS HAVE TO BE WORLD SPACE!!!!!!
	"""
	import numpy as np
	import math

	

	cuvc = tverts

	# calc U
	uwidth_a = cuvc[2][0] - cuvc[1][0]
	uwidth_b = cuvc[2][1] - cuvc[1][1]
	uwidth_c = cuvc[2][2] - cuvc[1][2]

	calc_uwidth = math.sqrt(uwidth_a * uwidth_a + uwidth_b * uwidth_b + uwidth_c * uwidth_c)

	calc_ux = uwidth_a / calc_uwidth
	calc_uy = uwidth_b / calc_uwidth
	calc_uz = uwidth_c / calc_uwidth


	# calc V
	vwidth_a = cuvc[0][0] - cuvc[1][0]
	vwidth_b = cuvc[0][1] - cuvc[1][1]
	vwidth_c = cuvc[0][2] - cuvc[1][2]

	calc_vwidth = math.sqrt(vwidth_a * vwidth_a + vwidth_b * vwidth_b + vwidth_c * vwidth_c)

	calc_vx = vwidth_a / calc_vwidth
	calc_vy = vwidth_b / calc_vwidth
	calc_vz = vwidth_c / calc_vwidth


	#
	# Actually, this is what hammer does too (kinda)
	#

	# three verts form two vectors.
	# if those verts are not from a perfect square - the angle between them is not 90 degrees
	vec_a = (calc_ux, calc_uy, calc_uz)
	vec_b = (calc_vx, calc_vy, calc_vz)

	# get cross product of those vectors
	vec_c = np.cross(vec_a, vec_b)

	# prepare to rotate things by 90 degrees in radians
	radians_angle = math.radians(-90)

	# first vector remains unchanged
	result_a = vec_a

	# now, use original vector A as an axis and rotate cross product around it
	result_b = np.dot(rotation_matrix(vec_a, radians_angle), vec_c)


	rer = {
		'u': result_a,
		'v': result_b
	}

	return rer



def blfoil_easy_brushes_v1(objs):
	"""Takes an array of blender objects. Returns easy brushes"""

	for me in objs:
		# get amount of islands
		bm = bmesh.new()
		bm.from_mesh(me.data)
		islands = [island for island in get_islands(bm, verts=bm.verts)['islands']]
		# islands = blfoil_get_island_facepair(me)
		
		# relate every vert to an island
		relations = {}
		for il_index, isld in enumerate(islands):
			for bv in isld:
				relations[bv] = il_index
			
		# print(relations)
		
		# print(islands[0])
		
		easy_islands = {}
		
		# easy way of creating total amount of islands for later assignation
		for island_n_index, island_n in enumerate(islands):
			easy_islands[island_n_index] = []
		
		
		bm.faces.ensure_lookup_table()
		for fc in bm.faces:
			# to which island does this face belong
			island_index = relations[fc.verts[0]]

			# reversed
			# vert_reversed = reversed()

			# fresh addition, revert if problems !
			# three_v = (fc.verts[0].co, fc.verts[1].co, fc.verts[2].co)

			all_v = []

			for vt in fc.verts:
				all_v.append(vt.co)
			
			"""
			# important todo: WHAT THE FUCK IS THIS FUCKING SHIT ???????????
			# update: improved

			# three_v = (revo[0], revo[1], revo[2])
			fuck = {}
			revo = reversed(fc.verts)
			vnum = 0
			for rev in revo:
				fuck[vnum] = rev
				vnum += 1
				if vnum > 2:
					break

			three_v = (fuck[0].co, fuck[1].co, fuck[2].co)
			"""

			revo_energy = [revo for revo in reversed(fc.verts)]
			three_v = (revo_energy[0].co, revo_energy[1].co, revo_energy[2].co)

			# todo: would it make more sense to do uv math right here ?
			face_payload = {
				'three': three_v,
				'allv': all_v
			}

			easy_islands[island_index].append(face_payload)

	return easy_islands


def blfoil_easy_brushes(objct):
	import math
	import time
	"""Takes a blender object. Returns easy brushes, all ready to go (world space n shit)"""

	# for me in objs:

	# get all verts
	bm = bmesh.new()
	bm.from_mesh(objct.data)

	# Which is faster?
	obj_verts = bm.verts
	# obj_verts = objct.data.vertices

	ob_islands = blfoil_get_island_facepair(objct)
	obj_mt_world = objct.matrix_world

	easy_islands = []

	# for fc in bm.faces:
	isl_take = int(round(time.time() * 1000))
	for isle in ob_islands:
		isl_payload = []
		for isle_face in isle:

			# todo: when exactly the ensure_lookup should happen?
			# could it happen on per-island basis?
			bm.faces.ensure_lookup_table()
			bm.verts.ensure_lookup_table()
			revo_energy = [obj_mt_world @ obj_verts[revo].co for revo in reversed(isle_face.vertices)]
			three_v = (revo_energy[0], revo_energy[1], revo_energy[2])

			# todo: would it make more sense to do uv math right here ?
			# update: Yes. Done

			# shit has to be even:
			# todo: this is still not that one proper mathematical implementation
			# but like... it's just one if, why bother with maths ?
			uv_verts = (three_v[0], three_v[1], three_v[2])
			if len(revo_energy) > 4:
				vtxstep = math.floor(len(revo_energy) / 3)
				uv_verts = revo_energy[0::vtxstep]

			# important todo: wait, what's the point of including 3 verts separately?
			face_payload = {
				'three': three_v,
				'allv': revo_energy,
				'uv': vert_uv_math(uv_verts),
				'bl_face_index': isle_face.index
			}

			isl_payload.append(face_payload)

		print('island took', int(round(time.time() * 1000)) - isl_take)

		easy_islands.append(isl_payload)


	bm.free()
	print('Done with islands of the object', objct.name)
	return easy_islands

