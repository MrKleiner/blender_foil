

// 
// ============================================================
// ------------------------------------------------------------
//                      name: gameinfo
// ------------------------------------------------------------
// ============================================================
// 




function gameinfo_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'gameinfo_set_info':
			// todo: this should exit but with different name
			// gameinfo_set_info(pl['payload'])
			break;
		case 'gminfo_icon_manager':
			// todo: this should exit but with different name
			// gminfo_icon_manager(true, pl['payload'])
			break;
		default:
			console.log('The gameinfo module has been called, but no corresponding action was found');
			break;
	}

}


function gameinfoman_app_loader()
{
	base_module_loader('game_config_game_info.html')
	.then(function(resolved) {

		// steam appid drowdown
		create_lizdropdown(
			'#gminfo_appid_dropdown',
			{
				'menu_name': 'Steam App ID',
				'menu_entries': [
					{
						'name': 'Half-Life 2',
						'dropdown_set': '220'
					},
					{
						'name': 'Half-Life 2: Episode One',
						'dropdown_set': '380'
					},
					{
						'name': 'Half-Life 2: Episode Two',
						'dropdown_set': '420'
					},
					{
						'name': 'Portal 2',
						'dropdown_set': '620'
					},
					{
						'name': 'left4Dead 2',
						'dropdown_set': '550'
					},
					{
						'name': 'Alien Swarm: Reactive Drop',
						'dropdown_set': '563560'
					},
					{
						'name': 'Black Mesa',
						'dropdown_set': '362890'
					}
				]
			}
		);


		// gametype dropdown
		create_lizdropdown(
			'#gminfo_gametype_dropdown',
			{
				'menu_name': 'Game Type',
				'default': 'Multiplayer_Only',
				'menu_entries': [
					{
						'name': 'Singleplayer Only',
						'dropdown_set': 'Singleplayer_Only'
					},
					{
						'name': 'Multiplayer Only',
						'dropdown_set': 'Multiplayer_Only'
					},
					{
						'name': 'Both',
						'dropdown_set': 'Both'
					}
				]
			}
		);

		// read gameinfo of the mod and set settings
		gameinfo_set_info()


	});
}



// takes an element with dropdown_set attribute (menu entry element)
function set_steam_appid_from_dropdown(dr_item)
{
	document.querySelector('#gminfo_appid_input').value = dr_item.getAttribute('dropdown_set');
}

function evalst(st){
	if (st.toString() == '1'){
		return true
	}
	if (st.toString() == '0'){
		return false
	}
	if (st == true){
		return '1'
	}
	if (st == false){
		return '0'
	}
	return null
}


// app context and fast config should be fully ready by this time
// important todo: there has to be a def dict
async function gameinfo_set_info()
{
	var inf = await bltalk.send({
		'action': 'gameinfoman_load_info',
		'payload': {
			'client_path': window.foil_context.full.client_folder_path
		}
	});
	log('gameinfo', 'Got gameinfo from blender:', inf)

	$('#gminfo_gamename_input').val(inf['game'])
	$('#gameinfo_mod_minititle').text(inf['game'])
	$('#gameinfo_mod_modfolderpath').val(window.foil_context.full.client_folder_path)
	$('#gminfo_gametitle_input').val(inf['title'])
	$('#gminfo_gameicon_input').val(inf['icon'])
	$('#gminfo_appid_input').val(inf['SteamAppId'])

	lizdropdowns.pool['gminfo_gametype_dropdown'].set_active(inf['type'])
	lizdropdowns.pool['gminfo_appid_dropdown'].set_active($('#gminfo_appid_input').val())

	// checkboxes
	// todo: fucking make names symmetrical
	lizcbox_stat('vr_support', evalst(inf['SupportsVR']))
	lizcbox_stat('icon_autoconvert', window.foil_context.full.autoconvert_icon)
	lizcbox_stat('dx8support', evalst(inf['SupportsDX8']))
	lizcbox_stat('no_mp_model_select', evalst(inf['NoModels']))
	lizcbox_stat('no_mp_crosshair_select', evalst(inf['NoCrosshair']))
	lizcbox_stat('adv_crosshair', evalst(inf['AdvCrosshair']))
	lizcbox_stat('has_portals', evalst(inf['HasPortals']))
	lizcbox_stat('no_difficulty_selection', evalst(inf['NoDifficulty']))
	lizcbox_stat('old_fleshlight', evalst(inf['use_legacy_flashlight']))

	gminfo_icon_manager()
}
// fs.existsSync

// basic info
function gameinfo_save_back()
{
	// use_legacy_flashlight
	
	// update context with new game name
	if ($('#gminfo_gamename_input').val().trim() == ''){
		window.foil_context.full.full_game_name = 'Sample Text';
	}else{
		window.foil_context.full.full_game_name = $('#gminfo_gamename_input').val();
	}
	window.foil_context.full.autoconvert_icon = lizcbox_stat('icon_autoconvert');

	bltalk.send({
		'action': 'gameinfo_save_back',
		'payload': {
			'gminfo_path': window.foil_context.full.gameinfo_path,
			'base_keys': {
				'game': window.foil_context.full.full_game_name,
				'title': $('#gminfo_gametitle_input').val(),
				'icon': $('#gminfo_gameicon_input').val(),
				'use_legacy_flashlight': evalst(lizcbox_stat('old_fleshlight')),
				'NoCrosshair': evalst(lizcbox_stat('no_mp_crosshair_select')),
				'SupportsVR': evalst(lizcbox_stat('vr_support')),
				'SupportsDX8': evalst(lizcbox_stat('dx8support')),
				'NoModels': evalst(lizcbox_stat('no_mp_model_select')),
				'AdvCrosshair': evalst(lizcbox_stat('adv_crosshair')),
				'HasPortals': evalst(lizcbox_stat('has_portals')),
				'NoDifficulty': evalst(lizcbox_stat('no_difficulty_selection'))
			},
			'app_id': $('#gminfo_appid_input').val()
		}
	});

	foil_save_context(false)
	$('#gameinfo_mod_minititle').text(window.foil_context.full.full_game_name)
}



// pass client location and icon path input

// todo: it's possible to check if file exists in js
async function gminfo_icon_manager(set=false, pl={})
{
	// remove quotation marks from the input
	$('#gminfo_gameicon_input').val($('#gminfo_gameicon_input').val().replaceAll('"', ''))

	// get the icon
	var get_icon = await bltalk.send({
		'action': 'gameinfoman_get_mod_icon',
		'payload': {
			'client_path': window.foil_context.full.client_folder_path,
			'icon_path': $('#gminfo_gameicon_input').val()
		}
	});
	log('gameinfo', 'Got icon from blender:', get_icon)

	if (get_icon['conversion_success'] == false){
		console.log('Icon conversion failed')
		return
	}

	// base64 to image
	// no fetch! yay! sync! yay!
	$('#gameinfo_icon_preview img').attr('src', lizard.b64toimg(get_icon['img_base64']));

}




