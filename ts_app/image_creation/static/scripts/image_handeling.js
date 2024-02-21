
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