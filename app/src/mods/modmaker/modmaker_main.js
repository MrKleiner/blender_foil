

function modmaker_module_manager(pl)
{
	switch (pl['mod_action']) {
		case 'set_engine_info':
			// modmaker_load_engine_info(pl['payload'])
			break;
		case 'load_resulting_engine':
			// modmaker_load_mod(pl['payload'])
			break;
		default:
			console.log('The modmaker module has been called, but no corresponding action was found')
			break;
	}
}


// important todo: return Promise, promise.resolve() for post-load actions
function newmodmaker_loader(mdl)
{
	base_module_loader('mod_maker.html')
		.then(function(resolved) {
			modmaker_load_engines()
		});
}



// the which keyword is needed,
// because there's a button to fetch already existing engines on first startup which is a different kind of operation
async function modmaker_load_engines(which='modmaker_load_saved_engines')
{
	var saved_engines = await bltalk.send({
		'action': which
	});

	console.log(saved_engines);
	$('#modmaker_engine_selector_pool').empty();
	for (var engi of saved_engines){
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




// This doesn't get any fresh data, but only treats existing one
// takes an object containing 'ess_bins' and 'sdk_bins'
function modmaker_check_engine_binaries(bins)
{
	// order the dlls nicely based on importance
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

	// essential (engine) bins
	var itemlist = $('#modmaker_engine_details_essenitalbins .modmaker_engine_details_list_items');
	itemlist.empty();
	for (var esbin of order_dict_essbins)
	{
		var b_entry = $('<div class="modmaker_engine_details_list_item"></div>')
		b_entry.append($('<div class="modmaker_engine_details_list_item_text"></div>').text(esbin));
		if (bins['ess_bins'][esbin] == true){
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
		if (bins['sdk_bins'][sdkbin][0] == true && bins['sdk_bins'][sdkbin][1] == true){
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/checkmark.svg"></div>');
		}else{
			b_entry.append('<div class="modmaker_engine_details_list_item_status"><img src="assets/cross.svg"></div>');
		}
		itemlist.append(b_entry);
	}
}






//
// Load Engine Info
//
async function modmaker_load_engine_info(engine)
{
	// visual feedback, highlight selected engine in the pool
	$('#modmaker_engine_selector .simple_list_v1_pool_item').removeClass('simple_list_v1_pool_item_const_active');
	$(engine).addClass('simple_list_v1_pool_item_const_active');


	// get engine info
	var eng_info = await bltalk.send({
		'action': 'modmaker_get_engine_info',
		'payload': {
			'engine_exe': engine.getAttribute('engine_path')
		}
	});
	console.log('Got engine info', eng_info);
	// save active engine selection
	window.modmaker_active_engine = {
		'elem': engine,
		'engpath': engine.getAttribute('engine_path')
	}


	// set <input> values

	// engine exe
	$('#modmaker_engine_details_exepath input').attr('value', eng_info['exe']).val(eng_info['exe']);
	// engine name
	$('#modmaker_engine_details_name input').attr('value', eng_info['engine_name']).val(eng_info['engine_name']);
	// engine icon
	$('#modmaker_engine_details_icon input').attr('value', eng_info['icon']).val(eng_info['icon']);
	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = eng_info['icon']

	// check binaries
	modmaker_check_engine_binaries(eng_info)

	// empty the installed clients pool
	$('#modmaker_client_selector_installed_pool').empty();


	// Spawn Clients
	var dropdown_eligible = []
	window.modmaker_clients_list = []

	for (var inc of eng_info['clients'])
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

	// check whether engine exe exists on HDD at the moment or no
	modmaker_check_engine_exe_exists()

	// applicable cl/sv .dll locations
	lzdrops.spawn(
		'#modmaker_spawn_client_dll_dropdown',
		'client_dlls',
		{
			'menu_name': 'Select .dll location',
			'menu_entries': dropdown_eligible
		}
	);

	// SDK 2013 SP dlls, SDK 2013 MP dlls
	
	lzdrops.spawn(
		'#modmaker_spawn_client_mpsp2013dlls',
		'2013_dlls',
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



// Check whether engine exe exists as of now
function modmaker_check_engine_exe_exists()
{
	if (fs.existsSync($('#modmaker_engine_details_exepath input').val())) {
		$('#modmaker_engine_details_exepath .modmaker_engine_details_item_status img')[0].src = 'assets/checkmark.svg'
		bltalk.send({
			'action': 'modmaker_check_engine_bins',
			'engine_exe': $('#modmaker_engine_details_exepath input').val()
		})
	} else {
		$('#modmaker_engine_details_exepath .modmaker_engine_details_item_status img')[0].src = 'assets/cross.svg'
	}

}



// save engine params
async function modmaker_save_engine_details()
{
	if (fs.existsSync($('#modmaker_engine_details_exepath input').val())) {
		console.log('Saving Engine Details...'); console.time('Saved Engine Details')
		var eng_details = await bltalk.send({
			'action': 'modmaker_save_engine_info',
			'payload': {
				'engine_exe': document.querySelector('#modmaker_engine_details_exepath input').value,
				'engine_name': document.querySelector('#modmaker_engine_details_name input').value,
				'icon': document.querySelector('#modmaker_engine_details_icon input').value
			}
		})
		console.timeEnd('Saved Engine Details')

		// todo: Why reload the whole thing ????
		bltalk.send({
			'action': 'modmaker_load_saved_engines'
		})
	}
}




function modmaker_check_icon()
{
	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = $('#modmaker_engine_details_icon input').val()
}


// spawn new engine
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
	return
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
		!lizard.array_is_same(clname.value.toLowerCase().trim().split(''), 'qwertyuiopasdfghjklzxcvbnm_-1234567890'.split(''))
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
async function modmaker_spawn_mod(ismapbase)
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

		var mdinfo = await bltalk.send({
			'action': 'modmaker_do_spawn_mod',
			'payload': do_mod_payload
		})

		modmaker_load_mod(mdinfo)

	// }

}



// delete new engine
function modmaker_newengine_del_config()
{
	// todo: kinda unreliable
	bltalk.send({
		'action': 'modmaker_delete_engine',
		'payload': {
			'engine': window.modmaker_active_engine['elem'].getAttribute('engine_path')
		}
	});
	window.modmaker_active_engine['elem'].remove();
	$('#modmaker_client_selector, #modmaker_engine_details').css('display', 'none');
}


function modmaker_set_active_client(cl)
{
	// $(set_active_client).addClass('simple_list_v1_pool_item_const_active');
	cl.toggleAttribute('selected_client');
	cl.classList.toggle('simple_list_v1_pool_item_const_active');
}


// takes mod info as an input
// actually, index is more like an id...
// todo: should mod loader be a part of modmaker ?
function modmaker_load_mod(md_info)
{
	// set index
	// window.foil_context['mod_context'] = md_info['project_index'];
	// set useless meta name
	// window.foil_context['mod_meta_name'] = md_info['project_name'];
	// dump everything because why not
	window.foil_context['full'] = md_info;

	dashboard_app_loader()
	// save context
	// foil_save_context(window.foil_context.full)
	foil_save_context(true)

}










