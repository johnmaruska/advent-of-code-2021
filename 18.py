from copy import deepcopy
import math


TEST_INPUT = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

with open('18.txt') as f:
    REAL_INPUT = f.read()


def parse_number(remaining):
    if remaining[0] == '[':
        left, remaining = parse_number(remaining[1:])  # without [
        assert remaining[0] == ','
        right, remaining = parse_number(remaining[1:])  # without ,
        assert remaining[0] == ']'
        remaining = remaining[1:]  # without ]
        return [[left, right], remaining]
    else:
        # cheating, just regex for d+
        num, remaining = remaining[0], remaining[1:]
        return [int(num), remaining]


def parse(input_str):
    return [parse_number(line)[0] for line in input_str.split('\n') if line]


def left_first_find(nested_xs, pred):
    def search_tree(parent, path=None):
        if path is None: path = []
        if pred(parent, path):  # parent is a leaf
            return path
        elif isinstance(parent, list):
            for idx, child in enumerate(parent):
                result = search_tree(child, path + [idx])
                if result: return result
            return None
        else:
            return None
    return search_tree(nested_xs)


def deep_get(tree, path):
    if not path:
        return tree
    elif isinstance(tree, list):
        return deep_get(tree[path[0]], path[1:])
    else:
        return None

def has_path(tree, path):
    return deep_get(tree, path) is not None


def deep_assign(tree, path, val):
    if len(path) == 1:
        tree[path[0]] = val
    else:
        deep_assign(tree[path[0]], path[1:], val)


def deep_update(tree, path, func):
    deep_assign(tree, path, func(deep_get(tree, path)))


def tree_scanner(node_order, tree, parent_path):
    if isinstance(tree, list):
        return (subpath for node in node_order
                for subpath in tree_scanner(node_order, tree[node], parent_path + [node]))
    else:
        return [parent_path]


def scan_past_pair_path(generator, path):
    for p in generator:
        if path == p[:len(path)]:
            break
    next(generator)
    return generator


def moving_left(tree, from_path):
    return scan_past_pair_path(tree_scanner([1, 0], tree, []), from_path)


def moving_right(tree, from_path):
    return scan_past_pair_path(tree_scanner([0, 1], tree, []), from_path)


def maybe_next(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None


def next_left_leaf(tree, from_path):
    return maybe_next(moving_left(tree, from_path))


def next_right_leaf(tree, from_path):
    return maybe_next(moving_right(tree, from_path))


def apply_explosion_rule(sf_number):
    def should_explode(parent, path):
        return isinstance(parent, list) and len(path) == 4

    def explode(tree, path):
        left, right = deep_get(tree, path)
        next_left, next_right = next_left_leaf(tree, path), next_right_leaf(tree, path)
        if next_left:
            deep_update(tree, next_left, lambda x: x + left)
        if next_right:
            deep_update(tree, next_right, lambda x: x + right)
        deep_assign(tree, path, 0)

    if path := left_first_find(sf_number, should_explode):
        explode(sf_number, path)
        return True
    return False


def check_explosion(sf_number, expected):
    number = deepcopy(sf_number)
    apply_explosion_rule(number)
    assert number == expected

check_explosion([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4])  # no left case
check_explosion([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]])  # no right case
check_explosion([[6,[5,[4,[3,2]]]], 1], [[6,[5,[7,0]]],3])
# # two applicable case
check_explosion([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
check_explosion([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]])


def split(number):
    return [math.floor(number/2), math.ceil(number/2)]

assert split(10) == [5, 5]
assert split(11) == [5, 6]
assert split(12) == [6, 6]

def apply_split_rule(sf_number):
    def should_split(leaf, path):
        return isinstance(leaf, int) and leaf >= 10

    if split_path := left_first_find(sf_number, should_split):
        deep_update(sf_number, split_path, split)
        return True
    return False


def sf_reduce(sf_number):
    reduced_number = deepcopy(sf_number)
    if apply_explosion_rule(reduced_number):
        return sf_reduce(reduced_number)
    elif apply_split_rule(reduced_number):
        return sf_reduce(reduced_number)
    else:
        return reduced_number


def add(a, b):
    return sf_reduce([a, b])


NUMBER = [[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]]
apply_explosion_rule(NUMBER); assert NUMBER == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
apply_explosion_rule(NUMBER); assert NUMBER == [[[[0,7],4],[15,[0,13]]],[1,1]]
apply_split_rule(NUMBER); assert NUMBER == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
apply_split_rule(NUMBER); assert NUMBER == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
apply_explosion_rule(NUMBER); assert NUMBER == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]


def sum_pairs(pairs):
    # this is just a reduce
    summation = sf_reduce(pairs[0])
    for pair in pairs[1:]:
        summation = add(summation, pair)
    return summation


def magnitude(number):
    if isinstance(number, int):
        return number
    else:
        return 3*magnitude(number[0]) + 2*magnitude(number[1])

PARSED = parse(TEST_INPUT)
SUMMED = sum_pairs(PARSED)
assert SUMMED == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
                  [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
assert magnitude(SUMMED) == 4140


def part1(input_str):
    return magnitude(sum_pairs(parse(input_str)))

assert part1(TEST_INPUT) == 4140
print(part1(REAL_INPUT))


def part2(input_str):
    pairs = parse(input_str)
    return max( magnitude(sum_pairs([pairs[i], pairs[j]]))
                for i in range(len(pairs))
                for j in range(len(pairs))
                if not i == j )

assert part2(TEST_INPUT) == 3993
print(part2(REAL_INPUT))
