foil.sys.skyboxer = {};






fsys.skyboxer.manager = function(pl)
{
	var skyboxer = fsys.skyboxer.main

	switch (pl['mod_action']) {
		case 'add_skybox_side':
			skyboxer.sides_filler(pl['image'], pl['side'], pl['pov_img'])
			break;
		case 'upd_side_status':
			skyboxer.update_status(pl['side'], pl['what'], pl['status'])
			break;
		case 'reset':
			skyboxer.reset_scene()
			break;
		case 'upd_work_status':
			skyboxer.update_status(pl)
			break;
		case 'set_sky_name':
			skyboxer.header_text(pl)
			break;
		case 'finished':
			skyboxer.sky_finished(pl)
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
var side_status_def = {
	'blender': '.blender_icon .icon_indicator_circle',
	'pfm': '.pfm_icon .icon_indicator_circle',
	'vtf': '.vtf_icon .icon_indicator_circle',
}

// double loading causes issues which ould be easily avoided by NOT performing double loads
fsys.skyboxer.app_loader = function()
{
	base_module_loader('skyboxer', false)
	.then(function(resolved) {
		// load previously loaded sky sides and name, if any
		console.log('skyboxer load existing sides');
		if (window['skyboxer_sky_name'] != undefined){
			$('#sky_name').text(window['skyboxer_sky_name']);
		}
		for (var skside in side_def_dict){
			if (window['skyboxer_savedside_' + side_def_dict[skside]] != undefined){
				$('#sky_' + side_def_dict[skside] + ' .skybox_square').attr('src', window['skyboxer_savedside_' + side_def_dict[skside]]);
			}
		}
	});
}





// takes two params:
// side_img - image binary
// side_d - string. Side, like "left"
fsys.skyboxer.main.sides_filler = function(side_img, side_d, pov)
{
	var mk_side_img = lizard.b64toimg(side_img)
	var mk_side_img_pov = lizard.b64toimg(pov)
	$('#sky_' + side_def_dict[side_d] + ' .skybox_square').attr('src', mk_side_img);
	window['skyboxer_savedside_' + side_def_dict[side_d]] = mk_side_img;
	window['skyboxer_savedside_pov' + side_def_dict[side_d]] = mk_side_img_pov;
}

// set status
fsys.skyboxer.main.update_status = function(wside, elem, status)
{
	var decide_status = 'lime'
	if (status == false){
		var decide_status = 'red'
	}
	$('#sky_' + side_def_dict[wside]).find(side_status_def[elem]).css('background', decide_status);
}

// resets scene and wipes sides cache
fsys.skyboxer.main.reset_scene = function()
{
	console.log('reset skyboxer scene');
	// painful do see it gone, but this has to be done
	delete window['skyboxer_sky_name'];
	for (var skside in side_def_dict){
		delete window['skyboxer_savedside_' + side_def_dict[skside]];
	}
	$('.icon_indicator_circle').css('background', 'red');
	$('.skybox_side_container .skybox_square').attr('src', 'assets/cross_square.png');
}

// updates status with given text
fsys.skyboxer.main.update_status = function(stat)
{
	$('#sky_compile_status').text(stat['status']);
}

// there's a big header on top...
// this takes given text and puts it into that header
fsys.skyboxer.main.header_text = function(skname)
{
	$('#sky_name').text(skname['skyname']);
	window['skyboxer_sky_name'] = skname['skyname'];
}

// trigger this when all the regular and POV sides were loaded
fsys.skyboxer.main.sky_finished = function(pl)
{
	try{
		window.skyboxer_pov.destroy()
	}catch(error){}

	window.skyboxer_pov = pannellum.viewer('skyboxer_preview_pov', {
		'type': 'cubemap',
		'cubeMap': [
			window['skyboxer_savedside_povfront'],
			window['skyboxer_savedside_povleft'],
			window['skyboxer_savedside_povback'],
			window['skyboxer_savedside_povright'],
			window['skyboxer_savedside_povup'],
			window['skyboxer_savedside_povdown']
		],
		'autoLoad': true,
		'showFullscreenCtrl': false,
		'showControls': false
	});

}


fsys.skyboxer.main.list_skies = async function()
{
	console.time('all skies')
	var inf = await bltalk.send({
		'action': 'skyboxer_get_all_skyboxes',
		'payload': {
			'gameinfo': foil.context.read.gameinfo_path
		}
	});
	print(inf)

	// load skies one by one
	for (var ldsky of inf){
		var sex = await bltalk.send({
			'action': 'skyboxer_get_sky_as_bitmap',
			'payload': {
				'skyinfo': ldsky
			}
		});

		$('#skyboxes_loaded_bitmaps').append(`
			<div class="zatychka">
			<div class="skyboxer_squares_inner">

				<!-- Row 1: Up -->
				<div class="skybox_sq_row_1" class="skybox_sq_row">
					<div class="sky_up" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['up_ldr'])}" class="skybox_square"></img>
					</div>
				</div>

				<!-- Row 2: Front Left Back Right -->
				<!-- todo: populate info squares on load. basically, create all of this on load... -->
				<div class="skybox_sq_row_2" class="skybox_sq_row">

					<div class="sky_front" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['ft_ldr'])}" class="skybox_square"></img>
					</div>

					<div class="sky_left" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['lf_ldr'])}" class="skybox_square"></img>
					</div>

					<div class="sky_back" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['bk_ldr'])}" class="skybox_square"></img>
					</div>

					<div class="sky_right" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['rt_ldr'])}" class="skybox_square"></img>
					</div>

				</div>


				<!-- Row 3: Down -->
				<div class="skybox_sq_row_3" class="skybox_sq_row">
					<div class="sky_down" class="skybox_side_container">
						<img draggable="false" src="${lizard.b64toimg(sex['dn_ldr'] || '')}" class="skybox_square"></img>
					</div>
				</div>


			</div>
			</div>
		`)


	}

	console.timeEnd('all skies')


}


function SUPER_IMPORTANT_SHITE()
{
	// https://github.com/katspaugh/wavesurfer.js
	// https://wavesurfer-js.org/
	// https://wavesurfer-js.org/api/class/src/wavesurfer.js~WaveSurfer.html
	// https://wavesurfer-js.org/plugins/regions.html
	// https://github.com/rochars/wavefile#read-wave-files


	var fi = "E:\\Gamess\\steamapps\\common\\Half-Life 2\\ep2\\sound\\banjo\\banjo_loop_03a_44100.wav"
	console.time('fuck')
	const WaveFile = require('wavefile').WaveFile;

	var sex = new WaveFile(fs.readFileSync(fi));
	wvinfo = sex.listCuePoints()[0]
	console.log(wvinfo)
	$('#modules_cont').empty()
	$('#modules_cont').append(`
	    <div id="wtfwhy" style="width: 600px; height: 200px; background: black;"></div>
	`)
	var wavesurfer = WaveSurfer.create({
	    container: '#wtfwhy',
	    waveColor: 'violet',
	    progressColor: 'purple',
	    plugins: [
	        WaveSurfer.regions.create({})
	    ]
	});

	wavesurfer.load(fi);

	wavesurfer.on('ready', function () {
	    wavesurfer.addRegion({
	        start: wvinfo.position / 1000,
	        end: wavesurfer.getDuration(),
	        loop: true,
	        drag: false,
	        resize: false
	    })
	    wavesurfer.play();
	    console.timeEnd('fuck')
	});

}