function select_column(pressed_column) {
    if (document.getElementById("column_selected")) {
        document.getElementById("column_selected").removeAttribute('id', "column_selected")
    }
    pressed_column.setAttribute('id', "column_selected");
}

function enlarge_image(element) {
    //Removes onclick attribute so that it no longer makes the image large

    element.removeAttribute("onclick")
    var image = element.closest(".image")
    image.classList.add("fullscreen_image")
    image.classList.remove("image")
    //Adds new onclick element to make the image small
    element.onclick = function () { small_image(this) };

}



function small_image(element) {
    //Removes onclick attribute so that it no longer makes the image small
    element.removeAttribute("onclick")
    var image = element.closest(".fullscreen_image")
    image.classList.add("image")
    image.classList.remove("fullscreen_image")
    //Adds new onclick element to enlarge image
    element.onclick = function () { enlarge_image(this) };

}


$(document).on('submit', '#delete_image_form', function (e) {   // Prevent default form submission behavior
    e.preventDefault();
    // Retrieve the delete button and its value

    let button = document.getElementById("delete_image_button");
    let button_value = button.value;
    // Send an AJAX POST request to delete the image

    $.ajax({
        type: 'POST',
        url: '/delete/' + button_value,
        success: function () {
            // Upon successful deletion, remove the corresponding list item
            button.closest('li').remove()
        },
        error: function () {
            alert("something went wrong")
        }
    })
});


window.onload = function() {
    $.ajax({
        type: 'Get',
        url: '/get_images/',
        success: function (data) {  
             // Get the reference to the list where images will be displayed
             var list = $("#image-list").find('ul');
            // Loop through each image returned from the server
            for (let i = 0; i < data["images"].length; i++) {
                    // Create a list item to hold each image
                    var li = document.createElement("li");
                    // Assign a class to the list item
                    li.className = "image";
                    // Get the current image object
                    var image_obj = data["images"][i][2];

                    // Populate the list item with image details and delete button
                    li.innerHTML =  "<div class=name_and_delete>" +  
                        "<p>" + data["images"][i][1] + "</p>" +
                                    "<form method=POST id=delete_image_form>" +  
                        "<button name=delete_image id=delete_image_button class=delete_standard value =" + data["images"][i][0] +" > X </button>" +
                                    "</form>" + "</div>" +
                                    "<div onClick=enlarge_image(this) class=image_list_image >"+
                                    "<img class=standard_img src=" + image_obj + ">" +
                                    "</div>";
                    // Append the list item to the list
                    list.append(li);
            }},
            error: function(data) {
                // If no images are returned, display an error message
                make_unclickable('dialogue_unclickable');
                var error_text = document.getElementById("error_text_load_images");
                var error_message = '<p id="errror_image_plot">' +  data["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("display_images_error").style.display = "inline-block";
        }
    });
};

function add_options(){

    return;
}
