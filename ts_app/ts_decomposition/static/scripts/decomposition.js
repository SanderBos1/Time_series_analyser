function select_column(pressed_column) {
    if (document.getElementById("column_selected")) {
        document.getElementById("column_selected").removeAttribute('id', "column_selected")
    }
    pressed_column.setAttribute('id', "column_selected");
}

$(document).ready(function () {
    $('#make_csv_residuals_form').submit(function (e) {
        e.preventDefault();
        if (document.getElementById("column_selected")) {
            var dataset = document.getElementById("file_display_selected").value
            var column = document.getElementById("column_selected").value
            $.ajax({
                headers: {
                    "X-CSRFToken": "{{ form.csrf_token._value() }}"
                },
                type: "POST",
                url: '/add_residuals/' + dataset + "/" + column,
                data: $('form').serialize(),
                success: function (data) {
                    // Display a success message
                    var ts_image = document.getElementById("plot_before")
                    var ts_image_after = document.getElementById("plot_after")
                    ts_image.innerHTML = "<img class=standard_img id=ts_img src=data:image/jpeg;base64," + data["ts_img"] + ">";
                    ts_image_after.innerHTML = "<img class=standard_img id=ts_img src=data:image/jpeg;base64," + data["ts_img_after"] + ">";
                    const feedback_text = document.getElementById("trend_file_made_feedback_text");
                    feedback_text.innerHTML = "Your residual object is saved."
                    // Reload the CSV data on the sidebar
                    load_csvdata()
                },
                error: function (data) {
                    // Handle errors
                    answer = JSON.parse(data['responseText'])
                    console.log(answer)

                    var error_text = document.getElementById("error_making_residual_csv");
                    var error_message = '<p id="error_trend_residual_plot_message">' + answer["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("make_stationary_csv_error").style.display = "inline-block";
                    // Make certain elements unclickable in case of error
                    make_unclickable("error_unclickable")
                }
            });

        }
        else {
            alert("No column selected")
        }


    })
});

