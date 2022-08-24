from pathlib import Path
import json
import os

thisdir = Path(__file__).parent


globl = """def appconnect_actions(cs):
    match cs['action']:
CASESREPLACE
            
        case _:
            # app_command_send({
            #     'app_module': 'echo_status',
            #     'mod_action': 'echo_status',
            #     'payload': 'Unknown incoming case'
            # })
            return 'wtf is even this'"""


standard_case = """
        case 'CASEREPALCE':
            app_command_send({
                'app_module': 'MODREPLACE',
                'mod_action': 'MODACTIONREPLACE',
                'sys_action_id': cs['sys_action_id'],
                'payload': PAYLOADREPLACE
            })
            return ''"""



with open(str(thisdir / 'funcdef.py'), 'r') as txtfile:
    funcdef = txtfile.readlines()

result_cases = ''

result_imports = ''

for ind, ln in enumerate(funcdef):
    if '#' in ln:
        funcdef[ind] = ''

loadjson = json.loads(''.join(funcdef))

for connect_entry in loadjson:

    if connect_entry.get('add_imports') != None:
        for addimport in connect_entry['add_imports']:
            result_imports += addimport + '\n'
        continue


    priority = {
        'js_module': 'echo_status' if connect_entry.get('js_module') == None else connect_entry.get('js_module'),
        'js_module_action': 'echo_status' if connect_entry.get('js_module_action') == None else connect_entry.get('js_module_action'),
    }
    result_cases += standard_case.replace('CASEREPALCE', connect_entry['incoming_case']).replace('MODREPLACE', priority['js_module']).replace('MODACTIONREPLACE', priority['js_module_action']).replace('PAYLOADREPLACE', connect_entry['python_function'] + """(cs['payload'])""")


with open((thisdir.parent / 'blfoil_appconnect.py'), 'w') as txtfile:
    funcdef = txtfile.write(result_imports + '\n' + globl.replace('CASESREPLACE', result_cases))







# =================================================
#              Also generate js binds
# =================================================




event_predef_start = """document.addEventListener('EVENT_TYPE', tr_event => {"""

event_predef_end = """});"""

all_events = {}

# thispath = Path(__file__)

# print(os.listdir(thispath.parent.parent 'app' / 'src' / 'mods'))

# print('ded'.endswith('ed'))

basepath = Path(thisdir.parent / 'app' / 'src' / 'mods')

# print(os.listdir(basepath))

collected = []

# core events like checkboxes shouldalways happen before anything else
for gmod in os.listdir(basepath):
    # print(gmod)
    gmodpath = Path(basepath / gmod)
    for findbind in os.listdir(gmodpath):
        # print(findbind)
        if findbind.endswith('events_bind.core.json'):
            print(findbind)
            collected.append(gmodpath / findbind)


for gmod in os.listdir(basepath):
    # print(gmod)
    gmodpath = Path(basepath / gmod)
    for findbind in os.listdir(gmodpath):
        # print(findbind)
        if findbind.endswith('events_bind.json'):
            print(findbind)
            collected.append(gmodpath / findbind)




# cycle trough found modules and collect events on per-module basis
module_events = {}

# for every module file
for mod in collected:
    # cycle trough each event
    with open(str(mod), 'r') as txtfile:
        opened = txtfile.read()

    fil = json.loads(opened)

    for evt in fil:
        if module_events.get(evt) == None:
            module_events[evt] = {}
        
        mkname = mod.parent.name + ' ' + mod.name.replace('events_bind.json', '').rstrip('_')

        module_events[evt][mkname] = []
        
        # append all bins
        for bind in fil[evt]:
            module_events[evt][mkname].append(bind)




allevents = ''


# for every event type
for etype in module_events:
    allevents += event_predef_start.replace('EVENT_TYPE', etype)
    # for every module
    for module_binds in module_events[etype]:
        # mark the module
        allevents += '\n'
        allevents += '\n'
        allevents += '\n'
        allevents += '\t// =========================================='
        allevents += '\n'
        allevents += '\t// \t' + module_binds
        allevents += '\n'
        allevents += '\t// =========================================='
        allevents += '\n'
        
        # add actual binds
        for addbind_index, addbind in enumerate(module_events[etype][module_binds]):
            c_action = addbind
            functionparams = ', '.join(list(filter(None, [
                # event goes first
                'tr_event' if c_action['pass_event'] == True else '',
                # then element
                ("""event.target.closest('""" + c_action.get('selector') + """')""") if c_action.get('pass_element') == True else '',
                # then params
                c_action.get('pass_params') if c_action.get('pass_params') != None and c_action.get('pass_params').strip() != '' else ''
            ])))
            allevents += '\n'
            allevents += '\t'
            allevents += """if (event.target.closest('""" + c_action['selector'] + """'))"""
            allevents += ' { ' + c_action['function'] + '(' + functionparams + ') }'
            # noooooooo
            allevents += ('else{ ' + c_action.get('else') + '(' + functionparams + ') }') if c_action.get('else') != None else ''
        
        allevents += '\n'
        allevents += '\n'
        
    allevents += '\n'
    allevents += event_predef_end
    allevents += '\n\n\n'


# print(allevents)

with open(str(thisdir.parent / 'app' / 'src' / 'mods' / 'main_app_core' / 'appgui_main_core_event_listeners.js'), 'w') as writebinds:
    writebinds.write(allevents)



