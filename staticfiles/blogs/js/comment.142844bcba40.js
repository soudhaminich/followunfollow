


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
        const servResponse = xhr.response
        const commentEl = document.getElementById("commentid")
        loadComments(commentEl)
        
    }
    xhr.send(myFormData)
}

const commentEl = document.getElementById("commentid")
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
    // console.log(listedItems)
    var finalMsgComment = "";
    var i = 0;
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
xhr.send()
}

loadComments(commentEl)

function LikeBtn()
{

    return "<button class='btn btn-sm'>Like</button>"
}

function formatCommentElement(commented){
    var formattedComment = "<div class='mb-4' id='comment-"+commented.id +"'"+ "><img class='rounded-circle' src='"+ commented.image +"'" +"width=40 height=40>"+"<small class='text-muted'>" + commented.user + "</small>" + 
    "<small class='text-muted'>&nbsp; " + commented.updated_time+"</small>" +"<p class='card-text'>&nbsp;  &nbsp;  &nbsp;" + commented.comment + "</p></div>"
    return formattedComment
}

