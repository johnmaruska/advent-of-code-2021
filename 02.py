# https://adventofcode.com/2021/day/2

import functools

TEST_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split("\n")

with open('02.txt') as f:
    REAL_INPUT = f.readlines()


# Part 1

def parse_l(line):
    # [direction, amount]
    split = line.split(" ")
    return [split[0], int(split[1])]

def parse(inp):
    # returns [(direction, amount), ...]
    return [parse_l(line) for line in inp]

assert parse(TEST_INPUT) == [
    ['forward', 5],
    ['down', 5],
    ['forward', 8],
    ['up', 3],
    ['down', 8],
    ['forward', 2]
]


def move_vector_pt1(pos2, vec):
    direction, magnitude = vec
    horizontal, depth = pos2
    assert direction in ['forward', 'up', 'down']
    if direction == 'forward':
        return [horizontal + magnitude, depth]
    elif direction == 'up':
        return [horizontal, depth - magnitude]
    elif direction == 'down':
        return [horizontal, depth + magnitude]

assert move_vector_pt1([0, 0], ['forward', 5]) == [5, 0]
assert move_vector_pt1([5, 0], ['down', 5]) == [5, 5]
assert move_vector_pt1([13, 5], ['up', 3]) == [13, 2]


def part1(movements):
    horizontal, depth = functools.reduce(move_vector_pt1, movements, [0, 0])
    return horizontal * depth

assert 150 == part1(parse(TEST_INPUT))
print(part1(parse(REAL_INPUT)))


# Part 2

def move_vector_pt2(pos3, vec):
    direction, magnitude = vec
    horizontal, depth, aim = pos3
    assert direction in ['forward', 'up', 'down']
    if direction == 'forward':
        return [horizontal + magnitude,
                depth + aim * magnitude,
                aim]
    elif direction == 'up':
        return [horizontal, depth, aim - magnitude]
    elif direction == 'down':
        return [horizontal, depth, aim + magnitude]

assert move_vector_pt2([0, 0, 0], ['forward', 5]) == [5, 0, 0]
assert move_vector_pt2([5, 0, 0], ['down', 5]) == [5, 0, 5]
assert move_vector_pt2([13, 40, 5], ['up', 3]) == [13, 40, 2]


def part2(movements):
    horizontal, depth, aim = functools.reduce(move_vector_pt2, movements, [0, 0, 0])
    return horizontal * depth

assert 900 == part2(parse(TEST_INPUT))
print(part2(parse(REAL_INPUT)))
