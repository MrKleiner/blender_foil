/*
============================================================
------------------------------------------------------------
                   Core info and functions
------------------------------------------------------------
============================================================
*/
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


// Smart base64 encode
function u8btoa(st) {
    return btoa(unescape(encodeURIComponent(st)));
}
// Smart base64 decode
function u8atob(st) {
    return decodeURIComponent(escape(atob(st)));
}

// quick base64 to json
function mkj(bd){
	return JSON.parse(u8atob(bd));
}

// bootleg logger
function log(wha)
{
	console.log('js: ' + wha)
}

// returns true if an array contains any element which is not present in another array
function array_elem_check(what, inwhat) {
    var magix = what.filter(f => !inwhat.includes(f));
    return magix.length > 0
}

// unused
function shell_end_c(err,code,signal)
{
	if (err) throw err;
	console.log('The exit code was: ' + code);
	console.log('The exit signal was: ' + signal);
	console.log('finished');
}


// ===================================================
//             reload app (f5 implementation)
// ===================================================

// todo: this doubles the keydown event binds
document.addEventListener('keydown', kvt => {
    console.log('keypress');
    app_reload_refresh(kvt)
});
function app_reload_refresh(evee)
{
	if (  evee.ctrlKey  &&  evee.keyCode == 82  ){
		location.reload()
	}
}


/*
===================================================
                    svg append
===================================================
*/

// load specified svg as an element so that it's possible to re-colour it
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


// actual mouse pos before any events
document.addEventListener('mousemove', event => {
	window.actualmpos = {
		'x': event.clientX,
		'y': event.clientY,
		'tgt': event.target
	}
});








/*
============================================================
------------------------------------------------------------
                  APP server listener
------------------------------------------------------------
============================================================
*/



// important todo: ability to create "sessions" during which many jsons could be tossed

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

	    // Basically, every single incoming request will result into a new session being created
	    // every session is an object with a port assigned to it (BIN-BON, INDIVIDUAL PORT TO EACH ONE OF THEM?)
	    // thankfully, once the sender is done with sending shit - a signal about connection termintaion is being sent
	    socket.on('end', function() {
	    	// console.log('Total:', window.cstorage)
	    	// console.log('Total:', cst)

	    	// have better ideas ?
	    	// comment on github
	    	console.log('Total:', window['cst_cache' + socket.remotePort.toString()])

	    	console.log('Closing connection with the client');

	    	// Data has to always be a json
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
	        delete window['cst_cache' + socket.remotePort.toString()]
	    });

	    // Don't forget to catch error, for your own sake.
	    socket.on('error', function(err) {
	        console.log('App server Error:', err);
	    });

	});

	// lizmenus_init()
	main_app_init()

	// TESTING
	// newmodmaker_loader()
	dashboard_app_loader()
	
});













/*
============================================================
------------------------------------------------------------
                          Sender
------------------------------------------------------------
============================================================
*/

// this sends commands to Blender's python
function apc_send(sendpayload)
{
	// it's impossible to have pre-defined ports
	// when blender server starts - a file with dynamically assigned port is generated
	// read its content and then send data to that port
	fetch('C:\\Users\\DrHax\\AppData\\Roaming\\Blender Foundation\\Blender\\3.1\\scripts\\addons\\blender_foil\\bdsmbind.sex', {
		'headers': {
			'accept': '*/*',
			'cache-control': 'no-cache',
			'pragma': 'no-cache'
		}
	})
	.then(function(response) {
		console.log(response.status);
		response.text().then(function(data) {
			window.gui_pot_connect = data.trim()


			var client = new net.Socket();
			client.connect(parseInt(window.gui_pot_connect), '127.0.0.1', function() {
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
			
		});
	});

}




















/*
============================================================
------------------------------------------------------------
                Base inits, like topbar menus
------------------------------------------------------------
============================================================
*/
function main_app_init()
{
	//
	// create Preferences menu in the top bar
	//
	create_lizmenu(
			'[apptoolbarctg="preferences"]',
			{
			'menu_name': 'Preferences',
			'menu_entries': [
				{
					'name': 'Toggle Heartbeat',
					'action': 'app_toggle_heartbeat',
					'icon': 'assets/heartbeat_icon.svg'
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

	//
	// create tools menu in the top bar
	//
	create_lizmenu(
		'[apptoolbarctg="tools"]',
		{
			'menu_name': 'Tools',
			'menu_entries': [
				{
					'name': 'Project Selector',
					'action': 'load_app_project_selector',
					'icon': 'assets/scene_icon.svg'
				},
				{
					'name': 'Mod Dashboard',
					'action': 'load_main_dashboard',
					'icon': 'assets/dashboard_icon.svg'
				},
/*				{
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
				},*/
				{
					'type': 'separator'
				},
				{
					'name': `Garry's Mod Tools`,
					'action': 'load_sound_manager_app',
					'icon': 'assets/gmod_icon.ico'
				},
				{
					'name': `Punchcard Generator`,
					'action': 'load_punchcard_generator',
					'icon': 'assets/punchcard_icon.svg'
				},
				{
					'name': `Library Maker`,
					'action': 'load_library_maker',
					'icon': 'assets/library_icon.svg'
				},
				{
					'type': 'separator'
				},
				{
					'name': 'Mod Maker',
					'action': 'load_newmodmaker',
					'icon': 'assets/mech_icon.svg'
				},
				{
					'name': 'Entity Definition File',
					'action': 'load_entity_definition_manager',
					'icon': 'assets/dna_icon.svg'
				}
			]
		}
	)


}


















