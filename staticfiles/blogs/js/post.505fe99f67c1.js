const postDetailElement = document.getElementById("post-detail");
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
            console.log(data)
        })
}
loadpost()
