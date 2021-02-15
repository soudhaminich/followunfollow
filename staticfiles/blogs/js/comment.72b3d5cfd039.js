


// commentMsg.innerHTML = 'Loading...'

function handleFormSubmit(event){
    event.preventDefault()
    // console.log(event)
    const myForm = event.target
    const myFormData = new FormData(myForm)
    console.log(myFormData)
    // for (var myItem of myFormData.entries()){
    //     console.log(myItem)
    // }
    const url = myForm.getAttribute("action")
    const method  = myForm.getAttribute("method")
    // console.log(myForm.getAttribute("action"))
    const xhr = new XMLHttpRequest();
 
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
    xhr.onload = function(){
        // console.log(xhr.response)
        const newComment = xhr.response
        const newCommentJson = JSON.parse(newComment)
        // console.log(newCommentJson.id)
        // const commentEl = document.getElementById("commentid")
        // loadComments(commentEl)
        const newCommentElement = formatCommentElement(newCommentJson)
        // console.log(newCommentElement)
        // commentContainerEl.prepend(newCommentElement)
        // Append new comment with existing one
        const orgHtml = commentContainerEl.innerHTML
        commentContainerEl.innerHTML = newCommentElement + orgHtml
        myForm.reset()

        
    }
    xhr.send(myFormData)
}



const commentContainerEl = document.getElementById("commentid")
const commentCreateFormEl = document.getElementById("comment-form")

commentCreateFormEl.addEventListener("submit", handleFormSubmit)

function loadComments(commentMsg){
    const xhr = new XMLHttpRequest();
    const method = 'GET'
    const url = document.getElementById("comment-form").action
    xhr.responseType = 'json'
    xhr.open(method, url)
    // console.log(url)
    xhr.onload = function(){
    // console.log(xhr.response)
    const servResponse = xhr.response
    // console.log(xhr.response)
    var listedItems = servResponse.response
    var repliedItems = servResponse.reply_response
    // console.log(repliedItems)
    // console.log(listedItems.length)
    var finalMsgComment = "";
    var repliedMsgComment = "";
    var i = 0;
    var j = 0;
    if (listedItems.length !== 0){
        // console.log('Logging')
        for (i=0;i<listedItems.length;i++){
                
            // console.log(listedItems[i])
            if (listedItems[i].user !== "")
            {
             if (repliedItems.length !== 0){
                    
                    for (j=0;j<repliedItems.length;j++){
                        if (typeof repliedItems[j] !== "undefined"){
                            // console.log(repliedItems[j].id)
                            var repliedObj = repliedItems[j]
                            var repliedLength = repliedItems.length
                            // console.log(repliedObj)
                            // var currreplyItem = formatCommentElement(repliedObj)
                            // finalMsgComment += currreplyItem 
                            var commentObj = listedItems[i]
                            // console.log(repliedItems.length)
                            // console.log(repliedItems)
                            if (commentObj.id === repliedObj.id) {
                                // console.log(repliedObj.length)
                                    var numOfExecution = j
                                    // cosnole.log(repliedObj.reply_id)
                                    var currItem = formatCommentElement(commentObj,repliedObj,repliedLength,numOfExecution,repliedObj.id)
                                    // console.log(currItem)
                                    // finalMsgComment += currItem 
                                    // console.log(finalMsgComment)
                                    }
                            // else  {
                            //     var currItem = formatCommentElement(commentObj,0,0,0)
                                

                            // }
                            finalMsgComment += currItem 
                                                              
                            }

                        }
                      
                    
                   
                    }
            // var commentObj = listedItems[i]
            // console.log(repliedObj)
            // if (commentObj.id === repliedObj.id) {
            //         var currItem = formatCommentElement(commentObj,repliedObj)
            //         finalMsgComment += currItem 
            //         }
            // else{
            //     var currItem = formatCommentElement(commentObj,0)
            //     finalMsgComment += currItem 
            //     }
            }

        }
    }
   
        // if (repliedItems.length !== 0){

        //     for (j=0;repliedItems.length;j++){

                

        //             console.log(repliedItems[j])
                
        //     }

        // }
        commentMsg.innerHTML = finalMsgComment
    
    
    

}
xhr.send()
}

loadComments(commentContainerEl)

function LikeBtn()
{

    return "<button class='btn btn-sm'>Like</button>"
}


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

function formatCommentElement(commented,replied,numOfReply,numOfExecution,replyItemId){


    var post_id = commented.post_id
    // console.log(replied, numOfReply, numOfExecution)
    const counterIteration = numOfExecution +1
    // console.log(commented.id)
    // console.log(CSRF_TOKEN)
    // var formattedComment = "<div class='mb-4' id='comment-"+commented.id +"'"+ "><img class='rounded-circle' src='"+ commented.image +"' " +"width=40 height=40>"+"<small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
    // "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p class='card-text'>&nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;" + commented.comment + "</p>" +
    // "<a hred='#' onclick='commentReply(" +commented.id+ ",1);' id='reply-"+commented.id +"' style='color:blue'>&nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;Reply</a><div id='comment-reply-"+commented.id +"'></div><div class='container'><div class='row'><div class='col-sm-10 col-sm-offset-1'>"+
    // "<form id='reply-form-"+commented.id +"'" +">"+"<textarea row='10' class='form-control mb-2' id='textarea-"+commented.id +"' style='display:none;' rows='4' cols='50' placeholder='write your reply' ></textarea>"+
    //  "<div class='d-flex flex-row'><div class='col ml-auto text-right px-0'> <button class='d-none btn pull-right btn-primary' onclick='submitReply(" +commented.id+","+commented.post_id+ ");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div></div></div></div></div>"
    
    if (replied !== 0 ){

        if ( numOfReply === 1 ){

                var formattedComment = "<div class='media'><img class='rounded-circle mr-3' src='"+ commented.image +"' " +"width=40 height=40>"+"<div class='media-body'><small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
                "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p>" + commented.comment + "</p>" + "<div class='media mt-3'>" +
                "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                "<form action='/comment/reply/"+commented.post_id+"'"+  "method='POST' id='reply-form-"+commented.id +"'" +">"+"<textarea class='form-control mt-0 mb-2' id='textarea-"+commented.id +"'  rows='4' placeholder='write your reply' name='textarea-name"+commented.id +"'></textarea>"+
                "<input type='hidden' id='input-"+commented.post_id+"'"+ "value="+commented.post_id+"><div class='col ml-auto text-right px-0'><button class='btn pull-right btn-primary' onclick='handleReplyClick(" +commented.id+","+commented.post_id+");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div><hr class='dashed'></div></div></div></div>"
        }
        else if (counterIteration <= numOfReply ){

            // var i = 1;
            
            // do {
            //     if (i === 1){
            // console.log(i,'Testing')
            if (counterIteration === 1)
            {
                var formattedComment = "<div class='media'><img class='rounded-circle mr-3' src='"+ commented.image +"' " +"width=40 height=40>"+"<div class='media-body'><small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
                "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p>" + commented.comment + "</p>" + "<div class='media mt-3'>" +
                "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                "</div></div></div>"
            }
            else if ( counterIteration === numOfReply){
                var formattedComment = "<small class='text-muted'>&nbsp;&nbsp;</small>" + 
                "<small class='text-muted'>&nbsp; </small>" +"<p></p><div class='media mt-3'>" +
                "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                "<form action='/comment/reply/"+commented.post_id+"'"+  "method='POST' id='reply-form-"+commented.id +"'" +">"+"<textarea class='form-control mt-0 mb-2' id='textarea-"+commented.id +"'  rows='4' placeholder='write your reply' name='textarea-name"+commented.id +"'></textarea>"+
                "<input type='hidden' id='input-"+commented.post_id+"'"+ "value="+commented.post_id+"><div class='col ml-auto text-right px-0'><button class='btn pull-right btn-primary' onclick='handleReplyClick(" +commented.id+","+commented.post_id+");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div></div><hr class='dashed'></div></div></div>"
            }
            else {
                // console.log(counterIteration)
                // console.log(replied)
                var formattedComment = "<small class='text-muted'>&nbsp;&nbsp;</small>" + 
                "<small class='text-muted'>&nbsp; </small>" +"<p></p><div class='media mt-3'>" +
                "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                "</div></div><hr class='dashed'></div>"
            }
                        
                // }
          
                // else {
                // var formattedComment = "<div class='media'><div class='media-body'>" + 
                // "<div class='media mt-3'>" +
                // "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                // "<form action='/comment/reply/"+commented.post_id+"'"+  "method='POST' id='reply-form-"+commented.id +"'" +">"+"<textarea class='form-control mt-0 mb-2' id='textarea-"+commented.id +"'  rows='4' placeholder='write your reply' name='textarea-name"+commented.id +"'></textarea>"+
                // "<input type='hidden' id='input-"+commented.post_id+"'"+ "value="+commented.post_id+"><div class='col ml-auto text-right px-0'><button class='btn pull-right btn-primary' onclick='handleReplyClick(" +commented.id+","+commented.post_id+");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div><hr class='dashed'></div></div></div></div>"
                // }
              
              }
        
            
            // for (i=0;numOfReply;i++){
                // for (i=0;i<numOfReply;i++){
                //     if ( i === 1){
                //         console.log(i)
                //         var formattedComment = "<div class='media'><img class='rounded-circle mr-3' src='"+ commented.image +"' " +"width=40 height=40>"+"<div class='media-body'><small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
                //         "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p>" + commented.comment + "</p>" + "<div class='media mt-3'>" +
                //         "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                //         "<div class='col ml-auto text-right px-0'></div></div><hr class='dashed'></div></div></div></div>"

                //     }
                // else if ( i > 1 && i < numOfReply ){
                //     var formattedComment = "<div class='media'><div class='media-body'>" + 
                //     "<div class='media mt-3'>" +
                //     "<div class='media-body'><div class='col-12'><img class='rounded-circle mr-3' src='"+ replied.image +"' " +"width=40 height=40><small class='text-muted'>&nbsp;&nbsp;" + replied.user + "</small><small class='text-muted'>&nbsp; " + replied.updated_time+"</small><p>" + replied.comment + "</p>"+
                //     "<form action='/comment/reply/"+commented.post_id+"'"+  "method='POST' id='reply-form-"+commented.id +"'" +">"+"<textarea class='form-control mt-0 mb-2' id='textarea-"+commented.id +"'  rows='4' placeholder='write your reply' name='textarea-name"+commented.id +"'></textarea>"+
                //     "<input type='hidden' id='input-"+commented.post_id+"'"+ "value="+commented.post_id+"><div class='col ml-auto text-right px-0'><button class='btn pull-right btn-primary' onclick='handleReplyClick(" +commented.id+","+commented.post_id+");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div><hr class='dashed'></div></div></div></div>"

                // }
                
                  

               
               
                // }
                
                   
                // console.log('else condition ',numOfReply)
                

            // }
        

                }
    else {

        var formattedComment = "<div class='media'><img class='rounded-circle mr-3' src='"+ commented.image +"' " +"width=40 height=40>"+"<div class='media-body'><small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
                "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p>" + commented.comment + "</p>" + "<div class='media mt-3'>" +
                "<div class='media-body'><div class='col-12'><form action='/comment/reply/"+commented.post_id+"'"+  "method='POST' id='reply-form-"+commented.id +"'" +">"+"<textarea class='form-control mt-0 mb-2' id='textarea-"+commented.id +"'  rows='4' placeholder='write your reply' name='textarea-name"+commented.id +"'></textarea>"+
                "<input type='hidden' id='input-"+commented.post_id+"'"+ "value="+commented.post_id+"><div class='col ml-auto text-right px-0'><button class='btn pull-right btn-primary' onclick='handleReplyClick(" +commented.id+","+commented.post_id+");' type='submit' id='button-"+commented.id +"' >Reply</button></form></div></div><hr class='dashed'></div></div></div></div>"
    }
    // var formattedComment = "<img class='rounded-circle' src='"+ commented.image +"' " +"width=40 height=40>"+"<small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
    // "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p class='card-text'>&nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;" + commented.comment + "</p>" +
    // ""+
    // "<div class='container pull-right'><form id='reply-form-"+commented.id +"'" +">"+"<textarea  class='form-control mb-2 pull-right' id='textarea-"+commented.id +"'  style='height:100px;width:400px;' placeholder='write your reply' ></textarea>"+
    //  " <button class='btn pull-right btn-primary' onclick='submitReply(" +commented.id+","+commented.post_id+ ");' type='submit' id='button-"+commented.id +"' >Reply</button><hr style='border-bottom:1px solid #8c8b8b'></form></div></div>"
    
    return formattedComment
}


function handleReplyFormSubmit(event){
    event.preventDefault()
    // console.log(event)
    // console.log(event)
    const myForm = event.target
    const myFormData = new FormData(myForm)
   
    // console.log(myFormData)
    // for (var myItem of myFormData.entries()){
    //     console.log(myItem)
    // }

    
    const CSRF_TOKEN = getCookie('csrftoken')
    const url = myForm.getAttribute("action")    
    console.log(url)
    const method  = myForm.getAttribute("method")
    const commentIdElement = myForm.getAttribute("id").slice(11)
    const postIdElement = myForm.getAttribute("action").slice(15)
    const textareaIdElement = document.getElementById('textarea-'+commentIdElement).value
    // console.log(myForm.getAttribute("id").slice(11))
    // const postIdElement = document.getElementById('input-'+postIdElement).value
    // console.log(textareaIdElement)
    data = JSON.stringify({
        'reply': textareaIdElement,
        'post_id':postIdElement
    })
    console.log(data)
    var params = 'orem=ipsum&name=binny';
    // console.log(myForm.getAttribute("action"))
    const xhr = new XMLHttpRequest();
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type","application/json")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken",CSRF_TOKEN)
    xhr.onload    = function(){
        // const newComment = xhr.response
        // const newCommentJson = JSON.parse(newComment)
        // console.log(newCommentJson)
        if(xhr.readyState == 4 && xhr.status == 200) {
            alert(xhr.responseText);
        }
        
    }
    xhr.send(data)
}


function handleReplyClick(commentId,post_id){

    
    const replyCreateFormEl = document.getElementById("reply-form-"+commentId)
    console.log(replyCreateFormEl)
    if(replyCreateFormEl){
        console.log('Submmitted')
        replyCreateFormEl.addEventListener("submit", handleReplyFormSubmit)

    }
    
//    const commentElementId = commentId
//    const postElementId = post_id
//    const CSRF_TOKEN = getCookie('csrftoken')
//    const replyElementValue = document.getElementById('textarea-'+commentId).value
//    console.log(replyElementValue)
//    method = "POST"
//    const data = JSON.stringify({
//     comment: replyElementValue
//    })

//    console.log(data)
//    url = "/comment/reply/"+post_id

//     const xhr = new XMLHttpRequest();
//     xhr.open(method, url)
//     xhr.setRequestHeader("Content-Type","application/json")
//     xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
//     xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
//     xhr.setRequestHeader("X-CSRFToken",CSRF_TOKEN)
//     // xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
//     xhr.onload = function(){
//         console.log(xhr.status,xhr.response)
        
        
//     }
//     xhr.send(data)
}


function submitReply(replyId,post_id){

    const currPostId = post_id
    var textareaElementValue = document.getElementById('textarea-'+replyId).value;
    // console.log(textareaElementValue)
    var commentReplyDivId = document.getElementById('comment-reply-'+replyId)
    $.ajax({
        method:"POST",
        data: {
            comment: textareaElementValue,
            post:currPostId,
            csrfmiddlewaretoken:getCookie('csrftoken'),
        },
        url: "/comment/reply/"+currPostId,
        
        success: function(data){
            $(".comment-reply-"+replyId).append( "<p>"+data['comment']+"</p>" );
            alert(data['comment'])
        },
        error: function(data){
            alert("An error occured, please try again later")
        }
    })
}
function commentReply(textareadId,setElement){

    var textareaIdElement = 'textarea-'+textareadId
    var my_disply = document.getElementById(textareaIdElement);
    
    var replyCommentIdElement = 'reply-'+textareadId
    var my_reply_comment = document.getElementById(replyCommentIdElement);
    
    var buttonReplyIdElement = 'button-'+textareadId
    var buttonReplyComment = document.getElementById(buttonReplyIdElement);
    // const orgHtml = commentContainerEl.innerHTML
    // commentContainerEl.innerHTML = newCommentElement + orgHtml
    if (setElement === 1) {
        my_disply.style.display = "block";
        buttonReplyComment.setAttribute('class','btn btn-primary');
        document.getElementById(replyCommentIdElement).setAttribute('onclick',"commentReply(" +textareadId+ ",2);")
    }
    else if(setElement === 2){
        my_disply.style.display = "none";
        buttonReplyComment.setAttribute('class','d-none btn btn-primary pull-right');
        document.getElementById(replyCommentIdElement).setAttribute('onclick',"commentReply(" +textareadId+ ",1);")
    }
        
}