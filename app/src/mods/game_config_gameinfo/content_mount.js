

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
					<lzcbox raw meaning="Game" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game') 					? 'set' : 'unset'}">game</lzcbox>
					<lzcbox raw meaning="Mod" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('mod') 					? 'set' : 'unset'}">mod</lzcbox>
					<lzcbox raw meaning="Game_Write" 			lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game_write') 			? 'set' : 'unset'}">game_write</lzcbox>
					<lzcbox raw meaning="GameBin" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('gamebin') 				? 'set' : 'unset'}">GameBin</lzcbox>
					<lzcbox raw meaning="Platform" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('platform') 				? 'set' : 'unset'}">platform</lzcbox>
					<lzcbox raw meaning="default_write_path" 	lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('default_write_path') 	? 'set' : 'unset'}">Default_Write_Path</lzcbox>
				</keys>
				<basepath></basepath>
				<input type="text" value="${entry['value'].replace(/(?<=\|)(.*?)(?=\|)/, '').replaceAll('|', '')}">
				<div class="mount_ctrl_btns">
					<div mv_up></div>
					<div mv_dn></div>
					<div del></div>
				</div>
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





async function gm_mount_save_back()
{
	// console.time('Saved Mounts')
	var paths = [];
	var rel_to_dict = {
		'engine': '|All_Source_Engine_Paths|',
		'client': '|gameinfo_path|',
		'abs': ''
	}
	for (var conm of document.querySelectorAll('#gameinfo_content_mount_pool_items .cmount_pool_entry'))
	{
		// key time, like Game+Write
		var key_type = '';
		for (var kt of conm.querySelectorAll('keys lzcbox')){
			// print(kt.lzbox().state)
			key_type += kt.lzbox().state ? (kt.getAttribute('meaning') + '+') : '';
		}
		paths.push({
			'key': key_type.rstrip('+'),
			'value': rel_to_dict[lzdrops.pool[conm.querySelector('lzdropdown').getAttribute('lzdropname')].active] + conm.querySelector('input').value.trim()
		})
	}
	print(paths)

	// Now save back
	var saved = await bltalk.send({
		'action': 'gameinfo_save_back_mounts',
		'payload': {
			'gminfo_path': foil.context.read.gameinfo_path,
			'search_paths': paths
		}
	});
	print(saved)
	// console.timeEnd('Saved Mounts')
}

// do this with pure js to save a few milliseconds...
// hover has to be responsible afterall...
function hlight_mount_keytype(cb)
{
	// print(cb.closest('lzcbox'))
	if (cb.closest('lzcbox') == null){
		for (var unlight of document.querySelectorAll('#mountpool_keys_descr keydescr')){
			unlight.classList.remove('keydescr_hlight')
		}
		return
	}
	// vanilla ok
	for (var unlight of document.querySelectorAll('#mountpool_keys_descr keydescr')){
		unlight.classList.remove('keydescr_hlight')
	}
	document.querySelector(`#mountpool_keys_descr keydescr[echo="${cb.getAttribute('meaning')}"]`).classList.add('keydescr_hlight')
}


function gm_add_mount_entry()
{
	pool = $('#gameinfo_content_mount_pool_items')
	// todo: this preset HTML is doubled...
	var mk_entry = $(`
		<div class="cmount_pool_entry">
			<keys>
				<lzcbox raw meaning="Game" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">game</lzcbox>
				<lzcbox raw meaning="Mod" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="set">mod</lzcbox>
				<lzcbox raw meaning="Game_Write" 			lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">game_write</lzcbox>
				<lzcbox raw meaning="GameBin" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">GameBin</lzcbox>
				<lzcbox raw meaning="Platform" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">platform</lzcbox>
				<lzcbox raw meaning="default_write_path" 	lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">Default_Write_Path</lzcbox>
			</keys>
			<basepath></basepath>
			<input type="text" value="custom/*">
			<div class="mount_ctrl_btns">
				<div mv_up></div>
				<div mv_dn></div>
				<div del></div>
			</div>
		</div>
	`)
	pool.append(mk_entry)

	lzdrops.spawn(
		mk_entry.find('basepath'),
		CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString(),
		{
			'menu_name': 'Relative To',
			'default': 'engine',
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

	// resync checkboxes
	lzcbox.resync()
}



















