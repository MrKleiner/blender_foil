window.$ = window.jQuery = require('./apis/jquery/3_6_0/jquery.min.js');
window.lizards_mouth = 'lizards_tongue';
const path = require('path');
const {PythonShell} = require('python-shell');
const zpypath = 'C:/Program Files (x86)/Steam/steamapps/common/Blender/3.1/python/bin/python.exe'
window.py_common_opts = {
		mode: 'text',
		pythonPath: zpypath,
		pythonOptions: ['-u'],
		scriptPath: path.join(__dirname, '/app/')
	  };
const net = require('net');



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


/*
function u8btoa(st){
  return btoa(unescape(encodeURIComponent(st)));
}

function u8atob(st){
  return atob(unescape(encodeURIComponent(st)));
}
*/

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
    // console.log('click_registered');

	// load skyboxer
    const skyboxer_app = event.target.closest('[lizmenu_action="load_skyboxer_app"]');
    if (skyboxer_app) { skyboxer_module_loader() }


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
	    	console.log('Total:', window['cst_cache' + socket.remotePort.toString()])

	    	console.log('Closing connection with the client');

	    	// Data should always be a json
	    	// input_d = JSON.parse(window.cstorage)
	    	// input_d = JSON.parse(cst)
	    	input_d = JSON.parse(window['cst_cache' + socket.remotePort.toString()])



	    	//
	    	// Decide what to do
	    	//
			switch (input_d['app_module']) {
				case 'skyboxer':
					skyboxer_module_manager(input_d)
					break;
				case 'load_skyboxer_app':
					skyboxer_module_loader()
					break;
				default:
					console.log('The transmission from the other world has ended, but requested action is unknown')
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
	newmodmaker_loader()

});

function main_app_init()
{
	// create Preferences menu
/*	var pr_menu_items = {
		'menu_name': 'Preferences',
		'menu_entries': [
			{
				'name': 'App Settings',
				'action': 'open_app_prefs',
				'icon': 'nen'
			},
			{
				'name': 'Mod Settings',
				'action': 'open_mod_prefs',
				'icon': 'nen'
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
	*/
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
		client.destroy(); // kill client after server's response
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
		window['current_app_module'] = 'skyboxer'
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



function newmodmaker_loader()
{
	$('#modules_cont').load('tools/mod_maker.html', function() {
		console.log('loaded')
	});
}

























































