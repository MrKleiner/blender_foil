


// ============================================================
// ------------------------------------------------------------
//                      name: gameinfo
// ------------------------------------------------------------
// ============================================================

foil.sys.gameinfo = {}
foil.sys.gameinfo.main = {}
foil.sys.gameinfo.mounts = {}



fsys.gameinfo.manager = function(pl)
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


fsys.gameinfo.app_loader = function()
{
	base_module_loader('game_config_game_info.html')
	.then(function(resolved) {

		// steam appid drowdown
		lzdrops.spawn(
			'#gminfo_appid_dropdown',
			'app_id',
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
		lzdrops.spawn(
			'#gminfo_gametype_dropdown',
			'game_type',
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
		fsys.gameinfo.main.load_info()


	});
}



// takes an element with dropdown_set attribute (menu entry element)
fsys.gameinfo.main.steam_id_from_dropdown = function(dr_item)
{
	document.querySelector('#gminfo_appid_input').value = dr_item.getAttribute('dropdown_set');
}

function evalst(st){
	if (st == undefined || st == null){return false}
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


// load info from context
// app context and fast config should be fully ready by this time
// important todo: there has to be a def dict
fsys.gameinfo.main.load_info = async function()
{
	// evaluate gameinfo through python and receive a json
	var inf = await bltalk.send({
		'action': 'gameinfoman_load_info',
		'payload': {
			'client_path': foil.context.read.client_folder_path
		}
	});
	log('gameinfo', 'Got gameinfo from blender:', inf)

	// set text inputs values
	$('#gminfo_gamename_input').val(inf['game'])
	$('#gameinfo_mod_minititle').text(inf['game'])
	$('#gameinfo_mod_modfolderpath').val(foil.context.read.client_folder_path)
	$('#gminfo_gametitle_input').val(inf['title'])
	$('#gminfo_gameicon_input').val(inf['icon'])
	$('#gminfo_appid_input').val(inf['SteamAppId'])

	// set dropdowns
	lzdrops.pool['game_type'].set(inf['type'])
	lzdrops.pool['app_id'].set($('#gminfo_appid_input').val())

	// set checkboxes
	// todo: fucking make names symmetrical
	// this var actually saves performance (by a few milliseconds)
	var cb = lzcbox.pool;
	var map_pool = {
		'vr_support': 				'SupportsVR',
		'dx8support': 				'SupportsDX8',
		'no_mp_model_select': 		'NoModels',
		'no_mp_crosshair_select': 	'NoCrosshair',
		'adv_crosshair': 			'AdvCrosshair',
		'has_portals': 				'HasPortals',
		'no_difficulty_selection': 	'NoDifficulty',
		'old_fleshlight': 			'use_legacy_flashlight'
	}
	cb['icon_autoconvert'].set(foil.context.read.autoconvert_icon)

	for (var setbox in map_pool){
		cb[setbox].set(evalst(inf[map_pool[setbox]] || '0'))
	}

	await fsys.gameinfo.main.load_icon()

	// lastly, show content mounts
	fsys.gameinfo.mounts.show_mounts(inf)
}
// fs.existsSync

// basic info
fsys.gameinfo.main.save_back = function()
{

	var cbs = lzcbox.pool;
	// update context with new game name
	if ($('#gminfo_gamename_input').val().trim() == ''){
		foil.context.prm('full_game_name', 'Illuminati confirmed', false);
	}else{
		foil.context.prm('full_game_name', $('#gminfo_gamename_input').val(), false);
	}
	foil.context.prm('autoconvert_icon', cbs['icon_autoconvert'].state, false);

	
	bltalk.send({
		'action': 'gameinfo_save_back',
		'payload': {
			'gminfo_path': foil.context.read.gameinfo_path,
			'base_keys': {
				'game': foil.context.read.full_game_name,
				'title': $('#gminfo_gametitle_input').val(),
				'icon': $('#gminfo_gameicon_input').val(),
				'use_legacy_flashlight': evalst(cbs['old_fleshlight'].state),
				'NoCrosshair': evalst(cbs['no_mp_crosshair_select'].state),
				'SupportsVR': evalst(cbs['vr_support'].state),
				'SupportsDX8': evalst(cbs['dx8support'].state),
				'NoModels': evalst(cbs['no_mp_model_select'].state),
				'AdvCrosshair': evalst(cbs['adv_crosshair'].state),
				'HasPortals': evalst(cbs['has_portals'].state),
				'NoDifficulty': evalst(cbs['no_difficulty_selection'].state)
			},
			'app_id': $('#gminfo_appid_input').val()
		}
	});

	foil.context.save()
	$('#gameinfo_mod_minititle').text(foil.context.read.full_game_name)
}



// pass client location and icon path input

// todo: it's possible to check if file exists in js
fsys.gameinfo.main.load_icon = async function()
{
	// remove quotation marks from the input
	$('#gminfo_gameicon_input').val($('#gminfo_gameicon_input').val().replaceAll('"', ''))

	// get the icon
	var get_icon = await bltalk.send({
		'action': 'gameinfoman_get_mod_icon',
		'payload': {
			'client_path': foil.context.read.client_folder_path,
			'icon_path': $('#gminfo_gameicon_input').val()
		}
	});
	log('gameinfo', 'Got icon from blender:', get_icon)

	if (get_icon['conversion_success'] == false){
		print('Icon conversion failed')
		return
	}

	// base64 to image
	// no fetch! yay! sync! yay!
	$('#gameinfo_icon_preview img').attr('src', lizard.b64toimg(get_icon['img_base64']));

}




