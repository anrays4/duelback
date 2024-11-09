const polling_time = JSON.parse(document.getElementById('polling_time').textContent);
var IamReady = true;

var dot_count = 1;
var search_dot = setInterval(function () {
    let dot = document.getElementById("dot-anim");
    if (dot_count == 1) {
        dot.innerText = "."
    } else if (dot_count == 2) {
        dot.innerText = ".."
    } else if (dot_count == 3) {
        dot.innerText = "..."
    }
    dot_count++;
    if (dot_count == 4) {
        dot_count = 1;
    }
}, 500)


let check_finding = setInterval(function () {
    let base_url = window.location.origin;
    const apiUrl = base_url + "/backgammon/find-match-is-ready/"
    request_sender_without_data(apiUrl);
    let check_response_is_coming = setInterval(function () {
        try {
            var res_data = JSON.parse(document.getElementById('request_res').innerText)
            var status = res_data['status']
        } catch {

        }
        if (status === "wait_more") {
            clearInterval(check_response_is_coming);
        } else if (status === "your_match_ready" && IamReady) {
            clearInterval(check_finding);
            clearInterval(check_response_is_coming);
            clearInterval(search_dot);

            let game_room_id = res_data['game_room_id'];
            let enemy_name = res_data['enemy_name'];
            let enemy_avatar = res_data['enemy_avatar'];
            let enemy_level = res_data['enemy_level'];

            set_enemy_found_details(enemy_name, enemy_avatar, enemy_level);

            setTimeout(function () {
                window.location.pathname = 'backgammon/playing-game/' + game_room_id + "/"
            }, 1500);

        } else if (status === "go_to_play") {
            clearInterval(check_finding);
            clearInterval(check_response_is_coming);
            clearInterval(search_dot);

            let game_room_id = res_data['game_room_id'];
            let enemy_name = res_data['enemy_name'];
            let enemy_avatar = res_data['enemy_avatar'];
            let enemy_level = res_data['enemy_level'];

            set_enemy_found_details(enemy_name, enemy_avatar, enemy_level);

            setTimeout(function () {
                window.location.pathname = 'backgammon/playing-game/' + game_room_id + "/"
            }, 1500);

        }

    }, 200);
}, polling_time * 1000);


function cancel_find_match() {
    IamReady = false;
    let base_url = window.location.origin;
    let apiurl = base_url + "/backgammon/cancel-find-match/"
    request_sender_without_data(apiurl);
    document.getElementById("fa-load").classList.remove("fa-xmark");
    document.getElementById("fa-load").classList.add("fa-spinner");
    setTimeout(function () {
        window.location.pathname = "/home"
    }, 1200);
}


function request_sender_without_data(url) {
    const apiUrl = url;
    const outputElement = document.getElementById("request_res");
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    };
    fetch(apiUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            outputElement.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error
            ('Error:', error);
        });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function set_enemy_found_details(name, avatar, level) {
    document.getElementById("enemy-name").innerText = name;
    document.getElementById("enemy-avatar").classList.remove("success");
    document.getElementById("enemy-avatar").classList.remove("circle");
    document.getElementById("enemy-lvl").innerText = level;
    console.log(avatar)
    if (avatar != null) {
        document.getElementById("enemy-avatar").src = avatar;
    }

}
