/*
============================================================
------------------------------------------------------------
                   Core info and functions
------------------------------------------------------------
============================================================
*/

// jQuery
window.$ = window.jQuery = require('./apis/jquery/3_6_0/jquery.min.js');

// Electron's pathlib
const path = require('path');

// Electron File System Access
const fs = require('fs');

// Electron UDP Module
const net = require('net');

//
// Obsolete Python Shell
//
/*
const {PythonShell} = require('python-shell');
const zpypath = 'C:/Program Files (x86)/Steam/steamapps/common/Blender/3.1/python/bin/python.exe';
window.py_common_opts = {
		mode: 'text',
		pythonPath: zpypath,
		pythonOptions: ['-u'],
		scriptPath: path.join(__dirname, '/app/')
	  };
function shell_end_c(err,code,signal)
{
	if (err) throw err;
	console.log('The exit code was: ' + code);
	console.log('The exit signal was: ' + signal);
	console.log('finished');
}
*/

// console.log(__dirname)

// Unknown
window.lizards_mouth = 'lizards_tongue';

// Current APP context
window.foil_context = {};

// UDP cache
window.blsocket_cache = {};

// Timeout for resolving ID
// by default - 30 seconds timeout
window.blwait_timeout = 1000*30;

// UDP await/resolve storage
window.blresolve = {};

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

// takes raw base64 string and converts it to imageurl
function b64toimg(b64)
{
	var bytes = lizard.base64DecToArr(b64)
	var blob = new Blob([bytes], {type: 'image/*'});
	var imageUrl = (window.URL || window.webkitURL).createObjectURL(blob);
	return imageUrl
}









// ===================================================
//             reload app (f5 implementation)
// ===================================================

// keybind: ctrl+r

// todo: this doubles the keydown event binds
document.addEventListener('keydown', kvt => {
    // console.log('keypress');
    app_reload_refresh(kvt)
    // todo: this really is a core feature...
    if (kvt.altKey && kvt.keyCode == 87 && window.current_app_module != 'main_dashboard'){
    	dashboard_app_loader()
    }
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
// important todo: this can be done synchronously with electron file manager
function svgappender()
{
	// console.group('Svg Append');
	// var ctable = []
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
			// console.log(response.status);
			response.text().then(function(data) {
				$(userItem).replaceWith(data);
			});
		});
		// userItem.parentNode.replaceChild(newItem, listItem);
	});
	console.log('Svg Appender No Errors');
	
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
===================================================
                    Close/Exit app
===================================================
*/
function blfoil_exit_app()
{
	window.close()
}







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
	// important todo: 
	const port = 1337;

	// Use net.createServer() in your code. This is just for illustration purpose.
	// Create a new TCP server.
	const server = new net.Server();
	// The server listens to a socket for a client to make a connection request.
	// Think of a socket as an end point.
	server.listen(port, function() {
	    console.info('Initialized Server listening for connection requests on socket localhost:', port);

	});

	// When a client requests a connection with the server, the server creates a new
	// socket dedicated to that client.
	// A new session has been created, everything inside is in the context of that session
	server.on('connection', function(socket) {
		// console.groupCollapsed('Server Connection');
			console.log('Got connection to the following socket:', socket.remotePort.toString());
			// create cache storage
			window['blsocket_cache']['cst_cache' + socket.remotePort.toString()] = '';
		    console.log('Cache assigned to', window['blsocket_cache']['cst_cache' + socket.remotePort.toString()]);
	    

	    // Now that a TCP connection has been established, the server can send data to
	    // the client by writing to its socket.
	    socket.write('Hello, client.');

	    // The server can also receive data from the client by reading from its socket.
	    // Client will be sending chunks of data DURING the session
	    // When data was received - write it down into storage
	    // todo: define storage as let ?
	    
	    socket.on('data', function(chunk) {
	        console.log('Data received from client:', {'len': chunk.length, 'data': chunk.toString()});
	        // window.cstorage += chunk.toString()
	        // cst += chunk.toString()
	        window['blsocket_cache']['cst_cache' + socket.remotePort.toString()] += chunk.toString()
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
	    	console.log('Connection closed. Collected data:', {
		    		'len': window['blsocket_cache']['cst_cache' + socket.remotePort.toString()].length,
		    		'data': window['blsocket_cache']['cst_cache' + socket.remotePort.toString()]
	    		}
	    	);

	    	// Data has to always be a json
	    	input_d = JSON.parse(window['blsocket_cache']['cst_cache' + socket.remotePort.toString()])

	    	// connection is closed now
	    	// console.groupEnd('Server Connection');

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
				case 'gameinfo':
					gameinfo_module_manager(input_d)
					break;
				case 'set_context':
					foil_set_context(input_d)
					break;
				case 'echo_status':
					blender_echo_status(input_d)
					break;
				case 'dashboard':
					dashboard_module_manager(input_d)
					break;
				default:
					console.log('The transmission from another world has ended, but requested action is unknown:', input_d['app_module']);
					break;
			}

			// resolve shit
			bltalk.resolveid(input_d['sys_action_id'], input_d['payload'])

			// flush the storage
			// todo: do this before switch ?
			// important: there could be a number of ongoing connections
			// only delete corresponding cache storage
			// flush buffers later
	        delete window.blsocket_cache['cst_cache' + socket.remotePort.toString()]
	        // window.blsocket_cache = {}
	        
	    });

	    // Don't forget to catch error, for your own sake.
	    socket.on('error', function(err) {
	        console.error('JS Server Error:', err);
	    });

	});

	// lizmenus_init()
	main_app_init()

	// TESTING
	// newmodmaker_loader()
	// dashboard_app_loader()
	// gameinfoman_app_loader()

	
});






















/*
============================================================
------------------------------------------------------------
                             Talker
------------------------------------------------------------
============================================================
*/


class blender_talker
{
	// constructor(height, width) {
	constructor() {
		console.log('Initialized Blender Talker')
	};

	// get info() {
	// 	return `Lizard's toybox. Version 0.32`
	// };




	/*
	============================================================
	------------------------------------------------------------
	                          Sender
	------------------------------------------------------------
	============================================================
	*/

	// this sends commands to Blender's python
	// basically, .send is just a nice word and a wrapper
	// + it's way easier to understand what's happening when it's split into functions
	exec_send(sendpayload, sys_id='default')
	{
		// a payload has to always have a payload, even if it's empty
		if (sendpayload.hasOwnProperty('payload')){
			var topayload = sendpayload;
		}else{
			var topayload = sendpayload;
			topayload['payload'] = '';
		}

		// it's impossible to have pre-defined ports
		// when blender server starts - a file with dynamically assigned port is generated
		// read its content and THEN send data to that port
		// important todo: simply try to pass location on app load ?
		// important todo: fetch is only a temp workaround, use native file reader
		fetch('C:\\Users\\DrHax\\AppData\\Roaming\\Blender Foundation\\Blender\\3.1\\scripts\\addons\\blender_foil\\bdsmbind.sex', {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			}
		})
		.then(function(response) {
			// console.group('Sender Connection');
			console.log('[Sender] Requested port on which Blender server is running. Fetch response status:', response.status, '(Has to be 200)');
			response.text().then(function(data) {
				window.gui_pot_connect = data.trim()
				console.log('[Sender] Acquired (constant) port from fetch:', window.gui_pot_connect);

				var client = new net.Socket();
				client.connect(parseInt(window.gui_pot_connect), '127.0.0.1', function() {
					console.log('[Sender] Connected to Blender server, port:', client.localPort);
					// client.write('Hello, server! Love, Client.');

					// set resolve id
					topayload['sys_action_id'] = sys_id;
					client.write(JSON.stringify(topayload));
				});

				client.on('data', function(data) {
					console.log('[Sender] Receiving data during connection from port', client.localPort, ':' ,data.toString());
					client.destroy()
				});

				client.on('close', function() {
					console.log('[Sender] Closed connection with port', client.localPort);
					// console.groupEnd('Sender Connection');
				});
				
			});
		});
	}


	// Why send and not get or talk ?
	// 1 - Because Fuck You
	// 2 - It actually makes sense: you're sending shit and it's your choice whether to await for the response or not
	send(pl){
		// generate resolve id reference
		// All New Sexy Feature!
		// every command now has an id attached which is being tossed back and forth
		// This makes it possible to have await/.then just like with fetch
		// basically blender talk is just like fetch now
		var action_id = CryptoJS.SHA256(lizard.rndwave(512, 'flac')).toString();
		console.log('[Sender] Generated random id', action_id)

		// todo: wat
		var remap_this = this;

		return new Promise(function(resolve, reject){
			// set resolve reference
			window.blresolve[action_id] = resolve
			remap_this.exec_send(pl, action_id)
		});
	}



	// resolve certain id
	resolveid(id, pl={}){
		try {
			console.log('Resolving UDP await', id)
			// resolve promise
			window.blresolve[id](pl)
			// delete promise from the storage
			delete window.blresolve[id]
		} catch (error) {
			console.log('Tried To Resolve non-existent id:', id)
		}
	}


	// clear cache
	clear_cache(){
		window.blsocket_cache = {};
	}


}
window.bltalk = new blender_talker();






























/*
============================================================
------------------------------------------------------------
                Module loader
------------------------------------------------------------
============================================================
*/

function base_module_loader(mdl, force=true)
{

	// todo: better logic
	var realname = mdl;
	if (!mdl.endsWith('.html')){
		var realname = mdl + '.html';
	}

	return new Promise(function(resolve, reject){

		// do not load module if it's already active
		if (force != true && realname.replace('.html', '') == window['current_app_module']){
			resolve(true);
		}else{
			// $('#modules_cont').empty();
			// todo: why use jquery ...
			console.log('Trying to load module', realname.replace('.html', ''), 'from', 'tools/' + realname);
			$('#modules_cont').load('tools/' + realname, function() {
				// checkboxes
				lizcboxes_init();
				// tooltips
				init_liztooltips();
				// append svg to html tree
				svgappender();
				// UILists init
				init_simple_ui_lists();

				// clear UDP cache
				// bltalk.clear_cache();

				window['current_app_module'] = realname.replace('.html', '');
				console.log('Loaded Module', window['current_app_module'], 'from', 'tools/' + realname, 'Base inits done');
				resolve(true);
			});
		}
	});
}










/*
============================================================
------------------------------------------------------------
                		Status echo
------------------------------------------------------------
============================================================
*/


function blender_echo_status(echo)
{
	try {
		// console.log('%c Blender says:', 'background: rgba(0, 0, 0, 0); color: #EB9C4E; font-weigth: bold;', echo['payload']);
		console.log('%c Blender says:', 'background: rgba(0, 0, 0, 0); color: #AA551D; font-weight: bold;', echo['payload']);
		// console.log(echo['payload']);
	} catch (error) {

	}
}



















/*
============================================================
------------------------------------------------------------
                		Context
------------------------------------------------------------
============================================================
*/


// This is only useful on startup (reload)
function foil_call_last_context()
{
	console.log('Asked Blender to give last used context');
	bltalk.send({
		'action': 'load_last_app_context',
		'payload': {
			'last_used': true
		}
	});
}

// this kinda belongs to the dashboard module, but really, it'd better be here
// expects a quick config payload and will set context from it
// when the context is being overwritten - the dashboard module always has to be loaded
function foil_set_context(ct)
{
	console.log('Startup last context response from Blender:', ct['payload']);
	var things = ct['payload'];

	if (things != false){
		// set index
		// window.foil_context['mod_context'] = things['project_index'];
		// set useless meta name
		// window.foil_context['mod_meta_name'] = things['project_name'];
		// dump everything because why not
		window.foil_context['full'] = things;

		console.log('App context set:', {'Index Id': things['project_index'], 'Project Name': things['project_name']})

		dashboard_app_loader()
	}

}


// save full context of the last opened project
function foil_save_last_context(ct)
{
	bltalk.send({
		'action': 'save_last_app_context',
		'payload': ct
	});
}


// save all contexts
// todo: safety measures
function foil_save_context(last=false)
{
	// save last
	if (last == true)
	{
		bltalk.send({
			'action': 'save_last_app_context',
			'payload': window.foil_context.full
		});
	}

	// save fast config
	// additive, will add to quick config
	bltalk.send({
		'action': 'save_app_quick_config',
		'payload': {
			'project_index': window.foil_context.full.project_index,
			'quick_config': window.foil_context.full
		}
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
					'name': `BINK Rubbish`,
					'action': 'load_bink_videomaker',
					'icon': 'assets/bink_logo_tr_empty.png'
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


	//
	// Set context
	//
	foil_call_last_context()

}

















