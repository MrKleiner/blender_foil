from .utils.shared import app_command_send
from .mods.app.modmaker.app_modmaker import *
from .blfoil_appconnect import *
from .mods.app.dashboard.app_dashboard import *

def appconnect_actions(cs):
    match cs['action']:

        case 'modmaker_get_preinstalled_engines':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'append_pre_installed',
                'payload': fetch_existing_engines(cs['payload'])
            })
            return ''
        case 'modmaker_get_engine_info':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'set_engine_info',
                'payload': modmaker_load_engine_info(cs['payload'])
            })
            return ''
        case 'modmaker_save_engine_info':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'payload': modmaker_save_engine_info(cs['payload'])
            })
            return ''
        case 'modmaker_load_saved_engines':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'accept_engines',
                'payload': modmaker_load_saved_engines(cs['payload'])
            })
            return ''
        case 'modmaker_delete_engine':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'payload': modmaker_kill_engine(cs['payload'])
            })
            return ''
        case 'modmaker_do_spawn_mod':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'payload': modmaker_spawn_new_client(cs['payload'])
            })
            return ''
        case 'dboard_launch_mod':
            app_command_send({
                'app_module': 'dashboard',
                'mod_action': 'dashboard_launched_mod_echo',
                'payload': dboard_launch_mod(cs['payload'])
            })
            return ''
        case 'dboard_kill_mod':
            app_command_send({
                'app_module': 'dashboard',
                'mod_action': 'dashboard_killed_mod_echo',
                'payload': dboard_kill_mod(cs['payload'])
            })
            return ''
        case 'save_last_app_context':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'payload': save_last_app_context(cs['payload'])
            })
            return ''
        case 'load_last_app_context':
            app_command_send({
                'app_module': 'set_context',
                'mod_action': 'set_context',
                'payload': load_last_app_context(cs['payload'])
            })
            return ''
            
        case _:
            return 'wtf is even this'