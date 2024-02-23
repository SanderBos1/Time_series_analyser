
window.addEventListener('load', function() {
    var csv_list = document.getElementsByClassName('file_display');
    console.log(csv_list)
    console.log(csv_list[0])
    if(csv_list[0]){
        csv_button_click(csv_list[0])
    }

    })



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
                "<button class=file_display  value=" + csv + " onClick='csv_button_click(this);return false;'>" + csv + "</button>" +
                "<button id=delete_file class=delete_standard name=delete_file value=" + csv + " onClick='delete_csv(this);return false;'>X</button>" + "</form>" +
                "</div>"
                list.append(li);
            }

        }
    })


}

$(document).ready(function() {
    load_csvdata()

  });


