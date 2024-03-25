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
                    $("#plot_before").html("<img class=standard_img id=autocorrelation_image src=data:image/jpeg;base64," + data["ts_img"] + ">");
                    $("#plot_after").html("<img class=standard_img id=autocorrelation_image src=data:image/jpeg;base64," + data["ts_img_after"] + ">");
                    $("#trend_file_made_feedback_text").html("Your residual object is saved.")
                    // Reload the CSV data on the sidebar
                    load_csvdata()
                },
                error: function (data) {
                    answer = JSON.parse(data['responseText'])
                    make_unclickable("error_unclickable")
                    $("#error_making_residual_csv").html('<p id="error_trend_residual_plot_message">' + answer["message"] + "</p>");
                    $( '#make_stationary_csv_error' ).show();
                }
            });

        }
        else {
            alert("No column selected")
        }


    })
});

