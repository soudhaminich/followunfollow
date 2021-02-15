
$(document).ready(function(){
    $("a").on('click', function(){
    console.log('Testing....')
    var this_ = $(this);
    console.log(this_);
    var commentUrl = this_.attr("href");
    console.log(commentUrl)
    
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