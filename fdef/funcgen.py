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



with open('funcdef.py', 'r') as txtfile:
    funcdef = txtfile.readlines()

result_cases = ''

for ind, ln in enumerate(funcdef):
    if '#' in ln:
        funcdef[ind] = ''

loadjson = json.loads(''.join(funcdef))

for connect_entry in loadjson:
    priority = {
        'js_module': 'echo_status' if connect_entry.get('js_module') == None else connect_entry.get('js_module'),
        'js_module_action': 'echo_status' if connect_entry.get('js_module_action') == None else connect_entry.get('js_module_action'),
    }
    result_cases += standard_case.replace('CASEREPALCE', connect_entry['incoming_case']).replace('MODREPLACE', priority['js_module']).replace('MODACTIONREPLACE', priority['js_module_action']).replace('PAYLOADREPLACE', connect_entry['python_function'] + """(cs['payload'])""")


with open((Path(__file__).parent.parent / 'blfoil_appconnect.py'), 'w') as txtfile:
    funcdef = txtfile.write(globl.replace('CASESREPLACE', result_cases))