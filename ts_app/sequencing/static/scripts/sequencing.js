function show_save_dialogue(){
    var save_dialogue = document.getElementById("image_trendresidual_save_form")
    save_dialogue.style.display = "inline-block";
}


function save_residuals(){
    var dataset = document.getElementById("file_display_selected").value
    var var_column = document.getElementById("residual_column_intrest").value
    $.ajax({
        type: "POST",
        url: '/trend/add_residuals/' + dataset + "/" + var_column,
        success: function (data) {
            console.log(data)
            if (data["answer"] == "Saved."){
                show_message("save_residualcsv_feedback",data['message'])
            }
            else{
                if(document.getElementById('error_trend_residual_plot_message')){
                    document.getElementById('error_trend_residual_plot_message').remove();
                }
                make_unclickable("error_unclickable")
                error_message = document.getElementById("plot_trend_residual_error")
                error_message.style.display="inline-block"
                var text = document.createElement("p");
                text.setAttribute("id", "error_trend_residual_plot_message")
                text.innerHTML = data["message"];
                error_message.appendChild(text)
            }
        }
    });
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
                    if(document.getElementById('trend_calculation_error')){
                        document.getElementById('trend_calculation_error').style.display="none";
                    }
                    var trend_value = document.getElementById("trend_value")
                    trend_value.innerHTML = data["p_value"]
                    var hypotheses = document.getElementById("hypothese_trend")
                    hypotheses.innerHTML = data["Hypotheses"]
                }
                else{
                    if(document.getElementById('error_trend_calculation_message')){
                        document.getElementById('error_trend_calculation_message').remove();
                    }
                    make_unclickable("error_unclickable")
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
    });
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
                    make_unclickable("error_unclickable")
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
        e.preventDefault(); 

        var dataset = document.getElementById("file_display_selected").value
        $.ajax({
            headers: { 
                "X-CSRFToken" : "{{ form.csrf_token._value() }}"
            },
            type: "POST",
            url: '/trend/residuals/' + dataset ,
            data: $('form').serialize(), 
            success: function (data) {
                if(data["message"] == "The image has been created."){
                    const img_div = document.getElementById("residuals_trend_div");
                    img_div.innerHTML = "<img class=standard_img id=trend_picture src=data:image/jpeg;base64," + data["img"] + ">";
                    document.getElementById("save_image_trend").style.display="inline-block";
                }
                else{
                    if(document.getElementById('error_trend_residual_plot_message')){
                        document.getElementById('error_trend_residual_plot_message').remove();
                    }
                    make_unclickable("error_unclickable")
                    error_message = document.getElementById("plot_trend_residual_error")
                    error_message.style.display="inline-block"
                    var text = document.createElement("p");
                    text.setAttribute("id", "error_trend_residual_plot_message")
                    text.innerHTML = data["message"];
                    error_message.appendChild(text)
                }
            }
        });

    })
});


function add_options(){
    var columns = document.getElementById("column_intrest");
    if(document.getElementById("residual_column_intrest")){
        var columns_draw = document.getElementById("residual_column_intrest");
        columns_draw.textContent = '';
        var show = "True";
    }
    columns.textContent = '';
    var csv_columns = document.getElementById("column_list_ul")
    var list = csv_columns.getElementsByTagName("li")
    for(let i = 0; i < list.length; i++){
        var option = list[i].innerHTML
        const element = document.createElement("option");
        element.value = option;
        element.innerHTML = option;
        columns.appendChild(element)
        if(Boolean(show)){
            var option2 = list[i].innerHTML
            const element2 = document.createElement("option");
            element2.value = option2;
            element2.innerHTML = option2;
            columns_draw.appendChild(element2)
        }

    }
}

$(document).ready(function() {
    $('#save_residual_image_form').submit(function (e) {
        image = document.getElementById("trend_picture")
        const data = new FormData(save_residual_image_form);
        form = Object.fromEntries(data.entries())
        src_image = image.src
        $.ajax({
            headers: { 
                'Accept': 'application/json',
                'Content-Type': 'application/json', 
            },
            type: "POST",
            url: '/save_image',
            data:JSON.stringify({
                "form":form,
                "src":src_image
            }),
            success: function (answer) {
                if(answer['message'] == "Image is saved."){
                    show_message("resimg_save_result_feedback",answer['message'] )
                }
            else{
                if(document.getElementById('error_text_save')){
                    document.getElementById('error_text_save').remove();
                }
                var error_text = document.getElementById("save_residual_image_error");
                var text = document.createElement("p");
                text.setAttribute("id", "error_text_save")
                text.innerHTML = answer['message'];
                error_text.appendChild(text)
                error_text.style.display="inline-block";
            }
        }
        });
        e.preventDefault(); 
    });

});
