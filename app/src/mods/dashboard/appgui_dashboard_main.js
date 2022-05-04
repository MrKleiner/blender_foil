
/*
=====================================================================
---------------------------------------------------------------------
                             Dashboard
---------------------------------------------------------------------
=====================================================================
*/


function dashboard_module_manager(pl)
{

	switch (pl['mod_action']) {
		case 'append_pre_installed':
			newmodmaker_accept_engines(pl['payload'])
			break;
		default:
			console.log('The dashboard module has been called, but no corresponding action was found')
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
	base_module_loader('main_dashboard.html')
	.then(function(resolved) {
		fetch('assets/sizetest.txt', {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			}
		})
		.then(function(response) {
			console.log(response.status, 'loaded test example UIList content placeholder for dashbaord maps UIList');
			response.text().then(function(data) {
				window.suggested_maps = JSON.parse(data)
			});
		});
	});
}