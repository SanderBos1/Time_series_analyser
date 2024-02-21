$(document).on('submit','#delete_image_form',function(e)
{   let button = document.getElementById("delete_image_button");
    let button_value = button.value;
    console.log(button_value);
    e.preventDefault();
    $.ajax({
        type:'POST',
        url:'/delete/' + button_value,
        success:function()
        {
            button.closest('li').remove()
        }
    })
});


window.onload = function() {
    $.ajax({
        type:'Get',
        url:'/get_images/',
        success:function(data)
        {   
            var list = $("#image-list").find('ul');
            for(var image in data){
                var li = document.createElement("li");
                li.className = "image";
                image_ojb = data[image];
                li.innerHTML =  "<div class=name_and_delete>" +  
                "<p>" + image + "</p>" +
                "<form method=POST id=delete_image_form>" +  
                "<button name=delete_image id=delete_image_button value =" + image +" > X </button>" +
                "</form>" + "</div>" +
                "<img class=image_list_image src=data:image/jpeg;base64," + image_ojb + ">";
                list.append(li);
            }

        }
    })
  };
