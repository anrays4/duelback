var place1 = [];
var place2 = [];
var place3 = [];
var place4 = [];
var place5 = [];
var place6 = [];
var place7 = [];
var place8 = [];
var place9 = [];
var place10 = [];
var place11 = [];
var place12 = [];
var place13 = [];
var place14 = [];
var place15 = [];
var place16 = [];
var place17 = [];
var place18 = [];
var place19 = [];
var place20 = [];
var place21 = [];
var place22 = [];
var place23 = [];
var place24 = [];

var tasIsMosavi = false;
var myTasActive1 = false;
var myTasActive2 = false;
var myTasList = [];
var myTas1 = 4;
var myTas2 = 1;
var moveCount = 0;
var selectedDice = 1;
var isMyTurn = false;
var myFirstScan = {};

var myTurnTas = 0;
var enemyTurnTas = 0;

var enemyOutDice = [];
var myOutDice = [];
var enemyTas1 = 5;
var enemyTas2 = 2;

var enemyFinishDice = [];
var myFinishDice = [];

var moveHistory = [];
var moveHistoryForSend = [];

var myTurnNum = 1;
var enemyTurnNum = 2;

var my_time;
var enemy_time;

var gameRoomId = JSON.parse(document.getElementById('game_room_id').textContent);
var gameTurnTime = JSON.parse(document.getElementById('turn_time').textContent);
var gameTurnTimeCounter = JSON.parse(document.getElementById('turn_time').textContent);
var canStartGame = false;
var pollingTime = 2;


// design first place of all dice
my_dice_list = document.querySelectorAll(".my-dices div");
enemy_dice_list = document.querySelectorAll(".enemy-dices div");

place1.push(my_dice_list[0], my_dice_list[1]);
place12.push(my_dice_list[2], my_dice_list[3], my_dice_list[4], my_dice_list[5], my_dice_list[6]);
place17.push(my_dice_list[7], my_dice_list[8], my_dice_list[9]);
place19.push(my_dice_list[10], my_dice_list[11], my_dice_list[12], my_dice_list[13], my_dice_list[14]);


place24.push(enemy_dice_list[0], enemy_dice_list[1]);
place13.push(enemy_dice_list[2], enemy_dice_list[3], enemy_dice_list[4], enemy_dice_list[5], enemy_dice_list[6]);
place8.push(enemy_dice_list[7], enemy_dice_list[8], enemy_dice_list[9]);
place6.push(enemy_dice_list[10], enemy_dice_list[11], enemy_dice_list[12], enemy_dice_list[13], enemy_dice_list[14]);

// myOutDice.push(my_dice_list[0], my_dice_list[1]);
// place19.push(my_dice_list[7], my_dice_list[8], my_dice_list[9]);
// place20.push(my_dice_list[2], my_dice_list[3], my_dice_list[4], my_dice_list[5], my_dice_list[6]);
// place22.push(my_dice_list[10], my_dice_list[11]);
// place23.push(my_dice_list[12], my_dice_list[13], my_dice_list[14]);
//
// place1.push(enemy_dice_list[0], enemy_dice_list[5]);
// place2.push(enemy_dice_list[1], enemy_dice_list[6]);
// place3.push(enemy_dice_list[2], enemy_dice_list[7]);
// place8.push(enemy_dice_list[3], enemy_dice_list[8]);
// place5.push(enemy_dice_list[4], enemy_dice_list[9]);
// place6.push(enemy_dice_list[11], enemy_dice_list[12], enemy_dice_list[13]);
// place7.push(enemy_dice_list[14],enemy_dice_list[10]);
fix_all_dice_position()

// if user is ready, send request for server
var check_dom_is_ready = setInterval(function () {
    if (document.readyState === 'complete') {
        clearInterval(check_dom_is_ready);
        show_and_hide_roll_btn(true)
        let req_check_again_my_game = setInterval(function () {
            let base_url = window.location.origin;
            let req_url = base_url + "/backgammon/i_am_ready/" + gameRoomId + "/"
            request_sender_without_data(req_url) // send i am ready
            let check_data_is_ready = setInterval(function () {
                try {
                    var res_data = JSON.parse(document.getElementById('request_res').innerText)
                    var status = res_data['status']
                } catch {

                }
                if (status == "please_wait") {
                    set_info_text("Loading game ...")
                    clearInterval(check_data_is_ready)

                } else if (status == "start_game") {
                    set_info_text("Game is starting ... ");
                    clearInterval(check_data_is_ready);
                    clearInterval(req_check_again_my_game);

                    roll_sound()

                    myTurnNum = res_data["my_turn_num"];
                    if (myTurnNum == 1) {
                        enemyTurnNum = 2;
                    } else {
                        enemyTurnNum = 1;
                    }

                    myTurnTas = res_data["turn_tas_player_" + myTurnNum];
                    enemyTurnTas = res_data["turn_tas_player_" + enemyTurnNum];
                    var tas_1 = res_data["main_tas_1"];
                    var tas_2 = res_data["main_tas_2"];
                    set_move_count(tas_1, tas_2);

                    show_tas(1, myTurnTas); // show my turn tas
                    show_tas(4, enemyTurnTas); // show enemy turn tas

                    if (res_data['turn'] == myTurnNum) {
                        isMyTurn = true;

                        myTas1 = tas_1;
                        myTas2 = tas_2;
                    } else {
                        isMyTurn = false;

                        enemyTas1 = tas_1;
                        enemyTas2 = tas_2;
                    }
                    setTimeout(function () {
                        set_info_text("");
                        if (isMyTurn) {
                            clearInterval(enemy_time);
                            my_time = start_turn_time();
                            show_and_hide_roll_btn(true);
                        } else {

                            var check_my_turn_polling = setInterval(function () {
                                let base_url = window.location.origin;
                                let req_url = base_url + "/backgammon/check_my_turn/turn/" + gameRoomId + "/";
                                polling_for_my_turn_request(req_url);
                                let check_data_is_ready_polling = setInterval(function () {
                                    try {
                                        var res_data = JSON.parse(document.getElementById('request_res').innerText)
                                        var status = res_data['status']

                                    } catch {

                                    }
                                    if (status == "you_can_play") {
                                        clearInterval(check_data_is_ready_polling);
                                        clearInterval(check_my_turn_polling);
                                        myTurnNum = res_data["my_turn_num"];
                                        if (myTurnNum == 1) {
                                            enemyTurnNum = 2;
                                        } else {
                                            enemyTurnNum = 1;
                                        }

                                        var tas_1 = res_data["main_tas_1"];
                                        var tas_2 = res_data["main_tas_2"];
                                        let move_history = res_data["move_history"]
                                        set_move_count(tas_1, tas_2);
                                        action_enemy_move(move_history);

                                        if (res_data['turn'] == myTurnNum) {
                                            isMyTurn = true;

                                            myTas1 = tas_1;
                                            myTas2 = tas_2;
                                        }
                                        setTimeout(function () {
                                            if (isMyTurn) {
                                                clearInterval(enemy_time);
                                                my_time = start_turn_time();

                                                show_and_hide_roll_btn(true);
                                            }
                                        }, 2000)

                                    } else if (status == "wait_more") {
                                        clearInterval(check_data_is_ready_polling);
                                    } else if (status == "you_win") {
                                        clearInterval(check_data_is_ready_polling);
                                        clearInterval(check_my_turn_polling);
                                        document.getElementById("win-alert-dis").classList.add("uk-open");
                                        setTimeout(function () {
                                            window.location.pathname = "/home";
                                        }, 5000);
                                    }
                                }, 200);

                            }, parseInt(res_data['waiting_poll_time']) * 1000)

                            play_enemy_turn();
                            clearInterval(my_time);
                            enemy_time = start_turn_time();
                        }
                    }, 2000)
                } else if (status == "game_cancel") {
                    set_info_text("Game is cancel !!!")
                    clearInterval(check_data_is_ready);
                    clearInterval(req_check_again_my_game);
                    document.getElementById("game-cancel").classList.add("uk-open");
                    setTimeout(function () {
                        window.location.pathname = "/home";
                    }, 5000);
                }
            }, 200)
        }, pollingTime * 1000)
    }
}, 100);


function confirm_move() {
    if (isMyTurn) {
        show_and_hide_roll_btn(false);
        let base_url = window.location.origin;
        let req_url = base_url + "/backgammon/confirm_my_move/" + gameRoomId + "/"
        let second_scan = JSON.stringify(get_all_place_status());
        let first_scan = JSON.stringify(myFirstScan);

        canStartGame = false;

        for (let i = 0; i < moveHistory.length; i++) {
            create_move_history_for_send(moveHistory[i][0], moveHistory[i][1], moveHistory[i][2]);
        }
        let move_history = JSON.stringify(moveHistoryForSend)
        confirm_my_move_request(req_url, move_history, second_scan, first_scan);
        moveHistory = [];
        moveHistoryForSend = [];

        let check_data_is_ready = setInterval(function () {
            try {
                var res_data = JSON.parse(document.getElementById('request_res').innerText)
                var status = res_data['status']
                var polling_time = res_data['waiting_poll_time'];
                enemyTas1 = res_data['main_tas_1'];
                enemyTas2 = res_data['main_tas_2'];

            } catch {

            }

            if (status == "wait_for_turn") {

                clearInterval(check_data_is_ready);
                var check_my_turn_polling = setInterval(function () {
                    let base_url = window.location.origin;
                    let req_url = base_url + "/backgammon/check_my_turn/turn/" + gameRoomId + "/";
                    polling_for_my_turn_request(req_url);
                    let check_data_is_ready_polling = setInterval(function () {
                        try {
                            var res_data = JSON.parse(document.getElementById('request_res').innerText)
                            var status = res_data['status']

                        } catch {

                        }
                        if (status == "you_can_play") {
                            clearInterval(check_data_is_ready_polling);
                            clearInterval(check_my_turn_polling);
                            myTurnNum = res_data["my_turn_num"];
                            if (myTurnNum == 1) {
                                enemyTurnNum = 2;
                            } else {
                                enemyTurnNum = 1;
                            }

                            var tas_1 = res_data["main_tas_1"];
                            var tas_2 = res_data["main_tas_2"];
                            let move_history = res_data["move_history"]
                            set_move_count(tas_1, tas_2);
                            action_enemy_move(move_history);

                            if (res_data['turn'] == myTurnNum) {
                                isMyTurn = true;

                                myTas1 = tas_1;
                                myTas2 = tas_2;
                            }
                            setTimeout(function () {
                                if (isMyTurn) {
                                    clearInterval(enemy_time);
                                    my_time = start_turn_time();

                                    show_and_hide_roll_btn(true);
                                }
                            }, 2000)

                        } else if (status == "wait_more") {
                            clearInterval(check_data_is_ready_polling);

                        } else if (status == "you_win") {
                            clearInterval(check_data_is_ready_polling);
                            clearInterval(check_my_turn_polling);
                            document.getElementById("win-alert").classList.add("uk-open");
                            setTimeout(function () {
                                window.location.pathname = "/home";
                            }, 5000);
                        } else if (status == "game_cancel") {
                            set_info_text("Game is cancel !!!")
                            clearInterval(check_data_is_ready_polling);
                            clearInterval(check_my_turn_polling);
                            document.getElementById("game-cancel").classList.add("uk-open");
                            setTimeout(function () {
                                window.location.pathname = "/home";
                            }, 5000);
                        } else if (status == "you_lose") {
                            set_info_text("Game is End !!!")
                            clearInterval(check_data_is_ready_polling);
                            clearInterval(check_my_turn_polling);
                            document.getElementById("lose-alert").classList.add("uk-open");
                            setTimeout(function () {
                                window.location.pathname = "/home";
                            }, 5000);
                        }

                    }, 200);

                }, parseInt(polling_time) * 1000);

                setTimeout(function () {
                    play_enemy_turn();
                    clearInterval(my_time);
                    enemy_time = start_turn_time();

                }, 1000)
            } else if (status == "you_win") {
                clearInterval(check_data_is_ready);
                document.getElementById("win-alert").classList.add("uk-open");
                setTimeout(function () {
                    window.location.pathname = "/home";
                }, 5000);
            } else if (status == "you_lose") {
                clearInterval(check_data_is_ready);
                document.getElementById("lose-alert").classList.add("uk-open");
                setTimeout(function () {
                    window.location.pathname = "/home";
                }, 5000);
            }
        }, 200)
        isMyTurn = false;
    }
}


function active_or_disable_btn_box() {
    fix_all_dice_position()
    if (isMyTurn) {
        document.getElementById("btn-box-id").style.display = "flex";
    } else {
        document.getElementById("btn-box-id").style.display = "none";
    }
}


function start_turn_time() {
    let bar_elm = document.getElementById("turn_time_bar");
    bar_elm.style.backgroundColor = "#51dd18";
    var time = gameTurnTimeCounter;
    var turn_time = setInterval(function () {
        time--;
        let percent_of_bar = time / gameTurnTime * 100;
        let bar_elm = document.getElementById("turn_time_bar");
        bar_elm.style.width = percent_of_bar + "%";
        if (percent_of_bar < 30) {
            bar_elm.style.backgroundColor = "red";
        }

        if (time < 0) {
            clearInterval(turn_time);
            bar_elm.style.backgroundColor = "#51dd18";

            setTimeout(function () {
                let base_url = window.location.origin;
                let req_url = base_url + "/backgammon/check_time/" + gameRoomId + "/";
                request_sender_without_data(req_url);
                let check_status = setInterval(function () {
                    try {
                        var res_data = JSON.parse(document.getElementById('request_res').innerText)
                        var status = res_data['status']

                    } catch {

                    }
                    if (status === "you_lose") {
                        clearInterval(check_status);
                        document.getElementById("lose-alert").classList.add("uk-open");
                        setTimeout(function () {
                            window.location.pathname = "/home";
                        }, 5000);
                    }
                }, 300);


            }, 1000);
        }

    }, 1000);
    return turn_time;
}


document.getElementById("main-dice1").addEventListener("click", select_tas_1)

function select_tas_1() {
    if (myTasActive1) {
        selectedDice = 1;
        document.getElementById("main-dice1").classList.add("selected-tas");
        document.getElementById("main-dice2").classList.remove("selected-tas");
        document.getElementById("dice-1-side-four").classList.add("selected-tas");
        document.getElementById("dice-2-side-four").classList.remove("selected-tas");
        document.getElementById("dice-1-side-three").classList.add("selected-tas");
        document.getElementById("dice-2-side-three").classList.remove("selected-tas");
    }
}

document.getElementById("main-dice2").addEventListener("click", select_tas_2)

function select_tas_2() {
    if (myTasActive2) {
        selectedDice = 2;
        document.getElementById("main-dice2").classList.add("selected-tas");
        document.getElementById("main-dice1").classList.remove("selected-tas");
        document.getElementById("dice-2-side-four").classList.add("selected-tas");
        document.getElementById("dice-1-side-four").classList.remove("selected-tas");
        document.getElementById("dice-2-side-three").classList.add("selected-tas");
        document.getElementById("dice-1-side-three").classList.remove("selected-tas");
    }
}

function unselect_tas() {
    selectedDice = 1;
    document.getElementById("main-dice2").classList.remove("selected-tas");
    document.getElementById("main-dice1").classList.remove("selected-tas");
    document.getElementById("dice-2-side-four").classList.remove("selected-tas");
    document.getElementById("dice-1-side-four").classList.remove("selected-tas");
    document.getElementById("dice-1-side-three").classList.remove("selected-tas");
    document.getElementById("dice-2-side-three").classList.remove("selected-tas");
}


function switch_dice_selected() {
    if (selectedDice == 1) {
        select_tas_2()
    } else {
        select_tas_1()
    }
}

function action_move(place_elm, dice_elm) { // arg = ( place elm , dice elm)
    if (tasIsMosavi) {
        var tasNumberForMove = myTas1;
        if (selectedDice == 2) {
            tasNumberForMove = myTas2;
        }
    } else {
        if (selectedDice == 1 && myTasActive1) {
            tasNumberForMove = myTas1;
        }
        if (selectedDice == 2 && myTasActive2) {
            tasNumberForMove = myTas2;
        }
    }

    let move_this_dice = get_last_dice_of_place(get_place_variable(place_elm)); // get last dice at place for move

    let nextPlaceForMove = get_next_place(place_elm, tasNumberForMove); // elm
    let next_place_variable = get_place_variable(nextPlaceForMove); // js_variable

    if (nextPlaceForMove == "dice_is_finished" && ((myTasActive1 || myTasActive2) || tasIsMosavi)) {
        let is_all_dice_in_my_home = false;
        for (let i = 0; i < 19; i++) {
            let place_elm = document.getElementById("p" + i);
            let place_var = get_place_variable(place_elm);
            if (place_var.length > 0) {
                if (place_var[0].id.split("-")[0] == "m") {
                    is_all_dice_in_my_home = true;
                    break;
                }
            }
        }
        if (is_all_dice_in_my_home == false) {
            let countMyFinishDice = myFinishDice.length + 1;
            let nextFinishPlace = "f-m-p-" + countMyFinishDice;

            if (can_go_for_finish(place_elm, tasNumberForMove)) {
                // add moving history for can use undo btn
                let dice_id = move_this_dice.id;
                let first_place_id = place_elm.id + "-" + (get_place_variable(place_elm).indexOf(move_this_dice) + 1);
                let next_position_id = nextFinishPlace;
                let history = [dice_id, first_place_id, next_position_id];
                moveHistory.push(history);

                move_dice_to(move_this_dice, nextFinishPlace)
                moveCount -= 1;
                myTasList.push(tasNumberForMove);
                // push and pop in js_variable
                let first_place_var = get_place_variable(place_elm);
                first_place_var.pop();
                myFinishDice.push(move_this_dice);
                if (selectedDice == 1) {
                    myTasActive1 = false;
                } else {
                    myTasActive2 = false;
                }
                switch_dice_selected();
            }


        }
    }

    if (can_move_to_this_place(next_place_variable) && nextPlaceForMove != "dice_is_finished" && ((myTasActive1 || myTasActive2) || tasIsMosavi)) {
        increase_block_for_place(next_place_variable, nextPlaceForMove); // if dice is more than 5 then increase block for place

        // attack for enemy dice and enemy dice move to out of enemy dice place
        //var is_you_attacked = false;
        var enemy_dice_is_alone = check_enemy_dice_is_alone(next_place_variable);
        if (enemy_dice_is_alone) {
            let enemy_dice_first_place = nextPlaceForMove.id + "-" + (parseInt(next_place_variable.indexOf(enemy_dice_is_alone)) + 1);
            next_place_variable.pop();
            enemyOutDice.push(enemy_dice_is_alone);

            let enemy_dice_last_place = "e-o-d-" + parseInt(enemyOutDice.length);
            moveHistory.push([enemy_dice_is_alone.id, enemy_dice_first_place, enemy_dice_last_place]);
            setTimeout(function () {
                move_dice_to(enemy_dice_is_alone, enemy_dice_last_place);
            }, 500)
        }

        // add moving history for can use undo btn
        let dice_id = move_this_dice.id;
        let first_place_id = place_elm.id + "-" + (get_place_variable(place_elm).indexOf(move_this_dice) + 1);
        var next_position_id = get_final_elm_for_move(next_place_variable, nextPlaceForMove);
        let history = [dice_id, first_place_id, next_position_id];
        moveHistory.push(history);

        // apply move
        move_dice_to(move_this_dice, next_position_id)
        moveCount -= 1;
        myTasList.push(tasNumberForMove);

        // push and pop in js_variable
        let first_place_var = get_place_variable(place_elm);
        first_place_var.pop();
        next_place_variable.push(move_this_dice);

        decrease_block_for_place(place_elm);

        if (selectedDice == 1) {
            myTasActive1 = false;
        } else {
            myTasActive2 = false;
        }
        switch_dice_selected()

    } else {
        if (myTasActive1 == false) {
            if (!can_move_to_this_place(get_place_variable(document.getElementById("p" + myTas2)))) {
                document.getElementById("go-btn").hidden = false;
            }
        } else if (myTasActive2 == false) {
            if (!can_move_to_this_place(get_place_variable(document.getElementById("p" + myTas1)))) {
                document.getElementById("go-btn").hidden = false;
            }
        }

        cant_move_sound();
        show_Go_btn();

        let dice_elm = get_last_dice_of_place(get_place_variable(place_elm))
        try {
            dice_elm.classList.add('shake');

            setTimeout(() => {
                dice_elm.classList.remove('shake');
            }, 300);
        } catch {

        }
    }

    move_this_dice.style.zIndex = next_place_variable.indexOf(move_this_dice) + 2;
    show_Go_btn();
    witch_dice_is_can_move();
}

function action_undo(auto = false) {
    if (moveHistory.length > 0) {
        move_sound()
        moveCount++;
        let last_move = moveHistory.pop();

        let last_tas = myTasList.pop();
        if (last_tas == myTas1) {
            myTasActive1 = true;
        } else if (last_tas == myTas2) {
            myTasActive2 = true;
        }

        let dice_id = last_move[0]
        let first_place_id = last_move[1]
        let last_place_id = last_move[2]

        let dice_elm = document.getElementById(dice_id);
        let first_place_elm = document.getElementById(first_place_id);
        let last_place_elm = document.getElementById(last_place_id);


        try {
            let first_place_var = get_place_variable(first_place_elm.parentElement);
            let last_place_var = get_place_variable(last_place_elm.parentElement);

            last_place_var.pop()
            first_place_var.push(dice_elm)
        } catch {

            let first_place_elm = document.getElementById(first_place_id.split("-")[0])
            let first_place_var = get_place_variable(first_place_elm)

            let last_place_var = get_place_variable(document.getElementById(last_place_id.split("-")[0]));
            last_place_var.pop()
            first_place_var.push(dice_elm)
            increase_block_for_place(first_place_var, first_place_elm)
        }

        move_dice_to(dice_elm, first_place_id);

        if (moveHistory.length > 0) {
            let move_history = moveHistory;
            let reversed_arr = move_history[move_history.length - 1]
            if (reversed_arr[0][0].split("-")[0] == "e") {

                let last_elm_in_outList = enemyOutDice;
                let enemy_dice_id = last_elm_in_outList[enemyOutDice.length - 1].id;
                let enemy_out_dice_elm = document.getElementById(enemy_dice_id);
                let place_for_back_id = reversed_arr[1];
                let place_for_back_elm = document.getElementById(place_for_back_id.split('-')[0]);
                let place_for_back_var = get_place_variable(place_for_back_elm);

                enemyOutDice.pop();
                place_for_back_var.push(enemy_out_dice_elm);
                increase_block_for_place(place_for_back_var, place_for_back_elm);

                move_dice_to(enemy_out_dice_elm, place_for_back_id);
                auto = true;
                moveHistory.pop();

            } else {
                auto = false;
            }
        }
        if (auto == false) {
            decrease_block_for_place(document.getElementById(last_place_id.split("-")[0]));
        }

    }
    show_Go_btn();
    witch_dice_is_can_move();
}


function can_go_for_finish(place_elm, tas_number) {
    if (place_elm.id.split("-")[0] == "p19") {
        var index_place = 6;
    } else if (place_elm.id.split("-")[0] == "p20") {
        var index_place = 5;
    } else if (place_elm.id.split("-")[0] == "p21") {
        var index_place = 4;
    } else if (place_elm.id.split("-")[0] == "p22") {
        var index_place = 3;
    } else if (place_elm.id.split("-")[0] == "p23") {
        var index_place = 2;
    } else if (place_elm.id.split("-")[0] == "p24") {
        var index_place = 1;
    } else {
        return false;
    }
    if (tas_number > index_place) {
        for (let i = index_place + 1; i <= 6; i++) {
            let place_var = get_place_variable(document.getElementById("p" + (25 - i)))
            if (place_var.length > 0 && place_var[0].id.split("-")[0] == "m") {
                return false
            }
        }
        return true
    } else if (tas_number <= index_place) {
        return true
    }

}


function get_final_elm_for_move(place_var, place_elm) { // arg (var, elm) , return (position id)
    let count_of_dice_in_place = place_var.length;
    let pos_id = place_elm.id + "-" + (count_of_dice_in_place + 1);
    return pos_id
}


function increase_block_for_place(place_variable, place_elm) { // arg (js_variable, elm)
    let dice_count_in_place = place_variable.length
    if (dice_count_in_place >= 5) {
        let new_block_index = parseInt(place_elm.childElementCount)
        let new_block_id = place_elm.id + "-" + new_block_index

        let new_block = document.createElement("div");
        new_block.id = new_block_id;
        new_block.className = "dice-place"

        place_elm.appendChild(new_block);

        fix_dice_position(place_elm);
    }
}


function decrease_block_for_place(place_elm) { // arg (elm)
    try {
        let place_var = get_place_variable(place_elm);
        if (place_var.length > 4) {
            let last_block = place_elm.lastChild;
            place_elm.removeChild(last_block);
            fix_dice_position(place_elm);
        }
    } catch {

    }
}


function check_enemy_dice_is_alone(place_var) { // arg = (js_variable) , return enemy dice elm or false
    var enemy_dice_count_in_this_place = 0;
    for (let i = 0; i < enemy_dice_list.length; i++) {
        if (place_var.includes(enemy_dice_list[i])) {
            enemy_dice_count_in_this_place += 1;
        }
    }
    if (enemy_dice_count_in_this_place == 1) {
        return get_last_dice_of_place(place_var);
    } else {
        return false;
    }
}


function get_next_place(first_place, tas_num) { // arg (elm , int) , return = next place element
    let first_place_number = parseInt(first_place.id.replace("p", ""));
    let next_place_number = first_place_number + tas_num

    if (next_place_number > 24) {
        return "dice_is_finished";
    }

    return document.getElementById("p" + next_place_number);
}


function get_place_of_dice(dice_elm) { // arg (elm of dice) , return (elm of dice place)
    if (isMyTurn && moveCount > 0 && canStartGame) {
        if (myOutDice.length > 0) {
            action_move(document.getElementById('p0'), dice_elm);
            return 0;
        }
        if (place1.includes(dice_elm)) {
            action_move(document.getElementById('p1'), dice_elm);

        } else if (place2.includes(dice_elm)) {
            action_move(document.getElementById('p2'), dice_elm);

        } else if (place3.includes(dice_elm)) {
            action_move(document.getElementById('p3'), dice_elm);

        } else if (place4.includes(dice_elm)) {
            action_move(document.getElementById('p4'), dice_elm);

        } else if (place5.includes(dice_elm)) {
            action_move(document.getElementById('p5'), dice_elm);

        } else if (place6.includes(dice_elm)) {
            action_move(document.getElementById('p6'), dice_elm);

        } else if (place7.includes(dice_elm)) {
            action_move(document.getElementById('p7'), dice_elm);

        } else if (place8.includes(dice_elm)) {
            action_move(document.getElementById('p8'), dice_elm);

        } else if (place9.includes(dice_elm)) {
            action_move(document.getElementById('p9'), dice_elm);

        } else if (place10.includes(dice_elm)) {
            action_move(document.getElementById('p10'), dice_elm);

        } else if (place11.includes(dice_elm)) {
            action_move(document.getElementById('p11'), dice_elm);

        } else if (place12.includes(dice_elm)) {
            action_move(document.getElementById('p12'), dice_elm);

        } else if (place13.includes(dice_elm)) {
            action_move(document.getElementById('p13'), dice_elm);

        } else if (place14.includes(dice_elm)) {
            action_move(document.getElementById('p14'), dice_elm);

        } else if (place15.includes(dice_elm)) {
            action_move(document.getElementById('p15'), dice_elm);

        } else if (place16.includes(dice_elm)) {
            action_move(document.getElementById('p16'), dice_elm);

        } else if (place17.includes(dice_elm)) {
            action_move(document.getElementById('p17'), dice_elm);

        } else if (place18.includes(dice_elm)) {
            action_move(document.getElementById('p18'), dice_elm);

        } else if (place19.includes(dice_elm)) {
            action_move(document.getElementById('p19'), dice_elm);

        } else if (place20.includes(dice_elm)) {
            action_move(document.getElementById('p20'), dice_elm);

        } else if (place21.includes(dice_elm)) {
            action_move(document.getElementById('p21'), dice_elm);

        } else if (place22.includes(dice_elm)) {
            action_move(document.getElementById('p22'), dice_elm);

        } else if (place23.includes(dice_elm)) {
            action_move(document.getElementById('p23'), dice_elm);

        } else if (place24.includes(dice_elm)) {
            action_move(document.getElementById('p24'), dice_elm);
        }
    }
}


function get_place_variable(place_elm) { // arg = (elm) return = (js_variable of place)
    if (place_elm.id == "p1") {
        return place1
    } else if (place_elm.id == "p2") {
        return place2
    } else if (place_elm.id == "p3") {
        return place3
    } else if (place_elm.id == "p4") {
        return place4
    } else if (place_elm.id == "p5") {
        return place5
    } else if (place_elm.id == "p6") {
        return place6
    } else if (place_elm.id == "p7") {
        return place7
    } else if (place_elm.id == "p8") {
        return place8
    } else if (place_elm.id == "p9") {
        return place9
    } else if (place_elm.id == "p10") {
        return place10
    } else if (place_elm.id == "p11") {
        return place11
    } else if (place_elm.id == "p12") {
        return place12
    } else if (place_elm.id == "p13") {
        return place13
    } else if (place_elm.id == "p14") {
        return place14
    } else if (place_elm.id == "p15") {
        return place15
    } else if (place_elm.id == "p16") {
        return place16
    } else if (place_elm.id == "p17") {
        return place17
    } else if (place_elm.id == "p18") {
        return place18
    } else if (place_elm.id == "p19") {
        return place19
    } else if (place_elm.id == "p20") {
        return place20
    } else if (place_elm.id == "p21") {
        return place21
    } else if (place_elm.id == "p22") {
        return place22
    } else if (place_elm.id == "p23") {
        return place23
    } else if (place_elm.id == "p24") {
        return place24
    } else if (place_elm.id == "p0") {
        return myOutDice
    } else {
        return myFinishDice
    }
}


function get_last_dice_of_place(place_var) { // arg = js_variable_of_place : example place11 , return = element of dice
    return place_var.slice(-1)[0]
}


function move_animation(dice_elm, x, y) { // arg (str ,int, int)
    $("#" + dice_elm.id).animate({
        left: x + "px",
        top: y + "px",

    }, 500)
}


function move_dice_to(dice_elm, position_id, anim = true) { // arg ( dice element , position id)
    move_sound()
    var x_position = document.getElementById(position_id).getBoundingClientRect().left;
    var y_position = document.getElementById(position_id).getBoundingClientRect().top;
    if (anim) {
        move_animation(dice_elm, x_position, y_position)
        let this_dice = dice_elm;
        this_dice.style.position = "fixed";
    } else {
        let this_dice = dice_elm;
        this_dice.style.position = "fixed";
        this_dice.style.top = y_position + "px";
        this_dice.style.left = x_position + "px";
    }


}


function can_move_to_this_place(place) { // arg = ( js_variable place12)
    var enemy_dice_count_in_this_place = 0;
    for (let i = 0; i < enemy_dice_list.length; i++) {
        if (place.includes(enemy_dice_list[i])) {
            enemy_dice_count_in_this_place += 1;
        }
    }
    if (enemy_dice_count_in_this_place > 1) {
        return false
    }
    return true
}


function fix_dice_position(place_elm, anim) { // arg (place_elm)
    let place_var = get_place_variable(place_elm);
    for (let i = 0; i < place_var.length; i++) {
        move_dice_to(place_var[i], place_elm.id + "-" + (i + 1), anim)
    }
}


function show_and_hide_roll_btn(show) { // arg (bool)  show = true , hide = false
    if (show) {
        if (isMyTurn) {
            unselect_tas();
            document.getElementById("my-profile-pic").classList.add("turn-border");
            document.getElementById("enemy-profile-pic").classList.remove("turn-border");
            document.getElementById("roll-tas-btn").style.display = "block";
            document.getElementById("main-dice2").style.display = "none";
            document.getElementById("main-dice1").style.display = "none";
            document.getElementById("main-dice3").style.display = "none";
            document.getElementById("main-dice4").style.display = "none";
        } else {
            unselect_tas();
            document.getElementById("my-profile-pic").classList.remove("turn-border");
            document.getElementById("roll-tas-btn").style.display = "none";
            document.getElementById("main-dice2").style.display = "none";
            document.getElementById("main-dice1").style.display = "none";
        }

    } else {
        document.getElementById("roll-tas-btn").style.display = "none";
        document.getElementById("main-dice3").style.display = "none";
        document.getElementById("main-dice4").style.display = "none";
        document.getElementById("main-dice2").style.display = "block";
        document.getElementById("main-dice1").style.display = "block";
    }
}


function click_roll_btn() {
    if (myTas1 == myTas2) {
        roll_sound_2()
    } else {
        roll_sound()
    }
    myFirstScan = get_all_place_status();
    show_and_hide_roll_btn(false);
    active_or_disable_btn_box();
    if (isMyTurn) {
        show_tas(1, myTas1);
        show_tas(2, myTas2);
        setTimeout(select_tas_1, 1200);
    }
    setTimeout(function () {
        canStartGame = true;
    }, 1200);
    if (myOutDice.length > 0) {
        if (!(can_move_to_this_place(get_place_variable(document.getElementById("p" + myTas1))) || can_move_to_this_place(get_place_variable(document.getElementById("p" + myTas2))))) {
            moveCount = 0;
            myTasActive1 = false;
            myTasActive2 = false;
            setTimeout(confirm_move, 4000);
        }
    }

    setTimeout(witch_dice_is_can_move, 1200);
    show_Go_btn();
}


function show_Go_btn() {
    if (moveCount === 0 || !is_exist_move()) {
        document.getElementById("go-btn").hidden = false;
    } else {
        document.getElementById("go-btn").hidden = true;
    }
}


function play_enemy_turn() {
    if (enemyTas1 == enemyTas2) {
        roll_sound_2()
    } else {
        roll_sound()
    }

    show_and_hide_roll_btn(true);
    active_or_disable_btn_box();
    show_tas(3, enemyTas1);
    show_tas(4, enemyTas2);

    document.getElementById("enemy-profile-pic").classList.add("turn-border");
}


function show_tas(tas_id, number) { // arg (int,int) (tas 3or4 for enemy and 1or2 for me, tas number )
    let tas_elm_id = "main-dice" + tas_id
    document.getElementById(tas_elm_id).style.display = "block";
    setTimeout(function () {
        rollDice(tas_elm_id, number);
    }, 200)

}

function rollDice(id_tas, number) { // arg (int)

    var elDiceOne = document.getElementById(id_tas);
    var r = parseInt(Math.random() * 10) + 1

    if (number == 1) {
        var degX = r * 360
        var degZ = r * 360
        elDiceOne.style.transform = "rotateX(" + degX + "deg) rotateZ(-" + degZ + "deg)";
    } else if (number == 2) {
        var degX = (2 * r + 1) * 180
        var degZ = r * 360
        elDiceOne.style.transform = "rotateX(" + degX + "deg) rotateZ(-" + degZ + "deg)";
    } else if (number == 3) {
        var degY = (4 * (r - 1) + 1) * 90
        var degZ = r * 360
        elDiceOne.style.transform = "rotateY(" + degY + "deg) rotateZ(-" + degZ + "deg)";
    } else if (number == 4) {
        var degX = (4 * (r - 1) + 3) * 90
        var degZ = r * 360
        elDiceOne.style.transform = "rotateX(" + degX + "deg) rotateZ(-" + degZ + "deg)";
    } else if (number == 5) {
        var degX = (4 * (r - 1) + 1) * 90
        var degZ = r * 360
        elDiceOne.style.transform = "rotateX(" + degX + "deg) rotateZ(-" + degZ + "deg)";
    } else if (number == 6) {
        var degY = (4 * (r - 1) + 3) * 90
        var degZ = r * 360
        elDiceOne.style.transform = "rotateY(" + degY + "deg) rotateZ(-" + degZ + "deg)";
    }
}

// arg(int,int) get two tas from server and check how much can moving, if cant moving send request to server for change turn
function set_move_count(tas_1, tas_2) {
    if (myOutDice.length > 0) {
        let can_move_with_tas1 = can_move_to_this_place(get_place_variable(get_next_place(document.getElementById("p0"), tas_1)));
        let can_move_with_tas2 = can_move_to_this_place(get_place_variable(get_next_place(document.getElementById("p0"), tas_2)));
        if (!can_move_with_tas1 && !can_move_with_tas2) {
            moveCount = 0;
            return false;
        }
    }
    if (tas_1 == tas_2) {
        tasIsMosavi = true;
        moveCount = 4;
        myTasActive1 = true;
        myTasActive2 = true;
    } else {
        moveCount = 2;
        myTasActive1 = true;
        myTasActive2 = true;
    }
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


function confirm_my_move_request(url, move_history, place_status, first_scan) {
    const apiUrl = url;
    const formdata = new FormData();
    formdata.append("move_history", move_history);
    formdata.append("first_scan", first_scan);
    formdata.append("second_scan", place_status);

    const outputElement = document.getElementById("request_res");

    const requestOptions = {
        method: 'POST',
        body: formdata,
        redirect: "follow",
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

function polling_for_my_turn_request(url) {
    const outputElement = document.getElementById("request_res");
    const requestOptions = {
        method: 'GET',
        redirect: "follow",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    };

    fetch(url, requestOptions)
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

function i_want_leave() {
    let base_url = window.location.origin;
    let req_url = base_url + "/backgammon/i_want_leave/" + gameRoomId + "/";
    request_sender_without_data(req_url);
    setInterval(function () {
        try {
            var res_data = JSON.parse(document.getElementById('request_res').innerText)
            var status = res_data['status']

        } catch {

        }
        if (status == "thanks") {
            window.location.pathname = "/home";
        }
    }, 300);
}


function fix_all_dice_position() {
    for (let i = 0; i < 25; i++) {
        fix_dice_position(document.getElementById("p" + i), false);
    }
}

window.onresize = function (event) {
    fix_all_dice_position();
};
window.onscroll = function (event) {
    fix_all_dice_position();
};


function get_all_place_status() {
    let status = {}
    for (let i = 1; i < 25; i++) {
        let new_place_var = []
        let place_var = get_place_variable(document.getElementById("p" + i));
        for (let j = 0; j < place_var.length; j++) {
            if (place_var[0].id.split("-")[0] == "m") {
                var my_user_turn_id = myTurnNum;
                new_place_var.push(my_user_turn_id)
            } else if (place_var[0].id.split("-")[0] == "e") {
                var my_user_turn_id = enemyTurnNum;
                new_place_var.push(my_user_turn_id)
            } else {

            }
        }
        if (myTurnNum == 2) {
            if (i == 0) {
                status["p" + i] = new_place_var;
            } else {
                status["p" + (25 - i)] = new_place_var;
            }
        } else {
            status["p" + i] = new_place_var;
        }

    }
    return status;
}

function is_all_dice_in_my_home() {
    let is_all_dice_in_my_home = true;
    for (let i = 0; i < 19; i++) {
        let place_elm = document.getElementById("p" + i);
        let place_var = get_place_variable(place_elm);
        if (place_var.length > 0) {
            if (place_var[0].id.split("-")[0] == "m") {
                is_all_dice_in_my_home = false;
                break;
            }
        }
    }
    return is_all_dice_in_my_home;
}

function is_exist_move() { // if is true then cant click to go btn for confirm move
    for (let i = 0; i < 25; i++) {
        let place_elm = document.getElementById("p" + i);
        let place_var = get_place_variable(place_elm);

        if (place_var.length > 0 && place_var[0].id.split("-")[0] == "m") {
            let next_place_elm_1 = get_next_place(place_elm, myTas1)
            let next_place_elm_2 = get_next_place(place_elm, myTas2)
            if (next_place_elm_1 == "dice_is_finished" && is_all_dice_in_my_home()) {
                if ((can_go_for_finish(place_elm, myTas1) && myTasActive1) || (can_go_for_finish(place_elm, myTas2) && myTasActive2)) {
                    return true;
                }
            } else {
                if (myTasActive1 && next_place_elm_1 != "dice_is_finished" && myOutDice.length == 0) {
                    let next_place_var_1 = get_place_variable(next_place_elm_1);
                    var move_is_exist_1 = can_move_to_this_place(next_place_var_1);
                } else {

                    move_is_exist_1 = false
                }
            }
            if (next_place_elm_2 == "dice_is_finished" && is_all_dice_in_my_home()) {
                if ((can_go_for_finish(place_elm, myTas1) && myTasActive1) || (can_go_for_finish(place_elm, myTas2) && myTasActive2)) {
                    return true;
                }
            } else {
                if (myTasActive2 && next_place_elm_2 != "dice_is_finished" && myOutDice.length == 0) {
                    let next_place_var_2 = get_place_variable(next_place_elm_2);
                    var move_is_exist_2 = can_move_to_this_place(next_place_var_2);
                } else {

                    move_is_exist_2 = false
                }
            }
            if ((move_is_exist_1 || move_is_exist_2) && myOutDice.length == 0) {
                return true;
            }
        }
    }
    document.getElementById("go-btn").hidden = false;
    return false;
}

function create_move_history_for_send(dice_id, first_place_id, next_place_id) {
    if (dice_id.split("-")[0] == "m") {
        var new_dice_id = "e-" + dice_id.split("-")[1] + "-" + dice_id.split("-")[2];
    } else if (dice_id.split("-")[0] == "e") {
        var new_dice_id = "m-" + dice_id.split("-")[1] + "-" + dice_id.split("-")[2];
    }
    let new_first_place_id = get_place_number_for_decrease_25(first_place_id.split("-")[0]) + "-" + first_place_id.split("-")[1];

    if (next_place_id.split("-")[0] == "f") {
        let i = next_place_id.split("-")[next_place_id.split("-").length - 1]
        var new_next_place_id = "f-p-" + i;

    } else if (next_place_id.split("-")[0] == "e") {
        let j = next_place_id.split("-")[next_place_id.split("-").length - 1]
        var new_next_place_id = "p0-" + j;
    } else {
        var new_next_place_id = get_place_number_for_decrease_25(next_place_id.split("-")[0]) + "-" + next_place_id.split("-")[1];
    }

    let new_move_history = [new_dice_id, new_first_place_id, new_next_place_id];
    moveHistoryForSend.push(new_move_history);

}

function action_enemy_move(move_history) { // arg (move_history)
    function runMoveSequence(moveIndex) {
        if (moveIndex >= move_history.length) {
            return true;
        }

        let dice_id = move_history[moveIndex][0];
        let first_place_id = move_history[moveIndex][1];
        let next_place_id = move_history[moveIndex][2];

        let dice_elm = document.getElementById(dice_id);
        let first_place_elm = document.getElementById(first_place_id.split('-')[0])
        let next_place_elm = document.getElementById(next_place_id.split('-')[0])


        if (first_place_id.split('-')[0] == "p0" && dice_id.split("-")[0] == "e") {
            var first_place_var = enemyOutDice;
        } else {
            var first_place_var = get_place_variable(first_place_elm)
        }
        first_place_var.pop();

        if (next_place_id.split('-')[0] == "f") {
            var next_place_var = enemyFinishDice;
        } else {
            if (next_place_id.split('-')[0] == "p0" && dice_id.split("-")[0] == "e") {
                var next_place_var = enemyOutDice;
            }
            var next_place_var = get_place_variable(next_place_elm)
        }
        next_place_var.push(dice_elm);

        if (next_place_id.split('-')[0] != "f") {
            increase_block_for_place(next_place_var, next_place_elm);
        }
        if (first_place_id.split('-')[0] != "p0") {
            decrease_block_for_place(first_place_elm);
        }

        move_dice_to(dice_elm, next_place_id);

        setTimeout(function () {
            runMoveSequence(moveIndex + 1);
        }, 400);
    }

    setTimeout(function () {
        return runMoveSequence(0);
    }, 400);
}

function get_place_number_for_decrease_25(place_str) {
    if (place_str == "p0") {
        return "p0"
    } else if (place_str == "p1") {
        return "p24"
    } else if (place_str == "p2") {
        return "p23"
    } else if (place_str == "p3") {
        return "p22"
    } else if (place_str == "p4") {
        return "p21"
    } else if (place_str == "p5") {
        return "p20"
    } else if (place_str == "p6") {
        return "p19"
    } else if (place_str == "p7") {
        return "p18"
    } else if (place_str == "p8") {
        return "p17"
    } else if (place_str == "p9") {
        return "p16"
    } else if (place_str == "p10") {
        return "p15"
    } else if (place_str == "p11") {
        return "p14"
    } else if (place_str == "p12") {
        return "p13"
    } else if (place_str == "p13") {
        return "p12"
    } else if (place_str == "p14") {
        return "p11"
    } else if (place_str == "p15") {
        return "p10"
    } else if (place_str == "p16") {
        return "p9"
    } else if (place_str == "p17") {
        return "p8"
    } else if (place_str == "p18") {
        return "p7"
    } else if (place_str == "p19") {
        return "p6"
    } else if (place_str == "p20") {
        return "p5"
    } else if (place_str == "p21") {
        return "p4"
    } else if (place_str == "p22") {
        return "p3"
    } else if (place_str == "p23") {
        return "p2"
    } else if (place_str == "p24") {
        return "p1"
    }
}

function witch_dice_is_can_move() {
    // for (let i = 0; i < 15; i++) {
    //     my_dice_list[i].classList.remove("can-move-border");
    // }
    // if (myTasActive1 || myTasActive2) {
    //     for (let i = 0; i < 25; i++) {
    //         let place_elm = document.getElementById("p" + i);
    //         let place_var = get_place_variable(place_elm);
    //
    //         if (place_var.length > 0 && place_var[0].id.split("-")[0] == "m") {
    //             let next_place_elm_1 = get_next_place(place_elm, myTas1);
    //             let next_place_elm_2 = get_next_place(place_elm, myTas2);
    //             let next_1 = get_place_variable(next_place_elm_1);
    //             let next_2 = get_place_variable(next_place_elm_2);
    //
    //             if (next_place_elm_1 == "dice_is_finished") {
    //                 var is_all_dice_in_my_home = false;
    //                 for (let i = 0; i < 19; i++) {
    //                     let place_elm = document.getElementById("p" + i);
    //                     let place_var = get_place_variable(place_elm);
    //                     if (place_var.length > 0) {
    //                         if (place_var[0].id.split("-")[0] == "m") {
    //                             is_all_dice_in_my_home = true;
    //                             break;
    //                         }
    //                     }
    //                 }
    //                 if (is_all_dice_in_my_home == false) {
    //                     let x = can_go_for_finish(next_place_elm_1, myTas1);
    //                     let y = can_go_for_finish(next_place_elm_1, myTas2);
    //                     if (x || y) {
    //                         let this_dice = get_last_dice_of_place(place_var);
    //                         this_dice.classList.add("can-move-border");
    //                     }
    //                 }
    //
    //             } else if (next_place_elm_2 == "dice_is_finished") {
    //                 var is_all_dice_in_my_home = false;
    //                 for (let i = 0; i < 19; i++) {
    //                     let place_elm = document.getElementById("p" + i);
    //                     let place_var = get_place_variable(place_elm);
    //                     if (place_var.length > 0) {
    //                         if (place_var[0].id.split("-")[0] == "m") {
    //                             is_all_dice_in_my_home = true;
    //                             break;
    //                         }
    //                     }
    //                 }
    //                 if (is_all_dice_in_my_home == false) {
    //                     let x = can_go_for_finish(next_place_elm_2, myTas1);
    //                     let y = can_go_for_finish(next_place_elm_2, myTas2);
    //                     if (x || y) {
    //                         let this_dice = get_last_dice_of_place(place_var);
    //                         this_dice.classList.add("can-move-border");
    //                     }
    //                 }
    //             } else {
    //                 let move_is_exist_1 = can_move_to_this_place(next_1);
    //                 let move_is_exist_2 = can_move_to_this_place(next_2);
    //                 if (move_is_exist_1 || move_is_exist_2) {
    //                     let this_dice = get_last_dice_of_place(place_var);
    //                     this_dice.classList.add("can-move-border");
    //                 }
    //             }
    //         }
    //     }
    // }
}

window.history.pushState(null, null, window.location.href);
window.onpopstate = function () {
    window.history.pushState(null, null, window.location.href);
};

// Optional: Prevent default back button behavior
window.addEventListener('popstate', function (event) {
    event.preventDefault();
});


function set_info_text(text) {
    document.getElementById("info-box").innerText = text;
}

function move_sound() {
    var sound = document.getElementById('moveSound');
    sound.currentTime = 0; // Reset to start
    sound.play(); // Play the sound
}

function roll_sound() {
    var sound = document.getElementById('rollSound');
    sound.currentTime = 0; // Reset to start
    sound.play(); // Play the sound
}

function roll_sound_2() {
    var sound = document.getElementById('roll2Sound');
    sound.currentTime = 0; // Reset to start
    sound.play(); // Play the sound
}

function cant_move_sound() {
    var sound = document.getElementById('cantMoveSound');
    sound.currentTime = 0; // Reset to start
    sound.play(); // Play the sound
}

