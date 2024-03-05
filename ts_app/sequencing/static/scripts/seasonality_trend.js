function show_save_dialogue(){
    var save_dialogue = document.getElementById("image_trendresidual_save_form")
    save_dialogue.style.display = "inline-block";
}

/* 
Gives the two variables that display p value and the hypotheses calculation there default values.
*/
function reset_var_pvalue(var_1, var_2){
    var trend_value = document.getElementById(var_1)
    trend_value.innerHTML = "Not yet defined."
    var hypotheses = document.getElementById(var_2)
    hypotheses.innerHTML  = "Not yet defined."
}

$(document).ready(function() {
    $('#statistical_trend_form').submit(function (e) {
        e.preventDefault(); 
        var dataset = document.getElementById("file_display_selected").value
        var form = new FormData($(this)[0])
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/trend/calculate/' + dataset,
            data:form,
            processData: false,
            contentType: false,            
            success: function (data) {
                
                if(data['message']=="Calculated."){
                    var trend_value = document.getElementById("trend_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_trend")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    make_unclickable("error_unclickable")
                    document.getElementById("trend_value").innerHTML = data["p_value"]
                    document.getElementById("hypothese_trend").innerHTML = data["Hypotheses"]
                    var error_text = document.getElementById("error_trend_pvalue");
                    var error_message = '<p id="errror_trend_pvalue">' +  data["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("trend_calculation_error").style.display="inline-block";
                }
            }
        });
    });
});


$(document).ready(function() {
    $('#seasonality_form').submit(function (e) {
        e.preventDefault(); 
        var dataset = document.getElementById("file_display_selected").value
        var form = new FormData($(this)[0])
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/seasonality/calculate/' + dataset,
            data: form, // serializes the form's elements.
            processData: false,
            contentType: false,
            success: function (data) {
                if(data['message']=="Calculated."){
                    var trend_value = document.getElementById("seasonality_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_seasonality")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    make_unclickable("error_unclickable")
                    document.getElementById("seasonality_value").innerHTML = data["p_value"]
                    document.getElementById("hypothese_seasonality").innerHTML = data["Hypotheses"]
                    var error_text = document.getElementById("error_seasonality_pvalue");
                    var error_message = '<p id="errror_seasonality_pvalue">' +  data["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("seasonality_calculation_error").style.display="inline-block";
                }
            }
        });
    });
});


$(document).ready(function() {
    $('#stationarity_form').submit(function (e) {
        e.preventDefault(); 
        var dataset = document.getElementById("file_display_selected").value
        var form = new FormData($(this)[0])
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/stationarity/calculate/' + dataset,
            data:form,
            processData: false,
            contentType: false,
            success: function (data) {
                if(data['message']=="Calculated."){
                    var trend_value = document.getElementById("stationarity_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_stationarity")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    make_unclickable("error_unclickable")
                    document.getElementById("seasonality_value").innerHTML = data["p_value"]
                    document.getElementById("hypothese_seasonality").innerHTML = data["Hypotheses"]
                    var error_text = document.getElementById("error_stationarity_pvalue");
                    var error_message = '<p id="errror_seasonality_pvalue">' +  data["message"] + "</p>";
                    error_text.innerHTML = error_message;
                    document.getElementById("stationarity_calculation_error").style.display="inline-block";
                }
            }
        });
    });
});

/* 

    Goal: 
    On the delete button click next to the csv file, 
    it will delete the html element and the csv file from the dataset.
*/


function add_options(){
    const columns = [document.getElementById("seasonality_column_var"),document.getElementById("trend_column_var"),document.getElementById("stationarity_column_var")] ;
    for(let column in columns){
        columns[column].textContent = '';
    }
    var csv_columns = document.getElementById("column_list_ul")
    var list = csv_columns.getElementsByTagName("li")
    for(let i = 0; i < list.length; i++){
        for(let j = 0; j < columns.length; j++){
            var option = list[i].innerHTML
            const element = document.createElement("option");
            element.value = option;
            element.innerHTML = option;
            columns[j].appendChild(element)
        }
    }
}

