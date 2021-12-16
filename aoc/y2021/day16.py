""" Day 16 Solutions """

from enum import IntEnum, Enum
from types import SimpleNamespace
import sys
import heapq
from collections import defaultdict, Counter
from time import time
import numpy as np
from aoc.y2021.utils import load_data


def hex2bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)


class OpType(IntEnum):
    SUM = 0
    PROD = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7


BITS = SimpleNamespace(
    VER_SLICE=slice(3),
    TYPE_SLICE=slice(3, 6),
    PAYLOAD_IDX=6,
    LIT_GRP_SLICE=slice(1, 5),
    LIT_GRP_LEN=5,
)


class LenType(IntEnum):
    LEN_IN_BITS = 0
    NUM_SUB_PKTS = 1


LEN_TYPE_BITS = {
    LenType.LEN_IN_BITS: 15,
    LenType.NUM_SUB_PKTS: 11,
}


ACCUM_OP = {
    OpType.SUM: sum,
    OpType.PROD: np.prod,
    OpType.MIN: min,
    OpType.MAX: max,
    OpType.LITERAL: lambda x: x,
    OpType.GREATER: lambda x: 1 if x[0] > x[1] else 0,
    OpType.LESS: lambda x: 1 if x[0] < x[1] else 0,
    OpType.EQUAL: lambda x: 1 if x[0] == x[1] else 0,
}

# Currently this is true:
# LITERAL HEADER + TWO ENTRIES = 16 bits: VVVTTTAAAAABBBBB,
# OPS MUST BE AT LEAST 18: VVVTTTPXXXXXXXXXXX
MIN_PKT_LEN_BITS = 16


def decode_bits_to_int(bit_str, bit_slice):
    return int(bit_str[bit_slice], 2)


def parse_header(bin_str):
    ver = decode_bits_to_int(bin_str, BITS.VER_SLICE)
    typ = decode_bits_to_int(bin_str, BITS.TYPE_SLICE)
    return ver, OpType(typ)


def parse_literal(bin_str):
    """Parse a literal packet"""
    ver, _ = parse_header(bin_str)
    consumed = BITS.PAYLOAD_IDX
    number = ""
    while True:
        number += bin_str[consumed:][BITS.LIT_GRP_SLICE]
        if not int(bin_str[consumed]):
            consumed += BITS.LIT_GRP_LEN
            break
        consumed += BITS.LIT_GRP_LEN
    number = int(number, 2)
    return number, ver, consumed


def parse_operator(bin_str):
    """Parse binary string for operator"""
    ver, op_type = parse_header(bin_str)

    # parse length type and determine number of bits or pkts:
    len_typ = LenType(int(bin_str[BITS.PAYLOAD_IDX]))
    idx = BITS.PAYLOAD_IDX + 1
    tot_len_in_bits = np.inf
    num_sub_pkts = np.inf
    if len_typ == LenType.LEN_IN_BITS:
        tot_len_in_bits = int(bin_str[idx : idx + LEN_TYPE_BITS[len_typ]], 2)
    if len_typ == LenType.NUM_SUB_PKTS:
        num_sub_pkts = int(bin_str[idx : idx + LEN_TYPE_BITS[len_typ]], 2)
    idx += LEN_TYPE_BITS[len_typ]
    bits_consumed, pkts_consumed = 0, 0
    total_ver = ver
    number_list = []

    # parse sub packets until done:
    while bits_consumed < tot_len_in_bits and pkts_consumed < num_sub_pkts:
        ver, typ = parse_header(bin_str[idx:])
        if typ == OpType.LITERAL:
            number, ver, consumed = parse_literal(bin_str[idx:])
        else:
            number, ver, consumed = parse_operator(bin_str[idx:])
        number_list.append(number)
        idx += consumed
        bits_consumed += consumed
        pkts_consumed += 1
        total_ver += ver

    # apply accumulator to collected numbers
    accumulator = ACCUM_OP[OpType(op_type)]
    number = accumulator(number_list)

    return number, total_ver, idx


def parse_binary_string(bin_str):
    """Parse a binary string"""
    ver, typ = parse_header(bin_str)
    consumed = 0
    ct = 0
    while consumed < len(bin_str) - MIN_PKT_LEN_BITS:
        ct += 1
        if typ == OpType.LITERAL:
            number, consumed = parse_literal(bin_str[consumed:])
        else:
            number, ver, consumed = parse_operator(bin_str[consumed:])
    assert ct == 1, "More than one outer packet parsed?"

    return number, ver


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    assert parse_binary_string(hex2bin("8A004A801A8002F478"))[1] == 16
    assert parse_binary_string(hex2bin("620080001611562C8802118E34"))[1] == 12
    assert parse_binary_string(hex2bin("C0015000016115A2E0802F182340"))[1] == 23
    assert parse_binary_string(hex2bin("A0016C880162017C3686B18A3D4780"))[1] == 31

    assert parse_binary_string(hex2bin("C200B40A82"))[0] == 3
    assert parse_binary_string(hex2bin("04005AC33890"))[0] == 54
    assert parse_binary_string(hex2bin("880086C3E88112"))[0] == 7
    assert parse_binary_string(hex2bin("CE00C43D881120"))[0] == 9
    assert parse_binary_string(hex2bin("F600BC2D8F"))[0] == 0
    assert parse_binary_string(hex2bin("9C005AC2F8F0"))[0] == 0
    assert parse_binary_string(hex2bin("9C0141080250320F1802104A08"))[0] == 1

    print("All tests passed.")

    number, total_ver = parse_binary_string(hex2bin(d[0]))
    result_1 = total_ver
    result_2 = number

    assert result_1 == 897
    assert result_2 == 9485076995911

    return result_1, result_2


def main():
    """Main function"""
    start = time()
    # load data:
    print("**** REAL DATA ****")
    d = load_data("day16.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)
    print(f"Took {time() - start:.3f}s")


if __name__ == "__main__":
    main()
