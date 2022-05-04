








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


























































































