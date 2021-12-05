# https://adventofcode.com/2021/day/5

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

with open('05.txt') as f:
    REAL_INPUT = f.read()


def parse_line(line_str):
    return [Point(*[int(x) for x in segment.split(",")])
            for segment in line_str.split(" -> ")]


assert parse_line("0,9 -> 5,9") == [Point(0, 9), Point(5, 9)]


def parse(input_str):
    return [parse_line(line) for line in input_str.split("\n") if line]


PARSED = [
    [Point(0, 9), Point(5, 9)],
    [Point(8, 0), Point(0, 8)],
    [Point(9, 4), Point(3, 4)],
    [Point(2, 2), Point(2, 1)],
    [Point(7, 0), Point(7, 4)],
    [Point(6, 4), Point(2, 0)],
    [Point(0, 9), Point(2, 9)],
    [Point(3, 4), Point(1, 4)],
    [Point(0, 0), Point(8, 8)],
    [Point(5, 5), Point(8, 2)]
]
assert parse(TEST_INPUT) == PARSED


def horizontal(segment):
    start, end = segment
    return start.x == end.x


def vertical(segment):
    start, end = segment
    return start.y == end.y


def reversible_range(start, end):
    increment = -1 if end < start else 1
    return range(start, end + increment, increment)


def segment_to_points(segment):
    p1, p2 = segment
    if horizontal(segment):
        start, end = min(p1.x, p2.x), max(p1.x, p2.x)
        return [Point(x, p1.y) for x in range(start, end + 1)]
    elif vertical(segment):
        start, end = min(p1.y, p2.y), max(p1.y, p2.y)
        return [Point(p1.x, y) for y in range(start, end + 1)]
    else:
        return [Point(x, y) for x, y in zip(reversible_range(p1.x, p2.x), reversible_range(p1.y, p2.y))]


assert segment_to_points([Point(0, 9), Point(5, 9)]) == [
    Point(0, 9),
    Point(1, 9),
    Point(2, 9),
    Point(3, 9),
    Point(4, 9),
    Point(5, 9)
]


def count_points(segments):
    counter = {}
    for segment in segments:
        for point in segment_to_points(segment):
            counter[point] = counter.get(point, 0) + 1
    return counter


def print_counts(point_counts):
    rows = ["".join( [str(point_counts.get(Point(col, row), '.'))
                               for col in range(10)])
            for row in range(10)]
    print("\n".join(rows))


def part1(input_str):
    segments = [segment for segment in parse(input_str)
                if horizontal(segment) or vertical(segment)]
    counts = count_points(segments)
    return len([c for c in counts.values() if c >= 2])


assert part1(TEST_INPUT) == 5
print(part1(REAL_INPUT))


def part2(input_str):
    segments = parse(input_str)
    counts = count_points(segments)
    return len([c for c in counts. values() if c >= 2])


assert part2(TEST_INPUT) == 12
print(part2(REAL_INPUT))
