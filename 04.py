# https://adventofcode.com/2021/day/4


TEST_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


with open('04.txt') as f:
    REAL_INPUT = f.read()


def are_boards_equal(board_a, board_b):
    for row_idx in range(len(board_a)):
        for col_idx in range(len(board_a[row_idx])):
            a_space = board_a[row_idx][col_idx]['number']
            b_space = board_b[row_idx][col_idx]['number']
            if a_space != b_space:
                return False
    return True


assert are_boards_equal(
    [[{'number': 1, 'marked': True}, {'number': 3, 'marked': True}],
     [{'number': 2, 'marked': True}, {'number': 4, 'marked': True}]],
    [[{'number': 1, 'marked': False}, {'number': 3, 'marked': False}],
     [{'number': 2, 'marked': False}, {'number': 4, 'marked': False}]]
    )


def board_already_won(board, win_order):
    for winner_board, number in win_order:
        if are_boards_equal(winner_board, board):
            return True
    return False


def parse_board(board):
    return [[{'number': int(n), 'marked': False}
             for n in row.split(" ") if n]
            for row in board.split("\n")
            if row]


def parse(input_str):
    sections = input_str.split("\n\n")
    numbers, boards = sections[0], sections[1:]
    return {
        "numbers": [int(n) for n in numbers.split(',')],
        "boards": [parse_board(board) for board in boards]
    }


def mark_board(board, number):
    for ridx, row, in enumerate(board):
        for cidx, col in enumerate(row):
            if col['number'] == number:
                board[ridx][cidx]['marked'] = True


def is_winner(board):
    for row in board:
        if all(space['marked'] for space in row):
            return True
    for col_idx in range(len(board[0])):
        column = [row[col_idx] for row in board]
        if all(space['marked'] for space in column):
            return True
    return False


def play_game(numbers, boards):
    win_order = []
    for number in numbers:
        for board in boards:
            if not board_already_won(board, win_order):
                mark_board(board, number)
                if is_winner(board):
                    win_order.append([board, number])
    return win_order


def score(winner, number):
    return number * sum([space['number'] for row in winner for space in row if not space['marked']])


def run_game(input_str):
    game = parse(input_str)
    return play_game(game['numbers'], game['boards'])


def part1(input_str):
    winner, number = run_game(input_str)[0]
    return score(winner, number)


def part2(input_str):
    winner, number = run_game(input_str)[-1]
    return score(winner, number)


assert part1(TEST_INPUT) == 4512
print(part1(REAL_INPUT))

assert part2(TEST_INPUT) == 1924
print(part2(REAL_INPUT))
