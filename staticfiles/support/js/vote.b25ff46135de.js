function upVote(comment_id) {

    let voteCount = document.getElementById(`vote-count-${comment_id}`).innerText
    const voteUser = {{ request.user.username }}
    console.log(voteUser)


}