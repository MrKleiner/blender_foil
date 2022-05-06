/*
=====================================================================
---------------------------------------------------------------------
                             Simple UILists
---------------------------------------------------------------------
=====================================================================
*/

function init_simple_ui_lists()
{
	console.groupCollapsed('Init UILists');
	document.querySelectorAll('uilist').forEach(function(userItem) {
		// todo: safety fallbacks ?
		var listcallback = userItem.getAttribute('windowlist');
		var mainparent = userItem.parentElement;
		var appender = 
		`
			<input type="text" class="simple_uilist_text_input">
			<div uilist_suggestfrom="` + listcallback + `" class="simple_uilist_suggest"></div>
		`;
		$(userItem.parentElement).append(appender);
		// todo: a mess ??
		var ulist = userItem.parentElement.querySelector('div.simple_uilist_suggest');
		// console.log('Uilist', ulist)
		userItem.remove();


		//
		// Do margins for a dropdown
		//

		// first - margin-top
		// margin top is: height of the resulting lizmenu + padding-top of the parent container

		// get padding of the parent container, if any

		var padding_top = parseInt(window.getComputedStyle(mainparent, null).getPropertyValue('padding-top').replace('px', ''));
		var margin_top = mainparent.offsetHeight;
		if (!isNaN(padding_top)){
			margin_top += padding_top
		}

		// second - margin-left
		var padding_left = parseInt(window.getComputedStyle(mainparent, null).getPropertyValue('padding-left').replace('px', ''));
		var margin_left = 0
		if (!isNaN(padding_left)){
			margin_left += padding_left * -1
		}


		// set style
		// todo: get rid of jquery
		$(ulist).css('margin-left', margin_left.toString() + 'px');
		$(ulist).css('margin-top', (margin_top + 5).toString() + 'px');
		console.log({
			'top': margin_top,
			'left': margin_left,
			'ref': listcallback
		});

	});
	console.groupEnd('Init UILists');
}


// important todo: dont append to html tree. Keep as a reference in memory
// takes container containing text input and the list container
// expects a referenced window object to be an array or strings
// important todo: rewrite. This is an extremely edgy way of displaying matches...
// store matched results in the same window object and then cycle through them.
function simple_ui_list_buildsuggest(keyvt, tgtsugest)
{

	var tgtsug = tgtsugest.parentElement;
	var prohibited_codes = [38, 40, 17, 18, 16, 20, 9, 91, 37, 39, 93, 92, 13, 27];

	if (prohibited_codes.includes(keyvt.keyCode)){
		return
	}


	var txt_inp = tgtsug.querySelector('input.simple_uilist_text_input');
	var ulist = tgtsug.querySelector('div.simple_uilist_suggest');
	// unhide thesuggestion list on every allowed keypress
	// so that it's easier to change shit after pressing enter
	ulist.style.display = null;
	// todo: slow ???
	var wincont = window[ulist.getAttribute('uilist_suggestfrom')];
	var querytext = txt_inp.value;
	ulist.innerHTML = '';

	var append_linit = 0;

	// todo: allow custom configs

	for (var centry of wincont){
		if (centry.toLowerCase().includes(querytext.toLowerCase()) && append_linit <= 300){
			append_linit++
			var bdsm = document.createElement('div');
			bdsm.setAttribute('class', 'simple_uilist_suggestion_entry');
			bdsm.textContent = centry
			if (append_linit >= 12){bdsm.style.display = 'none'}
			ulist.appendChild(bdsm);
		}
	}

}


function uilist_scroller(keyact, ulist)
{
	var ulist = ulist.parentElement.querySelector('.simple_uilist_suggest');

	var get_indexed = ulist.querySelector('[ulist_active_item]');
	var children_arrayed = Array.from(ulist.children);

	if (get_indexed == null){
		var uindex = -1
	}else{
		var uindex = children_arrayed.indexOf(get_indexed);
	}

	// todo: duplicates avoid

	// next element
	if (keyact.keyCode == 40 || keyact.keyCode == 9){
		keyact.preventDefault();
		// only if next element exists
		if (children_arrayed[uindex + 1] != undefined){

			// remove styles and remove active
			for (var rm of children_arrayed){
				rm.removeAttribute('ulist_active_item');
				rm.classList.remove('simple_uilist_suggestion_entry_active');
			}

			// hide previous
			var previous_last = children_arrayed[uindex - 10]
			// todo: also check if it's a valid node ?
			if (previous_last != undefined){
				previous_last.style.display = 'none';
				previous_last.setAttribute('ulist_visible', 'false');
			}

			// unhide next
			var enext = children_arrayed[uindex + 1]
			if (enext != undefined){
				enext.removeAttribute('style');
				enext.classList.add('simple_uilist_suggestion_entry_active');
				enext.setAttribute('ulist_visible', true);
				enext.setAttribute('ulist_active_item', true);
			}

			ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex + 1].textContent
		}
	}

	// previous
	if (keyact.keyCode == 38){
		keyact.preventDefault();
		// only if next element exists
		if (children_arrayed[uindex - 1] != undefined){

			// remove styles and remove active
			for (var rm of children_arrayed){
				rm.removeAttribute('ulist_active_item');
				rm.classList.remove('simple_uilist_suggestion_entry_active');
			}

			// hide previous
			var previous_last = children_arrayed[uindex + 10]
			// todo: also check if it's a valid node ?
			if (previous_last != undefined){
				previous_last.style.display = 'none';
				previous_last.setAttribute('ulist_visible', false);
			}

			// unhide next
			var enext = children_arrayed[uindex - 1]
			if (enext != undefined){
				enext.removeAttribute('style');
				enext.setAttribute('ulist_visible', true);
				enext.setAttribute('ulist_active_item', 'true');
				enext.classList.add('simple_uilist_suggestion_entry_active');
			}

			ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex - 1].textContent
		}
	}

	// apply
	if (keyact.keyCode == 13 && uindex != -1){
		keyact.preventDefault();
		ulist.parentElement.querySelector('input.simple_uilist_text_input').value = children_arrayed[uindex].textContent;
		uilist_showhide(ulist, false)
	}

}

// true = show
// false = hide
// takes suggest as an input
function uilist_showhide(thelisted, ustate)
{
	var thelist = thelisted.parentElement.querySelector('.simple_uilist_suggest');
	if (ustate == true){
		// console.log('LISTFFS', thelisted.parentElement)
		simple_ui_list_buildsuggest(false, thelisted.parentElement)
		thelist.style.display = null;
	}

	if (ustate == false){
		thelist.innerHTML = '';
		thelist.style.display = 'none';
	}
}