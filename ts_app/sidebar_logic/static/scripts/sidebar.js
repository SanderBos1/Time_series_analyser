

function csv_button_click(value) {
    // Get the currently selected file display element
    var current_selected = document.getElementById('file_display_selected');
    // If there's already a selected file, remove its id attribute
    if (current_selected) {
        current_selected.removeAttribute('id', "file_display_selected");
    }
    // Set the id attribute of the the clicked CSV file button

    value.setAttribute('id', "file_display_selected");
    $.ajax({
        type: "GET",
        // URL to fetch columns based on the value of the clicked button
        url: '/columns/' + value.value,
        success: function (data) {
            // Get the UL element where columns will be displayed
            var ul = document.getElementById("column_list_ul");
            // Clear the UL contents
            ul.innerHTML = "";
            // Iterate over columns data and create list items for each column
            for (var column_number in data) {
                var li = document.createElement("li");
                li.className = "dataset";
                column = data[column_number];
                li.innerHTML = column;
                ul.append(li);
            }
            // After adding columns, call add_options function 
            add_options();
        }
    });
}


function delete_csv(value){
    $.ajax({
        // AJAX request to delete the specified CSV file
        type: "POST",
        // URL to delete the CSV file based on its value
        url: '/delete_csv/' + value.value,
        success: function () {
            // Check if the currently selected file is deleted
            if(document.getElementById("file_display_selected")){
                if (value.value == document.getElementById("file_display_selected").value) {
                    // If the deleted file was selected, remove the associated columns list
                    var ul= document.getElementById("column_list_ul");
                    ul.innerHTML = ""
                }

            }
            // Clear the CSV list to update it after deletion
            list = document.getElementById("csv_list_ul");
            list.innerHTML = ""
            // Reload the CSV list and data after deletion
            load_csvdata()
    }
    });
};

/* 

    Goal: add the columns of the selected csv file to the options of the forms that need it.

*/


function load_csvdata() {
    // AJAX request to get CSV files data
    $.ajax({
        type:'Get',
        url:'/get_csvfiles',
        success:function(data)
        {   
            // Find the list where CSV files will be displayed
            var list = $("#data-directory-list").find('ul');
            // Get the UL element for CSV file list
            var ul = document.getElementById("csv_list_ul");
            // Clear the UL contents
            ul.innerHTML = ""
            // Iterate over CSV files data and create list items for each file
            for (var csv_number in data) {
                // Create HTML for each CSV file item, including buttons for display and deletion
                var li = document.createElement("li");
                li.className = "csv_file_list_item";
                csv = data[csv_number];
                li.innerHTML = "<div>" + "<form id=file_list_and_delete method=post>"+
                "<button class='file_display' value='"  + csv + "' onClick='csv_button_click(this);return false;'>" + csv + "</button>" +
                "<button id=delete_file class='delete_standard dialogue_unclickable' name=delete_file value='" + csv + "' onClick='delete_csv(this);return false;'>X</button>" + "</form>" +
                    "</div>"
                // Append the created list item to the list
                list.append(li);
            }

        }
    })


}



$(document).ready(function() {
    $('#upload_form').submit(function (e) {
        e.preventDefault()
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

    })
});




$(document).ready(function() {
    load_csvdata(); // Load CSV data when the document is ready
    
    // When the entire page (including images and other resources) is loaded
    window.addEventListener('load', function() {
        var csv_list = document.getElementsByClassName('file_display');
        setTimeout(function() {
            var csv_list = document.getElementsByClassName('file_display');
            if (csv_list.length > 0) {
                // If CSV file buttons exist, trigger a click event on the first one
                csv_button_click(csv_list[0]);
            }
        }, 50); 
    });
});



