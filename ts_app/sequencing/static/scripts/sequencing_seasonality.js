function add_options(){
    var columns = document.getElementById("column_intrest");
    columns.textContent = '';
    var dataset = document.getElementById("dataset");
    dataset.textContent = '';
    var time_column = document.getElementById("time_column");
    time_column.textContent = '';
    dataset.setAttribute('value', document.getElementById("file_display_selected").value)
    var csv_columns = document.getElementById("column_list_ul")
    var list = csv_columns.getElementsByTagName("li")
    for(let i = 0; i < list.length; i++){
        var option = list[i].innerHTML
        const element = document.createElement("option");
        const element2 = document.createElement("option");
        element.value = option;
        element2.value = option;
        element.innerHTML = option;
        element2.innerHTML = option;
        columns.appendChild(element)
        time_column.appendChild(element2)

    }
}


$(document).ready(function() {
    $('#seasonality_form').submit(function (e) {
        $.ajax({
            type: "POST",
            url: '/seasonality/calculate',
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                if(data=="something went wrong"){
                    document.getElementById("seasonality_answers").style.display="none"
                    document.getElementById("Error").style.display="inline"
                }
                else{
                document.getElementById("Error").style.display="none"
                document.getElementById("seasonality_answers").style.display="inline"
                var trend_value = document.getElementById("seasonality_value")
                trend_value.innerHTML = data.p_value 
                var hypotheses = document.getElementById("hypothese_seasonality")
                hypotheses.innerHTML = data.Hypotheses 
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