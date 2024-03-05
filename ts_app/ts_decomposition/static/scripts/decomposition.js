$(document).ready(function() {
    $('#make_csv_residuals_form').submit(function (e) {
        e.preventDefault(); 
        var dataset = document.getElementById("file_display_selected").value
        if (!dataset) {
            // Display an error message for invalid input
            make_unclickable("error_unclickable")
            var error_text = document.getElementById("error_making_residual_csv");
            var error_message = '<p id="error_trend_residual_plot_message">' +  "No dataset selected." + "</p>";
            error_text.innerHTML = error_message;
            document.getElementById("make_stationary_csv_error").style.display="inline-block";
            return;
        }
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/add_residuals/' + dataset ,
            data: $('form').serialize(), 
            success: function (data) {
                // Display a success message
                const feedback_text = document.getElementById("trend_file_made_feedback_text");
                 feedback_text.innerHTML = "Your residual object is saved."
                // Reload the CSV data on the sidebar
                load_csvdata()
            },
            error: function(data){
                 // Handle errors
                answer = JSON.parse(data['responseText'])
    
                var error_text = document.getElementById("error_making_residual_csv");
                var error_message = '<p id="error_trend_residual_plot_message">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("make_stationary_csv_error").style.display="inline-block";
                // Make certain elements unclickable in case of error
                make_unclickable("error_unclickable")
            }
        });

    })
});

function add_options(){
	var columns_draw = document.getElementById("residual_column_intrest");
    // Clear previous options
	columns_draw.innerHTML  = '';
	var csv_columns = document.getElementById("column_list_ul")
	var list = csv_columns.getElementsByTagName("li")
    Array.from(list).forEach(function(item) {
        var optionText = item.textContent;
        var option = new Option(optionText, optionText);
        columns_draw.appendChild(option);
    });
}
