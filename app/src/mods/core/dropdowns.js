/*
============================================================
------------------------------------------------------------
                   Simple dropdowns START
------------------------------------------------------------
============================================================
*/

function create_lizdropdown(slct, itemsd)
{
	//
	// Populate menu
	//

	var domenu = $(slct);

	domenu.empty();

	var gwidth = document.querySelector(slct).clientWidth;

	var menu_plate = $(`
		<div draggable="false" class="lizard_menu lizard_menu_dropdown">
			<div class="lizmenu_title"><span style="color: #BC4141">None</span></div>
			<div class="lizard_dropdown_arrow_icon">
				<img src="assets/arrow_down.svg">
			</div>
			<div style="width: ` + gwidth.toString() + `px" class="lizard_dropdown_entries">
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
					<div class="lizard_menu_entry_text">FATAL_ERROR</div>
				</div>
			`);

			// set icon
			// entry_plate.find('.lizard_menu_entry_icon img')[0].src = lzitem['icon'];
			// set entry text
			entry_plate.find('.lizard_menu_entry_text').text(lzitem['name']);
			// set item action
			entry_plate.attr('dropdown_set', lzitem['dropdown_set']);
			// svg condition
			// if (lzitem['svg'] != true){entry_plate.find('.lizard_menu_entry_icon img').css('object-fit', 'contain')}

		}else{
			// dropdowns don't need a separator
			// var entry_plate = $(`<div class="lizard_menu_separator"></div>`);
		}

		// append to entries pool
		menu_plate.find('.lizard_dropdown_entries').append(entry_plate);
	}

	// set menu title
	// which is basically an entry with separator
	// menu_plate.find('.lizmenu_title').text(itemsd['menu_name']);

	menu_plate.find('.lizard_dropdown_entries').append(`<div class="lizard_menu_separator"></div>`);
	menu_plate.find('.lizard_dropdown_entries').append(`
		<div style="pointer-events: none" class="lizard_menu_entry">
			<div class="lizard_dropdown_bottom_title lizard_menu_entry_text">` + itemsd['menu_name'] + `</div>
		</div>
	`);


	// append menu to target
	domenu.append(menu_plate)

	// select appended menu
	// todo: .append returns selector?
	var newmenu = domenu.find('.lizard_menu');
	// Make parent a hitbox too
	// todo: make this optional
	domenu.attr('haslizdropdown', true);
	// select menu items
	var newmenu_items = domenu.find('.lizard_dropdown_entries');


	// set default, if any
	// todo: this is pretty retarded
	if (itemsd['default'] != undefined){
		if (newmenu[0].querySelector('[dropdown_set="' + itemsd['default'] + '"]') != null){
			lizdropdown_set_active(newmenu[0].querySelector('[dropdown_set="' + itemsd['default'] + '"]'))
		}
	}

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
	newmenu_items.css('margin-top', (margin_top + 5).toString() + 'px')

}

Element.prototype.lizdropdown=function(set_to) {
    // if(value===undefined) value=true;
    // if(this.hasAttribute(attribute)) this.removeAttribute(attribute);
    // else this.addAttribute(attribute,value);
    // todo: poor logic. use ||
    // var tgt_menu_s = this.closest('.haslizdropdown') || this.closest('.lizard_menu')
	if (this.closest('[haslizdropdown]') != null){
		var tgt_menu_s = this.querySelector('.lizard_menu')
	}
	if (this.closest('.lizard_menu') != null){
		var tgt_menu_s = this.closest('.lizard_menu')
	}

    if (set_to == undefined){
	    if (tgt_menu_s != null){
	    	return tgt_menu_s.getAttribute('liz_active_item')
	    }else{
	    	return null
	    }
    }

};


function lizdropdown_set_active(toitem)
{
	var dropdownroot = toitem.closest('.lizard_menu');
	// set title
	// dropdownroot.querySelector('.lizmenu_title').innerText = toitem.getAttribute('dropdown_set');
	// console.log(toitem.querySelector('.lizard_menu_entry_text').textContent);
	dropdownroot.querySelector('.lizmenu_title').innerText = toitem.querySelector('.lizard_menu_entry_text').textContent;
	dropdownroot.querySelector('.lizard_dropdown_entries').style.visibility = 'hidden';
	dropdownroot.setAttribute('liz_active_item', toitem.getAttribute('dropdown_set'))
}


// important todo: wtf
function dropdown_showhide(anydrop)
{

	if (anydrop != null) {
		// should toggle
		/*
		if (dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility == 'visible'){
			dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility = 'hidden';
			dropdown_open.querySelector('.lizard_dropdown_entries').classList.add('lizdropdown_active');
		}else{
			dropdown_open.querySelector('.lizard_dropdown_entries').style.visibility = 'visible';
		}
		dropdown_open.querySelector('.lizard_dropdown_entries').style.opacity = 1;
		*/

		anydrop.querySelector('.lizard_dropdown_entries').classList.toggle('lizdropdown_entries_shown');
		anydrop.classList.toggle('lizdropdown_active');
		// dropdown_open.querySelector('.lizard_menu').classList.toggle('lizdropdown_active');

		document.querySelectorAll('[haslizdropdown]').forEach(function(userItem) {
			if (userItem != anydrop){
				userItem.querySelectorAll('.lizard_dropdown_entries, .lizard_menu, [haslizdropdown]').forEach(function(sel) {
					sel.classList.remove('lizdropdown_entries_shown');
					sel.classList.remove('lizdropdown_active');
				});
				userItem.classList.remove('lizdropdown_entries_shown');
				userItem.classList.remove('lizdropdown_active');
			}
		});

	} else {
    	// todo: jquery is actually slow as fuck
    	$('.lizard_dropdown_entries, .lizard_menu, [haslizdropdown]')
    	.removeClass('lizdropdown_entries_shown')
    	.removeClass('lizdropdown_active');
	}

}


// takes [haslizdropdown] dropdown element
class lzdropdown
{
	constructor(dr_id) {
		// this.height = height;
		// this.width = width;
		this.dref = dr_id
		this.drname = dr_id.getAttribute('id');
	}
	// returns all cboxes on a page
	get name()
	{
		return this.drname
	}

	set_active(entry)
	{
		// see if there's a valid entry
		for (var entr of this.dref.querySelectorAll('.lizard_menu_entry'))
		{
			if (entr.getAttribute('dropdown_set') == null){
				continue
			}
			if (entr.getAttribute('dropdown_set').toLowerCase() == entry.toLowerCase())
			{
				var mn = this.dref.querySelector('.lizard_menu_dropdown');
				var mnt = this.dref.querySelector('.lizmenu_title');
				mn.setAttribute('liz_active_item', entry)
				mnt.innerText = entr.textContent.trim()
			}
		}

	}
}




// todo: this looks weird
class lizdropdowns_shortcuts
{
	constructor() {
		// this.height = height;
		// this.width = width;
	}
	// returns all cboxes on a page
	get pool()
	{
		var pooled = {}
		document.querySelectorAll('[haslizdropdown]').forEach(function(userItem) {
			// pooled.push(userItem);
			// pooled[userItem.getAttribute('id')] = userItem.lizdropdown()
			pooled[userItem.getAttribute('id')] = new lzdropdown(userItem)
		});
		return pooled
	}
}

window.lizdropdowns = new lizdropdowns_shortcuts()




