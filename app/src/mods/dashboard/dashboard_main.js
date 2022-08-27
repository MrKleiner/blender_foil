

// =====================================================================
// ---------------------------------------------------------------------
//                              module name: dashboard
// ---------------------------------------------------------------------
// =====================================================================



function dashboard_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'dboard_set_applicable_maps':
			break;
		default:
			console.log('The dashboard module has been called, but no corresponding action was found:', pl['mod_action'])
			break;
	}

}

// soundscape manager
// soundscript manager
// vtf maker
// skyboxer
// substance painter connect
// chapter manager (with backgrounds)
// particle manifest generator
// gameinfo editor
// Pack mod as sourcemod/executable/zip
// hammer++ manager
// compilers switch
// propdata manager both predefined and prop-specific
// vehicle scripts maker
// actbusy script maker
// actremap script maker
// decal maker
// speech system script maker
// soundmixer script maker
// weapon script maker
// surfaceproperties manager


function dashboard_app_loader()
{
	if (window.foil_context.full.project_index != undefined || window.foil_context.full.project_index != null)
	{
		base_module_loader('main_dashboard.html')
		.then(function(resolved) {
			window.sample_huge_array = JSON.parse(fs.readFileSync((new Path(__dirname)).join('assets', 'sizetest.txt').toString(), {encoding:'utf8', flag:'r'}))
			log('dboard', 'loaded test example UIList content placeholder for dashbaord maps UIList');

			// load the rest of the info
			dashboard_set_ctrl_panel_from_context()

			// get applicable maps
			dboard_call_applicable_maps()

		});
	}

}

// set control panel shit from existing context
// context should never lie
function dashboard_set_ctrl_panel_from_context()
{
	var mcontext = window.foil_context.full;
	$('#dboard_mod_minititle').text(mcontext.full_game_name);
	$('#dboard_mod_modfolderpath').text(mcontext.client_folder_path);
	$('#dboard_mod_add_opts_input').text(mcontext.dboard_mod_add_opts_input)
	// checkboxes
	lizcbox_stat('fullscreen', mcontext.fullscreen)
	lizcbox_stat('intro_vid', mcontext.intro_vid)
	lizcbox_stat('loadtools', mcontext.loadtools)
	lizcbox_stat('maps_from_linked_gminfo', mcontext.maps_from_linked_gminfo)
	lizcbox_stat('start_from_map', mcontext.start_from_map)
	lizcbox_stat('use_add_options', mcontext.add_start_opts)
	$('#dboard_mod_preview_lauchprms').text(eval_launch_opts()['string'])
	$('#dboard_start_from_map_inp input').val(mcontext.starting_map);
}

// update the control panel when something has changed, like checkbox or smth
// and also context
function dboard_update_panel_vis()
{
	log('dboard', 'Evaluated launch options: ', eval_launch_opts());
	$('#dboard_mod_preview_lauchprms').text(eval_launch_opts()['string']);

	// save context
	var mcontext = window.foil_context.full;
	mcontext.fullscreen = lizcbox_stat('fullscreen')
	mcontext.intro_vid = lizcbox_stat('intro_vid')
	mcontext.loadtools = lizcbox_stat('loadtools')
	mcontext.maps_from_linked_gminfo = lizcbox_stat('maps_from_linked_gminfo')
	mcontext.start_from_map = lizcbox_stat('start_from_map')
	mcontext.add_start_opts = lizcbox_stat('use_add_options')
	mcontext.starting_map = $('#dboard_start_from_map_inp input').val().trim();

	// also save quick config
	foil_save_quick_config()

}


// takes either an element or a string
function dashboard_tool_loader(tool='none')
{
	// downside of auto-system: tool.getAttribute('dboardload') 
	// :(
	if (tool == undefined || tool == null){return}
	// if (tool.nodeType != 1 && !(tool instanceof String)){return}
	var sw = 'nil';
	if (tool.nodeType == 1){
		var sw = tool.getAttribute('dboardload');
	}

	switch (sw) {
		case 'skyboxer':
			skyboxer_module_loader()
			break;
		case 'gameinfo':
			gameinfoman_app_loader()
			break;
		default:
			console.log('Dashboard tried loading unknown module');
			break;
	}
}




// evaluates launch options and returns a cool object
function eval_launch_opts()
{
	var ev = {};
	var single_string = '';
	var separated = {};
	var cbpool = lizcboxes.pool;
	if (!cbpool['fullscreen']) { separated['windowed'] = [] }
	if (cbpool['loadtools']) { separated['tools'] = [] }
	if (!cbpool['intro_vid']) { separated['novid'] = [] }
	// if (cbpool['start_from_map'] && $('#dboard_start_from_map_inp').find('input').val().trim() != '') { separated['map'] = [$('#dboard_start_from_map_inp').find('input').val().trim()] }
	if (cbpool['start_from_map'] && $('#dboard_start_from_map_inp').find('input').val().trim() != '') { ev['map'] = $('#dboard_start_from_map_inp').find('input').val().trim().split('/').at(-1) }
	var parsed_opts = {};
	if (cbpool['use_add_options'] && $('#dboard_mod_add_opts_input').val().trim() != '') {
		var prepare_opts = $('#dboard_mod_add_opts_input').val().split(' ');
		var lastprm = '';
		for (var po in prepare_opts){
			if (prepare_opts[po].includes('-')){
				var lastprm = prepare_opts[po];
				parsed_opts[lastprm.replace('-', '')] = [];
			}else{
				parsed_opts[lastprm.replace('-', '')].push(prepare_opts[po].replace('-', ''));
			}
		}
	}

	ev['full'] = Object.assign({}, separated, parsed_opts);
	ev['base'] = separated;
	ev['add'] = parsed_opts;
	// create string
	ev['string'] = '';
	for (var opt in ev['full']){
		if (ev['full'][opt].length != 0){
			ev['string'] += ' -' + opt + ' ' + ev['full'][opt].join(' ');
		}else{
			ev['string'] += ' -' + opt;
		}
	}
	ev['string'] = ev['string'].trim();
	// console.log(cbpool)
	return ev

}


function dboard_launch_mod()
{
	bltalk.send({
		'action': 'dboard_launch_mod',
		'payload': {
			'engine': window.foil_context.full.engine_executable,
			'params': eval_launch_opts()['string'].split(' '),
			'map': eval_launch_opts()['map'],
			'client_name': window.foil_context.full.client_folder_path
		}
	});
}

function dboard_kill_mod()
{
	bltalk.send({
		'action': 'dboard_kill_mod',
		'payload': {
			'engine': window.foil_context.full.engine_executable,
			'params': eval_launch_opts()['string'].split(' '),
			'client_name': window.foil_context.full.client_folder_path
		}
	});
}





// save quick config from control panel
function foil_save_quick_config()
{
	bltalk.send({
		'action': 'save_app_quick_config',
		'payload': {
			'project_index': window.foil_context.full.project_index,
			'quick_config': window.foil_context.full
		}
	});
}



// ask Blender for applicable maps
async function dboard_call_applicable_maps()
{
	log('dboard', 'Called for applicable maps')
	// suggested_maps
	var maps = await bltalk.send({
		'action': 'dboard_get_suggested_maps',
		'payload': {
			'gminfo_path': window.foil_context.full.gameinfo_path,
			'suggest_linked': lizcbox_stat('maps_from_linked_gminfo')
		}
	});

	console.log('got applicable maps:', maps);
	window.suggested_maps = maps;

}











