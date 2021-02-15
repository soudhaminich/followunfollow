function upVote(comment_id) {

    // let voteCount = document.getElementById(`vote-count-${comment_id}`).innerText
    const voteUser = document.getElementById("userdetail").value
    const domain = window.location.host
    let OutputEl = document.getElementById(`vote-count-up-${comment_id}`)
    let OutputdownEl = document.getElementById(`vote-count-down-${comment_id}`)
    let protocol = 'http'
    if (window.location.protocol === 'https') {
        protocol = 'https'
    }
    const URL = document.getElementById(`currentupURL-${comment_id}`).value
    console.log(URL)
    fetch(URL)
        .then(response => response.json())
        .then((data) => {
            console.log(data.total_count)
            if (data.total_up_count) {
                OutputEl.innerText = 'Up ' + data.total_up_count
                OutputdownEl.innerText = 'Down ' + data.total_down_count

            }

        })
        .catch((error) => {
            console.error('Error:', error);
        });


}


function downVote(comment_id) {

    // let voteCount = document.getElementById(`vote-count-${comment_id}`).innerText
    const voteUser = document.getElementById("userdetail").value
    const domain = window.location.host
    let protocol = 'http'
    let OutputEl = document.getElementById(`vote-count-up-${comment_id}`)
    let OutputdownEl = document.getElementById(`vote-count-down-${comment_id}`)
    if (window.location.protocol === 'https') {
        protocol = 'https'
    }
    const URL = document.getElementById(`currentdownURL-${comment_id}`).value
    console.log(URL)
    fetch(URL)
        .then(response => response.json())
        .then((data) => {

            if (data.total_down_count) {
                OutputdownEl.innerText = 'Down ' + data.total_down_count
                OutputEl.innerText = 'Up ' + data.total_up_count
            }
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