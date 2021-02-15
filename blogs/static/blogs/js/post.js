var obj = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data() {
        return {
            info: null,
            loading: true,
            errored: false
        }
    },
    mounted() {
        axios
            .get('/api/post/133/')
            .then(response => {
                this.info = response.data
            })
            .catch(error => {
                console.log(error)
                this.errored = true
            })
            .finally(() => this.loading = false)
    }
})
//   delimiters: ["[[", "]]"],




const postDetailElement = document.getElementById("post-detail");

function loadpost() {

    fetch("/api/post/133/", {
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
            let newmomentParsedate = moment(blogPosteddate).fromNow(true)
            let commentURL = '/'
            let currentItem = `<div id='latest-item'>
                                <h2>${data.title}</h2>
                                <span>
                                <img class="rounded-circle" src="${data.author_image}" width="30" height="30">
                                <span><a href="{% url 'users:profile' object.author.username %}">${authorTitle}</a> - Posted
                                    on ${newmomentParsedate} ago </span>

                                </span>
                                <p class="article-content">${data.content}</p>

                                <hr>
                                <form id="comment-form" method='POST' action="${commentURL}">

                                <div class="marked-content-show">
                                </div>
                                <textarea class='form-control mb-2' rows='4' cols='50' placeholder='Write your comment/question' name='comment'
                                  required></textarea>
                                <button type="submit" id="commentmsgtest" class="btn btn-primary mt-2" style="float: right;">Send</button>
                              </form>
                                </div>`


            postDetailElement.innerHTML = currentItem
        })
}
loadpost()
