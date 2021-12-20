# https://adventofcode.com/2021/day/3

import functools

TEST_INPUT="""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split("\n")

with open('03.txt') as f:
    REAL_INPUT = f.read().splitlines()


# Part 1


def parse(inp):
    return [[int(x) for x in line] for line in inp]

BINARIES = parse(TEST_INPUT)

def invert(binary):
    assert set(binary) == set(['0', '1'])
    return ''.join('1' if x == '0' else '0' for x in binary)


def decimal(binary):
    return int(binary, 2)


assert decimal('01001') == 9
assert decimal('10110') == 22


def to_string(binary):
    return "".join([str(bit) for bit in binary])


def most_common_bit(binaries, index):
    bits = [binary[index] for binary in binaries]
    ones = bits.count(1)
    zeroes = bits.count(0)
    if ones >= zeroes: return 1
    if zeroes > ones:  return 0


def most_common_bits(binaries):
    return [most_common_bit(binaries, index)
            for index in range(len(binaries[0]))]


assert most_common_bits(BINARIES, 0) == [1, 0, 1, 1, 0]


def gamma_rate(binaries):
    return to_string(most_common_bits(binaries))


def epsilon_rate(gamma):
    return invert(gamma)


assert gamma_rate(BINARIES) == '10110'
assert epsilon_rate(gamma_rate(BINARIES)) == '01001'


def part1(binaries):
    gamma = gamma_rate(binaries)
    epsilon = epsilon_rate(gamma)
    return decimal(gamma) * decimal(epsilon)


assert 198 == part1(BINARIES)
print(part1(parse(REAL_INPUT)))


# Part 2


def find_rating(binaries, func):
    remaining = binaries
    for idx in range(len(binaries[0])):
        mcb = most_common_bit(remaining, idx)
        remaining = [b for b in remaining if func(b[idx], mcb)]
        if len(remaining) == 1:
            return to_string(remaining[0])
    print(remaining)
    assert False == "Should not have reached here"


def oxygen_generator_rating(binaries):
    def oxygen_filter(bit, common):
        return bit == common
    return find_rating(binaries, oxygen_filter)


assert oxygen_generator_rating(BINARIES) == '10111'


def co2_scrubber_rating(binaries):
    def co2_filter(bit, common):
        return bit != common
    return find_rating(binaries, co2_filter)


assert co2_scrubber_rating(BINARIES) == '01010'


def part2(binaries):
    oxygen_generator = oxygen_generator_rating(binaries)
    co2_scrubber = co2_scrubber_rating(binaries)
    return decimal(oxygen_generator) * decimal(co2_scrubber)

print(part2(parse(REAL_INPUT)))
