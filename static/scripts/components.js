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
			<div class= 'orange_top interaction_top'>
				<p id=dialogue_message> ${name} </p>
  				<button onclick="delete_dialogue(this)" class="delete_standard error_unclickable upload_delete">X</button>
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
		const delete_function = this.getAttribute('delete_function');        
		const message_id = this.getAttribute("message_id")

		this.innerHTML = `
			<div class='red_top interaction_top'>
				<p id=dialogue_message> ${name} </p>
  				<button onclick="${delete_function};make_clickable('error_unclickable')" class="button delete_standard upload_delete">X</button>
			</div>
			<div id=${message_id}>
    
			</div>
		`
	}
	disconnectedCallback() {

	}
	attributeChangedCallback(attrName, oldVal, newVal) {
        this.render();
    }

	static get observedAttributes() {
        return ['dialogue_name', 'delete_function', "message_id"];
    }


}


customElements.define('dialogue-element', dialogue);
customElements.define('error-dialogue', error);

