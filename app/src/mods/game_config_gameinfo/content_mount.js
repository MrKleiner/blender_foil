

function display_content_mounts(mounts)
{
	log('gameinfo', mounts)
	pool = $('#gameinfo_content_mount_pool_items')
	pool.empty()
		
	for (var entry of mounts['content_mount']){
		// init checkboxes
		var cbstate = entry['key'].split('+')
		var cbstate = cbstate.map(st => st.trim().toLowerCase());
		print('game' in cbstate)

		var mk_entry = $(`
			<div class="cmount_pool_entry">
				<keys>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game') 					? 'set' : 'unset'}">game</lzcbox>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('mod') 					? 'set' : 'unset'}">mod</lzcbox>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game_write') 			? 'set' : 'unset'}">game_write</lzcbox>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('gamebin') 				? 'set' : 'unset'}">GameBin</lzcbox>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('platform') 				? 'set' : 'unset'}">platform</lzcbox>
					<lzcbox raw lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('default_write_path') 	? 'set' : 'unset'}">Default_Write_Path</lzcbox>
				</keys>
				<basepath></basepath>
				<input type="text" value="${entry['value'].replace(/(?<=\|)(.*?)(?=\|)/, '').replaceAll('|', '')}">
			</div>
		`)
		pool.append(mk_entry)

		var set_to = (
			(entry['value'].toLowerCase().includes('all_source_engine_paths') ? 'engine' : false)
			||
			(entry['value'].toLowerCase().includes('gameinfo_path') ? 'client' : false)
			||
			('abs')
		)

		lzdrops.spawn(
			mk_entry.find('basepath'),
			CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString(),
			{
				'menu_name': 'Relative To',
				'default': set_to,
				'menu_entries': [
					{
						'name': 'Engine',
						'dropdown_set': 'engine'
					},
					{
						'name': 'Client',
						'dropdown_set': 'client'
					},
					{
						'name': 'Absolute',
						'dropdown_set': 'abs'
					}
				]
			}
		)
	}

	// resync checkboxes
	lzcbox.resync()
}