TEST_INPUT="""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


with open('10.txt') as f:
    REAL_INPUT = f.read()


def parse(input_str):
    return [line for line in input_str.split('\n') if line]


# char pairs
OPEN_TO_CLOSE = { '[': ']', '(': ')', '{': '}', '<': '>' }
CLOSE_TO_OPEN = {v: k for k, v in OPEN_TO_CLOSE.items()}

# line status
CORRUPTED = 2
INCOMPLETE = 1
COMPLETE = 0


def check_pairs(line):
    stack = []
    for char in line:
        if char in OPEN_TO_CLOSE:
            stack.append(char)
        if char in CLOSE_TO_OPEN:
            match = stack.pop()
            if match != CLOSE_TO_OPEN[char]:
                return [CORRUPTED, char]
    return [INCOMPLETE if stack else COMPLETE, stack]


CORRUPT_SCORE = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
def part1(input_str):
    checked = [check_pairs(line) for line in parse(input_str)]
    return sum([ CORRUPT_SCORE[char]
                 for status, char in checked
                 if status == CORRUPTED ])

assert part1(TEST_INPUT) == 26397
print(part1(REAL_INPUT))


def autocomplete(rem_stack):
    return [OPEN_TO_CLOSE[char] for char in reversed(rem_stack)]


AUTOCOMPLETE_SCORE = { ')': 1, ']': 2, '}': 3, '>': 4 }
def score_auto(added_chars):
    total = 0
    for char in added_chars:
        total = total * 5 + AUTOCOMPLETE_SCORE[char]
    return total

assert score_auto('}}]])})]') == 288957
assert score_auto(')}>]})') == 5566
assert score_auto('}}>}>))))') == 1480781
assert score_auto(']]}}]}]}>') == 995444
assert score_auto('])}>') == 294


def part2(input_str):
    checked = [check_pairs(line) for line in parse(input_str)]
    scores = [score_auto(autocomplete(stack))
              for status, stack in checked
              if status == INCOMPLETE]
    middle_idx = int(len(scores) / 2)
    return sorted(scores)[middle_idx]

assert part2(TEST_INPUT) == 288957
print(part2(REAL_INPUT))
