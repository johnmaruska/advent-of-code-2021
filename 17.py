from math import sqrt

TEST_INPUT = 'target area: x=20..30, y=-10..-5'

with open('17.txt') as f:
    REAL_INPUT = f.read().strip()


def parse(input_str):
    def parse_range(range_str):
        return [int(x) for x in range_str[2:].split('..')]
    x, y = input_str[13:].split(', ')
    return {'x': parse_range(x), 'y': parse_range(y)}


def summation(n):
    return int(n * (n + 1) / 2)


def part1(input_str):
    area = parse(input_str)
    return summation(abs(min(area['y'])) - 1)


assert 45 == part1(TEST_INPUT)
print(part1(REAL_INPUT))


def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


def between(n, num_range):
    lower, higher = sorted(num_range)
    return lower <= n and n <= higher


def summation_to(n):
    return int(1/2 * (sqrt(8 * n + 1) - 1))


def in_area(area, position):
    return between(position['x'], area['x']) and between(position['y'], area['y'])


def missed_area(area, probe):
    below_y  = probe['position']['y'] < min(area['y'])
    dropping = probe['velocity']['y'] < 0
    passed_x = probe['position']['x'] > max(area['x'])
    return passed_x or (below_y and dropping)


AREA = parse('target area: x=20..30, y=-10..-5')
assert AREA == {'x':[20, 30], 'y': [-10, -5]}
assert in_area(AREA, {'x': 25, 'y': -7})


def step(probe):
    position, velocity = probe['position'], probe['velocity']
    return {'position': {'x': position['x'] + velocity['x'],
                         'y': position['y'] + velocity['y']},
            'velocity': {'x': velocity['x'] - sign(velocity['x']),
                         'y': velocity['y'] - 1}}


def velocity_works(area, velocity):
    vx, vy = velocity
    probe = {'position': {'x': 0, 'y': 0},
             'velocity': {'x': vx, 'y': vy} }
    while True:
        probe = step(probe)
        if in_area(area, probe['position']):
            return True
        if missed_area(area, probe):
            return False

assert velocity_works(AREA, [7, 2])
assert velocity_works(AREA, [6, 3])
assert not velocity_works(AREA, [17, -4])


def all_solutions(area):
    max_x, max_y = max(area['x']), max(area['y'])
    min_x, min_y = min(area['x']), min(area['y'])
    return [[vx, vy]
            for vx in range(summation_to(min_x), (max_x + 1))
            for vy in range(min_y, abs(min_y))
            if velocity_works(area, [vx, vy])]


def part2(input_str):
    area = parse(input_str)
    return len(all_solutions(area))

assert 112 == part2(TEST_INPUT)
print(part2(REAL_INPUT))
