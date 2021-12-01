# Part 1

TEST_INPUT = """199
200
208
210
200
207
240
269
260
263""".split("\n")

with open('01.txt') as f:
    REAL_INPUT = f.readlines()

def parse(inp):
    return [int(s) for s in inp]

def part1(depth_readings):
    larger_count = 0
    for idx in range(1, len(depth_readings)):
        if depth_readings[idx] > depth_readings[idx-1]:
            larger_count += 1
    return larger_count

assert 7 == part1(parse(TEST_INPUT))
print(part1(parse(REAL_INPUT)))


# Part 2

def sliding_window(arr, n):
    return [[arr[start + offset] for offset in range(n)]
            for start in range(len(arr) - n + 1)]

assert list(sliding_window([0, 1, 2, 3], 2)) == [[0, 1], [1, 2], [2, 3]]
assert list(sliding_window([0, 1, 2, 3], 3)) == [[0, 1, 2], [1, 2, 3]]

def part2(depth_readings):
    larger_count = 0
    windows = list(sliding_window(depth_readings, 3))
    for idx in range(1, len(windows)):
        if sum(windows[idx]) > sum(windows[idx-1]):
            larger_count += 1
    return larger_count

assert 5 == part2(parse(TEST_INPUT))
print(part2(parse(REAL_INPUT)))
