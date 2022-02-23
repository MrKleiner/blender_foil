
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














# you can add (and store) variables to class with internal functions via self.whatever
# you can also have this name pre-defined and then overwrite it.
# All imports should happen in init. It will be reusable in all the other functions.
class lizardvmf:
	'Simple, but flexible vmf parser, read more at https://mrkleiner.github.io/source_tricks'
	# anything that is specified becomes defaults. Useful
	# Create a string at the very top of the class to make it a documentation
	# variables inside functions HAVE NO CONNECTION to the class variables no matter what
	# to access/write stored variables use self.whatever



	#
	# Defaults
	#

	# The beautiful soup object. None by default
	# This is a refined vmf xml bs4 object for manipulations and modifications
	lizard = None

	# The result of reconstructed vmf, None by default
	# Gotta be careful since this could give outdated results
	readyvmfstr = None




	#
	# Functionality
	#



	# Supposedly, the parse should happen when the class is being created...
	def __init__(self, pootis):
		from bs4 import BeautifulSoup, Tag, NavigableString
		import io

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


		# Since we're not dealing with files anymore (at least for now) - we cannot just do .readlines()
		# gotta use io module
		inpstr = io.StringIO(mapstring_input)
		# so that we have access to .readlines() again
		maplines = buf.readlines()

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
		lizard = BeautifulSoup(rawvmf, 'html.parser')

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



		# finally, write reconstruct back and return the string
		self.readyvmf = rcf
		return rcf


	# Returns a dict of basic stats
	def vmfstats(self):
		stats = {}

		# basic info

		# -- number of entities --
		# static props do not count
		allowance = {
			'hl2': 4096,
			'tf2': 4096,
			'portal2': 8192,
			'gmod': 16384
		}

		total = 0
		notcount = ['prop_static', 'sprite_clientside', 'prop_detail']
		for ent in lizard.select('map entity'):
			if not ent['classname'] in notcount:
				total += 1

		stats['enum_edict'] = total
		stats['total_ents'] = len(lizard.select('map entity'))

		return stats






# test
fr = open(r'E:\!!Blend_Projects\scripts\map_parser\example_map_src.vmf', 'r').read()

lol = lizardvmf(fr)

print(lol.vmfstats())