/*
============================================================
------------------------------------------------------------
                    Simple menus
------------------------------------------------------------
============================================================
*/

/*
function lizmenus_init()
{

	document.querySelectorAll('[lizmenu_initid]').forEach(function(userItem) {
		// console.log(userItem)

		var tgt_menu = userItem
		console.log(userItem);
		tgt_menu.style.marginTop = (userItem.parentElement.offsetHeight).toString() + 'px'
		tgt_menu.style.marginLeft = (-1 * parseInt(window.getComputedStyle(userItem.parentElement, null).getPropertyValue('padding-left').replace('px', ''))).toString() + 'px'
	});

}
*/





/*
 -----------------------
	      Maker
 -----------------------
*/

// takes selector string and items dict as an input
// dict is as follows:
/*
{
	'menu_name': 'Pootis',
	'menu_entries': [
		{
			'name': 'Skyboxer',
			'action': 'load_skyboxer_app',
			'icon': 'link/to/icon.png OR svg code',
			'icon_mode': 'bitmap OR svg'
		},
		{
			'name': 'Skyboxer',
			'action': 'load_skyboxer_app',
			'icon': 'link/to/icon.png OR svg code',
			'icon_mode': 'bitmap OR svg'
		}
	]
}
*/
// Example result:
/*
<div class="lizard_menu">
	<div class="lizmenu_title">Preferences</div>
	<div class="lizard_menu_entries">
		<div class="lizard_menu_entry">
			<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
			<div class="lizard_menu_entry_text">Entry</div>
		</div>
		<div class="lizard_menu_entry">
			<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
			<div class="lizard_menu_entry_text">Entry</div>
		</div>
	</div>
</div>
*/
// todo: Add more options for the menu and menu entries
function create_lizmenu(slct, itemsd)
{
	//
	// Populate menu
	//

	var domenu = $(slct);

	domenu.empty();

	var menu_plate = $(`
		<div class="lizard_menu">
			<div class="lizmenu_title">FATAL_ERROR</div>
			<div class="lizard_menu_entries">
			</div>
		</div>
	`);

	for (var lzitem of itemsd['menu_entries'])
	{
		// .hasOwnProperty('name')
		if (lzitem['type'] != 'separator')
		{
			var entry_plate = $(`
				<div class="lizard_menu_entry">
					<div class="lizard_menu_entry_icon"><img src="" class="lizmenu_entry_icon"></div>
					<div class="lizard_menu_entry_text">FATAL_ERROR</div>
				</div>
			`);

			// set icon
			entry_plate.find('.lizard_menu_entry_icon img')[0].src = lzitem['icon'];
			// set entry text
			entry_plate.find('.lizard_menu_entry_text').text(lzitem['name']);
			// set item action
			entry_plate.attr('lizmenu_action', lzitem['action']);
			// svg condition
			if (lzitem['svg'] != true){entry_plate.find('.lizard_menu_entry_icon img').css('object-fit', 'contain')}

		}else{
			var entry_plate = $(`<div class="lizard_menu_separator"></div>`);
		}

		// append to entries pool
		menu_plate.find('.lizard_menu_entries').append(entry_plate);
	}

	// set menu title
	menu_plate.find('.lizmenu_title').text(itemsd['menu_name']);

	// append menu to target
	domenu.append(menu_plate)

	// select appended menu
	// todo: .append returns selector?
	var newmenu = domenu.find('.lizard_menu');
	// Make parent a hitbox too
	// todo: make this optional
	domenu.attr('haslizmenu', true);
	// select menu items
	var newmenu_items = domenu.find('.lizard_menu_entries');


	//
	// set menu margins
	//

	// first - margin-top
	// margin top is: height of the resulting lizmenu + padding-top of the parent container

	// get padding of the parent container, if any
	var padding_top = parseInt(window.getComputedStyle(newmenu[0], null).getPropertyValue('padding-top').replace('px', ''));
	var margin_top = newmenu[0].offsetHeight
	if (!isNaN(padding_top)){
		margin_top += padding_top
	}

	// second - margin-left
	var padding_left = parseInt(window.getComputedStyle(newmenu.parent()[0], null).getPropertyValue('padding-left').replace('px', ''));
	var margin_left = 0
	if (!isNaN(padding_left)){
		margin_left += padding_left * -1
	}

	// set style
	newmenu_items.css('margin-left', margin_left.toString() + 'px')
	newmenu_items.css('margin-top', margin_top.toString() + 'px')

}











/*
document.querySelectorAll('.lizard_menu').forEach(function(userItem) {
    lizard_log(userItem);
    userItem.setAttribute('style', 'display: none;');
    // userItem.classList.add('lizhide');
});
*/

/*
document.addEventListener('mouseover', event => {
    // console.log('wtf');

    const pringles = event.target.closest('[lizards_menu]');
    if (pringles) { lizmenu_pos_fixup(pringles) }

});


function lizmenu_pos_fixup(lizmenu)
{
	
	var tgt_menu = lizmenu.querySelector('.lizard_menu');
	console.log(lizmenu);
	tgt_menu.style.marginTop = (lizmenu.offsetHeight).toString() + 'px'
	tgt_menu.style.marginLeft = (-1 * parseInt(window.getComputedStyle(lizmenu, null).getPropertyValue('padding-left').replace('px', ''))).toString() + 'px'

}

*/




