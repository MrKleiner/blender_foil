# wrap into quotation marks
def wap(ste):
	return '"' + str(ste) + '"'

# takes key name, object, whether to insert line break or not and number of tabs, returns reconstruct string
# converts given attribute name of a tag to .vmf standard key - value
def wapr(itr, ob, brk, tabs):
	mktabs = ''.join(['\t' for tb in range(int(tabs))])
	return mktabs + wap(itr) + ' ' + wap(ob[itr]) + ('\n' if int(brk) == 1 else '')

# takes tag as an input and number of tabs, returns unwrap
def addv(tg, nt):
	# return mktabs + wap(tg.name) + ' ' + wap(tg.string) + '\n'
	# return mktabs + wap(tg.string)
	return ''.join(['\t' for tb in range(int(nt))]) + tg.string

# open block with tabs and opening bracket
def op(tgname, ntc):
	mktabs = ''.join(['\t' for tb in range(int(ntc))])
	return mktabs + tgname + '\n' + mktabs + '{\n'

# close block
def cl(tabz):
	return ''.join(['\t' for tb in range(int(tabz))]) + '}\n'

def getspaces(ot, outof=21):
	# 21
	# newoutof = 50 if len(ot) >= 21 else 21
	return ''.join([' ' for tits in range(outof - len(ot))]) if len(ot) < outof else '\t'





def write_keyvalues(keyd):
	from bs4 import BeautifulSoup, Tag, NavigableString
	keydepth = len([1 for fuck in keyd.parents]) - 4
	target_st = ''
	target_st += '\n'
	target_st += op(wap(keyd.name) if 'quoted' in keyd.attrs else keyd.name, keydepth)

	# write keyvalues
	for keyv in keyd.children:
		# print(keyv.name == 'kv')
		# if not isinstance(keyv, NavigableString):
		if keyv.name == 'entr':
			target_st += '\n'

		if keyv.name == 'kv':
			#drop
			target_st += '\n'
			# key
			target_st += addv(keyv.gkey, keydepth + 1)
			# spaces
			target_st += getspaces(keyv.gkey.string)
			# value
			target_st += keyv.gval.string

		if keyv.name == 'ign':
			#drop
			target_st += '\n'
			# comment
			keyv.string = keyv.string.strip()
			target_st += addv(keyv.string, keydepth + 1)

	return target_st


# takes tag which is a dict
# rubbish
def build_keydict(lizdict, tgt_str):
	from bs4 import BeautifulSoup, Tag, NavigableString
	keydepth = len([1 for fuck in lizdict.parents])
	tgt_str += '\n'
	tgt_str += op(lizdict.name, keydepth)

	# write keyvalues
	for keyv in lizdict.children:
		if not isinstance(keyv, NavigableString):
			if keyv.name == 'entr':
				tgt_str += '\n'

			if keyv.name == 'kv':
				#drop
				tgt_str += '\n'
				# key
				tgt_str += addv(keyv.gkey, keydepth)
				# spaces
				tgt_str += getspaces(keyv.gkey)
				# value
				tgt_str += keyv.gkey.string

			if 'kdict' in keyv.attrs:
				build_keydict(lizdict, tgt_str)

	tgt_str += cl(keydepth)


#
# takes full bs object as an input, outputs a valid gameinfo string
#
def gameinfo_rebuilder(infolizard):
	result_gminfo = ''
	# open gameinfo
	# result_gminfo += op('"GameInfo"', 0)
	# write global game info
	print([kys for kys in infolizard.inforoot.GameInfo.children][1].name)
	result_gminfo += write_keyvalues(infolizard.inforoot.GameInfo)
	# csgo, if any
	if infolizard.inforoot.GameInfo.hidden_maps != None:
		result_gminfo += write_keyvalues(infolizard.inforoot.GameInfo.hidden_maps)
		result_gminfo += '\n'
		result_gminfo += cl(1)
	# write filesystem (it's literally empty lmfao)
	result_gminfo += write_keyvalues(infolizard.inforoot.GameInfo.FileSystem)
	# write SearchPaths
	result_gminfo += write_keyvalues(infolizard.inforoot.GameInfo.FileSystem.SearchPaths)
	# close SearchPaths
	result_gminfo += '\n'
	result_gminfo += cl(2)
	# close FileSystem
	result_gminfo += cl(1)
	# close GameInfo
	result_gminfo += cl(0)


	# I smoke the baddest dro
	# I stole a Camaro
	# I boned a lizard hoe
	# from that bus stop down the road
	# I drop the baddest bombs
	# I was born in Poznan
	# I CAN DO WHAT I WANT
	# Got them fly ass ниґґа drones

	return '\n'.join(result_gminfo.split('\n')[1:])