
/*
============================================================
------------------------------------------------------------
                  Simple tooltips START
------------------------------------------------------------
============================================================
*/


function init_liztooltips()
{
	console.groupCollapsed('Init Tooltips');
	document.querySelectorAll('liztooltip').forEach(function(userItem) {
		console.log(userItem);
		userItem.parentElement.setAttribute('liztooltip', userItem.innerHTML);
		userItem.parentElement.setAttribute('liztooltip_prms', userItem.getAttribute('liztooltip_prms'));
		userItem.remove();
	});
	console.groupEnd('Init Tooltips');
}

//
// 0: pos: top/left/right/bottom
// 1: toparent 1/0
// 2: padding
//

function lizshowtooltip(tl, evt) {
	// if no tooltip elem - create one
	if (document.querySelector('[lizards_tooltip_box]') == null){
		var liztipbox = document.createElement('div');
		liztipbox.setAttribute('lizards_tooltip_box', true);
		liztipbox.style.display = 'none';
		document.body.appendChild(liztipbox);
	}

	var lizardbox = document.querySelector('[lizards_tooltip_box]');
	var splitopts = tl.getAttribute('liztooltip_prms').split(':');
	var boxopts = {
		'pos': splitopts[0],
		'toparent': parseInt(splitopts[1]),
		'padding': parseInt(splitopts[2]),
		'delay': parseInt(splitopts[3])
	}
	lizardbox.innerHTML = tl.getAttribute('liztooltip');


	// construct position
	mrk_ect_timer = setTimeout(function() {
		lizardbox.style.display = 'flex';
		// todo: make it echo into a group
		// console.log('delayed call');
		// lizardbox.style.display = 'flex';
		// because this has to be evaluated right on call
		
		var tgt_e_pos = tl.getBoundingClientRect();

		var tgt_e_h = tl.offsetHeight;
		var tgt_e_w = tl.offsetWidth;

		var tboxh = lizardbox.getBoundingClientRect().height;
		var tboxw = lizardbox.getBoundingClientRect().width;
		// console.log(tboxh)

		var page_w = window.innerWidth;
		var page_h = window.innerHeight;
		
		// console.log(evt)
		var gl_cursor_loc_x = evt.pageX;
		var gl_cursor_loc_y = evt.pageY;
		
		var base_x = 0;
		var base_y = 0;

		var base_posdict = {
			'top': {
				'x': tgt_e_pos.x,
				'y': (tgt_e_pos.y - boxopts['padding']) - tboxh
			},
			'left': {
				'x': tgt_e_pos.x + tboxw,
				'y': tgt_e_pos.y
			},
			'right': {
				'x': tgt_e_pos.x + tgt_e_w + boxopts['padding'],
				'y': tgt_e_pos.y
			},
			'right_up': {
				'x': tgt_e_pos.x + tgt_e_w + boxopts['padding'],
				'y': (tgt_e_pos.y - tboxh) + tgt_e_h
			},
			'bottom':{
				'x': tgt_e_pos.x,
				'y': tgt_e_pos.y + tgt_e_h + boxopts['padding']
			}
		}

		// console.log(base_posdict[boxopts['pos']]['y'].toString() + 'px')

		var non_parent_margin_x = 0
		var non_parent_margin_y = 0

		// relative to mouse or element
		if (boxopts['toparent'] == 1){
			var finalpos_x = base_posdict[boxopts['pos']]['x']
			var finalpos_y = base_posdict[boxopts['pos']]['y']
		}else{
			var finalpos_x = window.actualmpos['x'] + boxopts['padding']
			var finalpos_y = window.actualmpos['y'] + boxopts['padding']

			var non_parent_margin_x = boxopts['padding'] + 5
			var non_parent_margin_y = boxopts['padding'] + 5
		}



		// fix clipping y
		// console.log(base_posdict[boxopts['pos']]['y'] + tboxh);
		if (base_posdict[boxopts['pos']]['y'] + tboxh > page_h){
			finalpos_y -= (((base_posdict[boxopts['pos']]['y'] - non_parent_margin_y) + tboxh) - (page_h - 5))
		}
		// fix clipping x
		if (base_posdict[boxopts['pos']]['x'] + tboxw > page_w){
			finalpos_x -= (((base_posdict[boxopts['pos']]['x'] - non_parent_margin_x) + tboxw) - (page_w - 5))
		}
		
		lizardbox.style.top = finalpos_y.toString() + 'px';
		lizardbox.style.left = finalpos_x.toString() + 'px';

		if (window.actualmpos['tgt'].closest('[liztooltip]')){
			lizardbox.style.visibility = 'visible';
		}
		

	}, boxopts['delay']);

}



// important todo: It's a pretty bootleg fix and logic is extremely poor
// There should be a better way of determining wether it's on or not
// init should also be done separately
function showliztooltip(tooltip_obj)
{
	if (tooltip_obj != null)
	{
		var tipbox = document.querySelector('[lizards_tooltip_box]');
		if (tipbox != null){
			if (tipbox.style.visibility != 'visible'){
				if (typeof mrk_ect_timer != 'undefined') { clearTimeout(mrk_ect_timer) }
				lizshowtooltip(tooltip_obj, event) 
			}
		}else{
			lizshowtooltip(tooltip_obj, event)
		}
	}else{
		// clearTimeout(mrk_ect_timer);
		// console.log(mrk_ect_timer);
		if (typeof mrk_ect_timer != 'undefined') { clearTimeout(mrk_ect_timer) }
		// $('[lizards_tooltip_box]').css('display', 'none');
		$('[lizards_tooltip_box]').css('visibility', 'hidden');
		// document.querySelector('[lizards_tooltip_box]').style.visibility = 'hidden';
	}
}















