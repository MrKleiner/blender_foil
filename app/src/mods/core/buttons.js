class simple_lizard_buttons
{
	// constructor(height, width) {
	constructor() {
		window.lizard_buttons = {};
		print('Initialized Simple Buttons');
	};


	// all-in-one function, does everything and does it reliably...
	resync(){
		// delete redundant
		for (var lbtn in window.lizard_buttons){
			// if element is not on the page - it means that it was deleted
			// (because we dont store it anywhere for later use)
			if (!document.body.contains(window.lizard_buttons[lbtn]['elem'][0])){
				delete window.lizard_buttons[lbtn]
			}
		}
	}

	lock(sel=''){
		$(sel).addClass('.btn_locked')
	}

	unlock(sel=''){
		$(sel).removeClass('.btn_locked')
	}


}
window.lzbtns = new simple_lizard_buttons();


