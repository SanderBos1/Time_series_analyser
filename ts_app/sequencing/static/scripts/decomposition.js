
$(document).ready(function() {
    $('#make_csv_residuals_form').submit(function (e) {
        e.preventDefault(); 
        var dataset = document.getElementById("file_display_selected").value
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/add_residuals/' + dataset ,
            data: $('form').serialize(), 
            success: function (data) {
                if(data["answer"] == "Saved."){
                    const feedback_text = document.getElementById("trend_file_made_feedback_text");
                    feedback_text.innerHTML = "Your residual object is saved."
                }
                else{
                    make_unclickable("error_unclickable")
                    var error_text = document.getElementById("error_making_residual_csv");
                    var error_message = '<p id="error_trend_residual_plot_message">' +  data["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("make_stationary_csv_error").style.display="inline-block";
                }
            }
        });

    })
});




function add_options(){
	var columns_draw = document.getElementById("residual_column_intrest");
	columns_draw.textContent = '';
	var csv_columns = document.getElementById("column_list_ul")
	var list = csv_columns.getElementsByTagName("li")
	for(let i = 0; i < list.length; i++){
		var option = list[i].innerHTML
		const element = document.createElement("option");
		element.value = option;
		element.innerHTML = option;
		columns_draw.appendChild(element)
	}
}
