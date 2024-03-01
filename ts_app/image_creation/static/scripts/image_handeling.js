function enlarge_image(element){
    element.removeAttribute("onclick")
    var image = element.closest(".image")
    image.classList.add("fullscreen_image")
    image.classList.remove("image")
    element.onclick = function(){small_image(this)};

}

function small_image(element){
    element.removeAttribute("onclick")
    var image = element.closest(".fullscreen_image")
    image.classList.add("image")
    image.classList.remove("fullscreen_image")
    element.onclick = function(){enlarge_image(this)};

}
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
            success: function (answer) {
                if(answer['message'] == "The image is uploaded."){
                    const img_div = document.getElementById("image_div");
                    img_div.innerHTML = "<img class=standard_img id=picture src=data:image/jpeg;base64," + answer["img"] + ">";
                    if(document.getElementById("image_error")){
                        document.getElementById("image_error").style.display="none";
                    }
                    document.getElementById("save_image_dialogue_button").style.display="inline-block";

                } 
                else{
                    if(document.getElementById('errror_image_plot')){
                        document.getElementById('errror_image_plot').remove();
                    }
                    var error_text = document.getElementById("image_error");
                    var text = document.createElement("p");
                    text.setAttribute("id", "errror_image_plot")
                    text.innerHTML = answer["message"];
                    error_text.appendChild(text)
                    error_text.style.display="inline-block";
                }
            }
    })

    });
});


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
                if(document.getElementById('error_text_save')){
                    document.getElementById('error_text_save').remove();
                }
                var error_text = document.getElementById("save_image_error");
                var text = document.createElement("p");
                text.setAttribute("id", "error_text_save")
                text.innerHTML = answer['message'];
                error_text.appendChild(text)
                error_text.style.display="inline-block";
            }
        }
    });
    });
    
});



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


window.onload = function() {
    $.ajax({
        type:'Get',
        url:'/get_images/',
        success:function(data)
        {  
            if(data["images"].length !=0){
                var list = $("#image-list").find('ul');
                for(var image in data["images"]){
                    var li = document.createElement("li");
                    li.className = "image";
                    image_ojb = data["images"][image];
                    li.innerHTML =  "<div class=name_and_delete>" +  
                    "<p>" + image + "</p>" +
                    "<form method=POST id=delete_image_form>" +  
                    "<button name=delete_image id=delete_image_button class=delete_standard value =" + image +" > X </button>" +
                    "</form>" + "</div>" +
                    "<div onClick=enlarge_image(this) class=image_list_image >"+
                    "<img class=standard_img src=" + image_ojb + ">" +
                    "</div>";
                    list.append(li);
            }
        }
        else{
            if(document.getElementById('error_loading_images')){
                document.getElementById('error_loading_images').remove();
            }
            var error_text = document.getElementById("display_images_error");
            var text = document.createElement("p");
            text.setAttribute("id", "error_loading_images")
            text.innerHTML = "Something went wrong";
            error_text.appendChild(text)
            error_text.style.display="inline-block";

        }


        }
    })
  };
