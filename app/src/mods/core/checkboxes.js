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

// todo: this looks weird
class lizcboxes_shortcuts
{
	constructor() {
		// this.height = height;
		// this.width = width;
	}
	// returns all cboxes on a page
	get pool()
	{
		var pooled = {}
		// console.log('get pool')
		document.querySelectorAll('[lizcbox]').forEach(function(userItem) {
			// pooled.push(userItem);
			pooled[userItem.parentElement.getAttribute('lizcbox_id')] = userItem.lizchecked()
		});
		return pooled
	}
}

window.lizcboxes = new lizcboxes_shortcuts()



// init all cboxes
function lizcboxes_init()
{
	console.groupCollapsed('Checkboxes Init');
	document.querySelectorAll('[lizcbox_init]').forEach(function(userItem) {

		console.log(userItem);

		if (userItem.getAttribute('lizcbox_init') == 'set'){
			// var htm_append = `
			// 	<div lizcbox class="lizcbox_container">
			// 		<img draggable="false" src="assets/checkmark.svg">
			// 	</div>
			// `
			var htm_append = `
				<div lizcbox="set" class="lizcbox_container">
					<div class="lizcbox_mark"></div>
				</div>
			`;
		}else{
			var htm_append = `
				<div lizcbox="unset" class="lizcbox_container">
					<div class="lizcbox_mark"></div>
				</div>
			`;
		}
		// hitbox
		if (userItem.hasAttribute('lizcbox_hashitbox')){
			userItem.parentElement.classList.add('lizcbox_hitbox')
		}
		userItem.innerHTML = htm_append;
		userItem.removeAttribute('lizcbox_init');
		userItem.removeAttribute('lizcbox_hashitbox');
	});
	console.groupEnd('Checkboxes Init');
}

// todo: safety measures ?
function lizcboxes_switch(tgtbox, state)
{
	tbox = tgtbox.querySelector('[lizcbox].lizcbox_container') || tgtbox
	// console.log('set status')
	// todo: getAttribute
	// will be faster
	if ($(tbox).attr('lizcbox') == 'set'){
		$(tbox).attr('lizcbox', 'unset');
	}else{
		$(tbox).attr('lizcbox', 'set');
	}
	
}


// takes lizcbox id and status as an input
// if no stat specified - checkbox state returned
function lizcbox_stat(sel, stat=null)
{
	
	var ss = document.querySelector('[lizcbox_id="' + sel + '"]');
	if (ss != null){
		return ss.querySelector('[lizcbox]').lizchecked(stat)
	}
	
}