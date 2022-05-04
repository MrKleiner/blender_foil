document.addEventListener('click', tr_event => {


	// ==========================================
	// 	dashboard dashboard
	// ==========================================

	if (event.target.closest('[dashboard_action="load_skyboxer"]')) { skyboxer_module_loader() }




	// ==========================================
	// 	main_app_core checkboxes
	// ==========================================

	if (event.target.closest('[lizcbox].lizcbox_container, .lizcbox_hitbox')) { lizcboxes_switch(event.target.closest('[lizcbox].lizcbox_container, .lizcbox_hitbox')) }




	// ==========================================
	// 	main_app_core core
	// ==========================================

	if (event.target.closest('[lizmenu_action="load_newmodmaker"]')) { newmodmaker_loader() }
	if (event.target.closest('[lizmenu_action="load_main_dashboard"]')) { dashboard_app_loader() }




	// ==========================================
	// 	main_app_core dropdowns
	// ==========================================

	if (event.target.closest('.lizard_dropdown_entries [dropdown_set]')) { lizdropdown_set_active(event.target.closest('.lizard_dropdown_entries [dropdown_set]')) }
	if (event.target.closest('[haslizdropdown]')) { dropdown_showhide(event.target.closest('[haslizdropdown]')) }else{ dropdown_showhide(event.target.closest('[haslizdropdown]')) }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_fetch_preinstalled')) { apc_send({'action': 'modmaker_get_preinstalled_engines'}) }
	if (event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) { modmaker_set_active_engine(event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) }
	if (event.target.closest('#new_engine_save_config')) { modmaker_save_engine_details() }
	if (event.target.closest('#modmaker_add_new_engine')) { modmaker_new_engine() }
	if (event.target.closest('#new_engine_del_config')) { modmaker_newengine_del_config() }
	if (event.target.closest('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item')) { modmaker_set_active_client(event.target.closest('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item')) }
	if (event.target.closest('#modmaker_spawn_client_mpsp2013dlls, #modmaker_spawn_client_dll_dropdown')) { modmaker_validate_required_options() }
	if (event.target.closest('#modmaker_new_client_from_tplate')) { modmaker_spawn_mod(false) }
	if (event.target.closest('#modmaker_new_client_newblank')) { modmaker_spawn_mod(true) }


});


document.addEventListener('mouseover', tr_event => {


	// ==========================================
	// 	main_app_core tooltips
	// ==========================================

	if (event.target.closest('[liztooltip]')) { showliztooltip(event.target.closest('[liztooltip]')) }else{ showliztooltip(event.target.closest('[liztooltip]')) }


});


document.addEventListener('keydown', tr_event => {


	// ==========================================
	// 	main_app_core ui_lists
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_scroller(tr_event, event.target.closest('.simple_uilist_text_input')) }


});


document.addEventListener('keyup', tr_event => {


	// ==========================================
	// 	main_app_core ui_lists
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { simple_ui_list_buildsuggest(tr_event, event.target.closest('.simple_uilist_text_input')) }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { modmaker_validate_required_options() }


});


document.addEventListener('focusout', tr_event => {


	// ==========================================
	// 	main_app_core ui_lists
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_showhide(event.target.closest('.simple_uilist_text_input'), false) }


});


document.addEventListener('focusin', tr_event => {


	// ==========================================
	// 	main_app_core ui_lists
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_showhide(event.target.closest('.simple_uilist_text_input'), true) }


});


document.addEventListener('change', tr_event => {


	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_engine_details_exepath input')) { modmaker_check_engine_exe_exists() }
	if (event.target.closest('#modmaker_engine_details_icon input')) { modmaker_check_icon() }
	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { modmaker_validate_required_options() }


});


