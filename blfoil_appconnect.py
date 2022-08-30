from .utils.shared import app_command_send
from .mods.app.modmaker.app_modmaker import *
from .blfoil_appconnect import *
from .mods.app.dashboard.app_dashboard import *
from .mods.app.gameinfoman.gameinfoman import *
from .mods.skyboxer.skybox_loader import *

def appconnect_actions(cs):
    match cs['action']:

        case 'modmaker_get_preinstalled_engines':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'append_pre_installed',
                'sys_action_id': cs['sys_action_id'],
                'payload': fetch_existing_engines(cs['payload'])
            })
            return ''
        case 'modmaker_get_engine_info':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'set_engine_info',
                'sys_action_id': cs['sys_action_id'],
                'payload': modmaker_load_engine_info(cs['payload'])
            })
            return ''
        case 'modmaker_save_engine_info':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': modmaker_save_engine_info(cs['payload'])
            })
            return ''
        case 'modmaker_load_saved_engines':
            app_command_send({
                'app_module': 'modmaker',
                'mod_action': 'accept_engines',
                'sys_action_id': cs['sys_action_id'],
                'payload': modmaker_load_saved_engines(cs['payload'])
            })
            return ''
        case 'modmaker_delete_engine':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': modmaker_kill_engine(cs['payload'])
            })
            return ''
        case 'modmaker_do_spawn_mod':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': modmaker_spawn_new_client(cs['payload'])
            })
            return ''
        case 'dboard_launch_mod':
            app_command_send({
                'app_module': 'dashboard',
                'mod_action': 'dashboard_launched_mod_echo',
                'sys_action_id': cs['sys_action_id'],
                'payload': dboard_launch_mod(cs['payload'])
            })
            return ''
        case 'dboard_kill_mod':
            app_command_send({
                'app_module': 'dashboard',
                'mod_action': 'dashboard_killed_mod_echo',
                'sys_action_id': cs['sys_action_id'],
                'payload': dboard_kill_mod(cs['payload'])
            })
            return ''
        case 'save_last_app_context':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': save_last_app_context(cs['payload'])
            })
            return ''
        case 'load_last_app_context':
            app_command_send({
                'app_module': 'set_context',
                'mod_action': 'set_context',
                'sys_action_id': cs['sys_action_id'],
                'payload': load_last_app_context(cs['payload'])
            })
            return ''
        case 'save_app_quick_config':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': save_app_quick_config(cs['payload'])
            })
            return ''
        case 'dboard_get_suggested_maps':
            app_command_send({
                'app_module': 'dashboard',
                'mod_action': 'dboard_set_applicable_maps',
                'sys_action_id': cs['sys_action_id'],
                'payload': dboard_get_suggested_maps(cs['payload'])
            })
            return ''
        case 'load_context_by_index':
            app_command_send({
                'app_module': '',
                'mod_action': '',
                'sys_action_id': cs['sys_action_id'],
                'payload': load_context_by_index(cs['payload'])
            })
            return ''
        case 'gameinfoman_load_info':
            app_command_send({
                'app_module': 'gameinfo',
                'mod_action': 'gameinfo_set_info',
                'sys_action_id': cs['sys_action_id'],
                'payload': gameinfoman_load_gminfo(cs['payload'])
            })
            return ''
        case 'gameinfo_save_back':
            app_command_send({
                'app_module': 'echo_status',
                'mod_action': 'echo_status',
                'sys_action_id': cs['sys_action_id'],
                'payload': gameinfo_save_back(cs['payload'])
            })
            return ''
        case 'gameinfoman_get_mod_icon':
            app_command_send({
                'app_module': 'gameinfo',
                'mod_action': 'gminfo_icon_manager',
                'sys_action_id': cs['sys_action_id'],
                'payload': gminfo_icon_vis_feedback(cs['payload'])
            })
            return ''
        case 'skyboxer_get_all_skyboxes':
            app_command_send({
                'app_module': '',
                'mod_action': '',
                'sys_action_id': cs['sys_action_id'],
                'payload': find_skyboxes(cs['payload'])
            })
            return ''
        case 'skyboxer_get_sky_as_bitmap':
            app_command_send({
                'app_module': '',
                'mod_action': '',
                'sys_action_id': cs['sys_action_id'],
                'payload': load_sky_bitmap(cs['payload'])
            })
            return ''
            
        case _:
            # app_command_send({
            #     'app_module': 'echo_status',
            #     'mod_action': 'echo_status',
            #     'payload': 'Unknown incoming case'
            # })
            return 'wtf is even this'