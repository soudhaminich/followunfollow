
const loadNotifyElement = document.getElementById("load-notify");
function loadNotification() {
    fetch("/api/notification/", {
        method: "GET",

        // headers: {
        //   Authorization: "Bearer " + access,
        //   "Content-Type": "application/json",
        // },
    })
        .then(response => {
            if (response.status !== 200) {

                throw new Error(response.status)
            }
            else {
                // console.log(response.json())
                return response.json()
            }
        })
        .then(data => {
            console.log(data.length);
            let finalNotifyCount = "";
            var currentItem = `${data.length}`
            finalNotifyCount += currentItem;
            loadNotifyElement.innerHTML = finalNotifyCount;

        })
}

// loadNotification()
setInterval(loadNotification, 5000);