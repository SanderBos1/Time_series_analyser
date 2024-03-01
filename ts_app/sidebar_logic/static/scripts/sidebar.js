
function show_upload(){
    var save_dialogue = document.getElementById("upload_csv_dialogue");
    save_dialogue.style.display="inline-block";
}




  function csv_button_click(value){
    var current_selected = document.getElementById('file_display_selected')
    if(current_selected){
        current_selected.removeAttribute('id', "file_display_selected")
    }
    value.setAttribute('id', "file_display_selected");
    $.ajax({
        type: "GET",
        url: '/columns/' + value.value,
        success: function (data) {
            var ul = document.getElementById("column_list_ul")
            ul.innerHTML = "";
            for(var column_number in data){
                var li = document.createElement("li");
                li.className = "dataset";
                column = data[column_number];
                li.innerHTML =  column   
                ul.append(li);
        }
        add_options()

    }

    });
};

function delete_csv(value){
    $.ajax({
        type: "POST",
        url: '/delete_csv/' + value.value,
        success: function () {
            if(document.getElementById("file_display_selected")){
                if(value.value == document.getElementById("file_display_selected").value){
                    var ul= document.getElementById("column_list_ul");
                    ul.innerHTML = ""
                }

            }
            list = document.getElementById("csv_list_ul");
            list.innerHTML = ""
            load_csvdata()

    }
    });
};


function load_csvdata(){
    $.ajax({
        type:'Get',
        url:'/get_csvfiles',
        success:function(data)
        {   
            var list = $("#data-directory-list").find('ul');
            var ul= document.getElementById("csv_list_ul");
            ul.innerHTML = ""
            for(var csv_number in data){
                var li = document.createElement("li");
                li.className = "csv_file_list_item";
                csv = data[csv_number];
                li.innerHTML = "<div>" + "<form id=file_list_and_delete method=post>"+
                "<button class='file_display dialogue_unclickable' value=" + csv + " onClick='csv_button_click(this);return false;'>" + csv + "</button>" +
                "<button id=delete_file class='delete_standard dialogue_unclickable' name=delete_file value=" + csv + " onClick='delete_csv(this);return false;'>X</button>" + "</form>" +
                "</div>"
                list.append(li);
            }

        }
    })


}



$(document).ready(function() {
    $('#upload_form').submit(function (e) {
        var form = new FormData($(this)[0])
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken",  "{{ form.csrf_token._value() }}");
                }
            },
            type:'POST',
            url:'/upload',
            data: form, 
            processData: false,
            contentType: false,
            success:function(data)
            {
                load_csvdata()
            }
        })
        e.preventDefault()

    })
});







$(document).ready(function() {
    load_csvdata()
      
window.addEventListener('load', function() {

    var csv_list = document.getElementsByClassName('file_display');

    if(csv_list[0]){
        csv_button_click(csv_list[0])
    }

    })

  });



