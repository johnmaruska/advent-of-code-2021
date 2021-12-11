from collections import namedtuple

TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

with open('11.txt') as f:
    REAL_INPUT = f.read()


Coord = namedtuple('Coord', ['x', 'y'])

# this is just acting as a namedtuple i can modify
# could be a dict but this seems nicer
class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.flashed = False


def parse(input_str):
    return [[Octopus(int(x)) for x in line]
            for line in input_str.split("\n")
            if line]


def all_coords(board):
    return [Coord(x, y)
            for y, row in enumerate(board)
            for x, cell in enumerate(row)]


def in_bounds(board, coord):
    in_x_bound = coord.x >= 0 and coord.x < len(board[0])
    in_y_bound = coord.y >= 0 and coord.y < len(board)
    return in_x_bound and in_y_bound


def adjacent(board, coord):
    adj = []  # no comprehension because assignment p =
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            p = Coord(coord.x + dx, coord.y + dy)
            if (dy != 0 or dx != 0) and in_bounds(board, p):
                adj.append(p)
    return adj


def octopus(board, coord):
    return board[coord.y][coord.x]


def should_flash(board, coord):
    oc = octopus(board, coord)
    return oc.energy > 9 and not oc.flashed


def flash(board, coord):
    """ Side-effecty, mutates board state. """
    octopus(board, coord).flashed = True
    for neighbor in adjacent(board, coord):
        octopus(board, neighbor).energy += 1
        if should_flash(board, neighbor):
            flash(board, neighbor)


def step(board):
    """ Side-effecty, mutates board state. """
    # energy level of each increases by 1
    for coord in all_coords(board):
        octopus(board, coord).flashed = False
        octopus(board, coord).energy += 1

    # do flashes
    for coord in all_coords(board):
        if should_flash(board, coord):
            flash(board, coord)

    # reset flashes
    total_flashes = 0
    for coord in all_coords(board):
        if octopus(board, coord).flashed:
            total_flashes += 1
            octopus(board, coord).energy = 0

    return total_flashes


def part1(input_str):
    board = parse(input_str)
    total_flashes = 0
    for i in range(100):
        total_flashes += step(board)
    return total_flashes


assert part1(TEST_INPUT) == 1656
print(part1(REAL_INPUT))


def part2(input_str):
    board = parse(input_str)
    octopi_count = len(all_coords(board))
    after_step = 0
    while True:
        flashes = step(board)
        after_step += 1
        if flashes == octopi_count:
            return after_step


assert part2(TEST_INPUT) == 195
print(part2(REAL_INPUT))
