function upVote(comment_id) {

    let voteCount = document.getElementById(`vote-count-${comment_id}`).innerText
    const voteUser = document.getElementById("userdetail").value
    const domain = window.location.host
    let protocol = 'http'
    if (window.location.protocol === 'https') {
        protocol = 'https'
    }
    console.log(`${protocol}://${domain}/question/vote/${comment_id}/`)

    url = "{% url 'support:vote_comment' comment_id %}"
    fetch(url)
        .then(response => response.json())
        .then((data) => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });


}


function downVote(comment_id) {

    let voteCount = document.getElementById(`vote-count-${comment_id}`).innerText
    const voteUser = document.getElementById("userdetail").value
    const domain = window.location.host
    let protocol = 'http'
    if (window.location.protocol === 'https') {
        protocol = 'https'
    }
    console.log(`${protocol}://${domain}/question/vote/`)
    fetch(`${protocol}://${domain}/question/vote/`)
        .then(response => response.json())
        .then((data) => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });


}

// document.addEventListener("DOMContentLoaded", upVote);

// const todoElement = document.getElementById("todo")

//     fetch('/todo/api')
//         .then(response => response.json())
//         .then((data) => {
//             console.log(data.response);
//             let finalTodoStr = ""
//             data.response.forEach(elem => {
//                 console.log('foreach', elem);
//                 var currentItem = `<div class='mb-4'><p> ${elem.name}</p></div>`
//                 finalTodoStr += currentItem
//             })
//             todoElement.innerHTML = finalTodoStr
//         })