from fgd_parser import FGDParser
from pathlib import Path
import json

# we need EVERYTHING !

blfoil_ents = {}
# Basically, every single Valve game...
fg42 = [
	'E:\\Gamess\\steamapps\\common\\Half-Life 2\\bin\\halflife2.fgd',
	'E:\\Gamess\\steamapps\\common\\Half-Life 2\\bin\\base.fgd',
	'E:\\Gamess\\steamapps\\common\\Half-Life 2\\bin\\hammerplusplus\\hammerplusplus_fgd.fgd',
	'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Alien Swarm Reactive Drop\\bin\\swarmbase.fgd',
	r'C:\Program Files (x86)\Steam\steamapps\common\Alien Swarm Reactive Drop\bin\swarm_fixed_ents.fgd',
	r'C:\Program Files (x86)\Steam\steamapps\common\Alien Swarm Reactive Drop\bin\reactivedrop.fgd',
	r'C:\Program Files (x86)\Steam\steamapps\common\Alien Swarm Reactive Drop\bin\swarm.fgd',
	r'C:\Program Files (x86)\Steam\steamapps\common\Alien Swarm Reactive Drop\bin\swarm.fgd',
	r'E:\Gamess\steamapps\common\Black Mesa\bin\bms.fgd',
	r'E:\Gamess\steamapps\common\Counter-Strike Global Offensive\bin\csgo.fgd',
	r'E:\Gamess\steamapps\common\Portal 2\bin\portal.fgd',
	r'E:\Gamess\steamapps\common\Portal 2\bin\portal2.fgd',
	r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\bin\tf.fgd',
	r'E:\Gamess\steamapps\common\Lambda Wars\lambdawars\lambdawars.fgd',
	r'E:\Gamess\steamapps\common\left 4 dead 2\bin\left4dead2.fgd',
	r'E:\!!Blend_Projects\scripts\wallworm4blender\clients\mapbase_release_build_v6_3\mapbase_shared\shared_misc\bin\base.fgd'
]

# fg42= []



# we care about any point entities except base classes
accept_marks = [
	'PointClass',
	'NPCClass',
	'KeyFrameClass',
	'MoveClass',
	'FilterClass',
	'SolidClass'
]

# it's very important what is int, float, str or enum...
type_def = {
	'axis': 'float',
	'node_id': 'int',
	'float': 'float',
	'integer': 'int',
	'choices': 'enum',
	'Choices': 'enum',
	'color255': 'colour'
}

type_def_index = {
	'float': 2,
	'int': 1,
	'enum': 4,
	'str': 0,
	'colour': 3
}
def kvflip(dic):
	newdic = {}
	# print(dic)
	for ded in dic:
		newdic[str(dic[ded])] = str(ded)
	return newdic


def indexof(where, ofwhat):
	for k in where:
		if where[k] == ofwhat:
			return k



for need_fgd in fg42:
	current_fgd = FGDParser(need_fgd)
	current_fgd.parse()

	# for every class, except base classes
	for fgd_cl in current_fgd.classes:

		# print(fgd_cl.class_type)
		# print(fgd_cl.class_type in accept_marks)
		if fgd_cl.class_type in accept_marks:

			blfoil_class_payload = [
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				{
					'origin_enabled': '1'
				}
			]

			# first - get what we have alr

			# strings, ints, floats, colours, enums and flags
			for cp in fgd_cl._properties:


				prop_payload = {}

				# everything but spawnflags from what we have already
				if cp['name'] != 'spawnflags':
					if cp.get('display_name') == None:
						print(cp)

					prop_payload['guiname'] = cp.get('display_name') or cp.get('name')
					prop_payload['idname'] = cp['name']
					prop_payload['default'] = cp.get('default') or ''
					prop_payload['descr'] = cp.get('doc') or ''

					# strings, ints and floats

					# int or float
					if cp['type'].lower() in type_def:
						if type_def[cp['type'].lower()] != 'enum':
							blfoil_class_payload[type_def_index[type_def[cp['type'].lower()]]].append(prop_payload)
					# else - string
					else:
						# print(blfoil_class_payload[0])
						# print('r u fking kiddin me')
						blfoil_class_payload[0].append(prop_payload)
						# print(blfoil_class_payload[0])

					

					# enums and bool enums
					if cp['type'].lower() == 'choices' and 'choices' in cp:

						decision_helper = []
						# todo: use generator
						for entr in cp['choices']:
							decision_helper.append(cp['choices'][entr].lower())

						# if so - this is a bool enum
						# all to lower
						# todo: this could be detected in a better way
						not_lowered = cp['choices']
						lowered = {}
						for lower in not_lowered:
							lowered[lower] = str(not_lowered[lower]).lower()

						lowered = kvflip(lowered)
						# print(lowered)

						if len(cp['choices']) == 2 and 'yes' in lowered and 'no' in lowered:
							# deflt = '0'
							yesno = {
								'yes': '1',
								'no': '0'
							}
							bool_enum_payload = {
								'guiname': cp.get('display_name') or cp.get('name'),
								'idname': cp['name'],
								'default': yesno.get(str(cp.get('default')).lower()) or cp.get('default') or '0',
								'descr': cp.get('doc') or ''
							}
							blfoil_class_payload[5].append(bool_enum_payload)

						# else - it's a standard enum
						else:
							eflip = kvflip(cp['choices'])
							gdef = '0'
							if cp.get('default') != None:
								# print(eflip)
								# print(str(cp['default']))
								# gdef = val_list.index(str(cp['default']))
								gdef = indexof(eflip, str(cp['default']))
							else:
								gdef = next(iter(eflip))

							std_enum_payload = {
								'guiname': cp.get('display_name') or cp.get('name'),
								'idname': cp['name'],
								# 'default': val_list.index(cp['default']),
								# 'default': str(cp.get('default') or 0),
								'default': str(gdef),
								'descr': cp.get('doc') or '',
								'eitems': eflip
							}
							blfoil_class_payload[4].append(std_enum_payload)


				# spawnflags
				if cp['name'] == 'spawnflags':
					for fl in cp['flags']:
						flag_payload = {
							'byte': cp['flags'][fl][0],
							'default': str(cp['flags'][fl][1]),
							# important todo: this is not a description, this is a flag name!!
							# 'descr': fl
							# update: done
							'guiname': fl
						}
						blfoil_class_payload[6].append(flag_payload)


			# outputs
			for outp in fgd_cl.output:
				blfoil_class_payload[7].append(outp.name)

			# inputs
			for inpt in fgd_cl.inputs:
				blfoil_class_payload[8].append(inpt.name)

			if fgd_cl.class_type == 'SolidClass':
				blfoil_class_payload[9]['brush_ent'] = '1'
			else:
				blfoil_class_payload[9]['brush_ent'] = '0'


			
			#
			# Then, get shit from bases
			#

			# there could be multiple bases...
			# print(fgd_cl.bases)
			if fgd_cl.name == 'prop_dynamic':
				# print(fgd_cl.bases)
				pass



			# BASES
			# AH YES, IT COULD BE FUCKING NESTED !!!!!!!

			bases_real = []
			# construct the REAL array of bases

			def getbas(nm):
				for rqb in current_fgd.classes:
					if rqb.name == nm:
						return rqb.bases

			# CMON THE CHAIN SHOULDNT BE LONGER THAN 10, RIGHT ????
			
			for strt in fgd_cl.bases:
				bases_real.append(strt)
				# print(strt)
				# branch 1
				if getbas(strt) != None:
					for b1 in getbas(strt):
						bases_real.append(b1)

				# branch 2
				if getbas(getbas(strt)) != None:
					for b2 in getbas(getbas(strt)) != None:
						bases_real.append(b2)
				
				# branch 3
				if getbas(getbas(getbas(strt))) != None:
					for b3 in getbas(getbas(getbas(strt))):
						bases_real.append(b3)
				
			# print(bases_real)
			# asdasdasd = ww
			

			# for find_base in fgd_cl.bases:
			for find_base in bases_real:
				# print(find_base)
				# find required base
				for rqb in current_fgd.classes:

					if rqb.name == find_base:
						# if fgd_cl.name == 'prop_dynamic':
						# 	print('found base:', rqb.name)
						# 	print('found base:', rqb.bases)
						# 	dwdas
						# strings, ints, floats, colours, enums and flags
						for cp in rqb._properties:
							# print(cp)
							prop_payload = {}

							# everything but spawnflags from what we have already
							if cp['name'].lower() != 'spawnflags':
								if cp.get('display_name') == None:
									print(cp)
								prop_payload['guiname'] = cp.get('display_name') or cp.get('name')
								prop_payload['idname'] = cp['name']
								prop_payload['default'] = cp.get('default') or ''
								prop_payload['descr'] = cp.get('doc') or ''

								# strings, ints and floats

								# int or float
								if cp['type'].lower() in type_def:
									if type_def[cp['type'].lower()] != 'enum':
										blfoil_class_payload[type_def_index[type_def[cp['type']]]].append(prop_payload)
								# else - string
								else:
									# print('append?')
									blfoil_class_payload[0].append(prop_payload)

								

								# enums and bool enums
								if cp['type'].lower() == 'choices' and 'choices' in cp:

									decision_helper = []
									# todo: use generator
									for entr in cp['choices']:
										decision_helper.append(cp['choices'][entr].lower())

									# if so - this is a bool enum
									# todo: this could be detected in a better way
									not_lowered = cp['choices']
									lowered = {}
									for lower in not_lowered:
										lowered[lower] = str(not_lowered[lower]).lower()

									lowered = kvflip(lowered)
									# print(lowered)

									if len(cp['choices']) == 2 and 'yes' in lowered and 'no' in lowered:
										print(lowered, fgd_cl.name)
										yesno = {
											'yes': '1',
											'no': '0'
										}
										bool_enum_payload = {
											'guiname': cp.get('display_name') or cp.get('name'),
											'idname': cp['name'],
											'default': yesno.get(str(cp.get('default')).lower()) or cp.get('default') or '0',
											'descr': cp.get('doc') or ''
										}
										blfoil_class_payload[5].append(bool_enum_payload)

									# else - it's a standard enum
									else:
										eflip = kvflip(cp['choices'])
										gdef = '0'
										if cp.get('default') != None:
											# print(eflip)
											# print(str(cp['default']))
											# gdef = val_list.index(str(cp['default']))
											gdef = indexof(eflip, str(cp['default']))

										std_enum_payload = {
											'guiname': cp.get('display_name') or cp.get('name'),
											'idname': cp['name'],
											# 'default': val_list.index(cp['default']),
											# 'default': str(cp.get('default')),
											'default': str(gdef),
											'descr': cp.get('doc') or '',
											'eitems': eflip
										}
										blfoil_class_payload[4].append(std_enum_payload)

							# spawnflags
							if cp['name'].lower() == 'spawnflags':
								for fl in cp['flags']:
									flag_payload = {
										'byte': str(cp['flags'][fl][0]),
										'default': str(cp['flags'][fl][1]),
										# important todo: this is not a description, this is a flag name!!
										# 'descr': fl
										# update: done
										'guiname': fl
									}
									blfoil_class_payload[6].append(flag_payload)



						# outputs
						for outp in rqb.output:
							blfoil_class_payload[7].append(outp.name)

						# inputs
						for inpt in rqb.inputs:
							blfoil_class_payload[8].append(inpt.name)

						# if fgd_cl.name == 'prop_dynamic':
						# 	print('payload:', prop_payload)
						# 	print(rqb.bases)
						# 	ddddasasd


			# toggle angles enabled and convert everything to string
			blfoil_class_payload[9]['angles_enabled'] = '0'
			for alltypes in blfoil_class_payload:
				for newprm in alltypes:
					# todo: nothing is more permanent than a temp solution
					try:
						if isinstance(newprm.get('default'), int) or isinstance(newprm.get('default'), float):
							newprm['default'] = str(newprm['default'])
						if newprm['idname'].lower() == 'angles':
							blfoil_class_payload[9]['angles_enabled'] = '1'
					except:
						pass

					

			blfoil_ents[fgd_cl.name] = blfoil_class_payload


# todo?: some brush entities don't have an origin
known_no_origin = [
	'func_viscluster',
	'func_detail',
	'func_lod'
]

# known_no_origin = []

for knob in known_no_origin:
	blfoil_ents[knob][9]['origin_enabled'] = '0'

problems = {}
limits = {
	0: 32,
	1: 32,
	2: 32,
	3: 8,
	4: 16,
	5: 16,
	6: 32,
	7: 8192,
	8: 8192,
	9: 8192
}
for lencheck in blfoil_ents:
	append_payload = False
	problem_payload = {}
	for dtype_index, dtype in enumerate(blfoil_ents[lencheck]):
		if len(dtype) > limits[dtype_index]:
			problem_payload[dtype_index] = len(dtype)
			append_payload = True
	if append_payload:
		problems[lencheck] = problem_payload
		print(lencheck)
		for pr in problem_payload:
			print('    ', pr, problem_payload[pr])



print(problems)

new_conf = open('blpe_all_lul.json', 'w')
new_conf.write(json.dumps(blfoil_ents, indent=4, sort_keys=False))

star = 16
premade = """    pr_enum_lizard_tits : EnumProperty(
        items=enum_returner_lizard_tits,
        name='Entity',
        description='I like bread',
        update=enum_tgt_lizard_tits
        )"""
for lol in range(30):
	break
	star += 1
	print('')
	print(premade.replace('lizard_tits', str(star)))