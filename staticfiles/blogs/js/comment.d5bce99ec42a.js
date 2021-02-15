


// commentMsg.innerHTML = 'Loading...'

function handleFormSubmit(event){
    event.preventDefault()
    // console.log(event)
    const myForm = event.target
    const myFormData = new FormData(myForm)
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
    xhr.onload = function(){
    // console.log(xhr.response)
    const servResponse = xhr.response
    var listedItems = servResponse.response
    console.log(listedItems.length)
    var finalMsgComment = "";
    var i = 0;
    if (listedItems.length !== 0){
        console.log('Logging')
        for (i=0;i<listedItems.length;i++){
            // console.log(listedItems[i])
            if (listedItems[i].user !== "")
            {
            var commentObj = listedItems[i]
            var currItem = formatCommentElement(commentObj)
            finalMsgComment += currItem 
            }
        }
        commentMsg.innerHTML = finalMsgComment
    }
    
    

}
xhr.send()
}

loadComments(commentContainerEl)

function LikeBtn()
{

    return "<button class='btn btn-sm'>Like</button>"
}

function formatCommentElement(commented){
    var formattedComment = "<div class='mb-4' id='comment-"+commented.id +"'"+ "><img class='rounded-circle' src='"+ commented.image +"' " +"width=40 height=40>"+"<small class='text-muted'>&nbsp;&nbsp;" + commented.user + "</small>" + 
    "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p class='card-text'>&nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;" + commented.comment + "</p>" +
    "<a hred='#' onclick='commentReply(" +commented.id+ ",1);' id='reply-"+commented.id +"' style='color:blue'>&nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;Reply</a><div class='container'><div class='row'><div class='col-sm-10 col-sm-offset-1'>"+
    "<form id='reply-form-'"+commented.id +"'"+ "method='POST' action='/'>&nbsp;&nbsp;&nbsp;<textarea row='10' class='form-control mb-2' id='textarea-"+commented.id +"' style='display:none;' rows='4' cols='50'></textarea></form>"+
     "<div class='d-flex flex-row'><div class='col ml-auto text-right px-0'> <button class='d-none btn pull-right btn-primary' type='submit' id='button-"+commented.id +"' >Reply</button></div></div></div></div></div></div>"
    
    return formattedComment
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