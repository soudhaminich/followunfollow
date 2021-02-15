
$(document).ready(function () {
    var loc = window.location;
    var wsStart = "ws://";
    var NotifyId = document.getElementById('notify')

    if (loc.protocol == "https:") {
        wsStart = "https://"
    }
    const noti_socket = new WebSocket(
        wsStart + loc.host + '/ws/notifs/'
    );
    console.log(wsStart + loc.host + '/ws/notifs/')
    noti_socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        // console.log(data.message)
        var notifySpanHtml = `<span class="text-white prior-font font-weight-bold number-span" id="notify">${data.message}</span>`
        NotifyId.innerHTML = notifySpanHtml;
        playSound('https://static.teckiy.com/notification/notification_alert.mp3');

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/ws/notifs/confirm/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ "notification_id": data.notification_id }));
    };

    noti_socket.onopen = function (e) {
        console.log('open', e)
    };

    noti_socket.onerror = function (e) {
        console.log('error', e)
    };

    noti_socket.onclose = function (e) {
        console.log('closed', e)
    };
});


function playSound(url) {
    const audio = new Audio(url);
    audio.play();
}
