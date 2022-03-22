
# Expects any kind of iterable object
# although it'll die if anything besides valid vmf is passed
def vmfparser(mlines):
	# todo: Fucking imports
	from bs4 import BeautifulSoup, Tag, NavigableString
	import io
	import base64

	maplines = mlines

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
					print('WHAT THE FUCK?', vst.strip())
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

	return lizard