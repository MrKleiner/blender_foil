# incoming_case:js_module:js_module_action:python_function
[
	# =========================================
	# 			   MOD MAKER MODULE
	# =========================================
	{
		"incoming_case": "modmaker_get_preinstalled_engines",
		# to where return the result of the python fucntion code execution
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
	}

]