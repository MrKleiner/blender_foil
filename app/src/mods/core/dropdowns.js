
// important todo: There is a number of approaches for nice wrappers
// one of them is like pepega structure
// another one is like jquery
// and so on...
// the only disadvatage of classes is that they have to be spawned first
// important todo: what are the disadvantages of using classes like this ?

// important todo: YES, this is very cool and it works, BUT
// it's a literal labirynth...
// for instance, there's no standard of where the active item is written down...
// shit's all around the place and every function does its job differently
class simple_lizard_dropdowns
{
	// constructor(height, width) {
	constructor() {
		window.lizard_dropdowns = {};


		// Element.prototype.lzdrop=function(set_to) {


		// };


		print('Initialized Simple Dropdowns');
	};






	// ============================================================
	// ------------------------------------------------------------
	//                    		Spawner
	// ------------------------------------------------------------
	// ============================================================
	spawn(slct, idname, itemsd, parent_hitbox)
	{
		// itemsd = 
		// {
		// 	'menu_name': 'Steam App ID',
		// 	'menu_entries': [
		// 		{
		// 			'name': 'Half-Life 2',
		// 			'dropdown_set': '220'
		// 		},
		// 		{
		// 			'name': 'Half-Life 2: Episode One',
		// 			'dropdown_set': '380'
		// 		}
		// 	]
		// }

		// cant have duplicate names
		// if (idname in window.lizard_dropdowns || idname == undefined){return}
		if (idname == undefined){return}

		// init
		var dn_container = $(slct);
		// clear target container
		dn_container.empty();

		// var gwidth = document.querySelector(slct).clientWidth;

		// empty template for the dropdown
		var menu_plate = $(`
			<lzdropdown lzdropname="${idname}" draggable="false" class="lzdropdpown">
				<div class="lz_dn_title"><span style="color: #BC4141">None</span></div>
				<div class="dn_arrow_icon">
					<img src="assets/arrow_down.svg">
				</div>
				<div class="lz_menu_entries foil_hidden">
				</div>
			</lzdropdown>
		`);


		// store reference
		window.lizard_dropdowns[idname] = {
			'elem': menu_plate,
			// 'selected': itemsd['default'] ? itemsd['default'] : null,
			'items': itemsd['menu_entries']
		}

		//
		// Populate menu
		//
		this.update(idname)


		// set menu title
		// which is basically an entry with separator
		var dn_entries_pool = menu_plate.find('.lz_menu_entries');
		dn_entries_pool.append(`<div class="lz_menu_separator"></div>`);
		dn_entries_pool.append(`
			<div class="lz_menu_entry lz_dn_bottom_title">
				<div class="lz_menu_entry_text">${itemsd['menu_name']}</div>
			</div>
		`);

		// nothing should be draggable
		menu_plate.find('*').attr('draggable', false);

		// append menu to the target
		dn_container.append(menu_plate)

		// select appended menu
		// todo: .append returns selector?
		// var newmenu = dn_container.find('.lizard_menu');

		// Make parent a hitbox too if asked
		if (parent_hitbox == true){
			dn_container.attr('haslizdropdown', true);
		}
		
		// select menu items
		// var newmenu_items = dn_entries_pool;


		// set default, if any
		// todo: this is pretty retarded
		if (itemsd['default'] != undefined){
			this.set_active(menu_plate.find(`[dropdown_set="${itemsd['default']}"]`))
		}

		//
		// set menu margins
		//

		// first - margin-top
		// margin top is: height of the resulting lizmenu + padding-top of the parent container

		// get padding of the parent container, if any
		// var padding_top = parseInt(window.getComputedStyle(menu_plate[0], null).getPropertyValue('padding-top').replace('px', ''));
		// var margin_top = menu_plate[0].offsetHeight
		// if (!isNaN(padding_top)){
		// 	margin_top += padding_top
		// }

		// second - margin-left
		var padding_left = parseInt(window.getComputedStyle(menu_plate.parent()[0], null).getPropertyValue('padding-left').replace('px', ''));
		var margin_left = 0
		if (!isNaN(padding_left)){
			margin_left += padding_left * -1
		}

		// set style
		dn_entries_pool.css('margin-left', margin_left.toString() + 'px');
		// dn_entries_pool.css('margin-top', (margin_top + 5).toString() + 'px')
		// dn_entries_pool.css('margin-top', '5px');
	}






	//
	// re-append all the entries from the window object to the visual dropdown
	//

	// if with is specified, then update the dropdown with the given array
	// else - simply pull from the window object
	update(dn_name=null, upd_with=null, additive=false){
		var dn_ent = window.lizard_dropdowns[dn_name]
		if (dn_ent == undefined){return}

		var this_items = window.lizard_dropdowns[dn_name]['items']

		// update with, if asked to
		if (upd_with != null && upd_with != undefined){
			// if additive - add stuff and dont delete previous
			if (additive == true){
				this_items = this_items.concat(upd_with);
			}else{
				this_items = upd_with;
			}
		}

		var entry_pool = dn_ent['elem'].find('.lz_menu_entries');
		// clear entry container
		entry_pool.empty()

		// spawn entries one by one
		for (var lzitem of dn_ent['items'])
		{
			// .hasOwnProperty('name')
			if (lzitem['type'] != 'separator')
			{
				var entry_tplate = $(`
					<div dropdown_set="${lzitem['dropdown_set']}" class="lz_menu_entry">
						<div class="lz_menu_entry_text">${lzitem['name']}</div>
					</div>
				`);

				// todo: allow icons
				// set icon
				// entry_tplate.find('.lizard_menu_entry_icon img')[0].src = lzitem['icon'];

				// svg condition
				// if (lzitem['svg'] != true){entry_tplate.find('.lizard_menu_entry_icon img').css('object-fit', 'contain')}
			}

			// append to entries pool
			entry_pool.append(entry_tplate);
		}
	}



	get pool(){
		var dn_list = {};
		var remap_t = this;
		for (var dn in window.lizard_dropdowns){
			// all thanks to let...
			// todo: so, how does this work exactly ?????
			let ensure = dn
			dn_list[dn] = {
				'name': ensure,
				'active': remap_t.get_active(ensure),
				set: function(towhich){
					remap_t.set_active(window.lizard_dropdowns[ensure]['elem'].find(`[dropdown_set="${towhich}"]`))
        		},
        		update: function(with_w=null){
					remap_t.update(ensure, with_w)
        		},
        		add: function(add_what=null){
					remap_t.update(ensure, add_what, true)
        		}
			}
		}

		return dn_list
	}


	// set_active(dn_name=null, active_what=null){
	// 	var thisdn = window.lizard_dropdowns[dn_name]
	// 	if (dn_name == null || active_what == null || thisdn == undefined){return}


	// }



	//
	// force flush storage
	//
	full_flush(){
		window.lizard_dropdowns = {};
	}





	//
	// force flush storage
	//
	red_check(){
		// not "of", because
		// Normal variables in JavaScript can't be deleted using the delete operator.
		// In strict mode, an attempt to delete a variable will throw an error and is not allowed.
		for (var dn in window.lizard_dropdowns){
			print(window.lizard_dropdowns, dn)
			if (!document.body.contains(window.lizard_dropdowns[dn]['elem'][0])){

				delete window.lizard_dropdowns[dn]
			}
		}
	}






	//
	// Set active item of the dropdown
	//

	// sadly, jQuery is neccessary to handle non-existing elements situations
	set_active(toitem)
	{

		var dropdownroot = $(toitem).closest('lzdropdown');
		// print('set_active', toitem[0], dropdownroot[0])
		// set title
		// dropdownroot.querySelector('.lizmenu_title').innerText = toitem.getAttribute('dropdown_set');
		// console.log(toitem.querySelector('.lizard_menu_entry_text').textContent);
		dropdownroot.find('.lz_dn_title').text($(toitem).find('.lz_menu_entry_text').text());
		// $('.lz_menu_entries').addClass('foil_hidden');
		dropdownroot.attr('lz_active_item', $(toitem).attr('dropdown_set'))
	}

	// get active value
	get_active(dn)
	{
		var this_dn = window.lizard_dropdowns[dn]
		if (this_dn == undefined){return null};
		return (this_dn['elem'].attr('lz_active_item') ? this_dn['elem'].attr('lz_active_item') : null)
	}


	// important todo: wtf
	// important todo: still too much BDSM
	showhide(anydrop=$('<img>'))
	{
		var drop = $(anydrop)

		if (!drop.find('.lz_menu_entries').hasClass('foil_hidden')){
			$('lzdropdown .lz_menu_entries').addClass('foil_hidden');
		}else{
			$('lzdropdown .lz_menu_entries').addClass('foil_hidden');
			drop.find('.lz_menu_entries').toggleClass('foil_hidden');
		}
	}




}
window.lzdrops = new simple_lizard_dropdowns();









