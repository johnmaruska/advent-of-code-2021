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


def find_min_position(positions, approach, cost_func):
    def total_cost(meet):
        return sum([cost_func(pos, meet) for pos in positions])
    return min(approach(positions), key=total_cost)

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


def mode(positions):
    highest_count = max(positions.count(x) for x in set(positions))
    return [x for x in set(positions) if positions.count(x) == highest_count]


def brute_force(positions):
    return list(range(min(positions), max(positions) + 1))


PART_1 = {'example': {'cost': 37,       'position': 2},
          'real':    {'cost': 337833,   'position': 331},
          'cost': distance}
PART_2 = {'example': {'cost': 168,      'position': 5},
          'real':    {'cost': 96678050, 'position': 461},
          'cost': fuel_cost}

def test(approach, input_str, expected, cost_func):
    actual_cost = find_min_cost(parse(input_str), approach, cost_func)
    actual_position = find_min_position(parse(input_str), approach, cost_func)
    print(f"approach {approach.__name__} test data => {actual_cost} == {expected['cost']}")
    print(f"positions are {actual_position} == {expected['position']}")
    # assert actual_cost == expected['cost']

def test_part(approach, part):
    test(approach, TEST_INPUT, part['example'], part['cost'])
    test(approach, REAL_INPUT, part['real'], part['cost'])

print("Part 1:")
test_part(median, PART_1)
test_part(brute_force, PART_1)

print("Part 2:")
test_part(median, PART_2)
test_part(brute_force, PART_2)


def part1(input_str):
    return find_min_cost(parse(input_str), median, distance)

assert part1(TEST_INPUT) == 37
print(part1(REAL_INPUT))


def part2(input_str):
    return find_min_cost(parse(input_str), mean, fuel_cost)

assert part2(TEST_INPUT) == 168
print(part2(REAL_INPUT))
