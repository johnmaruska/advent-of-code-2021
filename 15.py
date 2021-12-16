from collections import namedtuple
from queue import PriorityQueue

TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

with open('15.txt') as f:
    REAL_INPUT = f.read()


def parse(input_str):
    return [[int(x) for x in line]
            for line in input_str.split("\n") if line]

Coord = namedtuple('Coord', ['x', 'y'])


def adjacent(grid, coord):
    above = Coord(coord.x, coord.y - 1)
    below = Coord(coord.x, coord.y + 1)
    right = Coord(coord.x + 1, coord.y)
    left  = Coord(coord.x - 1, coord.y)

    def is_in_bounds(p):
        rows, cols = len(grid), len(grid[0])
        return (p.y < rows and p.y >= 0) and (p.x < cols and p.x >= 0)

    return [ p for p in [above, below, right, left] if is_in_bounds(p) ]


def bottom_right_most(grid):
    max_x, max_y = len(grid[0]) - 1, len(grid) - 1
    return Coord(max_x, max_y)


def best_first_search(grid):
    start, goal = Coord(0, 0), bottom_right_most(grid)
    queue = PriorityQueue()
    visited = set()
    queue.put((0, start))
    while not queue.empty():
        cost, coord = queue.get()
        if coord in visited:
            continue

        visited.add(coord)
        if goal == coord:
            return cost
        else:
            for neighbor in adjacent(grid, coord):
                if not neighbor in visited:
                    next_cost = cost + grid[neighbor.y][neighbor.x]
                    queue.put((next_cost, neighbor))


def part1(input_str):
    grid = parse(input_str)
    return best_first_search(grid)


assert part1(TEST_INPUT) == 40
print(part1(REAL_INPUT))


def embiggen(grid):
    def inc(x, n):
        if x + n > 9:
            return x + n - 9
        else:
            return x + n
    # widen rows
    grid = [[inc(x, n) for n in range(5) for x in row] for row in grid]
    # stack grids
    return [[inc(x, n) for x in row] for n in range(5) for row in grid]


def part2(input_str):
    grid = embiggen(parse(input_str))
    return best_first_search(grid)


assert part2(TEST_INPUT) == 315
print(part2(REAL_INPUT))
