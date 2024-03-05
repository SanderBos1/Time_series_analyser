/* 
Function to make the selected image element larger.
*/

function enlarge_image(element){
    element.removeAttribute("onclick")
    var image = element.closest(".image")
    image.classList.add("fullscreen_image")
    image.classList.remove("image")
    element.onclick = function(){small_image(this)};

}


/* 
Function to make the selected image element smaller.
*/
function small_image(element){
    element.removeAttribute("onclick")
    var image = element.closest(".fullscreen_image")
    image.classList.add("image")
    image.classList.remove("fullscreen_image")
    element.onclick = function(){enlarge_image(this)};

}

/*
Send the image_draw_form to the back end and displays the image on the screen.
Input: 
    Dataset: the selected dataset
    Form: The image drawn form of the html page
On success:
    Displays plot in the image holder
On failure:
    Displays error in the error dialogue

*/
$(document).ready(function() {
    $('#image_draw_form').submit(function (e) {
        e.preventDefault()
        var dataset = document.getElementById("file_display_selected").value
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
            success: function (data) {
                const img_div = document.getElementById("image_div");
                img_div.innerHTML = "<img class=standard_img id=picture src=data:image/jpeg;base64," + data["img"] + ">";
                document.getElementById("save_image_dialogue_button").style.display="inline-block";
            },
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


/*
Retrieves the created plot as image and saves it in the backend
Input: 
    Img: The created plot
    Form: The image drawn form of the html page
On success:
    Displays plot in the image holder
On failure:
    Displays error in the error dialogue

*/

$(document).ready(function() {
    $('#save_form').submit(function (e) {
        e.preventDefault(); 
        image = document.getElementById("picture")
        const data = new FormData(save_form);
        form = Object.fromEntries(data.entries())
        src_image = image.src
        $.ajax({
            headers: { 
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=utf-8', 
            },
            type: "POST",
            url: '/save_image',
            data:JSON.stringify({
                "form":form,
                "src":src_image}),
            success: function (answer) {
                if(answer['message'] == "Image is saved."){
                    show_message("image_save_feedback","Your image was saved")

                }
            else{
                make_unclickable('dialogue_unclickable')
                var error_text = document.getElementById("error_text_save_image");
                var error_message = '<p id="errror_image_plot">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("save_image_error").style.display="inline-block";
            }
        }
    });
    });
    
});



/* 
    Adds the columns of the csv files to the list */

function add_options(){
    if(document.getElementById("column_intrest")){
    var columns = document.getElementById("column_intrest");
    columns.textContent = '';
    var csv_columns = document.getElementById("column_list_ul")
    var list = csv_columns.getElementsByTagName("li")
    for(let i = 0; i < list.length; i++){
        var option = list[i].innerHTML
        const element = document.createElement("option");
        element.value = option;
        element.innerHTML = option;
        columns.appendChild(element)
    }
}
}


/* when an image is deleted it deleted the li element that holds that image */
$(document).on('submit','#delete_image_form',function(e)
{   
    e.preventDefault();
    let button = document.getElementById("delete_image_button");
    let button_value = button.value;
    $.ajax({
        type:'POST',
        url:'/delete/' + button_value,
        success:function()
        {
            button.closest('li').remove()
        }
    })
});


/*
    This function is triggered when the window loads. It makes an AJAX request to fetch all images from the server and displays them on the front end.
*/
window.onload = function() {
    $.ajax({
        type: 'Get',
        url: '/get_images/',
        success: function(data) {  
            // Check if there are any images returned from the server
            if (data["images"].length != 0) {
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
                }
            } else {
                // If no images are returned, display an error message
                make_unclickable('dialogue_unclickable');
                var error_text = document.getElementById("error_text_load_images");
                var error_message = '<p id="errror_image_plot">' +  data["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("display_images_error").style.display = "inline-block";
            }
        }
    });
};