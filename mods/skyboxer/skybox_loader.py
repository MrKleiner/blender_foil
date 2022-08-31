


#
# Important note the order from gameinfo IS preserved!
#

# important todo: this is not very realiable. There are many stupid assumptions
def gameinfo_paths_lookup(cl):
	from pathlib import Path
	import json
	from ...utils.lizard_tail.lizard_tail import lizard_tail
	from ...utils.shared import app_command_send, where_addon_root
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
def find_skyboxes(gminfopath):
	import subprocess, json
	from pathlib import Path
	from ...utils.lizard_tail.lizard_tail import lizard_tail
	from ...utils.shared import app_command_send, where_addon_root
	addon_root_dir = where_addon_root(__file__)

	lookup_paths = gameinfo_paths_lookup(gminfopath['gameinfo'])
	app_command_send({
		'app_module': 'echo_status',
		'mod_action': '',
		'payload': str(lookup_paths)
	})
	vpkexe = addon_root_dir / 'bins' / 'vpk' / 'vpk.exe'

	found_skyboxes = []

	# first - lookup vpks
	for vpk in lookup_paths['vpks']:
		# parameters to dump the contents of the vpk
		vpk_exe_prms = [
			# vpk exexutable
			str(vpkexe),
			# l = list contents. Fun fact: it's blazing fast
			'l',
			# vpk location
			str(vpk)
		]

		# get list of all the files in vpk
		vpkexe_output = subprocess.run(vpk_exe_prms, capture_output=True)
		# flist = [Path(file.strip()) for file in vpkexe_output.stdout.decode().split('\n') if not 'models/' in file and not 'sounds/' in file and not '.vmt' in file]
		
		# important todo: make an extremely rude assumption that all skyboxes are stored in the skybox folder
		flist = [Path(file.strip()) for file in vpkexe_output.stdout.decode().split('\n') if 'skybox/' in file]
		app_command_send({
			'app_module': 'echo_status',
			'mod_action': '',
			'payload': len(flist)
		})

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

		registry = [None]

		# some skies may not have the bottom
		for sky in flist:
			# tiny little filter
			if 'bk.vtf' in sky.name.lower():
				clear_name = sky.name.replace('bk.vtf', '')
				# print('processing', clear_name)
				folder = sky.parent

				# if this skybox is in the registry - continue
				# if (folder / clear_name) in registry:
				# 	continue


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
					hd_path = (folder / (clear_name + str(ldr_ns))).as_posix() if has_hdr == True else None
					ld_path = (folder / clear_name).as_posix()
					
					if ld_path in registry or (hd_path in registry and None in registry):
						continue

					found_skyboxes.append({
						'hdr': hd_path,
						'ldr': ld_path,
						'vpk': True,
						'vpk_path': str(vpk)
					})
					registry.append(ld_path)
					registry.append(hd_path)

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

					hd_path = (folder / clear_name).as_posix()
					ld_path = (folder / (clear_name.strip(hdr_ns).strip(ldr_ns))).as_posix() if has_ldr_fallback == True else None
					
					if ld_path in registry or (hd_path in registry and None in registry):
						continue

					# we found an HDR skybox with LDR fallback
					found_skyboxes.append({
						'hdr': hd_path,
						'ldr': ld_path,
						'vpk': True,
						'vpk_path': str(vpk)
					})
					registry.append(ld_path)
					registry.append(hd_path)
					continue








	# folders have priority over vpks
	registry = [None]
	# then - lookup folders
	for matfolder in lookup_paths['content_folders']['materials']:
		matfolder = Path(matfolder)
		for rawsky in matfolder.rglob('*.vtf'):
			# tiny little filter
			if 'bk.vtf' in rawsky.name.lower():
				clear_name = rawsky.name.replace('bk.vtf', '')
				# print('processing', clear_name)
				folder = rawsky.parent


				# if this skybox is in the registry - continue
				if (folder / clear_name) in registry:
					continue
				registry.append(folder / clear_name)

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

					hd_path = (folder / (clear_name + str(ldr_ns))).as_posix() if has_hdr == True else None
					ld_path = (folder / clear_name).as_posix()
					
					if ld_path in registry or (hd_path in registry and None in registry):
						continue

					found_skyboxes.append({
						'hdr': hd_path,
						'ldr': ld_path,
						'vpk': False,
						'vpk_path': str(vpk)
					})
					registry.append(ld_path)
					registry.append(hd_path)
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

					hd_path = (folder / clear_name).as_posix()
					ld_path = (folder / (clear_name.strip(hdr_ns).strip(ldr_ns))).as_posix() if has_ldr_fallback == True else None
					
					if ld_path in registry or (hd_path in registry and None in registry):
						continue

					# we found an HDR skybox with LDR fallback
					found_skyboxes.append({
						'hdr': hd_path,
						'ldr': ld_path,
						'vpk': False
					})
					registry.append(ld_path)
					registry.append(hd_path)
					continue


	print('Found all skyboxes')
	return found_skyboxes




# continuation of the chain
# takes skybox meta as an input generated by find_skyboxes
# returns bitmaps
def load_sky_bitmap(skyinfo):
	import subprocess, base64, json
	from pathlib import Path 
	from ...utils.lizard_tail.lizard_tail import lizard_tail
	from ...utils.shared import app_command_send, where_addon_root
	addon_root_dir = where_addon_root(__file__)

	magix = addon_root_dir / 'bins' / 'imgmagick' / 'magick.exe'
	ffmpeg = addon_root_dir / 'bins' / 'ffmpeg' / 'bin' / 'ffmpeg.exe'

	# todo: this is ungly
	skyinfo = skyinfo['skyinfo']

	vpkexe = addon_root_dir / 'bins' / 'vpk' / 'vpk.exe'
	vtfcmdexe = addon_root_dir / 'bins' / 'vtf_cmd' / 'bin' / 'x64' / 'VTFCmd.exe'
	ext_dir = vpkexe.parent
	skysides = [
		'ft',
		'lf',
		'bk',
		'up',
		'rt',
		'dn'
	]

	hl_dict = [
		'ldr',
		'hdr'
	]

	result_sky = {}

	#
	# again, start with vpks
	#
	if skyinfo['vpk'] == True:

		#
		# create folder structure
		#

		# create hdr, if any
		if skyinfo['hdr'] != None:
			(ext_dir / Path(skyinfo['hdr']).parent).mkdir(parents=True, exist_ok=True)
		# create ldr, if any
		if skyinfo['ldr'] != None:
			(ext_dir / Path(skyinfo['ldr']).parent).mkdir(parents=True, exist_ok=True)

		#
		# Extract files one by one, because apparently vpk.exe crashes when it cannot fine a file
		#
		vpk_exe_prms = [
			# vpk exexutable
			str(vpkexe),
			# x = extract content
			# important: before extracting the file - it's required to have the folder structre leading to that file
			'x',
			# vpk location
			str(skyinfo['vpk_path']),
			None
		]
		vtfcmd_prms = [
			# vtfcmd exexutable
			str(vtfcmdexe),
			# this is required
			'-file',
			# vtf location
			None
		]

		for extr in skysides:
			# try extracting HDR
			vpk_exe_prms[-1] = str(Path(str(skyinfo['hdr']) + extr + '.vtf'))
			# execute extraction
			extr_echo = subprocess.run(vpk_exe_prms, capture_output=True, cwd=str(ext_dir))
			print(extr_echo.stdout)


			# try extracting LDR
			vpk_exe_prms[-1] = str(Path(str(skyinfo['ldr']) + extr + '.vtf'))
			# execute extraction
			extr_echo = subprocess.run(vpk_exe_prms, capture_output=True, cwd=str(ext_dir))
			print(extr_echo.stdout)

		#
		# now that files are extracted - convert them to tga with vtfcmd and store in memory as base64
		#
		for svtf in skysides:
			# try both HDR and LDR for a side
			for hdld in hl_dict:
				# only proceed if hdr/ldr exists
				if skyinfo[hdld] == None:
					continue

				# important todo: Do NOT convert both HDR and LDR for previews

				# construct the path to vtf
				tgt_vtf = (ext_dir / Path(skyinfo[hdld] + svtf + '.vtf'))
				# only proceed further if this vtf exists
				if not tgt_vtf.is_file():
					result_sky[svtf + '_' + hdld] = None
					continue
				print('vtf file exists')
				vtfcmd_prms[-1] = str(tgt_vtf)
				vtf_conv_echo = subprocess.run(vtfcmd_prms, capture_output=True)

				# conversion done. Check success by checking the file existence
				if tgt_vtf.with_suffix('.tga').is_file():
					# convert shite with magick
					magix_prms = [
						str(magix),
						str(tgt_vtf.with_suffix('.tga')),

						# webp parameters
						'-quality', '0',
						'-define', 'webp:lossless=true',
						'-define', 'webp:partition-limit=0',
						'-define', 'webp:thread-level=1',
						str('webp:')
					]

					# ffmpeg is 10 times faster
					ffmpeg_prms = [
						# mpeg
						str(ffmpeg),
						# input
						'-i', str(tgt_vtf.with_suffix('.tga')),

						# resize
						# '-hwaccel', 'cuda',
						# '-hwaccel_output_format', 'cuda',
						# '--enable-nvenc',
						# '--enable-ffnvcodec',
						# '-h', 'encoder=h264_nvenc',
						
						# does nothing
						# (it works, but it's only for videos)
						'-vcodec', 'h264_nvenc',
						
						# change size
						# this will upscale sometimes
						# '-vf', 'scale=500:-1',

						# while this is smart
						# this is quite a hires preview
						# '-vf', 'scale=w=min(iw\\,500):h=-2',
						# this one is smaller
						'-vf', 'scale=w=min(iw\\,300):h=-2, vflip',

						# format
						'-c:v', 'webp',
						# ffmpeg encoding type
						'-f', 'image2pipe',
						# lossless
						# quite a heavy load
						# '-lossless', '0',
						# make it take even less space
						'-lossless', '0',
						# lossless compression
						# (now is lossy)
						'-compression_level', '0',
						# '-compression_level', '0',
						'-qscale', '50',
						# output to stdout
						'pipe:'
					]

					towebp = subprocess.run(ffmpeg_prms, capture_output=True)

					print('tga file exists')
					# if file exists - read its contents into buffer
					result_sky[svtf + '_' + hdld] = base64.b64encode(towebp.stdout).decode()





	#
	# Continue with files
	#
	if skyinfo['vpk'] == False:

		#
		# convert sides to tga with vtfcmd and store in memory as base64
		#
		for svtf in skysides:
			# try both HDR and LDR for a side
			for hdld in hl_dict:
				# only proceed if hdr/ldr exists
				if skyinfo[hdld] == None:
					continue
				# construct the path to vtf
				tgt_vtf = (ext_dir / Path(skyinfo[hdld] + svtf + '.vtf'))
				# only proceed further if this vtf exists
				if not tgt_vtf.is_file():
					result_sky[svtf + '_' + hdld] = None
					continue
				print('vtf file exists')
				vtfcmd_prms[-1] = str(tgt_vtf)
				vtf_conv_echo = subprocess.run(vtfcmd_prms, capture_output=True)

				# conversion done. Check success by checking the file existence
				if tgt_vtf.with_suffix('.tga').is_file():
					# convert shite with magick
					magix_prms = [
						str(magix),
						str(tgt_vtf.with_suffix('.tga')),

						# webp parameters
						'-quality', '0',
						'-define', 'webp:lossless=true',
						'-define', 'webp:partition-limit=0',
						'-define', 'webp:thread-level=1',
						str('webp:')
					]

					# ffmpeg is 10 times faster
					ffmpeg_prms = [
						# mpeg
						str(ffmpeg),
						# input
						'-i', str(tgt_vtf.with_suffix('.tga')),

						# resize
						# '-hwaccel', 'cuda',
						# '-hwaccel_output_format', 'cuda',
						# '--enable-nvenc',
						# '--enable-ffnvcodec',
						# '-h', 'encoder=h264_nvenc',
						
						# does nothing
						# (it works, but it's only for videos)
						'-vcodec', 'h264_nvenc',
						
						# change size
						# this will upscale sometimes
						# '-vf', 'scale=500:-1',

						# while this is smart
						# this is quite a hires preview
						# '-vf', 'scale=w=min(iw\\,500):h=-2',
						# this one is smaller
						'-vf', 'scale=w=min(iw\\,300):h=-2, vflip',

						# format
						'-c:v', 'webp',
						# ffmpeg encoding type
						'-f', 'image2pipe',
						# lossless
						# quite a heavy load
						# '-lossless', '0',
						# make it take even less space
						'-lossless', '0',
						# lossless compression
						# (now is lossy)
						'-compression_level', '6',
						# '-compression_level', '0',
						'-qscale', '50',
						# output to stdout
						'pipe:'
					]

					towebp = subprocess.run(ffmpeg_prms, capture_output=True)

					print('non-vpk tga file exists')
					# if file exists - read its contents into buffer
					result_sky[svtf + '_' + hdld] = base64.b64encode(towebp.stdout).decode()







	return result_sky




def mdma():
	pass
	# import json
	# sk = find_skyboxes(r'E:\Gamess\steamapps\common\Source SDK Base 2013 Singleplayer\ded123\gameinfo.txt', r"C:\Users\DrHax\AppData\Roaming\Blender Foundation\Blender\3.1\scripts\addons\blender_foil\bins\vpk\vpk.exe")
	# print(json.dumps(sk))
	# sex = load_sky_bitmap(sk[0], r"C:\Users\DrHax\AppData\Roaming\Blender Foundation\Blender\3.1\scripts\addons\blender_foil\bins\vpk\vpk.exe", r"C:\Users\DrHax\AppData\Roaming\Blender Foundation\Blender\3.1\scripts\addons\blender_foil\bins\vtf_cmd\bin\x64\VTFCmd.exe")
	# print(sex)
# mdma()