
window.onload = function() {
    $.ajax({
        type: 'Get',
        url: '/get_images/',
        success: function(data) {  
                // Get the reference to the list where images will be displayed
                var list = $("#image-list").find('ul');
                // Loop through each image returned from the server
                for (var image in data["images"]) {
                    // Create a list item to hold each image
                    var li = document.createElement("li");
                    // Assign a class to the list item
                    li.className = "image";
                    // Get the current image object
                    var image_obj = data["images"][image];
                    // Populate the list item with image details and delete button
                    li.innerHTML =  "<div class=name_and_delete>" +  
                                    "<p>" + image + "</p>" +
                                    "<form method=POST id=delete_image_form>" +  
                                    "<button name=delete_image id=delete_image_button class=delete_standard value =" + image +" > X </button>" +
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
