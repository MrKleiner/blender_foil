
# island iterator
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
	ret = {"islands" : []}
	verts = set(verts)
	while verts:
		v = verts.pop()
		verts.add(v)
		island = set(walk_island(v))
		ret["islands"].append(list(island))
		tag(island, False) # remove tag = True
		verts -= island
	return ret






def vert_uv_math(tverts):
	"""
	Expects a tuple of three vert location vectors: (Vector, Vector, Vector)
	IMPORTANT: VERT LOCATIONS HAVE TO BE WORLD SPACE!!!!!!
	"""

	import math

	cuvc = tverts

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

	rer = {
		'u': (calc_ux, calc_uy, calc_uz),
		'v': (calc_vx, calc_vy, calc_vz)
	}

	return rer




def blfoil_easy_brushes(objs):
	"""Takes an array of blender objects. Returns easy brushes"""

	for me in objs:
		# get amount of islands
		bm = bmesh.new()
		bm.from_mesh(me.data)
		islands = [island for island in get_islands(bm, verts=bm.verts)['islands']]
		
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

			three_v = (fc.verts[0].co, fc.verts[1].co, fc.verts[2].co)

			all_v = []

			for vt in fc.verts:
				all_v.append(vt.co)
			
			# todo: would it make more sense to do uv math right here ?
			face_payload = {
				'three': three_v,
				'allv': all_v
			}

			easy_islands[island_index].append(face_payload)

	return easy_islands
