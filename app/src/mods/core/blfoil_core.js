
// ============================================================
// ------------------------------------------------------------
//                   Core info and functions
// ------------------------------------------------------------
// ============================================================


// function getRowNum() {
//     let e = new Error();
//     e = e.stack.split("\n")[2].split(":");
//     e.pop();
//     return e.pop();
// }
// console.log(getRowNum())

// jQuery
window.$ = window.jQuery = require('./apis/jquery/3_6_0/jquery.min.js');

// remap print
// because we're gentlemen
window.paper_print = print

// important todo: also remap atob and btoa

// Electron's pathlib
// const path = require('path');

// Python-like pathlib
// todo: this import doesnt seem right
const Path = require('pathlib-js').default;

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

// various sys tools
window.foil = {}

// UDP await/resolve storage
// important to not: There could be a number of simultaneuos transfers. Do not delete this dict randomly
window.blresolve = {};

// quick base64 to json
function mkj(bd){
	return JSON.parse(u8atob(bd));
}

// app root
var got_root = new Path(__dirname)
while (true) {
    got_root = got_root.parent()
    if (got_root.basename == 'blender_foil'){
    	window.addon_root = got_root
        break
    }
}














// ============================================================
// ------------------------------------------------------------
//                             Logger
// ------------------------------------------------------------
// ============================================================

class fbi_logger
{
	// constructor(height, width) {
	constructor() {
		window.print = console.log.bind(window.console);
		window.log = this.module_log
		console.log('Initialized Fbi Logger');
	};


	//
	// ...arguments
	//

	// This is an extremely rare occasion of when blender wants to print something into the js console
	// and not in the debug console whatsoever
	blender_echo_status(pl){
		try {
			// console.log('%c Blender says:', 'background: rgba(0, 0, 0, 0); color: #EB9C4E; font-weigth: bold;', echo['payload']);
			console.log('%c Blender says:', 'background: rgba(0, 0, 0, 0); color: #AA551D; font-weight: bold;', pl['payload']);
			// console.log(echo['payload']);
		} catch (error) {

		}
	}

	// module: module name, if found in predef styles - style correspondingly. Else - wrap into []
	// log: an array of objects to log
	module_log(md=null, lg=''){
		// get pure list of stuff to actually log
		var clear_log = [...arguments].slice(1)

		var predef_styles = {
			'skyboxer': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#1F963B',
				'text': '[Skyboxer]'
			},
			'server': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#3852B2',
				'text': '[Server]'
			},
			'sender': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#C1186C',
				'text': '[Sender]'
			},
			'modmaker': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#6198CC',
				'text': '[Modmaker]'
			},
			'gameinfo': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#5F881E',
				'text': '[GameInfo]'
			},
			'dboard': {
				'bg': 'rgba(0, 0, 0, 0.0)',
				'fg': '#5C1EB8',
				'text': '[Dashboard]'
			}
		}

		// make the module name
		if (predef_styles.hasOwnProperty(md)){
			var module_name = `%c${predef_styles[md]['text']}`;
			var module_style = `background: ${predef_styles[md]['bg']}; color: ${predef_styles[md]['fg']}`;
		}else{
			var module_name = `[${md}]`;
			var module_style = '';
		}
		
		// absolute genius
		// return [module_name, module_style, ...clear_log]
		print(
			module_name,
			module_style,
			...clear_log
		)

	}

}
window.fbi = new fbi_logger();



























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



// ===================================================
//                     svg append
// ===================================================


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



// ===================================================
//                     Close/Exit app
// ===================================================

function blfoil_exit_app()
{
	window.close()
}












































// ============================================================
// ------------------------------------------------------------
//                   APP server listener
// ------------------------------------------------------------
// ============================================================




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
	    log('server', 'Initialized Server listening for connection requests on socket localhost:', port);

	});

	// When a client requests a connection with the server, the server creates a new
	// socket dedicated to that client.
	// A new session has been created, everything inside is in the context of that session
	server.on('connection', function(socket) {
		// console.groupCollapsed('Server Connection');
			log('server', 'Got connection to the following socket:', socket.remotePort.toString());
			// create cache storage
			window['blsocket_cache']['cst_cache' + socket.remotePort.toString()] = '';
		    log('server', 'Cache assigned to', 'cst_cache' + socket.remotePort.toString());
	    

	    // Now that a TCP connection has been established, the server can send data to
	    // the client by writing to its socket.
	    socket.write('Hello, client.');

	    // The server can also receive data from the client by reading from its socket.
	    // Client will be sending chunks of data DURING the session
	    // When data was received - write it down into storage
	    // todo: define storage as let ?
	    
	    socket.on('data', function(chunk) {
	        log('server', 'Data received from client:', {'len': chunk.length, 'data': chunk.toString()});
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
	    	log('server', 'Connection closed. Collected data:', {
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
					// foil_set_context(input_d)
					break;
				case 'echo_status':
					fbi.blender_echo_status(input_d)
					break;
				case 'dashboard':
					dashboard_module_manager(input_d)
					break;
				default:
					log('server', 'The transmission from another world has ended, but requested action is unknown:', input_d['app_module']);
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























// ============================================================
// ------------------------------------------------------------
//                              Talker
// ------------------------------------------------------------
// ============================================================



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

		// get port
		var port_bind = fs.readFileSync(window.addon_root.join('bdsmbind.sex').toString(), {encoding:'utf8', flag:'r'})
		log('sender', 'Read file containing bound port:', port_bind)
		// console.group('Sender Connection');

		window.gui_pot_connect = port_bind.trim()
		log('sender', 'Acquired (constant) port from fetch:', window.gui_pot_connect);

		var client = new net.Socket();
		client.connect(parseInt(window.gui_pot_connect), '127.0.0.1', function() {
			log('sender', 'Connected to Blender server, port:', client.localPort);
			// client.write('Hello, server! Love, Client.');

			// set resolve id
			topayload['sys_action_id'] = sys_id;
			client.write(JSON.stringify(topayload));
		});

		client.on('data', function(data) {
			log('sender', 'Receiving data during connection from port', client.localPort, ':' ,data.toString());
			client.destroy()
		});

		client.on('close', function() {
			log('sender', 'Closed connection with port', client.localPort);
			// console.groupEnd('Sender Connection');
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
		log('sender', 'Generated random id', action_id)

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























// ============================================================
// ------------------------------------------------------------
//                 Module loader
// ------------------------------------------------------------
// ============================================================


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
			print(`%cTrying to load module ${realname.replace('.html', '')} from tools/${realname}`, 'background: black; color: white',);
			$('#modules_cont').load('tools/' + realname, function() {
				// tooltips
				init_liztooltips();
				// important: checkboxes have to come AFTER tooltips
				// resync checkboxes
				lzcbox.resync();
				// append svg to html tree
				svgappender();
				// UILists init
				init_simple_ui_lists();

				// resync dropdowns
				lzdrops.red_check()


				// clear UDP cache
				// bltalk.clear_cache();

				window['current_app_module'] = realname.replace('.html', '');
				print('Loaded Module', window['current_app_module'], 'from', 'tools/' + realname, 'Base inits done');
				resolve(true);
			});
		}
	});
}


























// ============================================================
// ------------------------------------------------------------
//                 		Context
// ------------------------------------------------------------
// ============================================================




class foil_context_super_manager
{

	constructor() {
		window.foil.app_context = {};
		print('Initialized Context Manager');
	};

	// set OR get parameter
	prm(key=null, value=undefined, dosave=true){
		// if value is undefined, then it means that we're only getting a parameter
		if (value == undefined){
			return window.foil.app_context[key]
		}
		// if defined - set and maybe save
		window.foil.app_context[key] = value;
		if (dosave == true){
			this.save()
		}
	}

	// readonly shite
	get read(){
		// todo: there are better ways of duplicating shit
		var dupli = {}
		for (var k in window.foil.app_context){
			dupli[k] = window.foil.app_context[k]
		}
		return dupli
	}

	// save to disk
	async save(){
		// var bl_response = await bltalk.send({
		// 	'action': 'save_last_app_context',
		// 	'payload': window.foil.app_context
		// });
		var bl_response = await bltalk.send({
			'action': 'save_app_quick_config',
			'payload': {
				'project_index': window.foil.app_context.project_index,
				'quick_config': window.foil.app_context
			}
		});
		// because why not
		return bl_response
	}

	// switch projects
	async project_switch(pr_index=null){
		if (pr_index==null){return}
		// only switch on success
		var new_context = await this.load_index(pr_index)
		if (new_context['status'] == 'fail'){return}
		// do switch
		// set context
		window.foil.app_context = new_context
		// empty the container
		$('#modules_cont').empty()
		// and then simply load the dashboard app...
		dashboard_app_loader()
	}

	// get context of a certain index
	async load_index(idx){
		var got_context = await bltalk.send({
			'action': 'load_context_by_index',
			'payload': {
				'project_index': idx
			}
		});
		return got_context
	}

	// Get last used context
	async last_used(){
		var got_context = await bltalk.send({
			'action': 'load_context_by_index',
			'payload': {
				'project_index': idx
			}
		});
		return got_context
	}

	// Load last used context (in terms of actually loading it into the app)
	async load_last(){
		// important todo: manage all of this with native fs module
		var got_last_id = await bltalk.send({
			'action': 'load_last_app_context'
		});
		this.project_switch(got_last_id['project_index'])
	}


}
window.foil.context = new foil_context_super_manager();












// ============================================================
// ------------------------------------------------------------
//                 Base inits, like topbar menus
// ------------------------------------------------------------
// ============================================================

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
	window.foil.context.load_last()

}





