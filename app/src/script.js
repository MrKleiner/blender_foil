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


$(document).ready(function(){
	// Include Nodejs' net module.
	// const Net = require('net');
	// The port on which the server is listening.
	const port = 1337;

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
	server.on('connection', function(socket) {
	    console.log('A new connection has been established.');

	    // Now that a TCP connection has been established, the server can send data to
	    // the client by writing to its socket.
	    socket.write('Hello, client.');

	    // The server can also receive data from the client by reading from its socket.
	    socket.on('data', function(chunk) {
	        console.log('Data received from client:', chunk.toString());
	    });

	    // When the client requests to end the TCP connection with the server, the server
	    // ends the connection.
	    socket.on('end', function() {
	        console.log('Closing connection with the client');
	    });

	    // Don't forget to catch error, for your own sake.
	    socket.on('error', function(err) {
	        console.log('Error:', err);
	    });
	});

});


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


// takes two params:
// side_img - image binary
// side_d - string. Side, like "left"
function skyboxer_sides_filler(side_img, side_d)
{
	$('#sky_' + side_d)[0].src = side_img;
}





















































