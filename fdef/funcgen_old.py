from pathlib import Path
import json

globl = """def appconnect_actions(cs):
    match cs['action']:
CASESREPLACE
            
        case _:
            return 'wtf is even this'"""


standard_case = """
		case 'CASEREPALCE':
            app_command_send({
                'app_module': 'MODREPLACE',
                'mod_action': 'MODACTIONREPLACE',
                'payload': PAYLOADREPLACE
            })
            return ''"""



with open('funcdef.fcd', 'r') as txtfile:
    funcdef = txtfile.readlines()

result_cases = ''

for ln in funcdef:
	# case:js_module:js_module_action:python_function
	if not '//#' in ln and len(ln) > 10:
		line_splitted = ln.split(':')
		result_cases += standard_case.replace('CASEREPALCE', line_splitted[0].strip()).replace('MODREPLACE', line_splitted[1].strip()).replace('MODACTIONREPLACE', line_splitted[2].strip()).replace('PAYLOADREPLACE', line_splitted[3].strip() + """(cs['payload'])""")







with open('test.py', 'w') as txtfile:
    funcdef = txtfile.write(globl.replace('CASESREPLACE', result_cases))