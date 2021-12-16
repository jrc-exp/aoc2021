""" Day 16 Solutions """

import sys
import heapq
from collections import defaultdict, Counter
from time import time
import numpy as np
from aoc.y2021.utils import load_data


def hex2bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    def parse_header(bin_str):
        ver = int(bin_str[:3], 2)
        typ = int(bin_str[3:6], 2)
        return ver, typ

    def parse_literal(bin_str):
        ver, typ = parse_header(bin_str)
        assert typ == 4
        idx = 6
        number = ""
        while True:
            number += bin_str[idx + 1 : idx + 5]
            if not int(bin_str[idx]):
                idx += 5
                break
            idx += 5
        number = int(number, 2)
        return ver, typ, number, idx

    def parse_operator(bin_str):
        ver = int(bin_str[:3], 2)
        op_typ = int(bin_str[3:6], 2)
        len_typ = int(bin_str[6])
        idx = 7
        tot_len_in_bits = np.inf
        num_sub_pkts = np.inf
        if len_typ == 0:
            tot_len_in_bits = int(bin_str[idx : idx + 15], 2)
            idx += 15
        if len_typ == 1:
            num_sub_pkts = int(bin_str[idx : idx + 11], 2)
            idx += 11
        bits_consumed, pkts_consumed = 0, 0
        total_ver = ver
        number_list = []
        while bits_consumed < tot_len_in_bits and pkts_consumed < num_sub_pkts:
            ver, typ = parse_header(bin_str[idx:])
            if typ == 4:
                ver, typ, number, consumed = parse_literal(bin_str[idx:])
                number_list.append(number)
            else:
                ver, typ, consumed, spec_val = parse_operator(bin_str[idx:])
                number_list.append(spec_val)
            idx += consumed
            bits_consumed += consumed
            pkts_consumed += 1
            total_ver += ver
        if op_typ == 0:
            special_val = sum(number_list)
        if op_typ == 1:
            special_val = np.prod(number_list)
        if op_typ == 2:
            special_val = np.min(number_list)
        if op_typ == 3:
            special_val = np.max(number_list)
        if op_typ == 5:
            special_val = 1 if number_list[0] > number_list[1] else 0
        if op_typ == 6:
            special_val = 1 if number_list[0] < number_list[1] else 0
        if op_typ == 7:
            special_val = 1 if number_list[0] == number_list[1] else 0
        return total_ver, typ, idx, special_val

    assert parse_operator(hex2bin("8A004A801A8002F478"))[0] == 16
    assert parse_operator(hex2bin("620080001611562C8802118E34"))[0] == 12
    assert parse_operator(hex2bin("C0015000016115A2E0802F182340"))[0] == 23
    assert parse_operator(hex2bin("A0016C880162017C3686B18A3D4780"))[0] == 31

    assert parse_operator(hex2bin("C200B40A82"))[-1] == 3
    assert parse_operator(hex2bin("04005AC33890"))[-1] == 54
    assert parse_operator(hex2bin("880086C3E88112"))[-1] == 7
    assert parse_operator(hex2bin("CE00C43D881120"))[-1] == 9
    assert parse_operator(hex2bin("F600BC2D8F"))[-1] == 0
    assert parse_operator(hex2bin("9C005AC2F8F0"))[-1] == 0
    assert parse_operator(hex2bin("9C0141080250320F1802104A08"))[-1] == 1

    print("All tests passed.")

    result_1 = parse_operator(hex2bin(d[0]))[0]
    result_2 = parse_operator(hex2bin(d[0]))[-1]

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
