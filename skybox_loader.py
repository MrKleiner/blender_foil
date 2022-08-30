from pathlib import Path
from utils.lizard_tail.lizard_tail import lizard_tail
from utils.shared import app_command_send, where_addon_root
import json

addon_root_dir = where_addon_root(__file__)


#
# Important note the order from gameinfo IS preserved!
#

# important todo: this is not very realiable. There are many stupid assumptions
def gameinfo_paths_lookup(cl):
	# first evaluate gameinfo
	gminfo = lizard_tail(Path(cl).read_text())
	
	# ASSUME that gameinfo lays in the root of the client (as it fucking has to)
	client = Path(cl).parent

	# print(gminfo.search_paths)
	# store resulting shit here
	result = {
		'content_folders': {
			'materials': [],
			'models': [],
			'scripts': [],
			'sound': [],
			'resource': [],
			'cfg': []
		}
	}

	look_for_vpks_here = []
	# process entries one by one
	# find places to look for vpks at
	for entry in gminfo.search_paths:
		# the path entry of this key
		rawpath = entry['value']

		# it could be that the path is absolute. Account for that
		if '.vpk' in rawpath:
			trypath = Path(rawpath.replace('.vpk', '_dir.vpk'))
			if trypath.is_file():
				look_for_vpks_here.append(trypath)
				continue

		# base path
		basepath = client
		
		# if this is present in the entry - go up one directory
		# every other case means that the base path is the gameinfo path
		if '|all_source_engine_paths|' in rawpath.lower():
			basepath = client.parent

		# count how many times do we have to go up
		up_parents = rawpath.count('../')

		# if not zero - go up
		if up_parents != 0:
			# minues one because zero counts too
			basepath = basepath.parents[up_parents - 1]

		# now join the base path and the entry path
		joined_path = basepath / rawpath.lower().replace('|gameinfo_path|', '').replace('|all_source_engine_paths|', '').replace('../', '')
		print(joined_path)
		look_for_vpks_here.append(joined_path)

	print('break')
	
	# Now process all the paths and treat them accordingly
	found_vpks = []
	for lookpath in look_for_vpks_here:
		# if it's an absolute path - just add it right away
		if lookpath.is_file():
			found_vpks.append(lookpath)
			continue

		# if it wasnt an absoulte path in the first place, but became one after joining
		late_abs = lookpath.parent / lookpath.name.replace('.vpk', '_dir.vpk')
		if late_abs.is_file():
			found_vpks.append(late_abs)
			continue

		# if it's a directory WITHOUT /* - scan it NOT recursively
		if lookpath.is_dir():
			for globvpk in lookpath.glob('*.vpk'):
				if '_dir.vpk' in globvpk.name.lower():
					found_vpks.append(globvpk)
			
			#
			# Look for content folders
			#
			for cf in result['content_folders']:
				if (lookpath / cf).is_dir():
					result['content_folders'][cf].append((lookpath / cf))

			continue

		# if it's a directory WITH /* - scan it Recursively
		if lookpath.name.strip() == '*' and lookpath.parent.is_dir():
			for globvpk in lookpath.parent.rglob('*.vpk'):
				if '_dir.vpk' in globvpk.name.lower():
					found_vpks.append(globvpk)
			
			cflook = [sex for sex in lookpath.parent.rglob('*') if sex.is_dir()]
			
			#
			# Look for content folders
			#
			for cf in cflook:
				# a content folder only counts if there's no folder with the same name up its parent tree
				# RELATIVE to the base look path
				relative = cf.relative_to(lookpath.parent)
				if cf.name in result['content_folders'] and not cf in [cfname.name for cfname in relative.parents]:
					result['content_folders'][cf].append(lookpath.parent / relative)

			continue

	#
	# Быть или не быть: Сразу делать словарь или потом удалять дубликаты из массива? У массивов сиськи большие... :(
	#
	found_vpks = list(dict.fromkeys(found_vpks))
	result['vpks'] = found_vpks

	# remove content folder duplicates
	for rmdupli in result['content_folders']:
		result['content_folders'][rmdupli] = list(dict.fromkeys(result['content_folders'][rmdupli]))

	return result


# imporant: this is hardcoded to work with the reuslt of gameinfo_paths_lookup
# for now, thr whole chain past gameinfo_paths_lookup is hardcoded to work as a system to show skyboxes in the skyboxer app

# takes gameinfo location
# and path to the engine folder with with bin (vpk.exe n shit)
def find_skyboxes(gminfopath, enginepath):
	import subprocess

	lookup_paths = gameinfo_paths_lookup(r"E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer\ded123\gameinfo.txt")
	
	engpath = Path(enginepath)

	found_skyboxes = []

	# first - lookup vpks
	for vpk in lookup_paths['vpks']:
		# parameters to dump the contents of the vpk
		vpk_exe_prms = [
			# vpk exexutable
			str(engpath / 'bin' / 'vpk.exe'),
			# l = list contents. Fun fact: it's blazing fast
			'l',
			# vpk location
			str(vpk)
		]

		# get list of all the files in vpk
		vpkexe_output = subprocess.run(vpk_exe_prms, capture_output=True)
		flist = [Path(file.strip()) for file in vpkexe_output.stdout.decode().split('\n')]

		csides = [
			'ft',
			'lf',
			'bk',
			'up',
			'rt'
		]

		hdr_dict = [
			'hdr',
			'hdr-',
			'hdr_',
			'hdr ',
		]

		ldrfall_dict = [
			'',
			'-',
			'_',
			' ',

			'ldr',
			'-ldr',
			'_ldr',
			' ldr'
		]

		registry = []

		# some skies may not have the bottom
		for sky in flist:
			# tiny little filter
			if 'bk.vtf' in sky.name.lower():
				clear_name = sky.name.replace('bk.vtf', '')
				# print('processing', clear_name)
				folder = sky.parent
				regname = (sky.name
					.rstrip('bk.vtf')

					.rstrip('hdrbk.vtf')

					.rstrip('hdr-bk.vtf')

					.rstrip('hdr_bk.vtf')

					.rstrip('hdr bk.vtf')
				)


				# if this skybox is in the registry - continue
				if (folder / regname) in registry:
					continue
				registry.append(folder / regname)

				# check if all sides are actually there no matter the HDR whatsoever
				eligible = True
				for side in csides:
					if not (folder / (clear_name + side + '.vtf')) in flist:
						eligible = False
						break
				if eligible == False:
					continue


				hdr_path = None
				ldr_path = None

				# all sides are there, good
				# now check if it is OR has HDR
				hdrhits = 0
				hdr_ns = None

				#
				# check if it's HDR
				#
				for side in csides:
					# check for all naming schemas per side
					for ns in hdr_dict:
						# there have to be 5 hits in total
						if (folder / (clear_name.rstrip(ns) + ns + side + '.vtf')) in flist:
							# We have a hit. Write down naming schema and check next side
							hdrhits += 1
							# write down naming schema
							hdr_ns = ns
							break
				ishdr = True if hdrhits >= 5 else False
				print(clear_name, ishdr)

				# if it's not HDR, but eligible - we found an LDR version of this skybox
				# now check if it has an HDR version
				# check for all naming schemas per side
				ldr_ns = None
				hdrhits = 0
				if ishdr == False:
					# check if every side is present
					for side in csides:
						# for every HDR schema
						for hs in hdr_dict:
							# check every LDR schema
							for ld in ldrfall_dict:
								# there have to be 5 hits in total
								# add ldr schema --> add hdr schema --> check
								if (folder / (clear_name + ld + hs + side + '.vtf')) in flist:
									hdrhits += 1
									# write down naming schema
									ldr_ns = ld + hs
									break

					has_hdr = True if hdrhits >= 5 else False
					# if not all sides are present - write down skybox as LDR only and proceed to the next skybox
					found_skyboxes.append({
						'hdr': (folder / (clear_name + str(ldr_ns))).as_posix() if has_hdr == True else None,
						'ldr': (folder / clear_name).as_posix(),
						'vpk': True,
						'vpk_path': str(vpk)
					})
					# print((folder / (clear_name + str(ldr_ns))).as_posix(), (folder / clear_name).as_posix())
					continue


				#
				# if it IS HDR - we found the HDR, now try finding LDR fallback
				#
				has_ldr_fallback = False
				if ishdr == True:
					ldr_fallback_hits = 0
					for side in csides:
						# compare against LDR naming schemas
						for lds in ldrfall_dict:
							# strip HDR schema --> strip LDR schema --> check
							if (folder / (clear_name.rstrip(hdr_ns).rstrip(lds) + side + '.vtf')) in flist:
								# set schema
								ldr_ns = lds
								# add hit
								ldr_fallback_hits += 1
					has_ldr_fallback = True if ldr_fallback_hits >= 5 else False

					# we found an HDR skybox with LDR fallback
					found_skyboxes.append({
						'hdr': (folder / clear_name).as_posix(),
						'ldr': (folder / (clear_name.strip(hdr_ns).strip(ldr_ns))).as_posix() if has_ldr_fallback == True else None,
						'vpk': True,
						'vpk_path': str(vpk)
					})








	# folders have priority over vpks
	registry = []
	# then - lookup folders
	for matfolder in lookup_paths['content_folders']['materials']:
		matfolder = Path(matfolder)
		for rawsky in matfolder.rglob('*.vtf'):
			# tiny little filter
			if 'bk.vtf' in rawsky.name.lower():
				clear_name = rawsky.name.replace('bk.vtf', '')
				# print('processing', clear_name)
				folder = rawsky.parent
				regname = (rawsky.name
					.rstrip('bk.vtf')

					.rstrip('hdrbk.vtf')

					.rstrip('hdr-bk.vtf')

					.rstrip('hdr_bk.vtf')

					.rstrip('hdr bk.vtf')
				)


				# if this skybox is in the registry - continue
				if (folder / regname) in registry:
					continue
				registry.append(folder / regname)

				# check if all sides are actually there no matter the HDR whatsoever
				eligible = True
				for side in csides:
					if not (folder / (clear_name + side + '.vtf')).is_file():
						eligible = False
						break
				if eligible == False:
					continue


				hdr_path = None
				ldr_path = None

				# all sides are there, good
				# now check if it is OR has HDR
				hdrhits = 0
				hdr_ns = None

				#
				# check if it's HDR
				#
				for side in csides:
					# check for all naming schemas per side
					for ns in hdr_dict:
						# there have to be 5 hits in total
						if (folder / (clear_name.rstrip(ns) + ns + side + '.vtf')).is_file():
							# We have a hit. Write down naming schema and check next side
							hdrhits += 1
							# write down naming schema
							hdr_ns = ns
							break
				ishdr = True if hdrhits >= 5 else False
				print(clear_name, ishdr)

				# if it's not HDR, but eligible - we found an LDR version of this skybox
				# now check if it has an HDR version
				# check for all naming schemas per side
				ldr_ns = None
				hdrhits = 0
				if ishdr == False:
					# check if every side is present
					for side in csides:
						# for every HDR schema
						for hs in hdr_dict:
							# check every LDR schema
							for ld in ldrfall_dict:
								# there have to be 5 hits in total
								# add ldr schema --> add hdr schema --> check
								if (folder / (clear_name + ld + hs + side + '.vtf')).is_file():
									hdrhits += 1
									# write down naming schema
									ldr_ns = ld + hs
									break

					has_hdr = True if hdrhits >= 5 else False
					# if not all sides are present - write down skybox as LDR only and proceed to the next skybox
					found_skyboxes.append({
						'hdr': (folder / (clear_name + str(ldr_ns))).as_posix() if has_hdr == True else None,
						'ldr': (folder / clear_name).as_posix(),
						'vpk': True,
						'vpk_path': str(vpk)
					})
					# print((folder / (clear_name + str(ldr_ns))).as_posix(), (folder / clear_name).as_posix())
					continue


				#
				# if it IS HDR - we found the HDR, now try finding LDR fallback
				#
				has_ldr_fallback = False
				if ishdr == True:
					ldr_fallback_hits = 0
					for side in csides:
						# compare against LDR naming schemas
						for lds in ldrfall_dict:
							# strip HDR schema --> strip LDR schema --> check
							if (folder / (clear_name.rstrip(hdr_ns).rstrip(lds) + side + '.vtf')).is_file():
								# set schema
								ldr_ns = lds
								# add hit
								ldr_fallback_hits += 1
					has_ldr_fallback = True if ldr_fallback_hits >= 5 else False

					# we found an HDR skybox with LDR fallback
					found_skyboxes.append({
						'hdr': (folder / clear_name).as_posix(),
						'ldr': (folder / (clear_name.strip(hdr_ns).strip(ldr_ns))).as_posix() if has_ldr_fallback == True else None,
						'vpk': False
					})


	print('Found all skyboxes')
	return found_skyboxes


def mdma():
	sk = find_skyboxes(r'E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer\ded123\gameinfo.txt', r'E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer')
	print(json.dumps(sk))

mdma()