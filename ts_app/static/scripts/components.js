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
  				<button onclick="delete_dialogue(this)" class="delete_standard" id="upload_delete">X</button>
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
  				<button onclick="delete_dialogue(this)" class="delete_standard" id="upload_delete">X</button>
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

function show_dialogue(dialogue){
	console.log(dialogue)
    var save_dialogue = document.getElementById(dialogue)
    save_dialogue.style.display = "inline-block";
}
