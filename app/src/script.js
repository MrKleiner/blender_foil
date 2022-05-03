




Element.prototype.lizchecked=function(status) {
    // if(value===undefined) value=true;
    // if(this.hasAttribute(attribute)) this.removeAttribute(attribute);
    // else this.addAttribute(attribute,value);
    if (status == undefined)
    {
	    if (this.getAttribute('lizcbox') == 'set'){
	    	return true
	    }else{
	    	return false
	    }
	}else{
		if (status == true){
			this.setAttribute('lizcbox', 'set');
		}
		if (status == false){
			this.setAttribute('lizcbox', 'unset');
		}
	}
};







document.addEventListener('keydown', kvt => {
    // ===================================
    //               App
    // ===================================
    console.log('keypress');
    app_reload_refresh(kvt)

    const buildsuggestions = event.target.closest('.simple_uilist_text_input');
    if (buildsuggestions) { uilist_scroller(buildsuggestions.parentElement.querySelector('.simple_uilist_suggest'), kvt) }
    

});





document.addEventListener('keyup', kvt => {

    // ===================================
    //               modmaker
    // ===================================
    const validate_modmaker_opts_1 = event.target.closest('#modmaker_new_client_cl_name input');
    const validate_modmaker_opts_2 = event.target.closest('#modmaker_new_client_game_name input');
    if (validate_modmaker_opts_1 || validate_modmaker_opts_2){
    	modmaker_validate_required_options()
    }


    // simple_ui_list_buildsuggest(tgtsug)
	// load new modmaker
    const buildsuggestions = event.target.closest('.simple_uilist_text_input');
    if (buildsuggestions) { simple_ui_list_buildsuggest(buildsuggestions.parentElement, kvt) }





});




document.addEventListener('focusout', kvt => {

	console.log('asdasdasdasdasdasd')

    // ===================================
    //               uilists
    // ===================================
    const ulist_text_focus = event.target.closest('.simple_uilist_text_input');
    if (ulist_text_focus){uilist_showhide(ulist_text_focus.parentElement.querySelector('.simple_uilist_suggest'), false)}



});


document.addEventListener('focusin', kvt => {

	console.log('asdasdasdasdasdasd')

    // ===================================
    //               uilists
    // ===================================
    const ulist_text_focus = event.target.closest('.simple_uilist_text_input');
    if (ulist_text_focus){uilist_showhide(ulist_text_focus.parentElement.querySelector('.simple_uilist_suggest'), true)}



});





document.addEventListener('click', event => {
    console.log('click_registered');

    // ===================================
    //               Toolbar
    // ===================================

	// load skyboxer
    const skyboxer_app = event.target.closest('[dashboard_action="load_skyboxer"]');
    if (skyboxer_app) { skyboxer_module_loader() }

	// load new modmaker
    const load_newmodmaker_app = event.target.closest('[lizmenu_action="load_newmodmaker"]');
    if (load_newmodmaker_app) { newmodmaker_loader() }

	// load dashboard
    const load_dashboard_app = event.target.closest('[lizmenu_action="load_main_dashboard"]');
    if (load_dashboard_app) { dashboard_app_loader() }





















    // ===================================
    //            Checkbox API
    // ===================================

	// checkboxer
    const checkboxer = event.target.closest('[lizcbox].lizcbox_container');
    const checkboxer_hbox = event.target.closest('.lizcbox_hitbox');
    if (checkboxer || checkboxer_hbox) { lizcboxes_switch(checkboxer || checkboxer_hbox) }
















    // ===================================
    //            Dropdown API
    // ===================================

	// open dropdown
    const dropdown_open = event.target.closest('[haslizdropdown]');
    if (dropdown_open) {
    	// should toggle
    	/*
    	if (dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility == 'visible'){
    		dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility = 'hidden';
    		dropdown_open.querySelector('.lizard_dropdown_entries').classList.add('lizdropdown_active');
    	}else{
    		dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility = 'visible';
    	}
    	dropdown_open.querySelector('.lizard_dropdown_entries').style.opacity = 1;
    	*/
    	dropdown_open.querySelector('.lizard_dropdown_entries').classList.toggle('lizdropdown_entries_shown');
    	dropdown_open.classList.toggle('lizdropdown_active');
    	// dropdown_open.querySelector('.lizard_menu').classList.toggle('lizdropdown_active');
    }else{
    	// todo: this is actually slow as fuck
    	$('.lizard_dropdown_entries, .lizard_menu, [haslizdropdown]')
    	.removeClass('lizdropdown_entries_shown')
    	.removeClass('lizdropdown_active');
    }

	// set dropdown active item
    const dropdown_set = event.target.closest('.lizard_dropdown_entries [dropdown_set]');
    if (dropdown_set) {
    	var dropdownroot = dropdown_set.closest('.lizard_menu');
    	// set title
    	// dropdownroot.querySelector('.lizmenu_title').innerText = dropdown_set.getAttribute('dropdown_set');
    	// console.log(dropdown_set.querySelector('.lizard_menu_entry_text').textContent);
    	dropdownroot.querySelector('.lizmenu_title').innerText = dropdown_set.querySelector('.lizard_menu_entry_text').textContent;
    	dropdownroot.querySelector('.lizard_dropdown_entries').style.visibility = 'hidden';
    	dropdownroot.setAttribute('liz_active_item', dropdown_set.getAttribute('dropdown_set'))
    }























    // ===================================
    //               Modmaker
    // ===================================

	// append preinstalled
    const mdmapreinstalled = event.target.closest('#modmaker_fetch_preinstalled');
    if (mdmapreinstalled) {
		apc_send({
			'action': 'modmaker_get_preinstalled_engines'
		})
    }


	// set active engine
    const load_engine_info = event.target.closest('#modmaker_engine_selector .simple_list_v1_pool_item');
    if (load_engine_info) {
		apc_send({
			'action': 'modmaker_get_engine_info',
			'engine_exe': load_engine_info.getAttribute('engine_path')
		});
		window.modmaker_active_engine = {
			'elem': load_engine_info,
			'engpath': load_engine_info.getAttribute('engine_path')
		}
		$('#modmaker_engine_selector .simple_list_v1_pool_item').removeClass('simple_list_v1_pool_item_const_active');
		$(load_engine_info).addClass('simple_list_v1_pool_item_const_active');
    }

	// save engine details
    const save_engine_info = event.target.closest('#new_engine_save_config');
    if (save_engine_info) { modmaker_save_engine_details() }

	// create new engine
    const modmaker_mk_new_engine = event.target.closest('#modmaker_add_new_engine');
    if (modmaker_mk_new_engine) { modmaker_new_engine() }

	// delete new engine
    const modmaker_del_new_engine = event.target.closest('#new_engine_del_config');
    if (modmaker_del_new_engine) {
    	// todo: kinda unreliable
		apc_send({
			'action': 'modmaker_delete_engine',
			'engine': window.modmaker_active_engine['elem'].getAttribute('engine_path')
		});
		window.modmaker_active_engine['elem'].remove();
		$('#modmaker_client_selector, #modmaker_engine_details').css('display', 'none');
    }


	// set active client
    const set_active_client = event.target.closest('#modmaker_client_selector_installed_pool .simple_list_v1_pool_item');
    if (set_active_client) {
		// $(set_active_client).addClass('simple_list_v1_pool_item_const_active');
		set_active_client.toggleAttribute('selected_client');
		set_active_client.classList.toggle('simple_list_v1_pool_item_const_active');
    }


    // validator modmaker_validate_required_options()
    // todo: use comma in selector ?
    const validate_modmaker_opts_1 = event.target.closest('#modmaker_spawn_client_mpsp2013dlls');
    const validate_modmaker_opts_2 = event.target.closest('#modmaker_spawn_client_dll_dropdown');
    if (validate_modmaker_opts_1 || validate_modmaker_opts_2){
    	// console.log('validator')
    	modmaker_validate_required_options()
    }

    // create mod from raw
    const modmaker_mkmod_raw = event.target.closest('#modmaker_new_client_from_tplate');
    if (modmaker_mkmod_raw){
    	modmaker_spawn_mod(false)
    }

    // create mod from mapbase
    const modmaker_mkmod_mapbase = event.target.closest('#modmaker_new_client_newblank');
    if (modmaker_mkmod_mapbase){
    	modmaker_spawn_mod(true)
    }


















});



document.addEventListener('change', event => {
    // ===================================
    //               modmaker
    // ===================================
    console.log('changed')
    const modmaker_check_engine_exe = event.target.closest('#modmaker_engine_details_exepath input');
    if (modmaker_check_engine_exe) { modmaker_check_engine_exe_exists() }

    const modmaker_check_set_icon = event.target.closest('#modmaker_engine_details_icon input');
    if (modmaker_check_set_icon) { modmaker_check_icon() }


	// game options validator
    const validate_modmaker_opts_1 = event.target.closest('#modmaker_new_client_cl_name input');
    const validate_modmaker_opts_2 = event.target.closest('#modmaker_new_client_game_name input');
    if (validate_modmaker_opts_1 || validate_modmaker_opts_2){
    	modmaker_validate_required_options()
    }


});








document.addEventListener('mouseover', event => {
    // ===========================
    //           Toolstips
    // ===========================

    // important todo: It's a pretty bootleg fix and logic is extremely poor
    // There should be a better way of determining wether it's on or not
    // init should also be done separately
	const cursor_over_tooltip_obj = event.target.closest('[liztooltip]');
	if (cursor_over_tooltip_obj){
		var tipbox = document.querySelector('[lizards_tooltip_box]');
		if (tipbox != null){
			if (tipbox.style.visibility != 'visible'){
				if (typeof mrk_ect_timer != 'undefined') { clearTimeout(mrk_ect_timer) }
				lizshowtooltip(cursor_over_tooltip_obj, event) 
			}
		}else{
			lizshowtooltip(cursor_over_tooltip_obj, event)
		}
		
	}

	const cursor_over_tooltip_obj_leave_soon = event.target.closest('[liztooltip]');
	if (!cursor_over_tooltip_obj_leave_soon)
	{
		// clearTimeout(mrk_ect_timer);
		// console.log(mrk_ect_timer);
		if (typeof mrk_ect_timer != 'undefined') { clearTimeout(mrk_ect_timer) }
		// $('[lizards_tooltip_box]').css('display', 'none');
		$('[lizards_tooltip_box]').css('visibility', 'hidden');
		// document.querySelector('[lizards_tooltip_box]').style.visibility = 'hidden';
	}
    // ===========================
    //           Tooltips
    // ===========================
});

document.addEventListener('mousemove', event => {
	window.actualmpos = {
		'x': event.clientX,
		'y': event.clientY,
		'tgt': event.target
	}
});

document.addEventListener('mouseout', event => {
    // ===========================
    //           Tooltips
    // ===========================
/*    
	const cursor_over_tooltip_obj_leave_soon = event.target.closest('[liztooltip]');
	if (cursor_over_tooltip_obj_leave_soon)
	{
		if (event.target.closest('[liztooltip]') || )
		{
			// clearTimeout(mrk_ect_timer);
			// console.log(mrk_ect_timer);
			if (typeof mrk_ect_timer != 'undefined') { clearTimeout(mrk_ect_timer) }
			// $('[lizards_tooltip_box]').css('display', 'none');
			$('[lizards_tooltip_box]').css('visibility', 'hidden');
			// document.querySelector('[lizards_tooltip_box]').style.visibility = 'hidden';
		}
	}
*/
    // ===========================
    //           Tooltips
    // ===========================
});









/*
$( "#result" ).load( "ajax/test.html", function() {
  alert( "Load was performed." );
});

*/

/*
$(document).ready(function(){


	const net = require("net");
	let socket;

	// socket = remote_server ? net.connect(1337, 'localhost') : net.connect(1337);
	socket = net.connect(1337);

	// let ostream = fs.createWriteStream("./receiver/SC-02.pdf");
	let ostream = ''
	let date = new Date(), size = 0, elapsed;
	socket.on('data', chunk => {
	  size += chunk.length;
	  elapsed = new Date() - date;
	  socket.write(`\r${(size / (1024 * 1024)).toFixed(2)} MB of data was sent. Total elapsed time is ${elapsed / 1000} s`)
	  process.stdout.write(`\r${(size / (1024 * 1024)).toFixed(2)} MB of data was sent. Total elapsed time is ${elapsed / 1000} s`);
	  ostream.write(chunk);
	});
	socket.on("end", () => {
	  console.log(`\nFinished getting file. speed was: ${((size / (1024 * 1024)) / (elapsed / 1000)).toFixed(2)} MB/s`);
	        input_d = JSON.parse(ostream)
	        if (input_d['app_action'] == 'add_skybox_side')
	        {
	        	skyboxer_sides_filler(input_d['image'], input_d['side'])
	        }
	  process.exit();
	});



});

*/























/*
============================================================
------------------------------------------------------------
                    Simple menus START
------------------------------------------------------------
============================================================
*/

/*
function lizmenus_init()
{

	document.querySelectorAll('[lizmenu_initid]').forEach(function(userItem) {
		// console.log(userItem)

		var tgt_menu = userItem
		console.log(userItem);
		tgt_menu.style.marginTop = (userItem.parentElement.offsetHeight).toString() + 'px'
		tgt_menu.style.marginLeft = (-1 * parseInt(window.getComputedStyle(userItem.parentElement, null).getPropertyValue('padding-left').replace('px', ''))).toString() + 'px'
	});

}
*/





/*
 -----------------------
	      Maker
 -----------------------
*/

// takes selector string and items dict as an input
// dict is as follows:
/*
{
	'menu_name': 'Pootis',
	'menu_entries': [
		{
			'name': 'Skyboxer',
			'action': 'load_skyboxer_app',
			'icon': 'link/to/icon.png OR svg code',
			'icon_mode': 'bitmap OR svg'
		},
		{
			'name': 'Skyboxer',
			'action': 'load_skyboxer_app',
			'icon': 'link/to/icon.png OR svg code',
			'icon_mode': 'bitmap OR svg'
		}
	]
}
*/
// Example result:
/*
<div class="lizard_menu">
	<div class="lizmenu_title">Preferences</div>
	<div class="lizard_menu_entries">
		<div class="lizard_menu_entry">
			<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
			<div class="lizard_menu_entry_text">Entry</div>
		</div>
		<div class="lizard_menu_entry">
			<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
			<div class="lizard_menu_entry_text">Entry</div>
		</div>
	</div>
</div>
*/
// todo: Add more options for the menu and menu entries
function create_lizmenu(slct, itemsd)
{
	//
	// Populate menu
	//

	var domenu = $(slct);

	domenu.empty();

	var menu_plate = $(`
		<div class="lizard_menu">
			<div class="lizmenu_title">FATAL_ERROR</div>
			<div class="lizard_menu_entries">
			</div>
		</div>
	`);

	for (var lzitem of itemsd['menu_entries'])
	{
		// .hasOwnProperty('name')
		if (lzitem['type'] != 'separator')
		{
			var entry_plate = $(`
				<div class="lizard_menu_entry">
					<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
					<div class="lizard_menu_entry_text">FATAL_ERROR</div>
				</div>
			`);

			// set icon
			entry_plate.find('.lizard_menu_entry_icon img')[0].src = lzitem['icon'];
			// set entry text
			entry_plate.find('.lizard_menu_entry_text').text(lzitem['name']);
			// set item action
			entry_plate.attr('lizmenu_action', lzitem['action']);
			// svg condition
			if (lzitem['svg'] != true){entry_plate.find('.lizard_menu_entry_icon img').css('object-fit', 'contain')}

		}else{
			var entry_plate = $(`<div class="lizard_menu_separator"></div>`);
		}

		// append to entries pool
		menu_plate.find('.lizard_menu_entries').append(entry_plate);
	}

	// set menu title
	menu_plate.find('.lizmenu_title').text(itemsd['menu_name']);

	// append menu to target
	domenu.append(menu_plate)

	// select appended menu
	// todo: .append returns selector?
	var newmenu = domenu.find('.lizard_menu');
	// Make parent a hitbox too
	// todo: make this optional
	domenu.attr('haslizmenu', true);
	// select menu items
	var newmenu_items = domenu.find('.lizard_menu_entries');


	//
	// set menu margins
	//

	// first - margin-top
	// margin top is: height of the resulting lizmenu + padding-top of the parent container

	// get padding of the parent container, if any
	var padding_top = parseInt(window.getComputedStyle(newmenu[0], null).getPropertyValue('padding-top').replace('px', ''));
	var margin_top = newmenu[0].offsetHeight
	if (!isNaN(padding_top)){
		margin_top += padding_top
	}

	// second - margin-left
	var padding_left = parseInt(window.getComputedStyle(newmenu.parent()[0], null).getPropertyValue('padding-left').replace('px', ''));
	var margin_left = 0
	if (!isNaN(padding_left)){
		margin_left += padding_left * -1
	}

	// set style
	newmenu_items.css('margin-left', margin_left.toString() + 'px')
	newmenu_items.css('margin-top', margin_top.toString() + 'px')

}











/*
document.querySelectorAll('.lizard_menu').forEach(function(userItem) {
    lizard_log(userItem);
    userItem.setAttribute('style', 'display: none;');
    // userItem.classList.add('lizhide');
});
*/

/*
document.addEventListener('mouseover', event => {
    // console.log('wtf');

    const pringles = event.target.closest('[lizards_menu]');
    if (pringles) { lizmenu_pos_fixup(pringles) }

});


function lizmenu_pos_fixup(lizmenu)
{
	
	var tgt_menu = lizmenu.querySelector('.lizard_menu');
	console.log(lizmenu);
	tgt_menu.style.marginTop = (lizmenu.offsetHeight).toString() + 'px'
	tgt_menu.style.marginLeft = (-1 * parseInt(window.getComputedStyle(lizmenu, null).getPropertyValue('padding-left').replace('px', ''))).toString() + 'px'

}

*/




/*
============================================================
------------------------------------------------------------
                      Simple menus END
------------------------------------------------------------
============================================================
*/
















/*
============================================================
------------------------------------------------------------
                      svg append
------------------------------------------------------------
============================================================
*/


function svgappender()
{
	document.querySelectorAll('appendsvg').forEach(function(userItem) {
		// .replaceWith()
		fetch(userItem.getAttribute('svgsrc'), {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			}
		})
		.then(function(response) {
			console.log(response.status);
			response.text().then(function(data) {
				$(userItem).replaceWith(data)
			});
		});
		// userItem.parentNode.replaceChild(newItem, listItem);
	});
}

































/*
=====================================================================
---------------------------------------------------------------------
                             Simple UILists
---------------------------------------------------------------------
=====================================================================
*/

function init_simple_ui_lists()
{
	document.querySelectorAll('uilist').forEach(function(userItem) {
		// todo: safety fallbacks ?
		var listcallback = userItem.getAttribute('windowlist');
		var mainparent = userItem.parentElement;
		var appender = 
		`
			<input type="text" class="simple_uilist_text_input">
			<div uilist_suggestfrom="` + listcallback + `" class="simple_uilist_suggest"></div>
		`;
		$(userItem.parentElement).append(appender);
		// todo: a mess ??
		var ulist = userItem.parentElement.querySelector('div.simple_uilist_suggest');
		// console.log('Uilist', ulist)
		userItem.remove();


		//
		// Do margins for a dropdown
		//

		// first - margin-top
		// margin top is: height of the resulting lizmenu + padding-top of the parent container

		// get padding of the parent container, if any

		var padding_top = parseInt(window.getComputedStyle(mainparent, null).getPropertyValue('padding-top').replace('px', ''));
		var margin_top = mainparent.offsetHeight;
		if (!isNaN(padding_top)){
			margin_top += padding_top
		}

		// second - margin-left
		var padding_left = parseInt(window.getComputedStyle(mainparent, null).getPropertyValue('padding-left').replace('px', ''));
		var margin_left = 0
		if (!isNaN(padding_left)){
			margin_left += padding_left * -1
		}


		// set style
		// todo: get rid of jquery
		$(ulist).css('margin-left', margin_left.toString() + 'px');
		$(ulist).css('margin-top', (margin_top + 5).toString() + 'px');


	});
}


// dont append to html tree. Keep as a reference in memory
// takes container containing text input and the list container
// expects a referenced window object to be an array or strings
// important todo: rewrite. This is an extremely edgy way of displaying matches...
// store matched results in the same window object and then cycle through them.
function simple_ui_list_buildsuggest(tgtsug, keyvt)
{
	var prohibited_codes = [38, 40, 17, 18, 16, 20, 9, 91, 37, 39, 93, 92, 13, 27];

	if (prohibited_codes.includes(keyvt.keyCode)){
		return
	}

	var txt_inp = tgtsug.querySelector('input.simple_uilist_text_input');
	var ulist = tgtsug.querySelector('div.simple_uilist_suggest');
	// todo: slow ???
	var wincont = window[ulist.getAttribute('uilist_suggestfrom')];
	var querytext = txt_inp.value;
	ulist.innerHTML = '';

	var append_linit = 0;

	// todo: allow custom configs

	for (var centry of wincont){
		if (centry.toLowerCase().includes(querytext.toLowerCase()) && append_linit <= 300){
			append_linit++
			var bdsm = document.createElement('div');
			bdsm.setAttribute('class', 'simple_uilist_suggestion_entry');
			bdsm.textContent = centry
			if (append_linit >= 12){bdsm.style.display = 'none'}
			ulist.appendChild(bdsm);
		}
	}

}


function uilist_scroller(ulist, keyact)
{

	var get_indexed = ulist.querySelector('[ulist_active_item]');
	var children_arrayed = Array.from(ulist.children);

	if (get_indexed == null){
		var uindex = -1
	}else{
		var uindex = children_arrayed.indexOf(get_indexed);
	}

	// todo: duplicates avoid

	// next element
	if (keyact.keyCode == 40 || keyact.keyCode == 9){
		keyact.preventDefault();
		// only if next element exists
		if (children_arrayed[uindex + 1] != undefined){

			// remove styles and remove active
			for (var rm of children_arrayed){
				rm.removeAttribute('ulist_active_item');
				rm.classList.remove('simple_uilist_suggestion_entry_active');
			}

			// hide previous
			var previous_last = children_arrayed[uindex - 10]
			// todo: also check if it's a valid node ?
			if (previous_last != undefined){
				previous_last.style.display = 'none';
				previous_last.setAttribute('ulist_visible', 'false');
			}

			// unhide next
			var enext = children_arrayed[uindex + 1]
			if (enext != undefined){
				enext.removeAttribute('style');
				enext.classList.add('simple_uilist_suggestion_entry_active');
				enext.setAttribute('ulist_visible', true);
				enext.setAttribute('ulist_active_item', true);
			}

			ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex + 1].textContent
		}
	}

	// previous
	if (keyact.keyCode == 38){
		keyact.preventDefault();
		// only if next element exists
		if (children_arrayed[uindex - 1] != undefined){

			// remove styles and remove active
			for (var rm of children_arrayed){
				rm.removeAttribute('ulist_active_item');
				rm.classList.remove('simple_uilist_suggestion_entry_active');
			}

			// hide previous
			var previous_last = children_arrayed[uindex + 10]
			// todo: also check if it's a valid node ?
			if (previous_last != undefined){
				previous_last.style.display = 'none';
				previous_last.setAttribute('ulist_visible', false);
			}

			// unhide next
			var enext = children_arrayed[uindex - 1]
			if (enext != undefined){
				enext.removeAttribute('style');
				enext.setAttribute('ulist_visible', true);
				enext.setAttribute('ulist_active_item', 'true');
				enext.classList.add('simple_uilist_suggestion_entry_active');
			}

			ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex - 1].textContent
		}
	}

	// apply
	if (keyact.keyCode == 13 && uindex != -1){
		keyact.preventDefault();
		ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex].textContent;
		uilist_showhide(ulist, false)
	}

}

// true = show
// false == hide
function uilist_showhide(thelist, ustate)
{
	if (ustate == true){
		simple_ui_list_buildsuggest(thelist.parentElement, false)
		thelist.style.display = null;
	}

	if (ustate == false){
		thelist.innerHTML = '';
		thelist.style.display = 'none';
	}
}


































/*
============================================================
------------------------------------------------------------
                   Simple dropdowns START
------------------------------------------------------------
============================================================
*/

function create_lizdropdown(slct, itemsd)
{
	//
	// Populate menu
	//

	var domenu = $(slct);

	domenu.empty();

	var gwidth = document.querySelector(slct).clientWidth;

	var menu_plate = $(`
		<div class="lizard_menu">
			<div class="lizmenu_title"><span style="color: #BC4141">None</span></div>
			<div class="lizard_dropdown_arrow_icon">
				<img src="assets/arrow_down.svg">
			</div>
			<div style="width: ` + gwidth.toString() + `px" class="lizard_dropdown_entries">
			</div>
		</div>
	`);

	for (var lzitem of itemsd['menu_entries'])
	{
		// .hasOwnProperty('name')
		if (lzitem['type'] != 'separator')
		{
			var entry_plate = $(`
				<div class="lizard_menu_entry">
					<div class="lizard_menu_entry_text">FATAL_ERROR</div>
				</div>
			`);

			// set icon
			// entry_plate.find('.lizard_menu_entry_icon img')[0].src = lzitem['icon'];
			// set entry text
			entry_plate.find('.lizard_menu_entry_text').text(lzitem['name']);
			// set item action
			entry_plate.attr('dropdown_set', lzitem['dropdown_set']);
			// svg condition
			// if (lzitem['svg'] != true){entry_plate.find('.lizard_menu_entry_icon img').css('object-fit', 'contain')}

		}else{
			// dropdowns don't need a separator
			// var entry_plate = $(`<div class="lizard_menu_separator"></div>`);
		}

		// append to entries pool
		menu_plate.find('.lizard_dropdown_entries').append(entry_plate);
	}

	// set menu title
	// which is basically an entry with separator
	// menu_plate.find('.lizmenu_title').text(itemsd['menu_name']);

	menu_plate.find('.lizard_dropdown_entries').append(`<div class="lizard_menu_separator"></div>`);
	menu_plate.find('.lizard_dropdown_entries').append(`
		<div style="pointer-events: none" class="lizard_menu_entry">
			<div class="lizard_dropdown_bottom_title lizard_menu_entry_text">` + itemsd['menu_name'] + `</div>
		</div>
	`);



	// append menu to target
	domenu.append(menu_plate)

	// select appended menu
	// todo: .append returns selector?
	var newmenu = domenu.find('.lizard_menu');
	// Make parent a hitbox too
	// todo: make this optional
	domenu.attr('haslizdropdown', true);
	// select menu items
	var newmenu_items = domenu.find('.lizard_dropdown_entries');


	//
	// set menu margins
	//

	// first - margin-top
	// margin top is: height of the resulting lizmenu + padding-top of the parent container

	// get padding of the parent container, if any
	var padding_top = parseInt(window.getComputedStyle(newmenu[0], null).getPropertyValue('padding-top').replace('px', ''));
	var margin_top = newmenu[0].offsetHeight
	if (!isNaN(padding_top)){
		margin_top += padding_top
	}

	// second - margin-left
	var padding_left = parseInt(window.getComputedStyle(newmenu.parent()[0], null).getPropertyValue('padding-left').replace('px', ''));
	var margin_left = 0
	if (!isNaN(padding_left)){
		margin_left += padding_left * -1
	}

	// set style
	newmenu_items.css('margin-left', margin_left.toString() + 'px')
	newmenu_items.css('margin-top', (margin_top + 5).toString() + 'px')

}

Element.prototype.lizdropdown=function(set_to) {
    // if(value===undefined) value=true;
    // if(this.hasAttribute(attribute)) this.removeAttribute(attribute);
    // else this.addAttribute(attribute,value);
    // todo: poor logic. use ||
    // var tgt_menu_s = this.closest('.haslizdropdown') || this.closest('.lizard_menu')
	if (this.closest('[haslizdropdown]') != null){
		var tgt_menu_s = this.querySelector('.lizard_menu')
	}
	if (this.closest('.lizard_menu') != null){
		var tgt_menu_s = this.closest('.lizard_menu')
	}

    if (set_to == undefined){
	    if (tgt_menu_s != null){
	    	return tgt_menu_s.getAttribute('liz_active_item')
	    }else{
	    	return null
	    }
    }

};


function lizdropdown_set_active(active_item)
{

}















































/*
============================================================
------------------------------------------------------------
                  Simple checkboxes START
------------------------------------------------------------
============================================================
*/

// init all cboxes
function lizcboxes_init()
{
	document.querySelectorAll('[lizcbox_init]').forEach(function(userItem) {
		console.log(userItem);

		if (userItem.getAttribute('lizcbox_init') == 'set'){
			// var htm_append = `
			// 	<div lizcbox class="lizcbox_container">
			// 		<img draggable="false" src="assets/checkmark.svg">
			// 	</div>
			// `
			var htm_append = `
				<div lizcbox="set" class="lizcbox_container">
					<div class="lizcbox_mark"></div>
				</div>
			`;
		}else{
			var htm_append = `
				<div lizcbox="unset" class="lizcbox_container">
					<div class="lizcbox_mark"></div>
				</div>
			`;
		}
		// hitbox
		if (userItem.hasAttribute('lizcbox_hashitbox')){
			userItem.parentElement.classList.add('lizcbox_hitbox')
		}
		userItem.innerHTML = htm_append;
		userItem.removeAttribute('lizcbox_init');
		userItem.removeAttribute('lizcbox_hashitbox');
	});
}

// todo: safety measures ?
function lizcboxes_switch(tgtbox, state)
{
	tbox = tgtbox.querySelector('[lizcbox].lizcbox_container') || tgtbox

	// todo: getAttribute
	// will be faster
	if ($(tbox).attr('lizcbox') == 'set'){
		$(tbox).attr('lizcbox', 'unset');
	}else{
		$(tbox).attr('lizcbox', 'set');
	}
	
}

/*
============================================================
------------------------------------------------------------
                  Simple checkboxes END
------------------------------------------------------------
============================================================
*/















/*
============================================================
------------------------------------------------------------
                  Simple tooltips START
------------------------------------------------------------
============================================================
*/


function init_liztooltips()
{
	document.querySelectorAll('liztooltip').forEach(function(userItem) {
		console.log(userItem);
		userItem.parentElement.setAttribute('liztooltip', userItem.innerHTML);
		userItem.parentElement.setAttribute('liztooltip_prms', userItem.getAttribute('liztooltip_prms'));
		userItem.remove();
	});
}

//
// 0: pos: top/left/right/bottom
// 1: toparent 1/0
// 2: padding
//

function lizshowtooltip(tl, evt) {
	// if no tooltip elem - create one
	if (document.querySelector('[lizards_tooltip_box]') == null){
		var liztipbox = document.createElement('div');
		liztipbox.setAttribute('lizards_tooltip_box', true);
		liztipbox.style.display = 'none';
		document.body.appendChild(liztipbox);
	}

	var lizardbox = document.querySelector('[lizards_tooltip_box]');
	var splitopts = tl.getAttribute('liztooltip_prms').split(':');
	var boxopts = {
		'pos': splitopts[0],
		'toparent': parseInt(splitopts[1]),
		'padding': parseInt(splitopts[2]),
		'delay': parseInt(splitopts[3])
	}
	lizardbox.innerHTML = tl.getAttribute('liztooltip');


	// construct position
	mrk_ect_timer = setTimeout(function() {
		lizardbox.style.display = 'flex';
		// todo: make it echo into a group
		// console.log('delayed call');
		// lizardbox.style.display = 'flex';
		// because this has to be evaluated right on call
		
		var tgt_e_pos = tl.getBoundingClientRect();

		var tgt_e_h = tl.offsetHeight;
		var tgt_e_w = tl.offsetWidth;

		var tboxh = lizardbox.getBoundingClientRect().height;
		var tboxw = lizardbox.getBoundingClientRect().width;
		// console.log(tboxh)

		var page_w = window.innerWidth;
		var page_h = window.innerHeight;
		
		// console.log(evt)
		var gl_cursor_loc_x = evt.pageX;
		var gl_cursor_loc_y = evt.pageY;
		
		var base_x = 0;
		var base_y = 0;

		var base_posdict = {
			'top': {
				'x': tgt_e_pos.x,
				'y': (tgt_e_pos.y - boxopts['padding']) - tboxh
			},
			'left': {
				'x': tgt_e_pos.x + tboxw,
				'y': tgt_e_pos.y
			},
			'right': {
				'x': tgt_e_pos.x + tgt_e_w + boxopts['padding'],
				'y': tgt_e_pos.y
			},
			'right_up': {
				'x': tgt_e_pos.x + tgt_e_w + boxopts['padding'],
				'y': (tgt_e_pos.y - tboxh) + tgt_e_h
			},
			'bottom':{
				'x': tgt_e_pos.x,
				'y': tgt_e_pos.y + tgt_e_h + boxopts['padding']
			}
		}

		// console.log(base_posdict[boxopts['pos']]['y'].toString() + 'px')

		var non_parent_margin_x = 0
		var non_parent_margin_y = 0

		// relative to mouse or element
		if (boxopts['toparent'] == 1){
			var finalpos_x = base_posdict[boxopts['pos']]['x']
			var finalpos_y = base_posdict[boxopts['pos']]['y']
		}else{
			var finalpos_x = window.actualmpos['x'] + boxopts['padding']
			var finalpos_y = window.actualmpos['y'] + boxopts['padding']

			var non_parent_margin_x = boxopts['padding'] + 5
			var non_parent_margin_y = boxopts['padding'] + 5
		}



		// fix clipping y
		// console.log(base_posdict[boxopts['pos']]['y'] + tboxh);
		if (base_posdict[boxopts['pos']]['y'] + tboxh > page_h){
			finalpos_y -= (((base_posdict[boxopts['pos']]['y'] - non_parent_margin_y) + tboxh) - (page_h - 5))
		}
		// fix clipping x
		if (base_posdict[boxopts['pos']]['x'] + tboxw > page_w){
			finalpos_x -= (((base_posdict[boxopts['pos']]['x'] - non_parent_margin_x) + tboxw) - (page_w - 5))
		}
		
		lizardbox.style.top = finalpos_y.toString() + 'px';
		lizardbox.style.left = finalpos_x.toString() + 'px';

		if (window.actualmpos['tgt'].closest('[liztooltip]')){
			lizardbox.style.visibility = 'visible';
		}
		

	}, boxopts['delay']);

}










/*
=====================================================================
---------------------------------------------------------------------
                             Dashboard
---------------------------------------------------------------------
=====================================================================
*/


function dashboard_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'append_pre_installed':
			newmodmaker_accept_engines(pl['payload'])
			break;
		default:
			console.log('The dashboard module has been called, but no corresponding action was found')
			break;
	}

}

// soundscape manager
// soundscript manager
// vtf maker
// skyboxer
// substance painter connect
// chapter manager (with backgrounds)
// particle manifest generator
// gameinfo editor
// Pack mod as sourcemod/executable/zip
// hammer++ manager
// compilers switch
// propdata manager both predefined and prop-specific
// vehicle scripts maker
// actbusy script maker
// actremap script maker
// decal maker
// speech system script maker
// soundmixer script maker
// weapon script maker
// surfaceproperties manager


function dashboard_app_loader()
{
	// important todo: make this a pre-defined function
	$('#modules_cont').load('tools/main_dashboard.html', function() {
		console.log('loaded dashboard');
		lizcboxes_init();
		init_liztooltips();
		svgappender();
		init_simple_ui_lists();
		// apc_send({
		// 	'action': 'modmaker_load_saved_engines'
		// });
		window['current_app_module'] = 'main_dashboard';
		// window.suggested_maps = 
		fetch('assets/sizetest.txt', {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			}
		})
		.then(function(response) {
			console.log(response.status);
			response.text().then(function(data) {
				window.suggested_maps = JSON.parse(data)
			});
		});

	});
}








































































