window.$ = window.jQuery = require('./apis/jquery/3_6_0/jquery.min.js');
window.lizards_mouth = 'lizards_tongue';
const path = require('path');
const {PythonShell} = require('python-shell');
const zpypath = 'C:/Program Files (x86)/Steam/steamapps/common/Blender/3.1/python/bin/python.exe';
const fs = require('fs');
window.py_common_opts = {
		mode: 'text',
		pythonPath: zpypath,
		pythonOptions: ['-u'],
		scriptPath: path.join(__dirname, '/app/')
	  };
const net = require('net');


/*
function u8btoa(st){
  return btoa(unescape(encodeURIComponent(st)));
}

function u8atob(st){
  return atob(unescape(encodeURIComponent(st)));
}
*/

// encode
function u8btoa(st) {
    return btoa(unescape(encodeURIComponent(st)));
}
// decode
function u8atob(st) {
    return decodeURIComponent(escape(atob(st)));
}

function mkj(bd){
	return JSON.parse(u8atob(bd));
}

function log(wha)
{
	console.log('js: ' + wha)
}


function shell_end_c(err,code,signal)
{
	if (err) throw err;
	console.log('The exit code was: ' + code);
	console.log('The exit signal was: ' + signal);
	console.log('finished');
};

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


function app_reload_refresh(evee)
{
	if (  evee.ctrlKey  &&  evee.keyCode == 82  ){
		location.reload()
	}
}


document.addEventListener('keydown', kvt => {
    console.log('keypress');
    app_reload_refresh(kvt)
});

document.addEventListener('click', event => {
    console.log('click_registered');

    // ===================================
    //               Toolbar
    // ===================================

	// load skyboxer
    const skyboxer_app = event.target.closest('[lizmenu_action="load_skyboxer_app"]');
    if (skyboxer_app) { skyboxer_module_loader() }

	// load new modmaker
    const load_newmodmaker_app = event.target.closest('[lizmenu_action="load_newmodmaker"]');
    if (load_newmodmaker_app) { newmodmaker_loader() }





















    // ===================================
    //            Checkbox API
    // ===================================

	// checkboxer
    const checkboxer = event.target.closest('[lizcbox].lizcbox_container');
    const checkboxer_hbox = event.target.closest('.lizcbox_hitbox');
    if (checkboxer || checkboxer_hbox) { lizcboxes_switch(checkboxer || checkboxer_hbox) }




















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
























});



document.addEventListener('change', event => {
    const modmaker_check_engine_exe = event.target.closest('#modmaker_engine_details_exepath input');
    if (modmaker_check_engine_exe) { modmaker_check_engine_exe_exists() }

    const modmaker_check_set_icon = event.target.closest('#modmaker_engine_details_icon input');
    if (modmaker_check_set_icon) { modmaker_check_icon() }






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
============================================================
------------------------------------------------------------
                          Listener
------------------------------------------------------------
============================================================
*/

// window.cstorage = ''
// let cst = ''

// important todo: separate server into a separate function
$(document).ready(function(){
	// Include Nodejs' net module.
	// const Net = require('net');
	// The port on which the server is listening.
	const port = 1337;

	// var stor = ''

	// Use net.createServer() in your code. This is just for illustration purpose.
	// Create a new TCP server.
	const server = new net.Server();
	// The server listens to a socket for a client to make a connection request.
	// Think of a socket as an end point.
	server.listen(port, function() {
	    console.log('Server listening for connection requests on socket localhost:', port);
	});

	// When a client requests a connection with the server, the server creates a new
	// socket dedicated to that client.
	// A new session has been created, everything inside is in the context of that session
	server.on('connection', function(socket) {
		// let cst = ''
		console.log(socket)
		window['cst_cache' + socket.remotePort.toString()] = ''
	    console.log('A new connection has been established.');

	    // Now that a TCP connection has been established, the server can send data to
	    // the client by writing to its socket.
	    socket.write('Hello, client.');

	    // The server can also receive data from the client by reading from its socket.
	    // Client will be sending chunks of data DURING the session
	    // When data was received - write it down into storage
	    // todo: define storage as let ?
	    
	    socket.on('data', function(chunk) {
	        console.log('Data received from client:', chunk.toString());
	        // window.cstorage += chunk.toString()
	        // cst += chunk.toString()
	        window['cst_cache' + socket.remotePort.toString()] += chunk.toString()
	    });

	    // When the client requests to end the TCP connection with the server, the server
	    // ends the connection.
	    // End means that presumably, all chunks of data have been sent by now
	    socket.on('end', function() {
	    	// console.log('Total:', window.cstorage)
	    	// console.log('Total:', cst)

	    	// have better ideas ?
	    	// comment on github
	    	console.log('Total:', window['cst_cache' + socket.remotePort.toString()])

	    	console.log('Closing connection with the client');

	    	// Data has to always be a json
	    	// input_d = JSON.parse(window.cstorage)
	    	// input_d = JSON.parse(cst)
	    	input_d = JSON.parse(window['cst_cache' + socket.remotePort.toString()])



	    	//
	    	// Decide what to do
	    	//

	    	// important todo: this has to be a separate function
			switch (input_d['app_module']) {
				case 'skyboxer':
					skyboxer_module_manager(input_d)
					break;
				case 'load_skyboxer_app':
					skyboxer_module_loader()
					break;
				case 'modmaker':
					modmaker_module_manager(input_d)
					break;
				default:
					console.log('The transmission from another world has ended, but requested action is unknown');
					break;
			}



			// flush the storage
	        // window.cstorage = ''
	        // let cst = ''
	        delete window['cst_cache' + socket.remotePort.toString()]
	    });


	    // Don't forget to catch error, for your own sake.
	    socket.on('error', function(err) {
	        console.log('Error:', err);
	    });

	});

	// lizmenus_init()
	main_app_init()

	// TESTING
	// newmodmaker_loader()
	
});

function main_app_init()
{
	// create Preferences menu
	create_lizmenu(
			'[apptoolbarctg="preferences"]',
			{
			'menu_name': 'Preferences',
			'menu_entries': [
				{
					'name': 'Mod Settings',
					'action': 'open_mod_prefs',
					'icon': 'assets/wrench_icon.svg'
				},
				{
					'name': 'App Settings',
					'action': 'open_app_prefs',
					'icon': 'assets/cog_icon.svg'
				},
				{
					'type': 'separator'
				},
				{
					'name': 'Exit',
					'action': 'exit_app',
					'svg': true,
					'icon': 'assets/app_exit_icon.svg'
				}
			]
		}
	)

	// create tools menu
	create_lizmenu(
			'[apptoolbarctg="tools"]',
			{
			'menu_name': 'Tools',
			'menu_entries': [
				{
					'name': 'Skyboxer',
					'action': 'load_skyboxer_app',
					'icon': 'assets/world_sky_icon.svg'
				},
				{
					'name': 'Sound Manager',
					'action': 'load_sound_manager_app',
					'icon': 'assets/speaker_icon.svg'
				},
				{
					'name': 'Soundscape Manager',
					'action': 'load_sound_manager_app',
					'icon': 'assets/soundscape_icon.svg'
				},
				{
					'type': 'separator'
				},
				{
					'name': 'Mod Maker',
					'action': 'load_newmodmaker',
					'icon': 'assets/mech_icon.svg'
				}
			]
		}
	)


}







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
                          Sender
------------------------------------------------------------
============================================================
*/

function apc_send(sendpayload)
{
	var client = new net.Socket();
	client.connect(50000, '127.0.0.1', function() {
		console.log('Connected');
		// client.write('Hello, server! Love, Client.');
		client.write(JSON.stringify(sendpayload));
	});

	client.on('data', function(data) {
		console.log('Received: ' + data);
		client.destroy()
	});

	client.on('close', function() {
		console.log('Connection closed');
	});
}









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
				'y': (tgt_e_pos.y) - tboxh
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

		// relative to mouse or element
		if (boxopts['toparent'] == 1){
			var finalpos_x = base_posdict[boxopts['pos']]['x']
			var finalpos_y = base_posdict[boxopts['pos']]['y']
		}else{
			var finalpos_x = window.actualmpos['x'] + boxopts['padding']
			var finalpos_y = window.actualmpos['y'] + boxopts['padding']
		}



		// fix clipping y
		// console.log(base_posdict[boxopts['pos']]['y'] + tboxh);
		if (base_posdict[boxopts['pos']]['y'] + tboxh > page_h){
			finalpos_y -= ((base_posdict[boxopts['pos']]['y'] + tboxh) - (page_h - 5))
		}
		// fix clipping x
		if (base_posdict[boxopts['pos']]['x'] + tboxw > page_w){
			finalpos_x -= ((base_posdict[boxopts['pos']]['x'] + tboxw) - (page_w - 5))
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
                               Skyboxer
---------------------------------------------------------------------
=====================================================================
*/

function skyboxer_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'add_skybox_side':
			skyboxer_sides_filler(pl['image'], pl['side'])
			break;
		case 'upd_side_status':
			skyboxer_status_updater(pl['side'], pl['what'], pl['status'])
			break;
		case 'reset':
			skyboxer_scene_reset()
			break;
		case 'upd_work_status':
			skyboxer_update_wstatus(pl)
			break;
		case 'set_sky_name':
			skybox_set_sky_name(pl)
			break;
		default:
			console.log('The module has been called, but no corresponding action was found')
			break;
	}

}

var	side_def_dict = {
        'bk': 'back',
        'dn': 'down',
        'ft': 'front',
        'lf': 'left',
        'rt': 'right',
        'up': 'up'
    }


// double loading causes issues which ould be easily avoided by NOT performing double loads
function skyboxer_module_loader()
{
	if (window['current_app_module'] != 'skyboxer')
	{
		// load this module and then populate skybox sides, if any
		$('#modules_cont').load('tools/skyboxer.html', function() {
			for (var skside in side_def_dict){
				if (window['skyboxer_savedside_' + side_def_dict[skside]] != undefined){
					$('#sky_' + side_def_dict[skside] + ' .skybox_square').attr('src', window['skyboxer_savedside_' + side_def_dict[skside]]);
				}
			}
		});
		window['current_app_module'] = 'skyboxer';
	}else{
		console.log('skyboxer module is loaded initially')
	}
}



var side_status_def = {
	'blender': '.blender_icon .icon_indicator_circle',
	'pfm': '.pfm_icon .icon_indicator_circle',
	'vtf': '.vtf_icon .icon_indicator_circle',
}

// takes two params:
// side_img - image binary
// side_d - string. Side, like "left"
function skyboxer_sides_filler(side_img, side_d)
{
	fetch('data:image/png;base64,' + side_img)
	.then(function(response) {
		console.log(response.status);
		response.blob().then(function(data) {
			// pgload(data, pgx, response.status)

			// var boobs = new Blob([reader.result], {type: etgt.files[0].type });
			var urlCreator = window.URL || window.webkitURL;
			var imageUrl = urlCreator.createObjectURL(data);

			$('#sky_' + side_def_dict[side_d] + ' .skybox_square').attr('src', imageUrl);
			window['skyboxer_savedside_' + side_def_dict[side_d]] = imageUrl;
		});
	});


	
	// $('#sky_' + side_def_dict[side_d])[0].src = '';
	// $('#sky_' + side_def_dict[side_d])[0].src = side_img + '?' + new Date().getTime();
}

// set status
function skyboxer_status_updater(wside, elem, status)
{
	var decide_status = 'lime'
	if (status == false){
		var decide_status = 'red'
	}
	$('#sky_' + side_def_dict[wside]).find(side_status_def[elem]).css('background', decide_status);
}

function skyboxer_scene_reset()
{
	$('.icon_indicator_circle').css('background', 'red');
	$('.skybox_side_container .skybox_square').attr('src', 'assets/cross_square.png');
}


function skyboxer_update_wstatus(stat)
{
	$('#sky_compile_status').text(stat['status']);
}

function skybox_set_sky_name(skname)
{
	$('#sky_name').text(skname['skyname']);
}


/*
=====================================================================
---------------------------------------------------------------------
                            Skyboxer END
---------------------------------------------------------------------
=====================================================================
*/


















/*
=====================================================================
---------------------------------------------------------------------
                             New Mod Maker
---------------------------------------------------------------------
=====================================================================
*/

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

		tgt_pool.append(mkitem);

	}

	// unlock engine details
	$('#modmaker_client_selector, #modmaker_engine_details').removeAttr('style');

	modmaker_check_engine_exe_exists()

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
	$('#modmaker_engine_details_exepath input').attr('value', 'hl3.eckze').val('hl3.eckze');
	// engine name
	$('#modmaker_engine_details_name input').attr('value', 'half-life 3').val('half-life 3');
	// engine icon
	$('#modmaker_engine_details_icon input').attr('value', '').val('');
	$('#modmaker_engine_details_icon .modmaker_engine_details_item_status img')[0].src = '';

	$('#modmaker_engine_details_items .modmaker_engine_details_list .modmaker_engine_details_list_items .modmaker_engine_details_list_item .modmaker_engine_details_list_item_status img').attr('src', '');

	$('#modmaker_client_selector, #modmaker_engine_details').removeAttr('style');
}










































