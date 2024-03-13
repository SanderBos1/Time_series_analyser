$(document).ready(function () {
    $('#register_form').submit(function (e) {
        e.preventDefault()
        console.log("test")
        var form = new FormData($(this)[0])
        // AJAX request to submit the form data
        $.ajax({
            beforeSend: function (xhr, settings) {
                // Add CSRF token to the request headers if not a safe HTTP method or cross-domain request
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}");
                }
            },
            type: 'POST',
            url: 'register_user',
            data: form,
            processData: false,
            contentType: false,
            success: function (data) {
                alert("you have registered")
            },
            error: function (data) {
                console.log(data)
            }
              
        })

    })
});
