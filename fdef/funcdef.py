# incoming_case:js_module:js_module_action:python_function
[
	# =========================================
	# 			   MOD MAKER MODULE
	# =========================================
	# add imports, because modules require imports...
	{
		"add_imports": [
			"from .utils.shared import app_command_send",
			"from .mods.app.modmaker.app_modmaker import *",
			"from .blfoil_appconnect import *"
		]
	},
	{
		"incoming_case": "modmaker_get_preinstalled_engines",
		# to where return the result of the python fucntion code execution
		# do not include to automatically forward to "echo" module
		"js_module": "modmaker",
		"js_module_action": "append_pre_installed",
		# python function to execute on server run by Blender
		"python_function": "fetch_existing_engines"
	},
	{
		"incoming_case": "modmaker_get_engine_info",
		"js_module": "modmaker",
		"js_module_action": "set_engine_info",
		"python_function": "modmaker_load_engine_info"
	},
	{
		"incoming_case": "modmaker_save_engine_info",
		"python_function": "modmaker_save_engine_info"
	},
	{
		"incoming_case": "modmaker_load_saved_engines",
		"js_module": "modmaker",
		"js_module_action": "accept_engines",
		"python_function": "modmaker_load_saved_engines"
	},
	{
		"incoming_case": "modmaker_delete_engine",
		"python_function": "modmaker_kill_engine"
	},
	{
		"incoming_case": "modmaker_do_spawn_mod",
		"python_function": "modmaker_spawn_new_client"
	},


	# =========================================
	# 			   DASHBOARD MODULE
	# =========================================
	{
		"add_imports": [
			"from .mods.app.dashboard.app_dashboard import *"
		]
	},
	# Launch the game with all the params n stuff
	{
		"incoming_case": "dboard_launch_mod",
		"js_module": "dashboard",
		"js_module_action": "dashboard_launched_mod_echo",
		"python_function": "dboard_launch_mod"
	},
	# kill the instance of the game
	{
		"incoming_case": "dboard_kill_mod",
		"js_module": "dashboard",
		"js_module_action": "dashboard_killed_mod_echo",
		"python_function": "dboard_kill_mod"
	},
	# save mod context, so that it's possible to load it on reload
	{
		"incoming_case": "save_last_app_context",
		"python_function": "save_last_app_context"
	},
	# load app context on app reload
	{
		"incoming_case": "load_last_app_context",
		"js_module": "set_context",
		"js_module_action": "set_context",
		"python_function": "load_last_app_context"
	}
]