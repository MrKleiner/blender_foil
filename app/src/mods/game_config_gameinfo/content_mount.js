

// takes mounts array as an input
foil.sys.gameinfo.mounts.show_mounts = function(mounts)
{
	log('gameinfo', mounts)
	pool = $('#gameinfo_content_mount_pool_items')
	pool.empty()
		
	for (var entry of mounts['content_mount']){
		// init checkboxes
		var cbstate = entry['key'].split('+')
		// python-like strip every element in an array (strip trailing +s)
		var cbstate = cbstate.map(st => st.trim().toLowerCase());
		print('game' in cbstate)

		var mk_entry = $(`
			<div class="cmount_pool_entry">
				<mvtop moverhit></mvtop>
				<mvbot moverhit></mvbot>
				<keys>
					<lzcbox raw meaning="Game" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game') 					? 'set' : 'unset'}">game</lzcbox>
					<lzcbox raw meaning="Mod" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('mod') 					? 'set' : 'unset'}">mod</lzcbox>
					<lzcbox raw meaning="Game_Write" 			lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('game_write') 			? 'set' : 'unset'}">game_write</lzcbox>
					<lzcbox raw meaning="GameBin" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('gamebin') 				? 'set' : 'unset'}">GameBin</lzcbox>
					<lzcbox raw meaning="Platform" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('platform') 				? 'set' : 'unset'}">platform</lzcbox>
					<lzcbox raw meaning="default_write_path" 	lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="${cbstate.includes('default_write_path') 	? 'set' : 'unset'}">Default_Write_Path</lzcbox>
				</keys>
				<basepath></basepath>
				<input nobracks ux type="text" value="${entry['value'].replace(/(?<=\|)(.*?)(?=\|)/, '').replaceAll('|', '')}">
				<div class="mount_ctrl_btns">
					<dragger></dragger>
					<kill>
						<liztooltip liztooltip_prms="top:1:10:200">
							Hold alt and click on this icon to delete a mount entry.
						</liztooltip>
					</kill>
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
	// resync tooltips
	init_liztooltips()
}




// save mounts back to gameinfo.txt
fsys.gameinfo.mounts.save_back = async function()
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
fsys.gameinfo.mounts.hlight_mount_keytype = function(cb)
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






// spawn a mount entry
fsys.gameinfo.mounts.add_mount_entry = function()
{
	pool = $('#gameinfo_content_mount_pool_items')
	// todo: this preset HTML is doubled...
	var mk_entry = $(`
		<div class="cmount_pool_entry">
			<mvtop moverhit></mvtop>
			<mvbot moverhit></mvbot>
			<keys>
				<lzcbox raw meaning="Game" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">game</lzcbox>
				<lzcbox raw meaning="Mod" 					lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="set">mod</lzcbox>
				<lzcbox raw meaning="Game_Write" 			lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">game_write</lzcbox>
				<lzcbox raw meaning="GameBin" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">GameBin</lzcbox>
				<lzcbox raw meaning="Platform" 				lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">platform</lzcbox>
				<lzcbox raw meaning="default_write_path" 	lzcbox_id="${CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString()}" lzcbox_init="unset">Default_Write_Path</lzcbox>
			</keys>
			<basepath></basepath>
			<input nobracks ux type="text" value="custom/*">
			<div class="mount_ctrl_btns">
				<dragger></dragger>
				<kill>
					<liztooltip liztooltip_prms="top:1:10:200">
						Hold alt and click on this icon to delete a mount entry.
					</liztooltip>
				</kill>
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
	// resync tooltips
	init_liztooltips()
}




fsys.gameinfo.mounts.start_mount_drag = function(etgt)
{
	// kill any selection. It breaks everything...
	window.getSelection().removeAllRanges()

	var entry =  etgt.closest('.cmount_pool_entry');
	var compstyle = getComputedStyle(entry);
	var mounts = fsys.gameinfo.mounts;

	// remove any shine effects
	entry.classList.remove('mount_hlight');
	entry.classList.remove('mount_nohlight');

	// important todo: body[special] is a very bad way of achieving this
	document.body.setAttribute('tmp_special', true);

	// declare this object as moving
	mounts.moving_item = entry;
	mounts.moving_item_halfheight = int(compstyle.height.replace('px', ''));
	// store width
	entry.style.width = compstyle.width
	// offset, because lazyness. For now.
	mounts.moving_item.style.top = str(window.actualmpos.y + mounts.moving_item_halfheight) + 'px';

	// placeholder so that shit doesnt jump
	// nextElementSibling
	entry.before(lizard.ehtml(`<div invis_placeholder style="width:${compstyle.width}; height:${int(compstyle.height) + int(compstyle.marginTop) + int(compstyle.marginBottom)}px"></div>`))

	// unhide hitboxes everywhere except this
	document.querySelector('#gameinfo_content_mount_pool_items').setAttribute('moving', true);
	entry.setAttribute('move_tgt', true);
}


fsys.gameinfo.mounts.propagate_entry_move = function()
{
	var mounts = fsys.gameinfo.mounts;

	// if no element to move - just dont do anything at all
	if (mounts.moving_item == null || mounts.moving_item == undefined){return}

	mounts.moving_item.style.top = str(window.actualmpos.y + mounts.moving_item_halfheight) + 'px';
	// print(window.actualmpos.y)
}


fsys.gameinfo.mounts.apply_mount_move = function(evee)
{
	var mounts = fsys.gameinfo.mounts;
	var mv_target = mounts.moving_item;
	var pool_entry = evee.target.closest('.cmount_pool_entry');

	var mv_hitbox = evee.target.closest('[moverhit]');
	print(pool_entry, mv_hitbox)



	var last_hover = document.querySelector('.cmount_pool_entry[vis_mv_top], .cmount_pool_entry[vis_mv_bottom]')
	print('Last hover:', last_hover)

	if (last_hover != null){

		print('Last hover vistop:', last_hover.hasAttribute('vis_mv_top'))
		print('Last hover visbot:', last_hover.hasAttribute('vis_mv_bottom'))


		// if the first child of the pool has hover top attrbute - append it to the beginning of the pool
		if (last_hover.hasAttribute('vis_mv_top')){
			last_hover.before(mv_target)
		}
		// if the last element of the pool has hover bottom attribute - append it to the bottom of the pool
		if (last_hover.hasAttribute('vis_mv_bottom')){
			last_hover.after(mv_target)
		}
	}


	// remove styling from moving target
	mv_target.removeAttribute('move_tgt');
	// remove styling from the page
	document.querySelector('#gameinfo_content_mount_pool_items').removeAttribute('moving');

	// remove top offset
	mv_target.style.top = null
	// remove stored width
	mv_target.style.width = null

	// shine it
	mounts.shine_mount(mounts.moving_item)

	// unregister the item from moving elements
	fsys.gameinfo.mounts.moving_item = null;
	document.body.removeAttribute('tmp_special')

	// remove placeholders
	$('[invis_placeholder]').remove();

	// remove visualizers
	$('.cmount_pool_entry').removeAttr('vis_mv_top');
	$('.cmount_pool_entry').removeAttr('vis_mv_bottom');



	// finally, resave mounts back
	fsys.gameinfo.mounts.save_back()
}




fsys.gameinfo.mounts.visualize_move_tgt = function(etgt)
{
	var hover_entry = etgt.closest('.cmount_pool_entry');

	// remove hover effects from other elements with vanilla js because why not
	for (var novis of document.querySelectorAll('.cmount_pool_entry')){
		novis.removeAttribute('vis_mv_top');
		novis.removeAttribute('vis_mv_bottom');
	}

	// if top then show border from the top
	if (etgt.tagName.toLowerCase() == 'mvtop'){
		hover_entry.setAttribute('vis_mv_top', true);
	}

	// if bottom then show border ftom the bottom
	if (etgt.tagName.toLowerCase() == 'mvbot'){
		hover_entry.setAttribute('vis_mv_bottom', true);
	}
}


fsys.gameinfo.mounts.kill_mount_entry = function(evee)
{
	if (evee.altKey){
		evee.target.closest('.cmount_pool_entry').remove();
	}
	window.getSelection().removeAllRanges()
	// save back
	fsys.gameinfo.mounts.save_back()
}


fsys.gameinfo.mounts.shine_mount = function(tgt)
{
	let shite = tgt;
	shite.classList.remove('mount_hlight');
	shite.classList.remove('mount_nohlight');
	shite.classList.add('mount_hlight');
	jsleep(200)
	.then(function(response) {
		shite.classList.add('mount_nohlight');
		jsleep(600)
		.then(function(response) {
			// $('#gameinfo_content_mount_pool_items .cmount_pool_entry:not(#gameinfo_content_mount_pool_items[moving] .cmount_pool_entry)')

			// .removeClass('mount_hlight mount_nohlight')
			shite.classList.remove('mount_hlight');
			shite.classList.remove('mount_nohlight');
		});
	});
}


