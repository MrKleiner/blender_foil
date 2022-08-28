







class simple_lizard_checkboxes
{
	// constructor(height, width) {
	constructor() {
		window.lizard_checkboxes = {};

		/*
		Element.prototype.lizchecked=function(status) {
		    // if(value===undefined) value=true;
		    // if(this.hasAttribute(attribute)) this.removeAttribute(attribute);
		    // else this.addAttribute(attribute,value);
		    if (!this.hasAttribute('lizcbox')){ return null }
		    if (status == undefined || status == null)
		    {
			    if (this.getAttribute('lizcbox') == 'set'){
			    	return true
			    }else{
			    	return false
			    }
			}else{
				if (status == true){
					this.setAttribute('lizcbox', 'set');
					// return true
				}
				if (status == false){
					this.setAttribute('lizcbox', 'unset');
					// return false
				}
			}
		}
		*/

		print('Initialized Simple Checkboxes');
	};






	// ============================================================
	// ------------------------------------------------------------
	//                    		Spawner
	// ------------------------------------------------------------
	// ============================================================
	
	// all-in one function
	resync()
	{
		// spawn checkboxes
		for (var cb of document.querySelectorAll('lzcbox')){
			var mkbox = $(`
				<div cbtitle>${cb.innerText.trim()}</div>
				<div cmark_outer>
					<div cmark_inner></div>
				</div>
			`)

			// set asked state
			$(cb).attr('lzcbox_state', ($(cb).attr('lzcbox_init') == 'set') ? 'set' : 'unset')
			// remove init attr
			$(cb).removeAttr('lzcbox_init')
			// mark as done
			$(cb).attr('lzcbox_done', true)

			// set html of the checkbox
			$(cb).html(mkbox)

			// add to the registry
			window.lizard_checkboxes[$(cb).attr('lzcbox_id')] = {
				'elem': $(cb)
			}
		}

		// redundancy check
		for (var check in window.lizard_checkboxes){
			if (!document.body.contains(window.lizard_checkboxes[check]['elem'][0])){
				delete window.lizard_checkboxes[check]
			}
		}
	}



	get pool(){
		var ch_list = {};
		var remap_t = this;
		for (var ch in window.lizard_dropdowns){
			let ensure = ch
			dn_list[ch] = {
				'name': ensure,
				'state': remap_t.state(ensure),
				set: function(towhich){
					remap_t.set_active(window.lizard_dropdowns[ensure]['elem'].find(`[dropdown_set="${towhich}"]`))
        		}
			}
		}

		return dn_list
	}


	state(cbox=null){
		if (cbox==null){return}
		return $(cbox).closest('lzcbox').attr('lzcbox_state') || null
	}



}
window.lzcbox = new simple_lizard_checkboxes();









