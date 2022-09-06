foil.sys.dashboard = {};
fsys.dashboard.main = {};

// =====================================================================
// ---------------------------------------------------------------------
//                              module name: dashboard
// ---------------------------------------------------------------------
// =====================================================================



foil.sys.dashboard.manager = function(pl)
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


fsys.dashboard.app_loader = function()
{
	// if (window.foil_context.full.project_index != undefined || window.foil_context.full.project_index != null)
	// {
		base_module_loader('main_dashboard.html')
		.then(function(resolved) {
			window.sample_huge_array = JSON.parse(fs.readFileSync((new Path(__dirname)).join('assets', 'sizetest.txt').toString(), {encoding:'utf8', flag:'r'}))
			log('dboard', 'loaded test example UIList content placeholder for dashbaord maps UIList');

			// load the rest of the info
			fsys.dashboard.main.absorb_context()

			// get applicable maps
			fsys.dashboard.main.list_maps()

		});
	// }
}

// set control panel shit from existing context
// context should never lie
fsys.dashboard.main.absorb_context = function()
{
	var mcontext = foil.context.read;
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
	$('#dboard_mod_preview_lauchprms').text(fsys.dashboard.main.eval_launch_opts()['string'])
	$('#dboard_start_from_map_inp input').val(mcontext.starting_map);
}

// collect data from control panel and save it to context
fsys.dashboard.main.save = function()
{
	log('dboard', 'Evaluated launch options: ', fsys.dashboard.main.eval_launch_opts());
	$('#dboard_mod_preview_lauchprms').text(fsys.dashboard.main.eval_launch_opts()['string']);

	// save context
	var mcontext = foil.context.read;
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
	foil.context.save()

}


// load a tool from the list from the left
// takes either an element or a string
fsys.dashboard.main.load_tool = function(tool='none')
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
fsys.dashboard.main.eval_launch_opts = function()
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


// launch the game
fsys.dashboard.main.launch_mod = function()
{
	bltalk.send({
		'action': 'dboard_launch_mod',
		'payload': {
			'engine': foil.context.prm('engine_executable'),
			'params': eval_launch_opts()['string'].split(' '),
			'map': eval_launch_opts()['map'],
			'client_name': foil.context.read.client_folder_path
		}
	});
}

// kill the game
fsys.dashboard.main.kill_mod = function()
{
	bltalk.send({
		'action': 'dboard_kill_mod',
		'payload': {
			'engine': foil.context.prm('engine_executable'),
			'params': eval_launch_opts()['string'].split(' '),
			'client_name': foil.context.prm('client_folder_path')
		}
	});
}







// ask Blender for applicable maps
fsys.dashboard.main.list_maps = async function()
{
	log('dboard', 'Called for applicable maps')
	// suggested_maps
	var maps = await bltalk.send({
		'action': 'dboard_get_suggested_maps',
		'payload': {
			'gminfo_path': foil.context.read.gameinfo_path,
			'suggest_linked': lzcbox.pool['maps_from_linked_gminfo'].state
		}
	});

	print('got applicable maps:', maps);
	window.suggested_maps = maps;

}











print('reached dashboard file end')