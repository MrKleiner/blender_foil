
# Expects any kind of iterable object
# although it'll die if anything besides valid vmf is passed
def gameinfoparser(mlines):
	# todo: Fucking imports
	from bs4 import BeautifulSoup, Tag, NavigableString
	import io
	import base64
	import time

	maplines = mlines

	rawvmf = ''

	
	important_timings = int(round(time.time() * 1000))

	# open xml root
	rawvmf += ('<inforoot>' + '\n')

	for mpindex, mapline in enumerate(maplines):
		if not mapline.strip().startswith('//'):
			# try, because invalid index appears when we reach the very last line of the string

			# wait, wtf was that ????
			# maplinef = mapline.split('//')[0]
			maplinef = mapline
			try:
				if '{\n' in maplines[mpindex + 1]:
					isquoted = 'quoted' if maplines[mpindex].count('"') > 1 else ''
					rawvmf += (maplinef.replace(maplines[mpindex].strip(), '').replace('\n', '') + '<item kdict ' + isquoted + ' type="' + maplines[mpindex].replace('"', '').strip() + '">' + '\n')
					maplines[mpindex] = ''
					# print(maplines[mpindex])
			except:
				pass

			if '}\n' in maplinef:
				rawvmf += (maplinef.replace('}\n', '') + '</item>' + '\n')

			if not '}\n' in maplinef and not '{\n' in maplinef and len(maplines[mpindex].strip()) != 0:
				rawvmf += '<kv>' + maplines[mpindex].split('//')[0] + '</kv>'
				# rawvmf += '<kv>' + maplines[mpindex] + '</kv>'

			if not '}\n' in maplinef and not '{\n' in maplinef and len(maplines[mpindex].strip()) == 0:
				rawvmf += '<entr></entr>'
		else:
			rawvmf += '<ign>' + maplines[mpindex] + '</ign>'


	rawvmf += ('</inforoot>')

	print('lizvmf vmf convert took', int(round(time.time() * 1000)) - important_timings, 'msec')

	# return rawvmf

	#
	# refinery
	#

	# This will be a bs4 xml object
	# It will be modified (refined)
	important_timings = int(round(time.time() * 1000))
	lizard = BeautifulSoup(rawvmf, 'lxml', multi_valued_attributes=None)
	print('lizvmf bs4 read with lxml took', int(round(time.time() * 1000)) - important_timings, 'msec')



	# rename tags to their corresponding namez
	# todo: name them the proper way right away ?
	for etname in lizard.select('inforoot item'):
		etname.name = etname['type']
		del etname['type']


	def splitbyfirstchar(inpstr, ch):
		rubbish = str(inpstr).split(str(ch))
		one = rubbish[0]
		del rubbish[0]
		two = str(ch).join(rubbish)
		return (one, two)
		

	for kvt in lizard.select('inforoot GameInfo kv'):
		kv_str = kvt.string.strip()
		# print(kv_str)
		kv_format = splitbyfirstchar(kv_str.replace('\t', ' '), ' ')
		print(kv_format)
		kvt.string = ''
		keytag = lizard.new_tag('gkey')
		if kv_format[0].count('"') > 1:
			keytag['quoted'] = True
		keytag.string = kv_format[0].strip().replace('"', '')
		kvt['keyname'] = kv_format[0].strip().replace('"', '')
		kvt.append(keytag)

		valuetag = lizard.new_tag('gval')
		if kv_format[1].count('"') > 1:
			valuetag['quoted'] = True
		valuetag.string = kv_format[1].strip().replace('"', '')
		kvt.append(valuetag)


	return lizard