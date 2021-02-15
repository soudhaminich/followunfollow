$(document).ready(function () {
    alert('Page is loaded');
});

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