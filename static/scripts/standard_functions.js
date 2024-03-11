
function show_unshow(element){
	var element = document.getElementById(element);
	if (element.classList.contains("hidden")){
		element.classList.remove("hidden");
	}
	else {
		element.classList.add("hidden");
	}
}


function show_dialogue(dialogue, block_side_buttons = false) {
	var save_dialogue = document.getElementById(dialogue);
	save_dialogue.style.display = "flex";
	if (Boolean(block_side_buttons)) {
		make_unclickable("dialogue_unclickable");
	}
}

function delete_dialogue_error(value) {
	var dialogue = value.closest(".dialogue-element");
	dialogue.style.display = "none";
}

function delete_dialogue(value) {
	var dialogue = value.closest(".dialogue-element");
	dialogue.style.display = "none";
	if (document.getElementsByClassName("dialogue_unclickable")) {
		make_clickable("dialogue_unclickable");
	}
}


function make_unclickable(unclickable_class) {
	elements = document.getElementsByClassName(unclickable_class);
	for (let element of elements) {
		element.style.pointerEvents = "none";
	}
}

function make_clickable(clickable_class) {
	elements = document.getElementsByClassName(clickable_class);
	for (let element of elements) {
		element.style.pointerEvents = "auto";
	}

}

function show_message(message_holder, message) {
	message_holder_html = document.getElementById(message_holder)
	message_holder_html.innerHTML = message
	setTimeout(() => {
		message_holder_html.innerHTML = ""
	}, 2000);

}

function reset(id_htmlobject) {
	var object_intrest = document.getElementById(id_htmlobject)
	object_intrest.innerHTML = ""
}