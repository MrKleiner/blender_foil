

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
			print('The dashboard module has been called, but no corresponding action was found:', pl['mod_action'])
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
	var cb_pool = lzcbox.pool
	cb_pool['fullscreen'].set(mcontext.fullscreen)
	cb_pool['intro_vid'].set(mcontext.intro_vid)
	cb_pool['loadtools'].set(mcontext.loadtools)
	cb_pool['maps_from_linked_gminfo'].set(mcontext.maps_from_linked_gminfo)
	cb_pool['start_from_map'].set(mcontext.start_from_map)
	cb_pool['use_add_options'].set(mcontext.add_start_opts)
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
	var cb_pool = lzcbox.pool;
	mcontext.fullscreen = cb_pool['fullscreen'].state
	mcontext.intro_vid = cb_pool['intro_vid'].state
	mcontext.loadtools = cb_pool['loadtools'].state
	mcontext.maps_from_linked_gminfo = cb_pool['maps_from_linked_gminfo'].state
	mcontext.start_from_map = cb_pool['start_from_map'].state
	mcontext.add_start_opts = cb_pool['use_add_options'].state
	mcontext.starting_map = $('#dboard_start_from_map_inp input').val().trim();
	// print(mcontext)
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
			print('Dashboard tried loading unknown module');
			break;
	}
}




// evaluates launch options and returns a cool object
function eval_launch_opts()
{
	var ev = {};
	var single_string = '';
	var separated = {};
	var cbpool = lzcbox.pool;

	// append parameters
	// todo: bro wtf we got rid of if statements, but it's still messy
	cbpool['fullscreen'].state ? (separated['windowed'] = []) : null
	cbpool['loadtools'].state ? (separated['tools'] = []) : null
	cbpool['intro_vid'].state ? (separated['novid'] = []) : null


	// if asked to start from a map AND the map name input is not empty - add map aprameter to the dictionary
	if (cbpool['start_from_map'].state && $('#dboard_start_from_map_inp input').val().trim() != ''){
		// todo why split ?
		// ev['map'] = $('#dboard_start_from_map_inp input').val().trim().split('/').at(-1)
		ev['map'] = $('#dboard_start_from_map_inp input').val().trim()
	}
	var parsed_opts = {};
	if (cbpool['use_add_options'].state && $('#dboard_mod_add_opts_input').val().trim() != '') {
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

	// delete duplicates ?
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
			'suggest_linked': lzcbox.pool['maps_from_linked_gminfo'].state
		}
	});

	print('got applicable maps:', maps);
	window.suggested_maps = maps;

}











