from collections import defaultdict, namedtuple
from copy import copy

TEST_INPUT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

SLIGHTLY_LARGER_TEST = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

EVEN_LARGER_TEST = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


with open('12.txt') as f:
    REAL_INPUT = f.read()


def parse(input_str):
    return [line.split("-") for line in input_str.split("\n") if line]


def make_graph(edges):
    graph = defaultdict(set)
    for start, end in edges:
        graph[start].add(end)
        graph[end].add(start)
    return graph


def can_visit(cave, visits):
    return cave.isupper() or visits.get(cave, 0) == 0


def can_visit_pt2(cave, visits):
    any_small_visited_twice = any(v >= 2 for k, v in visits.items() if k.islower())
    if can_visit(cave, visits):
        return True
    else:
        return (visits[cave] == 1 \
                and not any_small_visited_twice \
                and cave not in ['start', 'end'])


def paths(graph, start, end, can_visit_func, curr_path = None, visits = None):
    if curr_path is None:
        curr_path = []
    curr_path = curr_path + [start]

    if visits is None:
        visits = {}
    visits = copy(visits)  # don't mutate outer version
    visits[start] = visits.get(start, 0) + 1

    if start == end:
        return [curr_path]
    else:
        return [path
                for neighbor in graph[start] if can_visit_func(neighbor, visits)
                for path in paths(graph, neighbor, end, can_visit_func, curr_path, visits) ]


def part1(input_str):
    graph = make_graph(parse(input_str))
    return len(paths(graph, 'start', 'end', can_visit))

assert part1(TEST_INPUT) == 10
assert part1(SLIGHTLY_LARGER_TEST) == 19
assert part1(EVEN_LARGER_TEST) == 226
print(part1(REAL_INPUT))


def part2(input_str):
    graph = make_graph(parse(input_str))
    return len(paths(graph, 'start', 'end', can_visit_pt2))

assert part2(TEST_INPUT) == 36
assert part2(SLIGHTLY_LARGER_TEST) == 103
assert part2(EVEN_LARGER_TEST) == 3509
print(part2(REAL_INPUT))
