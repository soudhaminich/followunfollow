
$(document).ready(function(){
    $("a").on('click', function(){
    console.log('Testing....')
    var this_ = $(this);
    console.log(this_);
    var commentUrl = this_.attr("href");
    console.log(commentUrl)
    $.ajax({
        data: {
            csrfmiddlewaretoken:getCookie('csrftoken'),
        },
        url: favoriteUrl,
        method: "POST",
        success: function(data){

                    console.log(data)
        }

    })
    
    // $.ajax({
    
    //     url: favoriteUrl,
    //     method: "GET",
    //     success: function(data){
    
    //       console.log(data);
    //       $.each(data , function(){
    //         $(this_).attr("href", String(data.url));
    //         $(this_).attr("style", "font-size:24px;float: right;color:"+String(data.color));
    
    //       })
    //     },
    //     error: function(data){
    //       console.log(data)
    //       console.log(error)
    //     }
    // })
    })
    });

function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }