from math import prod

with open('16.txt') as f:
    REAL_INPUT = f.read().strip()

HEX_TO_BINARY = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

def decimal(binary):
    return int(binary, 2)

def binary(hexadecimal):
    return ''.join(HEX_TO_BINARY[hit] for hit in hexadecimal)

assert binary('D2FE28') == '110100101111111000101000'
assert binary('38006F45291200') == '00111000000000000110111101000101001010010001001000000000'
assert binary('EE00D40C823060') == '11101110000000001101010000001100100000100011000001100000'

def version(packet):
    return decimal(packet[:3])

def type_id(packet):
    return decimal(packet[3:6])


def parse_packet(packet_str):
    T = type_id(packet_str)
    literal, subpackets = None, None
    if T == 4:
        parsed, rem_str = parse_literal(packet_str)
    else:
        parsed, rem_str = parse_operator(packet_str)
    return {'V': version(packet_str), 'T': T, **parsed}, rem_str


def parse_literal(packet):
    groups, i = [], 0
    rem_str = packet[6:]
    while True:
        group = rem_str[:5]
        rem_str = rem_str[5:]
        groups.append(group[1:])
        if group[0] == '0': break
    return {'V': version(packet), 'T': type_id(packet), 'A': decimal(''.join(groups))}, rem_str

PARSED_LITERAL, _ = parse_literal('110100101111111000101000')
assert 2021 == PARSED_LITERAL['A']


def parse_I0(packet_str):
    L = decimal(packet_str[7:22])  # total length in bits of subpackets
    subpacket_bits, rem_str = packet_str[22:22+L], packet_str[22+L:]
    subpackets, bits_used = [], 0

    while subpacket_bits:
        subpacket, subpacket_bits = parse_packet(subpacket_bits)
        subpackets.append(subpacket)
    return {'L': L, 'subpackets': subpackets}, rem_str

PARSED_I0, _ = parse_I0('00111000000000000110111101000101001010010001001000000000')
assert 27 == PARSED_I0['L']
assert 10 == PARSED_I0['subpackets'][0]['A']
assert 20 == PARSED_I0['subpackets'][1]['A']


def parse_I1(packet_str):
    L = decimal(packet_str[7:18])  # number of subpackets
    rem_str = packet_str[18:]
    subpackets = []
    while len(subpackets) < L:
        subpacket, rem_str = parse_packet(rem_str)
        subpackets.append(subpacket)
    return {'L': L, 'subpackets': subpackets}, rem_str

PARSED_I1, _ = parse_I1('11101110000000001101010000001100100000100011000001100000')
assert 3 == PARSED_I1['L']
assert 1 == PARSED_I1['subpackets'][0]['A']
assert 2 == PARSED_I1['subpackets'][1]['A']
assert 3 == PARSED_I1['subpackets'][2]['A']


def parse_operator(packet_str):
    I = packet_str[6]
    if I == '0':
        parsed, rem_str = parse_I0(packet_str)
    else:
        parsed, rem_str = parse_I1(packet_str)
    return {'I': I, **parsed}, rem_str


def sum_versions(packet):
    sub_sum = sum([sum_versions(subpacket) for subpacket in packet.get('subpackets', [])])
    return packet['V'] + sub_sum


def part1(input_str):
    parsed, _ = parse_packet(binary(input_str))
    return sum_versions(parsed)


PARSED_PACKET, _ = parse_packet(binary('8A004A801A8002F478'))
assert 4 == PARSED_PACKET['V']
assert 1 == PARSED_PACKET['subpackets'][0]['V']
assert 5 == PARSED_PACKET['subpackets'][0]['subpackets'][0]['V']
assert 6 == PARSED_PACKET['subpackets'][0]['subpackets'][0]['subpackets'][0]['V']
assert 16 == sum_versions(PARSED_PACKET)

assert 12 == part1('620080001611562C8802118E34')
assert 23 == part1('C0015000016115A2E0802F182340')
assert 31 == part1('A0016C880162017C3686B18A3D4780')

print(part1(REAL_INPUT))


def eval_packet(packet):
    T = packet['T']
    if T == 4:
        return packet['A']

    subpackets = [eval_packet(subpacket) for subpacket in packet['subpackets']]
    def gt(xs): return xs[0] > xs[1]
    def lt(xs): return xs[0] < xs[1]
    def eq(xs): return xs[0] == xs[1]
    fn = [sum, prod, min, max, None, gt, lt, eq]
    return fn[T](subpackets)


def part2(input_str):
    parsed, _ = parse_packet(binary(input_str))
    return eval_packet(parsed)

assert part2('C200B40A82')     == 3   # sum
assert part2('04005AC33890')   == 54  # product
assert part2('880086C3E88112') == 7   # min
assert part2('CE00C43D881120') == 9   # max
assert part2('D8005AC2A8F0')   == 1   # <
assert part2('F600BC2D8F')     == 0   # >
assert part2('9C005AC2F8F0')   == 0   # ==
assert part2('9C0141080250320F1802104A08') == 1  # 1 + 3 == 2 * 2
print(part2(REAL_INPUT))
