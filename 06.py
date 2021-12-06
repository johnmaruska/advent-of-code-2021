TEST_INPUT="""3,4,3,1,2"""
SPAWN_TIME = 7
NUM_DAYS = 80

with open('06.txt') as f:
    REAL_INPUT = f.read()


def parse(input_str):
    return [int(x) for x in input_str.split(",")]


def step_day(fish):
    if fish == 0:
        return SPAWN_TIME - 1
    else:
        return fish - 1

assert step_day(0) == 6
assert step_day(1) == 0


def freqs_dict():
    return {k: 0 for k in range(SPAWN_TIME + 2)}

def frequencies(xs):
    freqs = freqs_dict()
    for x in xs:
        freqs[x] = freqs[x] + 1
    return freqs


assert frequencies([3, 4, 3, 1, 2]) == {
    0: 0, 1: 1, 2: 1, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0
}

def pass_day(freqs):
    new_freqs = freqs_dict()
    for k, v in freqs.items():
        new_freqs[step_day(k)] += v
    new_freqs[SPAWN_TIME + 1] = freqs[0]
    return new_freqs

assert pass_day(frequencies([3, 4, 3, 1, 2])) == {
    0: 1, 1: 1, 2: 2, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0
}

assert pass_day(frequencies([2, 3, 2, 0, 1])) == {
    0: 1, 1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 1
}

def simulate(input_str, days):
    # This is a good spot for a reduce
    freqs = frequencies(parse(input_str))
    for day in range(days):
        freqs = pass_day(freqs)
    return sum(freqs.values())


def part1(input_str):
    return simulate(input_str, 80)

assert part1(TEST_INPUT) == 5934
print(part1(REAL_INPUT))


def part2(input_str):
    return simulate(input_str, 256)

assert part2(TEST_INPUT) == 26984457539
print(part2(REAL_INPUT))
