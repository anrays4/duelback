from django.shortcuts import get_object_or_404

from .models import GameRoom


def create_table_state(room_id):
    game_room = get_object_or_404(GameRoom, id=room_id)
    board_state = {
        'p0': [],
        'p1': [1, 1],
        'p2': [],
        'p3': [],
        'p4': [],
        'p5': [],
        'p6': [2, 2, 2, 2, 2],
        'p7': [],
        'p8': [2, 2, 2],
        'p9': [],
        'p10': [],
        'p11': [],
        'p12': [1, 1, 1, 1, 1],
        'p13': [2, 2, 2, 2, 2],
        'p14': [],
        'p15': [],
        'p16': [],
        'p17': [1, 1, 1],
        'p18': [],
        'p19': [1, 1, 1, 1, 1],
        'p20': [],
        'p21': [],
        'p22': [],
        'p23': [],
        'p24': [2, 2],
    }
    game_room.place_status = board_state
    game_room.save()


def validate_moves(dice1, dice2, moves):
    print(moves)
    if len(moves) == 0:
        return True
    dices = []
    dices += [dice1, dice2]
    if dices[0] == dices[1]:
        dices += [dice1, dice2]

    # ابتدا بررسی ساختار object های داخل لیست moves
    for move in moves:
        if len(move) != 3:
            return False  # هر حرکت باید شامل 3 آیتم باشد

        # بررسی قالب مقادیر object ها
        move_type = move[0]  # "m-d-i" یا "e-d-i"
        start_position = move[1]  # "pi-j"
        end_position = move[2]  # "pi-j" یا "f-p-i"

        # چک کردن اینکه مقادیر با قالب داده شده سازگار باشند
        if not (move_type.startswith("m-d-") or move_type.startswith("e-d-")):
            return False
        if not start_position.startswith("p"):
            return False
        if not (end_position.startswith("p") or end_position.startswith("f-p-")):
            return False

        # گرفتن i و j از object ها
        try:
            x = start_position.split("-")[0]  # استخراج i از pi-j
            x = int(x.removeprefix(x[0]))
            if x > 0:
                x = 25 - x
            if end_position.startswith("p"):
                y = end_position.split("-")[0]  # استخراج i از pi-j در حالت "pi-j"
                y = int(y.removeprefix(y[0]))
                y = 25 - y
            else:
                y = 25  # در حالت "f-p-i"، مقدار y را 25 قرار می‌دهیم
        except ValueError:
            return False  # اگر نتوانستیم اعداد را از قالب جدا کنیم، خطا می‌دهیم

        # فقط اگر مقدار اول "e-d-i" باشد، عملیات چک کردن تاس‌ها انجام می‌شود
        if move_type.startswith("e-d-"):
            diff = x - y  # محاسبه x - y
            if diff < 0:
                diff = -diff
            if diff < 0:
                return False  # حرکت غیرمعتبر است چون diff نباید منفی باشد
            # بررسی اینکه آیا تاس مطابقت دارد یا نه
            if diff in dices:
                dices.remove(diff)  # اگر تاس مطابقت داشت، آن را از لیست حذف می‌کنیم
            elif end_position.startswith("f-p-") and diff < max(dices, default=7):
                # در حالت "f-p-i"، اگر مقدار diff از کوچک‌ترین مقدار تاس‌ها کمتر باشد، حرکت مجاز است
                dices.remove(max(dices))
                continue
            else:
                return False  # اگر تاس موجود نبود یا حرکت معتبر نبود

    # اگر همه موارد معتبر بودند
    return True


def update_board_status(current_turn, place_status, moves):
    e = current_turn
    if current_turn == 1:
        m = 2
    else:
        m = 1

    board_state = place_status

    for move in moves:
        # بررسی قالب مقادیر object ها
        move_type = move[0]  # "m-d-i" یا "e-d-i"
        start_position = move[1]  # "pi-j"
        end_position = move[2]  # "pi-j" یا "f-p-i"

        # گرفتن i و j از object ها
        try:
            x = start_position.split("-")[0]  # استخراج pi از pi-j
            if end_position.startswith("p"):
                y = end_position.split("-")[0]  # استخراج i از pi-j در حالت "pi-j"
            else:
                y = 25  # در حالت "f-p-i"، مقدار y را 25 قرار می‌دهیم
        except ValueError:
            return False  # اگر نتوانستیم اعداد را از قالب جدا کنیم، خطا می‌دهیم

        # فقط اگر مقدار اول "e-d-i" باشد، عملیات چک کردن تاس‌ها انجام می‌شود
        if move_type.startswith("e-d-"):
            if int(x[1]) != 0:
                try:
                    board_state[x].pop()
                except:
                    pass
                if type(y) != int:
                    board_state[y].append(e)
            else:
                board_state[x].remove(e)
                board_state[y].append(e)

        else:
            if int(x[1]) != 0:
                try:
                    board_state[x].pop()
                except:
                    pass
                if int(y.removeprefix(y[0])) != 25:
                    board_state[y].append(m)
            else:
                board_state[x].remove(m)
                board_state[y].append(m)

    # اگر همه موارد معتبر بودند
    return board_state


def win_check(place_status):
    board_state = place_status.values()

    player_1_win = True
    player_2_win = True

    for place in board_state:
        if 1 in place:
            player_1_win = False
        if 2 in place:
            player_2_win = False

    if player_1_win:
        return 1
    elif player_2_win:
        return 2
    else:
        return 3

