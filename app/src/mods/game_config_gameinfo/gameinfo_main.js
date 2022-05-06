
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
				'default': 'Singleplayer_Only',
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
	});
}



// takes an element with dropdown_set attribute (menu entry element)
function set_steam_appid_from_dropdown(dr_item)
{
	document.querySelector('#gminfo_appid_input').value = dr_item.getAttribute('dropdown_set');
}


