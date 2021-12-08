TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

with open('08.txt') as f:
    REAL_INPUT = f.read()


def parse_line(line):
    uniq_displays, four_digits = line.split(' | ')
    return uniq_displays.split(' '), four_digits.split(' ')


def parse(input_str):
    return [parse_line(line) for line in input_str.split('\n') if line]


DIGIT_SEGMENTS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

def solve_guaranteed(uniq_displays):
    solved_displays = {}
    for display in uniq_displays:
        matches = [[digit, segments] for digit, segments in DIGIT_SEGMENTS.items()
                   if len(segments) == len(display)]
        if len(matches) == 1:
            digit, segments = matches[0]
            solved_displays[digit] = display
    return solved_displays


def segment_counts(displays):
    return {segment: len([display for display in displays if segment in display])
            for segment in 'abcdefg'}


# {'a': 8, 'b': 6, 'c': 8, 'd': 7, 'e': 4, 'f': 9, 'g': 7}
# {'a': 6, 'b': 4, 'c': 4, 'd': 5, 'e': 3, 'f': 5, 'g': 6}
COUNT_PAIRS = {
    (8, 6): 'a', (6, 4): 'b', (8, 4): 'c', (7, 5): 'd', (4, 3): 'e', (9, 5): 'f', (7, 6): 'g'
}
def solve_by_count(encoded_displays, digit_encodings):
    solved_segments = {}
    display_counts = segment_counts(encoded_displays)
    without_decoded = segment_counts(set(encoded_displays) - set(v for v in digit_encodings.values()))
    for encoded_segment in 'abcdefg':
        pair = tuple([display_counts[encoded_segment], without_decoded[encoded_segment]])
        correct_segment = COUNT_PAIRS[pair]
        solved_segments[encoded_segment] = correct_segment
    return solved_segments


def decode(display, code):
    decoded = set(code[segment] for segment in display)
    for digit, segments in DIGIT_SEGMENTS.items():
        if set(segments) == decoded:
            return digit


def solve_entry(entry):
    unique_displays, digits = entry
    guaranteed = solve_guaranteed(unique_displays)
    code = solve_by_count(unique_displays, guaranteed)
    return [decode(digit, code) for digit in digits]



def part1(input_str):
    entries = parse(input_str)
    decoded_entries = [solve_entry(entry) for entry in entries]
    return len([digit for digits in decoded_entries for digit in digits
                if digit in {1, 4, 7, 8}])

assert part1(TEST_INPUT) == 26
print(part1(REAL_INPUT))


def digits_to_int(digits):
    return int(''.join(str(d) for d in digits))


def part2(input_str):
    entries = parse(input_str)
    decoded_entries = [solve_entry(entry) for entry in entries]
    return sum(digits_to_int(digits) for digits in decoded_entries)


assert part2(TEST_INPUT) == 61229
print(part2(REAL_INPUT))
