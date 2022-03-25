import json
nen = open('blpe_main_old.json').read()
old_blpe = json.loads(nen)

new_blpe = {}

# classnames
for etype in old_blpe:
	print(etype)
	new_blpe[etype] = []


	# data types

	# strings
	doplayload = []
	for data_string in old_blpe[etype][0]:
		# print(data_type)
		splitter = old_blpe[etype][0][data_string].split(':-:')
		new_payload = {
			"guiname": data_string,
			"idname": splitter[0],
			"default": splitter[1].strip(),
			"descr": splitter[2]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)

	# ints
	doplayload = []
	for data_string in old_blpe[etype][1]:
		# print(data_type)
		splitter = old_blpe[etype][1][data_string].split(':-:')
		new_payload = {
			"guiname": data_string,
			"idname": splitter[0],
			"default": splitter[1].strip(),
			"descr": splitter[2]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)


	# floats
	doplayload = []
	for data_string in old_blpe[etype][2]:
		# print(data_type)
		splitter = old_blpe[etype][2][data_string].split(':-:')
		new_payload = {
			"guiname": data_string,
			"idname": splitter[0],
			"default": splitter[1].strip(),
			"descr": splitter[2]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)

	# colours
	doplayload = []
	for data_string in old_blpe[etype][3]:
		# print(data_type)
		splitter = old_blpe[etype][3][data_string].split(':-:')
		new_payload = {
			"guiname": data_string,
			"idname": splitter[0],
			"default": splitter[1].strip(),
			"descr": splitter[2]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)



	# standard enums
	doplayload = []
	for data_string in old_blpe[etype][4]:
		# print(data_type)
		splitter = data_string.split(':-:')
		new_payload = {
			"guiname": data_string.split(':-:')[0],
			"idname": "nil",
			"default": splitter[1].strip(),
			"descr": splitter[2],
			"eitems": {}
		}
		for item in old_blpe[etype][4][data_string][0]:
			new_payload['idname'] = old_blpe[etype][4][data_string][0][item].split(':-:')[0]
			new_payload['eitems'][item] = old_blpe[etype][4][data_string][0][item].split(':-:')[1]
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)


	# boolean list enums
	doplayload = []
	for data_string in old_blpe[etype][5]:
		# print(data_type)
		splitter = old_blpe[etype][5][data_string].split(':-:')
		new_payload = {
			"guiname": data_string,
			"idname": splitter[0],
			"default": splitter[1].strip(),
			"descr": splitter[2]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)


	# flags
	doplayload = []
	for data_string in old_blpe[etype][6]:
		# print(data_type)
		splitter = old_blpe[etype][6][data_string].split(':-:')
		new_payload = {
			"byte": data_string,
			"default": splitter[0].strip(),
			"descr": splitter[1]
		}
		doplayload.append(new_payload)
	new_blpe[etype].append(doplayload)

	
	# outputs
	doplayload = []
	for data_string in old_blpe[etype][7]:
		doplayload.append(data_string)
	new_blpe[etype].append(doplayload)
	
	# inputs
	doplayload = []
	for data_string in old_blpe[etype][8]:
		doplayload.append(data_string)
	new_blpe[etype].append(doplayload)

	# bledner config
	doplayload = {}
	for data_string in old_blpe[etype][9]:
		doplayload[data_string] = old_blpe[etype][9][data_string]
	new_blpe[etype].append(doplayload)




new_conf = open('lol.json', 'w')
new_conf.write(json.dumps(new_blpe, indent=4, sort_keys=False))