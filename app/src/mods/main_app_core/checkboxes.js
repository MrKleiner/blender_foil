Element.prototype.lizchecked=function(status) {
    // if(value===undefined) value=true;
    // if(this.hasAttribute(attribute)) this.removeAttribute(attribute);
    // else this.addAttribute(attribute,value);
    if (status == undefined)
    {
	    if (this.getAttribute('lizcbox') == 'set'){
	    	return true
	    }else{
	    	return false
	    }
	}else{
		if (status == true){
			this.setAttribute('lizcbox', 'set');
		}
		if (status == false){
			this.setAttribute('lizcbox', 'unset');
		}
	}
}



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

	// todo: getAttribute
	// will be faster
	if ($(tbox).attr('lizcbox') == 'set'){
		$(tbox).attr('lizcbox', 'unset');
	}else{
		$(tbox).attr('lizcbox', 'set');
	}
	
}

