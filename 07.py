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


def median(positions):
    positions = sorted(positions)
    return positions[int(len(positions) / 2)]


def mean(positions):
    return round(sum(positions) / len(positions))


def part1(input_str):
    positions = parse(input_str)
    meeting_point = median(positions)
    return sum([distance(pos, meeting_point) for pos in positions])

assert part1(TEST_INPUT) == 37
print(part1(REAL_INPUT))


def part2(input_str):
    positions = parse(input_str)
    meeting_point = mean(positions)
    return sum([fuel_cost(pos, meeting_point) for pos in positions])

assert part2(TEST_INPUT) == 168
print(part2(REAL_INPUT))
