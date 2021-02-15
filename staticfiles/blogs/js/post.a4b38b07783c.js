const postDetailElement = document.getElementById("post-detail");
console.log(moment("20111031", "YYYYMMDD").fromNow())
function loadpost() {

    fetch("/api/post/134/", {
        method: "GET",

    })
        .then(response => {
            if (response.status !== 200) {

                throw new Error(response.status)
            }
            else {
                return response.json()
            }
        }).then(data => {

            const authorTitle = data.username
            const blogPosteddate = data.date_posted
            let currentItem = `<div id='latest-item'>
                                <h2>${data.title}</h2>
                                <span>
                                <img class="rounded-circle" src="${data.author_image}" width="30" height="30">
                                <span><a href="{% url 'users:profile' object.author.username %}">${authorTitle}</a> - Posted
                                    on ${blogPosteddate} ago </span>

                                </span>
                                </div>`
            postDetailElement.innerHTML = currentItem
        })
}
loadpost()
