

function modmaker_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'append_pre_installed':
			newmodmaker_accept_engines(pl['payload'])
			break;
		case 'accept_engines':
			newmodmaker_accept_engines(pl['payload'])
			break;
		case 'set_engine_info':
			modmaker_load_engine_info(pl['payload'])
			break;
		case 'set_engine_info_bins':
			modmaker_accept_engine_binaries(pl['payload'])
			break;
		default:
			console.log('The modmaker module has been called, but no corresponding action was found')
			break;
	}

}


function newmodmaker_loader()
{
	$('#modules_cont').load('tools/mod_maker.html', function() {
		console.log('loaded');
		lizcboxes_init();
		init_liztooltips();
		apc_send({
			'action': 'modmaker_load_saved_engines'
		});
		window['current_app_module'] = 'modmaker';
	});
}


function newmodmaker_accept_engines(pl)
{
	console.log(pl);
	$('#modmaker_engine_selector_pool').empty();
	for (var engi of pl){
		var engine_gui_payload = $('<div class="simple_list_v1_pool_item"></div>')

		var pl_icon = engine_gui_payload.append('<div class="simple_list_v1_pool_item_icon"><img draggable="false" src="' + engi['icon'] + '"></div>');
		// var pl_icon = $('<div class="simple_list_v1_pool_item_icon"><img draggable="false" src="' + '' + '"></div>');
		engine_gui_payload.append(pl_icon);
		var pl_name = $('<div class="simple_list_v1_pool_item_name"></div>');
		engine_gui_payload.append(pl_name);
		var pl_descr = $('<div class="simple_list_v1_pool_item_descr"></div>');
		engine_gui_payload.append(pl_descr);

		engine_gui_payload.attr({
			'engine_path': engi['engine_path'],
			'engine_name': engi['engine_name'],
			'engine_icon': engi['icon']
		});

		// console.log(engine_gui_payload)

		pl_name.text(engi['engine_name']);
		pl_descr.text(engi['engine_path']);

		$('#modmaker_engine_selector_pool').append(engine_gui_payload);

	}
	// set active engine, if any
	if (window.modmaker_active_engine != undefined){
		console.log('[engine_path="' + window.modmaker_active_engine['engpath'] + '"]')
		$('#modmaker_engine_selector .simple_list_v1_pool_item').removeClass('simple_list_v1_pool_item_const_active');
		$('[engine_path="' + window.modmaker_active_engine['engpath'].replaceAll('\\', '\\\\') + '"]').addClass('simple_list_v1_pool_item_const_active');
	}
}


function modmaker_accept_engine_binaries(pl)
{
	// fuck
	var order_dict_essbins = [
		'engine.dll',
		'datacache.dll',
		'inputsystem.dll',
		'launcher.dll',
		'mdllib.dll',
		'tier0.dll',
		'vgui2.dll',
		'vphysics.dll',
		'vstdlib.dll',
		'vguimatsurface.dll',
		'unitlib.dll',
		'soundsystem.dll'
	]

	var ordered_dict_sdkbins = [
		'vrad exe/dll',
		'hammer exe/dll',
		'vtex exe/dll',
		'vvis exe/dll',
		'vrad exe/dll',
		'hlmv.exe',
		'studiomdl.exe',
		'hlfaceposer.exe',
		'height2ssbump.exe',
		'vpk.exe'
	]

	// essential bins
	var itemlist = $('#modmaker_engine_details_essenitalbins .modmaker_engine_details_list_items');
	itemlist.empty();
	for (var esbin of order_dict_essbins)
	{
		var b_entry = $('<div class="modmaker_engine_details_list_item"></div>')
		b_entry.append($('<div class="modmaker_engine_details_list_item_text"></div>').text(esbin));
		if (pl['ess_bins'][esbin] == true){
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/checkmark.svg"></div>');
		}else{
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/cross.svg"></div>');
		}
		itemlist.append(b_entry)
	}

	// SDK bins
	var itemlist = $('#modmaker_engine_details_sdkbins .modmaker_engine_details_list_items');
	itemlist.empty();
	for (var sdkbin of ordered_dict_sdkbins)
	{
		var b_entry = $('<div class="modmaker_engine_details_list_item"></div>')
		b_entry.append($('<div class="modmaker_engine_details_list_item_text"></div>').text(sdkbin));
		if (pl['sdk_bins'][sdkbin][0] == true && pl['sdk_bins'][sdkbin][1] == true){
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/checkmark.svg"></div>');
		}else{
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/cross.svg"></div>');
		}
		itemlist.append(b_entry);
	}
}


// set active engine
function modmaker_load_engine_info(pl)
{

	console.log(pl);
	// <div class="modmaker_engine_details_list_item">
	// 	<div class="modmaker_engine_details_list_item_text">engine.dll</div>
	// 	<div class="modmaker_engine_details_list_item_status"><img src="assets/checkmark.svg"></div>
	// </div>


	// engine exe
	$('#modmaker_engine_details_exepath input').attr('value', pl['exe']).val(pl['exe']);
	// engine name
	$('#modmaker_engine_details_name input').attr('value', pl['engine_name']).val(pl['engine_name']);
	// engine icon
	$('#modmaker_engine_details_icon input').attr('value', pl['icon']).val(pl['icon']);
	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = pl['icon']

	modmaker_accept_engine_binaries(pl)

	$('#modmaker_client_selector_installed_pool').empty();

	var dropdown_eligible = []

	window.modmaker_clients_list = []

	for (var inc of pl['clients'])
	{
		var tgt_pool = $('#modmaker_client_selector_installed_pool');
		// <div class="simple_list_v1_pool_item">
		// 	<div class="simple_list_v1_pool_item_icon"><img draggable="false" src="assets/hl2_flat.ico"></div>
		// 	<div class="simple_list_v1_pool_item_name">Half-Life 2</div>
		// 	<div class="simple_list_v1_pool_item_descr">hl2</div>
		// </div>

		var mkitem = $('<div class="simple_list_v1_pool_item"></div>');
		mkitem.append('<div class="simple_list_v1_pool_item_icon"><img draggable="false" src="' + inc['client_icon'] + '"></div>');
		mkitem.append('<div class="simple_list_v1_pool_item_name">' + inc['client_name'] + '</div>');
		mkitem.append('<div class="simple_list_v1_pool_item_descr">' + inc['folder_name'] + '</div>');
		mkitem[0].setAttribute('clientpath', inc['folder_name']);
		window.modmaker_clients_list.push(inc['folder_name']);
		if (inc['hasdll'] == true){
			mkitem[0].setAttribute('hasdll', true)
			mkitem.append($('<img liztooltip_prms="right:0:15:2000" src="assets/punchcard_bootleg_cut_b.png" class="simple_list_v1_pool_item_descr_icon">')
				.attr('liztooltip',
					`<img 
						style="width: 300px; height: 300px; object-fit: contain; object-position: center;" 
						src="assets/5mb.webp"
					 >
			 		 <div 
			 		 style="position: absolute; margin-left: 100px; color: white; font-size: 50px; font-family: 'Roboto'; font-weight: 600"
			 		 >
		 		 	 5 MB
			 		 </div>
					 <img 
						style="margin-top: 10px; width: 300px; height: 100px; object-fit: contain; object-position: top;" 
						src="assets/punchcard.png"
					 >
		 		 `));
			
			// if this entry has dll - append it to the dll dropdown
			dropdown_eligible.push({
				'name': inc['folder_name'],
				'dropdown_set': inc['folder_name']
			});
		}

		tgt_pool.append(mkitem);

	}

	// unlock engine details
	$('#modmaker_client_selector, #modmaker_engine_details').removeAttr('style');

	modmaker_check_engine_exe_exists()
/*
	var dropdown_eligible = []

	// create a dropdown of eligible clients with dlls
	// todo this creation should happen on item appends
	// update: Done
	document.querySelectorAll('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item[hasdll="true"]').forEach(function(userItem) {
		console.log(userItem);

		var dropdown_st = userItem.querySelector('.simple_list_v1_pool_item_descr').textContent

		dropdown_eligible.push({
			'name': dropdown_st,
			'dropdown_set': dropdown_st
		})

	});

*/
	// applicable cl/sv .dll locations
	create_lizdropdown(
		'#modmaker_spawn_client_dll_dropdown',
		{
			'menu_name': 'Select .dll location',
			'menu_entries': dropdown_eligible
		}
	);

	// SDK 2013 SP dlls, SDK 2013 MP dlls
	
	create_lizdropdown(
		'#modmaker_spawn_client_mpsp2013dlls',
		{
			'menu_name': 'Default SDK binaries',
			'menu_entries': [
				{
					'name': 'Do not include',
					'dropdown_set': 'dont'
				},
				{
					'name': 'SDK Base 2013 SP episodic',
					'dropdown_set': '2013_sp_episodic'
				},
				{
					'name': 'SDK Base 2013 SP hl2',
					'dropdown_set': '2013_sp_hl2'
				},
				{
					'name': 'SDK Base 2013 MP',
					'dropdown_set': '2013_mp'
				}
			]
		}
	);

}



async function modmaker_save_engine_details()
{
	if (fs.existsSync($('#modmaker_engine_details_exepath input').val())) {
		await apc_send({
			'action': 'modmaker_save_engine_info',
			'engine_exe': document.querySelector('#modmaker_engine_details_exepath input').value,
			'engine_name': document.querySelector('#modmaker_engine_details_name input').value,
			'icon': document.querySelector('#modmaker_engine_details_icon input').value
		})

		// todo: Why reload the whole thing ????
		apc_send({
			'action': 'modmaker_load_saved_engines'
		})
	}
}


function modmaker_check_engine_exe_exists()
{
	if (fs.existsSync($('#modmaker_engine_details_exepath input').val())) {
		$('#modmaker_engine_details_exepath .modmaker_engine_details_item_status img')[0].src = 'assets/checkmark.svg'
		apc_send({
			'action': 'modmaker_check_engine_bins',
			'engine_exe': $('#modmaker_engine_details_exepath input').val()
		})
	} else {
		$('#modmaker_engine_details_exepath .modmaker_engine_details_item_status img')[0].src = 'assets/cross.svg'
	}

}


function modmaker_check_icon()
{
	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = $('#modmaker_engine_details_icon input').val()
}


function modmaker_new_engine()
{
	// engine exe
	$('#modmaker_engine_details_exepath input').attr('value', '').val('');
	// engine name
	$('#modmaker_engine_details_name input').attr('value', '').val('');
	// engine icon
	$('#modmaker_engine_details_icon input').attr('value', '').val('');
	// engine not valid
	$('#modmaker_engine_details_exepath .modmaker_engine_details_item_status img')[0].src = 'assets/cross.svg'

	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = '';

	$('#modmaker_engine_details_items .modmaker_engine_details_list .modmaker_engine_details_list_items .modmaker_engine_details_list_item .modmaker_engine_details_list_item_status img').attr('src', '');

	$('#modmaker_client_selector, #modmaker_engine_details').removeAttr('style');
	$('#modmaker_client_selector').css('display', 'none');
}



function modmaker_validate_required_options()
{
	// important todo: game name cannot be empty (for now)
	// while it actually can (like ASW)
	var def_dll_dropdown = document.querySelector('#modmaker_spawn_client_mpsp2013dlls');
	var present_dll_dropdown = document.querySelector('#modmaker_spawn_client_dll_dropdown');
	// because even if it's reused twice - it's bad
	var clname = document.querySelector('#modmaker_new_client_cl_name input');
	var allowed_fname = 'qwertyuiopasdfghjklzxcvbnm'.split('');
	gm_conds = [
		document.querySelector('#modmaker_new_client_game_name input').value != '',
		clname.value != '',
		(def_dll_dropdown.lizdropdown() != null && def_dll_dropdown.lizdropdown() != 'dont') || present_dll_dropdown.lizdropdown() != null,
		// client name should not be present in the clients list
		!window.modmaker_clients_list.includes(clname.value),
		// name can only contain certain characters
		!array_elem_check(clname.value.toLowerCase().trim().split(''), 'qwertyuiopasdfghjklzxcvbnm_-1234567890'.split(''))
	]
	// if all conditions are met
	// important todo: visual feedback on what's wrong
	var lockunlock = document.querySelectorAll('#modmaker_new_client_from_tplate, #modmaker_new_client_newblank');
	if (gm_conds[0] && gm_conds[1] && gm_conds[2] && gm_conds[3] && gm_conds[4]){
		lockunlock.forEach(function(userItem) {
			userItem.classList.remove('app_regular_btn_blocked');
		});
	}else{
		lockunlock.forEach(function(userItem) {
			userItem.classList.add('app_regular_btn_blocked');
		});
	}

}


//
// yeet
//
function modmaker_spawn_mod(ismapbase)
{

	// if (ismapbase == true)
	// {
		link_clients = [];
		if (document.querySelector('#modmaker_new_mapbase_link_selected [lizcbox]').lizchecked()){
			document.querySelectorAll('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item').forEach(function(userItem) {
				if (userItem.hasAttribute('selected_client')){
					link_clients.push(userItem.getAttribute('clientpath'));
				}
			});
		}
		do_mod_payload = {
			'mapbase': ismapbase,
			'pbr': document.querySelector('#modmaker_new_mapbase_dopbr [lizcbox]').lizchecked(),
			'cl_name': document.querySelector('#modmaker_new_client_cl_name input').value,
			'game_name': document.querySelector('#modmaker_new_client_game_name input').value,
			'engine_exe': window.modmaker_active_engine.engpath,
			'link_content': link_clients,
			'default_dll': document.querySelector('#modmaker_spawn_client_mpsp2013dlls').lizdropdown(),
			'link_binaries': document.querySelector('#modmaker_mknew_raw_linked_binaries_cbox [lizcbox]').lizchecked()
		}

		apc_send({
			'action': 'modmaker_do_spawn_mod',
			'payload': do_mod_payload
		})

	// }

}

