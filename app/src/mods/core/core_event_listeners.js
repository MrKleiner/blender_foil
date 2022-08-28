document.addEventListener('click', tr_event => {


	// ==========================================
	// 	core checkboxes_events_bind.core.json
	// ==========================================

	if (event.target.closest('[lizcbox].lizcbox_container, .lizcbox_hitbox')) { lizcboxes_switch(event.target.closest('[lizcbox].lizcbox_container, .lizcbox_hitbox')) }




	// ==========================================
	// 	core core_events_bind.core.json
	// ==========================================

	if (event.target.closest('[lizmenu_action="load_newmodmaker"]')) { newmodmaker_loader() }
	if (event.target.closest('[lizmenu_action="load_main_dashboard"]')) { dashboard_app_loader() }
	if (event.target.closest('[apptoolbarctg="preferences"] [lizmenu_action="exit_app"]')) { blfoil_exit_app() }




	// ==========================================
	// 	core dropdowns_events_bind.core.json
	// ==========================================

	if (event.target.closest('lzdropdown .lz_menu_entries [dropdown_set]')) { lzdrops.set_active(event.target.closest('lzdropdown .lz_menu_entries [dropdown_set]')) }
	if (event.target.closest('[haslizdropdown], lzdropdown')) { lzdrops.showhide(event.target.closest('[haslizdropdown], lzdropdown')) }else{ lzdrops.showhide(event.target.closest('[haslizdropdown], lzdropdown')) }




	// ==========================================
	// 	dashboard dashboard
	// ==========================================

	if (event.target.closest('[dashboard_action="load_skyboxer"]')) { skyboxer_module_loader() }
	if (event.target.closest('.main_dashboard_util[dboardload]')) { dashboard_tool_loader(event.target.closest('.main_dashboard_util[dboardload]')) }
	if (event.target.closest('#main_dashboard_right_ctrl .lizcbox_hitbox')) { dboard_update_panel_vis() }
	if (event.target.closest('#dboard_mod_launchgame')) { dboard_launch_mod() }
	if (event.target.closest('#dboard_mod_killgame')) { dboard_kill_mod() }
	if (event.target.closest('#dboard_suggest_linked_maps_c')) { dboard_call_applicable_maps() }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('#gminfo_appid_dropdown [dropdown_set]')) { set_steam_appid_from_dropdown(event.target.closest('#gminfo_appid_dropdown [dropdown_set]')) }
	if (event.target.closest('#gameinfo_ctrl .lizcbox_hitbox')) { gameinfo_save_back() }
	if (event.target.closest('#gameinfo_ctrl .lz_menu_entries')) { gameinfo_save_back() }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_fetch_preinstalled')) { modmaker_load_engines(which='modmaker_get_preinstalled_engines') }
	if (event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) { modmaker_load_engine_info(event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) }
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
	// 	core tooltips_events_bind.core.json
	// ==========================================

	if (event.target.closest('[liztooltip]')) { showliztooltip(event.target.closest('[liztooltip]')) }else{ showliztooltip(event.target.closest('[liztooltip]')) }


});


document.addEventListener('keydown', tr_event => {


	// ==========================================
	// 	core ui_lists_events_bind.core.json
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_scroller(tr_event, event.target.closest('.simple_uilist_text_input')) }


});


document.addEventListener('keyup', tr_event => {


	// ==========================================
	// 	core ui_lists_events_bind.core.json
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { simple_ui_list_buildsuggest(tr_event, event.target.closest('.simple_uilist_text_input')) }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { modmaker_validate_required_options() }


});


document.addEventListener('focusout', tr_event => {


	// ==========================================
	// 	core ui_lists_events_bind.core.json
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_showhide(event.target.closest('.simple_uilist_text_input'), false) }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('#gminfo_gamename_input-, #gminfo_gametitle_input-, #gminfo_gameicon_input-, #gminfo_appid_input-')) { gameinfo_save_back() }


});


document.addEventListener('focusin', tr_event => {


	// ==========================================
	// 	core ui_lists_events_bind.core.json
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_showhide(event.target.closest('.simple_uilist_text_input'), true) }


});


document.addEventListener('change', tr_event => {


	// ==========================================
	// 	dashboard dashboard
	// ==========================================

	if (event.target.closest('#dboard_mod_add_opts_input, #dboard_start_from_map_inp input')) { dboard_update_panel_vis() }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('#gminfo_gamename_input, #gminfo_gametitle_input, #gminfo_gameicon_input, #gminfo_appid_input')) { gameinfo_save_back() }
	if (event.target.closest('#gminfo_gameicon_input')) { gminfo_icon_manager() }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_engine_details_exepath input')) { modmaker_check_engine_exe_exists() }
	if (event.target.closest('#modmaker_engine_details_icon input')) { modmaker_check_icon() }
	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { modmaker_validate_required_options() }


});


