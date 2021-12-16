from collections import defaultdict

TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

with open('14.txt') as f:
    REAL_INPUT = f.read()


def parse_rules(rules_str):
    split_rules = [rule.split(' -> ') for rule in rules_str.split("\n") if rule]
    return {k: v for k, v in split_rules}


def parse(input_str):
    template, rules_str = input_str.split("\n\n")
    return template, parse_rules(rules_str)


def sliding_pairs(template):
    return [f"{template[i]}{template[i+1]}" for i in range(len(template) - 1)]


def frequencies(pairs):
    d = defaultdict(int)
    for pair in pairs:
        d[pair] += 1
    return d


def elements(pairs):
    return set([element for pair in pairs for element in pair])


def count_elements(template, freqs):
    counts = defaultdict(int)

    # add freq count for each element in each pair
    for pair, freq in freqs.items():
        for element in pair:
            counts[element] += freq
    # add first and last element since they won't be double counted
    counts[template[0]] += 1
    counts[template[-1]] += 1
    # halve each counts since they all get double counted
    return {k: int(v/2) for k, v in counts.items()}


def step(freqs, rules):
    next_freqs = defaultdict(int)
    for pair, freq in freqs.items():
        if pair in rules:
            mid_char = rules[pair]
            next_freqs[f"{pair[0]}{mid_char}"] += freq
            next_freqs[f"{mid_char}{pair[1]}"] += freq
        else:
            next_freqs[pair] += freq
    return next_freqs


def spread_after_steps(input_str, n_steps):
    template, rules = parse(input_str)
    freqs = frequencies(sliding_pairs(template))
    for steps in range(n_steps):
        freqs = step(freqs, rules)
    counts = count_elements(template, freqs)
    most_common, least_common = max(counts.values()), min(counts.values())
    return most_common - least_common


def part1(input_str):
    return spread_after_steps(input_str, 10)

assert part1(TEST_INPUT) == 1588
print(part1(REAL_INPUT))


def part2(input_str):
    return spread_after_steps(input_str, 40)

assert part2(TEST_INPUT) == 2188189693529
print(part2(REAL_INPUT))
