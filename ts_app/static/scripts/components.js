class dialogue extends HTMLElement {

	constructor() { 
        super();               
    }

    connectedCallback() {        
        this.render();
    }

    render() {
		const name = this.getAttribute('dialogue_name');        

		this.innerHTML = `
			<div class=orange_top>
				<p id=dialogue_message> ${name} </p>
  				<button onclick="delete_dialogue(this)" class="delete_standard error_unclickable" id="upload_delete">X</button>
			</div>
		`;
	}
	disconnectedCallback() {

	}
	attributeChangedCallback(attrName, oldVal, newVal) {
        this.render();
    }

	static get observedAttributes() {
        return ['dialogue_name'];
    }


}



class error extends HTMLElement {

	constructor() { 
        super();               
    }

    connectedCallback() {        
        this.render();
    }

    render() {
		const name = this.getAttribute('dialogue_name');        

		this.innerHTML = `
			<div class=red_top>
				<p id=dialogue_message> ${name} </p>
  				<button onclick="delete_dialogue(this);make_clickable('error_unclickable')" class="delete_standard" id="upload_delete">X</button>
			</div>
		`
	}
	disconnectedCallback() {

	}
	attributeChangedCallback(attrName, oldVal, newVal) {
        this.render();
    }

	static get observedAttributes() {
        return ['dialogue_name'];
    }


}


customElements.define('dialogue-element', dialogue);
customElements.define('error-dialogue', error);

function show_dialogue(dialogue, block_side_buttons=false){
    var save_dialogue = document.getElementById(dialogue);
    save_dialogue.style.display = "inline-block";
	if(Boolean(block_side_buttons)){
		make_unclickable("dialogue_unclickable");
	}
}


function delete_dialogue(value){
    var dialogue = value.closest(".dialogue-element");
    dialogue.style.display="none";
	if(document.getElementsByClassName("dialogue_unclickable")){
		make_clickable("dialogue_unclickable");
}
}


function make_unclickable(unclickable_class){
	elements = document.getElementsByClassName(unclickable_class);
	for(let element of elements){
		element.style.pointerEvents = "none";
	}
}

function make_clickable(clickable_class){
	elements = document.getElementsByClassName(clickable_class);
	for(let element of elements){
		element.style.pointerEvents = "auto";
	}

}

function show_message(message_holder, message){
	message_holder_html = document.getElementById(message_holder)
	message_holder_html.innerHTML = message
	setTimeout(() =>{
		message_holder_html.innerHTML=""
	}, 2000);

}