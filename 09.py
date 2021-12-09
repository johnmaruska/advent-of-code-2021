from collections import namedtuple
from math import prod

TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""

with open('09.txt') as f:
    REAL_INPUT = f.read()

Point = namedtuple('Point', ['x', 'y'])


def parse(input_str):
    return [[int(digit) for digit in line]
            for line in input_str.split("\n") if line]


def adjacent_points(heightmap, point):
    above = Point(point.x, point.y - 1)
    below = Point(point.x, point.y + 1)
    right = Point(point.x + 1, point.y)
    left  = Point(point.x - 1, point.y)

    def is_in_bounds(p):
        rows, cols = len(heightmap), len(heightmap[0])
        return (p.y < rows and p.y >= 0) and (p.x < cols and p.x >= 0)

    return [ p for p in [above, below, right, left] if is_in_bounds(p) ]


def height(heightmap, point):
    return heightmap[point.y][point.x]


def is_low_point(heightmap, point):
    adjacent_heights = [height(heightmap, p) for p in adjacent_points(heightmap, point)]
    return height(heightmap, point) < min(adjacent_heights)


def all_points(heightmap):
    return [Point(x=c, y=r)
            for c in range(len(heightmap[0]))
            for r in range(len(heightmap))]


def find_low_points(heightmap):
    return [p for p in all_points(heightmap) if is_low_point(heightmap, p)]


def sum_risk_levels(heights):
    return len(heights) + sum(heights)


def part1(input_str):
    heightmap = parse(input_str)
    heights = [height(heightmap, p) for p in find_low_points(heightmap)]
    return sum_risk_levels(heights)


assert part1(TEST_INPUT) == 15
print(part1(REAL_INPUT))


def next_flow(heightmap, point):
    return [p for p in adjacent_points(heightmap, point)
            if height(heightmap, p) < height(heightmap, point)]


def fed_directly_by(heightmap):
    fed_by = {}
    for point in all_points(heightmap):
        for nxt in next_flow(heightmap, point):
            fed_by[nxt] = fed_by.get(nxt, set()).union(set([point]))
    return fed_by


# technically this is just "points that flow into this point"
# when point is a low point, that makes it a basin
def basin(point, fed_by_map, heightmap):
    def build_basin(p):
        feeders = fed_by_map.get(p, {})
        return {p}.union(*[build_basin(feeder)
                           for feeder in feeders
                           if height(heightmap, feeder) != 9])
    return build_basin(point)


def part2(input_str):
    heightmap = parse(input_str)
    fed_by_map = fed_directly_by(heightmap)
    basins = [basin(p, fed_by_map, heightmap) for p in find_low_points(heightmap)]
    return prod(sorted(len(b) for b in basins)[-3:])


assert part2(TEST_INPUT) == 1134
print(part2(REAL_INPUT))
