$(document).ready(function() {
    $('#image_draw_form').submit(function (e) {
        var dataset = document.getElementById("file_display_selected").value

        $.ajax({
            type: "POST",
            url: '/make_image/'+ dataset,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                const img_div = document.getElementById("image_div");
                img_div.innerHTML = "<img id=picture src=data:image/jpeg;base64," + data + ">";

            }
        });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});



$(document).ready(function() {
    $('#image_save_form').submit(function (e) {
        $.ajax({
            type: "POST",
            url: '/save_image',
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                console.log(data)  // display the returned data in the console.
            }
        });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});


function add_options(){
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


$(document).on('submit','#delete_image_form',function(e)
{   let button = document.getElementById("delete_image_button");
    let button_value = button.value;
    console.log(button_value);
    e.preventDefault();
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
            var list = $("#image-list").find('ul');
            for(var image in data){
                var li = document.createElement("li");
                li.className = "image";
                image_ojb = data[image];
                li.innerHTML =  "<div class=name_and_delete>" +  
                "<p>" + image + "</p>" +
                "<form method=POST id=delete_image_form>" +  
                "<button name=delete_image id=delete_image_button class=delete_standard value =" + image +" > X </button>" +
                "</form>" + "</div>" +
                "<img class=image_list_image src=data:image/jpeg;base64," + image_ojb + ">";
                list.append(li);
            }

        }
    })
  };
