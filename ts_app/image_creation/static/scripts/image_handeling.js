function enlarge_image(element){
    //Removes onclick attribute so that it no longer makes the image large

    element.removeAttribute("onclick")
    var image = element.closest(".image")
    image.classList.add("fullscreen_image")
    image.classList.remove("image")
    //Adds new onclick element to make the image small
    element.onclick = function(){small_image(this)};

}



function small_image(element){
    //Removes onclick attribute so that it no longer makes the image small
    element.removeAttribute("onclick")
    var image = element.closest(".fullscreen_image")
    image.classList.add("image")
    image.classList.remove("fullscreen_image")
    //Adds new onclick element to enlarge image
    element.onclick = function(){enlarge_image(this)};

}

$(document).ready(function() {
    $('#image_draw_form').submit(function (e) {
        e.preventDefault()
        //Retrieves the dataset that is going to be used
        var dataset = document.getElementById("file_display_selected").value
        //Retrieves the form that is going to be send to the backend
        var form = new FormData($(this)[0])
        $.ajax({
            headers: { 
                "X-CSRFToken": "{{ form.csrf_token._value() }}",
            },
            type: "POST",
            url: '/make_image/'+ dataset,
            data: form, 
            processData: false,
            contentType: false,
            // Handle successful response

            success: function (data) {
                const img_div = document.getElementById("image_div");
                img_div.innerHTML = "<img class=standard_img id=picture src=data:image/jpeg;base64," + data["img"] + ">";
                document.getElementById("save_image_dialogue_button").style.display="inline-block";
            },
            // Handle failed response
            error: function(data){
                answer = JSON.parse(data['responseText'])
                make_unclickable('dialogue_unclickable')
                var error_text = document.getElementById("error_text_draw_image");
                var error_message = '<p id="errror_image_plot">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("image_error").style.display="inline-block";
                }
    })

    });
});



$(document).ready(function() {
    $('#save_form').submit(function (e) {
        e.preventDefault(); 

        // Retrieve the image element
        const image = $("#picture")[0];
        // Retrieve the form element
        const data = new FormData(save_form);
        const form = Object.fromEntries(data.entries())
        // Retrieve image encoding
        const srcImage = image.src;
        // Send an AJAX request to save the image
        $.ajax({
            headers: { 
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=utf-8', 
            },
            type: "POST",
            url: '/save_image',
            data:JSON.stringify({
                "form":form,
                "src":srcImage}),
        // Handle successful response
            success: function () {
                show_message("image_save_feedback","Your image was saved")
            },
        // Handle failed response
            error: function(data){
                answer = JSON.parse(data['responseText'])
                make_unclickable('dialogue_unclickable')
                var error_text = document.getElementById("error_text_save_image");
                var error_message = '<p id="errror_image_plot">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("save_image_error").style.display="inline-block";
            }
    });
    });
    
});


function add_options(){

    const columns = document.getElementById("column_interest");
    const csvColumns = document.getElementById("column_list_ul");

      
    // Check if both elements exist
    if (columns && csvColumns) {
        // Clear existing options
        columns.innerHTML = '';
        
        // Iterate over list items and create options
        csvColumns.querySelectorAll("li").forEach(function(item) {
            const option = document.createElement("option");
            option.value = item.textContent;
            option.textContent = item.textContent;
            columns.appendChild(option);
        });
    }
}


$(document).on('submit','#delete_image_form',function(e)
{   // Prevent default form submission behavior
    e.preventDefault(); 
     // Retrieve the delete button and its value

    let button = document.getElementById("delete_image_button");
    let button_value = button.value;
    // Send an AJAX POST request to delete the image

    $.ajax({
        type:'POST',
        url:'/delete/' + button_value,
        success:function()
        {   
            // Upon successful deletion, remove the corresponding list item
            button.closest('li').remove()
        },
        error:function(){
            alert("something went wrong")
        }
    })
});


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