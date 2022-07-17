# tic tac toe machine learning bot
import random
brain = {}
current_state = '222222222'
bot_moves = []


def show_board(board_state):
    board_state = board_state.replace(
        '0', 'O').replace('1', 'X').replace('2', '-')
    print(board_state[0], '|', board_state[1], 'GG|', board_state[2])
    print(board_state[3], '|', board_state[4], '|', board_state[5])
    print(board_state[6], '|', board_state[7], '|', board_state[8])


def take_move_from_brain(board_state):
    try:
        moves = brain[board_state]
        return moves
    except KeyError:
        empty_slots = {}
        for x in range(len(board_state)):
            if board_state[x] == '2':
                empty_slots[x+1] = 1
        brain[board_state] = empty_slots
        return empty_slots


def choose_best_move(moves, rand_probability):
    best_move = 0
    best_move_point = -9999999
    x = random.random()
    if x < rand_probability:
        move_list = []
        for i in moves:
            move_list.append(i)
        a = random.randint(1, len(move_list))
        return move_list[a-1]
    # -------
    for i in moves:
        if type(best_move) == int:
            if moves[i] > best_move_point:
                best_move_point = moves[i]
                best_move = i
            elif moves[i] == best_move_point and not i == 0:
                best_move = [best_move, i]
        else:
            if moves[i] > best_move_point:
                best_move = i
                best_move_point = moves[i]
            elif moves[i] == best_move_point:
                best_move.append(i)

    if type(best_move) == int:
        return best_move
    else:
        x = random.randint(0, len(best_move)-1)
        return best_move[x]


def play_move_x(count, is_bot):
    global bot_moves
    global current_state
    if is_bot == True:
        bot_moves.append(current_state+'-'+str(count))

    current_state_list = []
    for i in current_state:
        current_state_list.append(i)

    current_state_list[count-1] = '1'
    current_state = ""
    for i in current_state_list:
        current_state += i


def play_move_o(count, is_bot):
    global bot_moves
    global current_state

    if is_bot:
        bot_moves.append(current_state+'-'+str(count))
    current_state_list = []
    for i in current_state:
        current_state_list.append(i)

    current_state_list[count-1] = '0'
    current_state = ""
    for i in current_state_list:
        current_state += i
    return True


def reward(is_win, point):
    global bot_moves
    bot_moves.reverse()
    if is_win == '0':
        point = -point
    elif is_win == '2':
        point = -point/2
    for move in range(0, len(bot_moves)):
        move_str = bot_moves[move].split('-')
        move_code = move_str[0]
        move_num = move_str[1]
        try:
            brain[move_code][int(move_num)] += point/(move+1)
        except Exception as ex:
            print(brain)
            # print(bot_moves)
            print(move_num)
            print(bot_moves)
            breakpoint()
    bot_moves.reverse()


def save_brain(name, brain):
    file = open(f'brains/{name}.txt', 'w')
    print(f'The brain named "{name}" is saving...')
    for i in brain:
        file.write(f'{i}')
        for x in brain[i]:
            file.write(f'_{x}:{brain[i][x]}')
        file.write('\n')
    file.close()
    print(f'Brain has saved.')


def load_brain(name):
    global brain
    try:
        file = open(f'brains/{name}.txt', 'r')
        print(f'The brain named "{name}" is loading...')
        for line in file:
            line = line.rstrip()
            line = line.split('_')
            moves = {}
            for x in range(1, len(line)):
                moves[int(line[x].split(':')[0])] = float(
                    line[x].split(':')[1])
            brain[line[0]] = moves
        file.close()
        print('Brain has loaded.')
    except FileNotFoundError:
        print(f'The file named "{name}" not found')


def play_random(num):  # num = '1' for x | num = '0' for O
    global current_state
    if check_finish() != '-1':
        return
    empty_slots = []
    for x in range(len(current_state)):
        if current_state[x] == '2':
            empty_slots.append(x)
    a = random.randint(0, len(empty_slots)-1)

    current_list = []
    for x in current_state:
        current_list.append(x)
    current_list[empty_slots[a]] = num
    current_state = ""
    for x in current_list:
        current_state += x


def check_finish():
    if current_state[0] != "2" and (current_state[0] == current_state[1] == current_state[2] or current_state[0] == current_state[3] == current_state[6] or current_state[0] == current_state[4] == current_state[8]):
        return current_state[0]
    elif current_state[3] != "2" and current_state[3] == current_state[4] == current_state[5]:
        return current_state[3]
    elif current_state[6] != "2" and (current_state[6] == current_state[7] == current_state[8] or current_state[6] == current_state[4] == current_state[2]):
        return current_state[6]
    elif current_state[1] != "2" and current_state[1] == current_state[4] == current_state[7]:
        return current_state[1]
    elif current_state[2] != "2" and current_state[2] == current_state[5] == current_state[8]:
        return current_state[2]
    elif '2' not in current_state:
        return '2'
    else:
        return '-1'


# side = 1(X) / 0(O) count = match count, start_random =
def train(side, count, start_random, random_reduce):
    global brain
    global current_state
    global bot_moves
    if side == '1' or side == 1:
        current_random = start_random
        for x in range(count):
            while check_finish() == '-1':
                moves = take_move_from_brain(current_state)
                choosed_move = choose_best_move(moves, current_random)
                play_move_x(choosed_move, True)
                play_random('0')
            reward(check_finish(), 1)
            current_random -= random_reduce
            current_state = '222222222'
            bot_moves = []
            if x % 10000 == 0:
                print(x)
    elif side == '0' or side == 0:
        current_random = start_random
        for x in range(count):
            while check_finish() == '-1':
                play_random('1')
                if check_finish() != '-1':
                    break
                moves = take_move_from_brain(current_state)
                choosed_move = choose_best_move(moves, current_random)
                play_move_o(choosed_move, True)
            reward(check_finish(), -1)
            current_random -= random_reduce
            current_state = '222222222'
            bot_moves = []
            if x % 10000 == 0:
                print(x)


def play_with_human(side):  # side=1:X 0:O:
    global current_state
    current_state = '222222222'
    if side == 1:
        while True:
            moves = take_move_from_brain(current_state)
            choosed_move = choose_best_move(moves, 0)
            play_move_x(choosed_move, True)
            show_board(current_state)
            if check_finish() != '-1':
                break
            slot = int(input('Please enter a slot for O: '))
            if play_move_o(slot, False):
                pass
        if check_finish() == '1':
            print('X is Won!')
        elif check_finish() == '0':
            print('O is Won!')
        else:
            print('Draw!')
    elif side == 0:
        while check_finish() == '-1':
            show_board(current_state)
            slot = int(input('Please enter a slot for X: '))
            if play_move_x(slot, False):
                pass
            if check_finish() != '-1':
                break
            moves = take_move_from_brain(current_state)
            choosed_move = choose_best_move(moves, 0)
            play_move_o(choosed_move, True)

        if check_finish() == '1':
            print('X is Won!')
        elif check_finish() == '0':
            print('O is Won!')
        else:
            print('Draw!')


load_brain('brain_1m_08_0000001_2')
while True:
    play_with_human(1)

train(0, 10000, 0.8, 0.0001)
save_brain('aysima', brain)
# load_brain('deneme2')1
# print(brain['211200012'])
# print(check_finish())
#moves = take_move_from_brain('222222222')
#print(choose_best_move(moves, 1))
