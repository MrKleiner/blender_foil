"""
why = [
    {
        'keyname': 'lizards',
        'key_content': [
            {
                'keyname': 'iguana',
                'keycontent': '1'
            },
            {
                'keyname': 'geko',
                'keycontent': '1'
            }
        
        ]
    },
    
    {
        'keyname': 'snakes',
        'key_content': [
            {
                'keyname': 'python',
                'keycontent': '1'
            },
            {
                'keyname': 'cobra',
                'keycontent': '0'
            }
        
        ]
    }
]


result = ''

def printStruct(struc, indent=0):
  if isinstance(struc, dict):
    print ('  '*indent+'{')
    for key,val in struc.items():
      if isinstance(val, (dict, list, tuple)):
        print ('  '*(indent+1) + str(key) + '=> ')
        printStruct(val, indent+2)
      else:
        print ('  '*(indent+1) + str(key) + '=> ' + str(val))
    print ('  '*indent+'}')
  elif isinstance(struc, list):
    print ('  '*indent + '[')
    for item in struc:
      printStruct(item, indent+1)
    print ('  '*indent + ']')
  elif isinstance(struc, tuple):
    print ('  '*indent + '(')
    for item in struc:
      printStruct(item, indent+1)
    print ('  '*indent + ')')
  else: print ('  '*indent + str(struc))
    


d = [{'a1':1, 'a2':2, 'a3':3}, [1,2,3], [{'b1':1, 'b2':2}, {'c1':1}], 'd1', 'd2', 'd3']




printStructv(why)



====================================== SOURCE
 def printStruct(struc, indent=0):
   if isinstance(struc, dict):
     print ('  '*indent+'{')
     for key,val in struc.items():
       if isinstance(val, (dict, list, tuple)):
         print ('  '*(indent+1) + str(key) + '=> ')
         printStruct(val, indent+2)
       else:
         print ('  '*(indent+1) + str(key) + '=> ' + str(val))
     print ('  '*indent+'}')
   elif isinstance(struc, list):
     print ('  '*indent + '[')
     for item in struc:
       printStruct(item, indent+1)
     print ('  '*indent + ']')
   elif isinstance(struc, tuple):
     print ('  '*indent + '(')
     for item in struc:
       printStruct(item, indent+1)
     print ('  '*indent + ')')
   else: print ('  '*indent + str(struc))










"""

















why = [
    {
        'keyname': 'GameInfo',
        'keycontent': [
            {
                'keyname': 'lizards',
                'key_content': [
                    {
                        'keyname': 'iguana',
                        'keycontent': '1'
                    },
                    {
                        'keyname': 'geko',
                        'keycontent': '1'
                    },
                    {
                        'keyname': 'geko',
                        'keycontent': 'pootis'
                    }
                
                ]
            },

            {
                'keyname': 'snakes',
                'key_content': [
                    {
                        'keyname': 'python',
                        'keycontent': '1'
                    },
                    {
                        'keyname': 'cobra',
                        'keycontent': '0'
                    }
                
                ]
            }
        ]
    }
]

global result, kl
result = ''
kl = 0

# regular print
def drop(wh):
    print(wh)
    return '\n' + wh

def adds(wh):
    print(wh)
    return wh

def printStruct(struc, indent=0):
	global result, kl
	if isinstance(struc, dict):
		#print ('  '*indent+'{')
		for key,val in struc.items():
			if isinstance(val, (dict, list, tuple)):
				#print ('  '*(indent+1) + '"' + str(key) + '" ')
				printStruct(val, indent+2)
			else:
				if key == 'keycontent' and isinstance(val, str):
					result += adds (' '*(15 - kl) + ' "' + str(val) + '"')
				if key == 'keyname':
					kl = len(str(val))
					result += drop ('  '*(indent+1) + '"' + str(val) + '"')
					#print ('  '*indent+'}')
	elif isinstance(struc, list):
		result += drop ('  '*(indent-1) + '{')
		for item in struc:
		printStruct(item, indent+1)
		result += drop ('  '*(indent-1) + '}')
	elif isinstance(struc, tuple):
		result += drop ('  '*indent + '(')
	for item in struc:
		printStruct(item, indent+1)
		result += drop ('  '*indent + ')')
	else: result += drop ('  '*indent + str(struc))


"""
def printStruct(struc, indent=0):
  global result, kl
  if isinstance(struc, dict):
    #print ('  '*indent+'{')
    for key,val in struc.items():
      if isinstance(val, (dict, list, tuple)):
        #print ('  '*(indent+1) + '"' + str(key) + '" ')
        printStruct(val, indent+2)
      else:
        if key == 'keycontent' and isinstance(val, str):
            result += adds (' '*(15 - kl) + ' "' + str(val) + '"')
        if key == 'keyname':
          kl = len(str(val))
          result += drop ('  '*(indent+1) + '"' + str(val) + '"')
    #print ('  '*indent+'}')
  elif isinstance(struc, list):
    result += drop ('  '*(indent-1) + '{')
    for item in struc:
      printStruct(item, indent+1)
    result += drop ('  '*(indent-1) + '}')
  elif isinstance(struc, tuple):
    result += drop ('  '*indent + '(')
    for item in struc:
      printStruct(item, indent+1)
    result += drop ('  '*indent + ')')
  else: result += drop ('  '*indent + str(struc))
    
"""

d = [{'a1':1, 'a2':2, 'a3':3}, [1,2,3], [{'b1':1, 'b2':2}, {'c1':1}], 'd1', 'd2', 'd3']


print('drop1')

printStruct(why)

print('result')

print(result)