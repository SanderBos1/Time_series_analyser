// Adds on click events to buttons



document.addEventListener("DOMContentLoaded", function() {
    function addButtonClickListener(buttonId, dialogueId) {
        var button = document.getElementById(buttonId);
        if (!button) {
            console.error("Button with ID " + buttonId + " not found.");
            return;
        }
        button.addEventListener("click", function() {
            show_dialogue(dialogueId, 'true');
        });
    }

    addButtonClickListener("statest_trend_button", "stattest_trend_dialogue");
    addButtonClickListener("statest_seasonality_button", "stattest_seasonality_dialogue");
    addButtonClickListener("statest_stationarity_button", "stattest_stationarity_dialogue");
});

function reset_var_pvalue(pValueElementId, hypothesesElementId) {
    var pValueElement = document.getElementById(pValueElementId);
    var hypothesesElement = document.getElementById(hypothesesElementId);

    // Check if elements exist before attempting to reset their values
    if (!pValueElement || !hypothesesElement) {
        console.error("One or both elements not found.");
        return;
    }

    // Reset values to default
    pValueElement.innerHTML = "Not yet defined.";
    hypothesesElement.innerHTML = "Not yet defined.";
}

$(document).ready(function() {
    $('#statistical_trend_form').submit(function (e) {
        e.preventDefault(); 

        var dataset = document.getElementById("file_display_selected").value
        var form = new FormData($(this)[0])
        
        // Validate the selected dataset
        if (!dataset) {
            console.error("No dataset selected.");
            return;
        }
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
                // Display trend value and hypotheses
                document.getElementById("trend_value").innerHTML = data["p_value"];
                document.getElementById("hypothese_trend").innerHTML = data["Hypotheses"];
            },
            error: function(data){
                // Handle errors
                answer = JSON.parse(data['responseText'])
                make_unclickable("error_unclickable")
                document.getElementById("trend_value").innerHTML = "Not yet defined"
                document.getElementById("hypothese_trend").innerHTML = "Not yet defined"
                var error_text = document.getElementById("error_trend_pvalue");
                var error_message = '<p id="errror_trend_pvalue">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("trend_calculation_error").style.display="inline-block";

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
                // Display trend value and hypotheses
                document.getElementById("seasonality_value").innerHTML = data["p_value"];
                document.getElementById("hypothese_seasonality").innerHTML = data["Hypotheses"];
            },
            error: function(data){
                // Handle errors
                answer = JSON.parse(data['responseText'])
                make_unclickable("error_unclickable")
                document.getElementById("seasonality_value").innerHTML = "Not yet defined"
                document.getElementById("hypothese_seasonality").innerHTML = "Not yet defined"
                var error_text = document.getElementById("error_seasonality_pvalue");
                var error_message = '<p id="errror_seasonality_pvalue">' +  answer['message']+ "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("seasonality_calculation_error").style.display="inline-block";
    
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
                // Display trend value and hypotheses
                document.getElementById("stationarity_value").innerHTML = data["p_value"];
                document.getElementById("hypothese_stationarity").innerHTML = data["Hypotheses"];
                },
            error: function(data){
                // Handle errors
                answer = JSON.parse(data['responseText'])
                make_unclickable("error_unclickable")
                document.getElementById("seasonality_value").innerHTML = "Not yet defined"
                document.getElementById("hypothese_seasonality").innerHTML = "Not yet defined"
                var error_text = document.getElementById("error_stationarity_pvalue");
                var error_message = '<p id="errror_seasonality_pvalue">' +  answer["message"] + "</p>";
                error_text.innerHTML = error_message;
                document.getElementById("stationarity_calculation_error").style.display="inline-block";
        
                }
        });
    });
});

function add_options() {
    // Clear options for each column select element
    const columnSelects = [
        document.getElementById("seasonality_column_var"),
        document.getElementById("trend_column_var"),
        document.getElementById("stationarity_column_var")
    ];

    columnSelects.forEach(function(columnSelect) {
        if (columnSelect) {
            columnSelect.innerHTML = ''; // Clear options
        }
    });

    // Populate options from the column list
    const csvColumns = document.getElementById("column_list_ul");
    if (!csvColumns) {
        console.error("Column list element not found.");
        return;
    }

    Array.from(csvColumns.getElementsByTagName("li")).forEach(function(listItem) {
        const optionText = listItem.textContent;
        columnSelects.forEach(function(columnSelect) {
            if (columnSelect) {
                const option = new Option(optionText, optionText);
                columnSelect.appendChild(option);
            }
        });
    });
}
