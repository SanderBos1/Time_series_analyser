$(document).ready(function() {
    $('#trend_form').submit(function (e) {
        $.ajax({
            type: "POST",
            url: '/trend/calculate',
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                if(data=="something went wrong"){
                    document.getElementById("trend_answers").style.display="none"
                    document.getElementById("Error").style.display="inline"
                }
                else{
                document.getElementById("Error").style.display="none"
                document.getElementById("trend_answers").style.display="inline"
                var trend_value = document.getElementById("trend_value")
                trend_value.innerHTML = data.p_value 
                var hypotheses = document.getElementById("hypothese_trend")
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


function add_options(){
    var columns = document.getElementById("column_intrest");
    columns.textContent = '';
    var dataset = document.getElementById("dataset");
    dataset.textContent = '';
    dataset.setAttribute('value', document.getElementById("file_display_selected").value)
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

