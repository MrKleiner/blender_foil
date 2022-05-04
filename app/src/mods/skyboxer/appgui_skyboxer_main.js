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
		console.log('skybox side b64 to img conversion status (has to be 200)', response.status);
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
	console.log('reset skyboxer scene');
	// painful do see it gone, but this has to be done
	delete window['skyboxer_sky_name'];
	for (var skside in side_def_dict){
		delete window['skyboxer_savedside_' + side_def_dict[skside]];
	}
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
	window['skyboxer_sky_name'] = skname['skyname'];
}

