document.addEventListener('click', tr_event => {


	// ==========================================
	// 	core checkboxes_events_bind.core.json
	// ==========================================

	if (event.target.closest('lzcbox, .lizcbox_hitbox lzcbox')) { lzcbox.set_state(event.target.closest('lzcbox, .lizcbox_hitbox lzcbox')) }




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

	if (event.target.closest('[dashboard_action="load_skyboxer"]')) { fsys.skyboxer.app_loader() }
	if (event.target.closest('.main_dashboard_util[dboardload]')) { fsys.dashboard.load_tool(event.target.closest('.main_dashboard_util[dboardload]')) }
	if (event.target.closest('#main_dashboard_right_ctrl lzcbox, #main_dashboard_right_ctrl .lzcbox_hitbox')) { fsys.dashboard.main.save() }
	if (event.target.closest('#dboard_mod_launchgame')) { fsys.dashboard.main.launch_mod() }
	if (event.target.closest('#dboard_mod_killgame')) { fsys.dashboard.main.kill_mod() }
	if (event.target.closest('#dboard_suggest_linked_maps_c')) { fsys.dashboard.main.list_maps() }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('#gminfo_appid_dropdown [dropdown_set]')) { fsys.gameinfo.main.steam_id_from_dropdown(event.target.closest('#gminfo_appid_dropdown [dropdown_set]')) }
	if (event.target.closest('#gameinfo_ctrl .lizcbox_hitbox, #gameinfo_ctrl lzcbox, #gameinfo_ctrl .lz_menu_entries')) { fsys.gameinfo.main.save_back() }
	if (event.target.closest('.cmount_pool_entry lzcbox, .cmount_pool_entry lzdropdown [dropdown_set]')) { fsys.gameinfo.mounts.save_back() }
	if (event.target.closest('#gameinfo_content_mount lzbtn[btname="add_mount_pool_item"]')) { fsys.gameinfo.mounts.add_mount_entry() }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_fetch_preinstalled')) { fsys.modmaker.main.load_engines(which='modmaker_get_preinstalled_engines') }
	if (event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) { fsys.modmaker.main.load_eninge_info(event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item')) }
	if (event.target.closest('#new_engine_save_config')) { fsys.modmaker.main.save_engine_info() }
	if (event.target.closest('#modmaker_add_new_engine')) { fsys.modmaker.main.spawn_engine() }
	if (event.target.closest('#new_engine_del_config')) { fsys.modmaker.main.del_engine() }
	if (event.target.closest('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item')) { fsys.modmaker.main.set_active_client(event.target.closest('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item')) }
	if (event.target.closest('#modmaker_spawn_client_mpsp2013dlls, #modmaker_spawn_client_dll_dropdown')) { fsys.modmaker.main.validate_modspawn_options() }
	if (event.target.closest('#modmaker_new_client_from_tplate')) { fsys.modmaker.main.spawn_mod(false) }
	if (event.target.closest('#modmaker_new_client_newblank')) { fsys.modmaker.main.spawn_mod(true) }


});


document.addEventListener('mouseover', tr_event => {


	// ==========================================
	// 	core tooltips_events_bind.core.json
	// ==========================================

	if (event.target.closest('[liztooltip]')) { showliztooltip(event.target.closest('[liztooltip]')) }else{ showliztooltip(event.target.closest('[liztooltip]')) }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('.cmount_pool_entry keys lzcbox')) { fsys.gameinfo.mounts.hlight_mount_keytype(event.target.closest('.cmount_pool_entry keys lzcbox')) }


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

	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { fsys.modmaker.main.validate_modspawn_options() }


});


document.addEventListener('focusout', tr_event => {


	// ==========================================
	// 	core ui_lists_events_bind.core.json
	// ==========================================

	if (event.target.closest('.simple_uilist_text_input')) { uilist_showhide(event.target.closest('.simple_uilist_text_input'), false) }


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

	if (event.target.closest('#dboard_mod_add_opts_input, #dboard_start_from_map_inp input')) { fsys.dashboard.main.save() }




	// ==========================================
	// 	game_config_gameinfo gameinfo
	// ==========================================

	if (event.target.closest('#gminfo_gamename_input, #gminfo_gametitle_input, #gminfo_gameicon_input, #gminfo_appid_input')) { fsys.gameinfo.main.save_back() }
	if (event.target.closest('#gminfo_gameicon_input')) { fsys.gameinfo.main.load_icon() }
	if (event.target.closest('.cmount_pool_entry input')) { fsys.gameinfo.mounts.save_back() }




	// ==========================================
	// 	modmaker modmaker
	// ==========================================

	if (event.target.closest('#modmaker_engine_details_exepath input')) { fsys.modmaker.main.check_enigne_exe() }
	if (event.target.closest('#modmaker_engine_details_icon input')) { fsys.modmaker.main.check_icon() }
	if (event.target.closest('#modmaker_new_client_cl_name input, #modmaker_new_client_game_name input')) { fsys.modmaker.main.validate_modspawn_options() }


});


