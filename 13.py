from collections import namedtuple

TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

with open('13.txt') as f:
    REAL_INPUT = f.read()


Coord = namedtuple('Coord', ['x', 'y'])
Fold = namedtuple('Fold', ['axis', 'value'])


def parse_fold(fold_str):
    axis, val = fold_str[11:].split('=')
    return Fold(axis, int(val))


def parse_coord(coord_str):
    x, y = coord_str.split(",")
    return Coord(int(x), int(y))


def parse(input_str):
    dots, folds = input_str.split("\n\n")
    dots = [parse_coord(d) for d in dots.split("\n") if d]
    folds = [parse_fold(f) for f in folds.split("\n") if f]
    return dots, folds


def make_paper(coords):
    max_x = max(c.x for c in coords)
    max_y = max(c.y for c in coords)
    paper = [[False for x in range(max_x + 1)]
             for y in range(max_y + 1)]
    for coord in coords:
        paper[coord.y][coord.x] = True
    return paper


def merge_papers(a, b):
    return [[a[y][x] or b[y][x]
             for x in range(len(a[y]))]
            for y in range(len(a))]


def fold_x(paper, col):
    unchanged = [row[:col] for row in paper]
    flipped = [list(reversed(row[col+1:])) for row in paper]
    return merge_papers(unchanged, flipped)


def fold_y(paper, row):
    unchanged = paper[:row]
    flipped = list(reversed(paper[row+1:]))
    return merge_papers(unchanged, flipped)


def fold_paper(paper, fold):
    if fold.axis == 'x':
        return fold_x(paper, fold.value)
    else:
        return fold_y(paper, fold.value)


def count_visible(paper):
    return len([cell
                for row in paper
                for cell in row
                if cell])

def part1(input_str):
    dots, folds = parse(input_str)
    paper = make_paper(dots)
    return count_visible(fold_paper(paper, folds[0]))


assert part1(TEST_INPUT) == 17
print(part1(REAL_INPUT))


def str_paper(paper):
    return '\n'.join([''.join(['#' if cell else '.' for cell in row])
                      for row in paper])


def part2(input_str):
    dots, folds = parse(input_str)
    paper = make_paper(dots)
    for fold in folds:
        paper = fold_paper(paper, fold)
    return paper

print(str_paper(part2(REAL_INPUT)))
