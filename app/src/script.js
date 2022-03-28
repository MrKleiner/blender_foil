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


/*
============================================================
------------------------------------------------------------
                          Listener
------------------------------------------------------------
============================================================
*/

window.cstorage = ''

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
	    console.log('A new connection has been established.');

	    // Now that a TCP connection has been established, the server can send data to
	    // the client by writing to its socket.
	    socket.write('Hello, client.');

	    // The server can also receive data from the client by reading from its socket.
	    // Client will be sending chunks of data DURING the session
	    // When data was received - write it down into storage
	    // todo: define storage as let ?
	    let cst = ''
	    socket.on('data', function(chunk) {
	        console.log('Data received from client:', chunk.toString());
	        // window.cstorage += chunk.toString()
	        cst += chunk.toString()
	    });

	    // When the client requests to end the TCP connection with the server, the server
	    // ends the connection.
	    // End means that presumably, all chunks of data have been sent by now
	    socket.on('end', function() {
	    	// console.log('Total:', window.cstorage)
	    	console.log('Total:', cst)
	    	console.log('Closing connection with the client');

	    	// Data should always be a json
	    	// input_d = JSON.parse(window.cstorage)
	    	input_d = JSON.parse(cst)


	    	//
	    	// Decide what to do
	    	//
			switch (input_d['app_module']) {
				case 'skyboxer':
					skyboxer_module_manager(input_d)
					break;
				default:
					console.log('The transmission from the other world has ended, but requested action is unknown')
					break;
			}



			// flush the storage
	        // window.cstorage = ''
	        let cst = ''
	    });


	    // Don't forget to catch error, for your own sake.
	    socket.on('error', function(err) {
	        console.log('Error:', err);
	    });


	});


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
                          Sender
------------------------------------------------------------
============================================================
*/

function apc_send()
{
	var client = new net.Socket();
	client.connect(50000, '127.0.0.1', function() {
		console.log('Connected');
		client.write('Hello, server! Love, Client.');
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
		default:
			console.log('The module has been called, but no corresponding action was found')
			break;
	}



}




// takes two params:
// side_img - image binary
// side_d - string. Side, like "left"
function skyboxer_sides_filler(side_img, side_d)
{
	side_def_dict = {
        'bk': 'back',
        'dn': 'down',
        'ft': 'front',
        'lf': 'left',
        'rt': 'right',
        'up': 'up'
    }

	$('#sky_' + side_def_dict[side_d] + ' .skybox_square')[0].src = 'data:image/png;base64,' + side_img;
	// $('#sky_' + side_def_dict[side_d])[0].src = '';
	// $('#sky_' + side_def_dict[side_d])[0].src = side_img + '?' + new Date().getTime();
}





















































