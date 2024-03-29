function select_column(pressed_column) {
    if (document.getElementById("column_selected")) {
        document.getElementById("column_selected").removeAttribute('id', "column_selected")
    }
    pressed_column.setAttribute('id', "column_selected");
    document.getElementById('column').innerHTML = pressed_column.value
}

$(document).ready(function() {
    $('#image_draw_form').submit(function (e) {
        e.preventDefault()
        //Retrieves the dataset that is going to be used
        var dataset = document.getElementById("file_display_selected").value
        if (document.getElementById("column_selected")) {
            var column = document.getElementById("column_selected").value
            //Retrieves the form that is going to be send to the backend
            var form = new FormData($(this)[0])
            $.ajax({
                headers: {
                    "X-CSRFToken": "{{ form.csrf_token._value() }}",
                },
                type: "POST",
                url: '/make_image/' + dataset + "/" + column,
                data: form,
                processData: false,
                contentType: false,
                // Handle successful response

                success: function (data) {
                    const img_div = document.getElementById("image_div");
                    img_div.innerHTML = "<img class=standard_img id=picture src=data:image/jpeg;base64," + data["img"] + ">";
                    document.getElementById("save_image_dialogue_button").style.display = "inline-block";
                },
                // Handle failed response
                error: function (data) {
                    answer = JSON.parse(data['responseText'])
                    make_unclickable('dialogue_unclickable')
                    var error_text = document.getElementById("error_text_draw_image");
                    var error_message = '<p id="errror_image_plot">' + answer["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("image_error").style.display = "inline-block";
                }
            });
        }
        else{
             alert("no column selected")
        }
    })

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



