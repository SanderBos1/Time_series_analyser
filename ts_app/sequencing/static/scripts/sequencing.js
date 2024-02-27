$(document).ready(function() {
    $('#trend_form').submit(function (e) {
        var dataset = document.getElementById("file_display_selected").value
        $.ajax({
            type: "POST",
            url: '/trend/calculate/' + dataset,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                if(data['message']=="Calculated."){
                    var trend_value = document.getElementById("trend_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_trend")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    if(document.getElementById('error_trend_calculation_message')){
                        document.getElementById('error_trend_calculation_message').remove();
                    }
                    var trend_value = document.getElementById("trend_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_trend")
                    hypotheses.innerHTML = data["Hypotheses"]
                    var error_text = document.getElementById("trend_calculation_error");
                    var text = document.createElement("p");
                    text.setAttribute("id", "error_trend_calculation_message")
                    text.innerHTML = data["message"];
                    error_text.appendChild(text)
                    error_text.style.display="inline-block";
                }
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
    $('#seasonality_form').submit(function (e) {
        var dataset = document.getElementById("file_display_selected").value
        $.ajax({
            type: "POST",
            url: '/seasonality/calculate/' + dataset,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                if(data['message']=="Calculated."){
                    var trend_value = document.getElementById("seasonality_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_seasonality")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    if(document.getElementById('error_seasonality_calculation_message')){
                        document.getElementById('error_seasonality_calculation_message').remove();
                    }
                    var trend_value = document.getElementById("seasonality_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_seasonality")
                    hypotheses.innerHTML = data["Hypotheses"]
                    var error_text = document.getElementById("seasonality_calculation_error");
                    var text = document.createElement("p");
                    text.setAttribute("id", "error_seasonality_calculation_message")
                    text.innerHTML = data["message"];
                    error_text.appendChild(text)
                    error_text.style.display="inline-block";
                }
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
    $('#draw_residul_form').submit(function (e) {
        var dataset = document.getElementById("file_display_selected").value
        var var_column = document.getElementById("column_intrest").value
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
                }
            },
            type: "POST",
            url: '/trend/residuals/' + dataset + "/" + var_column,
            data: $('form').serialize(), 
            success: function (data) {
                const img_div = document.getElementById("residuals_trend_div");
                img_div.innerHTML = "<img id=picture src=data:image/jpeg;base64," + data + ">";
            }
        });
        e.preventDefault(); 

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

