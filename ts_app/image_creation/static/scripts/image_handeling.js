
$(document).ready(function() {
    $('#image_save_form').submit(function (e) {
        console.log("test")

        $.ajax({
            type: "POST",
            url: '/save_image/',
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



$(document).ready(function() {
    $('#image_draw_form').submit(function (e) {
        console.log("test")

        $.ajax({
            type: "POST",
            url: '/make_image',
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

function add_options(){
    var columns = document.getElementById("columns");
    columns.textContent = '';
    var time_columns = document.getElementById("time_columns");
    console.log(time_columns)
    console.log(columns)
    time_columns.textContent = '';
    var csv_columns = document.getElementById("column_list_ul")
    var list = csv_columns.getElementsByTagName("li")
    for(let i = 0; i < list.length; i++){
        var option = list[i].innerHTML
        const element = document.createElement("option");
        const element_2 = document.createElement("option");
        element.value = option;
        element_2.value = option;
        element.innerHTML = option;
        element_2.innerHTML = option;
        time_columns.appendChild(element)
        columns.appendChild(element_2)
    }
}
