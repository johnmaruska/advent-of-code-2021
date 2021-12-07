TEST_INPUT = """16,1,2,0,4,2,7,1,2,14"""

with open('07.txt') as f:
    REAL_INPUT = f.read()


def parse(input_str):
    return [int(x) for x in input_str.split(",")]


def distance(start, end):
    return abs(end - start)


def fuel_cost(start, end):
    d = distance(start, end)
    return int(d*(d+1)/2)


def find_min_cost(positions, approach, cost_func):
    return min([sum([cost_func(pos, meet) for pos in positions]) for meet in approach(positions)])


def median(positions):
    positions = sorted(positions)
    midpoint = len(positions) / 2
    if int(midpoint) == midpoint:
        candidates = [positions[int(midpoint)]]
    else:
        candidates = [positions[int(midpoint)], positions[int(midpoint) + 1]]
    return candidates


def mean(positions):
    mean = sum(positions) / len(positions)
    return [int(mean), int(mean) + 1]


def part1(input_str):
    return find_min_cost(parse(input_str), median, distance)

assert part1(TEST_INPUT) == 37
print(part1(REAL_INPUT))


def part2(input_str):
    return find_min_cost(parse(input_str), mean, fuel_cost)

assert part2(TEST_INPUT) == 168
print(part2(REAL_INPUT))
