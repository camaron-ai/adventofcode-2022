import json
from typing import List, Union, Tuple
import itertools
from dataclasses import dataclass

PacketType = List[Union[int, List[int]]]
Pair = Tuple[PacketType, PacketType]

TEST_PAIR = """[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


EXPECTED_TEST_PAIR = (
    [1,[2,[3,[4,[5,6,7]]]],8,9],
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    )


def parse_single_pair(pair_plain_text: str) -> Pair:
    p1, p2 = pair_plain_text.splitlines()

    return json.loads(p1), json.loads(p2)

assert parse_single_pair(TEST_PAIR) == EXPECTED_TEST_PAIR


def parse_input(plain_text: str ) -> List[Pair]:
    return [
        parse_single_pair(pair_plain_text) 
        for pair_plain_text in plain_text.strip().split('\n\n')
        ]


def compare_integers(x1: int, x2: int) -> int:
    """return 1 if x1 < x2, 0 if x1 == x2 else -1"""
    return min(max(x2 - x1, -1), 1)

def is_pair_in_right_order(
    p1: PacketType,
    p2: PacketType,
    i: int = 0
    ) -> bool:

    # if we reach the end of any package is because
    # we couldn't make a decision before, therefore 
    # if len(p1) < len(p2), then they are in order
    # if they are equal, we can not make a decision
    # otherwise, they are not in order
    if i == min(len(p1), len(p2)):
        return compare_integers(len(p1), len(p2))
    
    left, right = p1[i], p2[i]
    left_is_int = isinstance(left, int)
    right_is_int = isinstance(right, int)

    if left_is_int and right_is_int:
        status = compare_integers(left, right)
    else:
        left = [left] if left_is_int else left
        right = [right] if right_is_int else right

        # determine if the inner package is in order
        status = is_pair_in_right_order(left, right)
    # not decision can be made so far, move to the next element
    if status == 0:
        return is_pair_in_right_order(p1, p2, i + 1)
    return status


def compute_right_index_sum(pairs: List[Pair]):
    return sum(
        [i + 1 
        for i, pair in enumerate(pairs)
        if is_pair_in_right_order(*pair) == 1])

@dataclass
class Packet:
    packet: PacketType
    def __lt__(self, other: 'Packet') -> bool:
        return is_pair_in_right_order(self.packet, other.packet) == 1


def find_decoder_key(pairs):
    packets = list(itertools.chain.from_iterable(pairs))
    packets.append([[2]])
    packets.append([[6]])
    # sort them using the above function
    sorted_packets = sorted(packets, key=Packet)

    # find the indices of the divider packets
    first_div_packet_idx = sorted_packets.index([[2]]) + 1
    second_div_packet_idx = sorted_packets.index([[6]]) + 1
    # return the decoder key
    return first_div_packet_idx * second_div_packet_idx


if __name__ == '__main__':

    with open('data/test_case.txt') as f:
        test_plain_text = f.read()
    
    test_case = parse_input(test_plain_text)
    test_right_index_sum = compute_right_index_sum(test_case)

    assert test_right_index_sum == 13, test_right_index_sum

    test_decoder_key = find_decoder_key(test_case)
    assert test_decoder_key == 140


    with open('data/input.txt') as f:
        plain_text = f.read()
    
    pairs = parse_input(plain_text)
    right_index_sum = compute_right_index_sum(pairs)
    print(right_index_sum)

    decoder_key = find_decoder_key(pairs)
    print(decoder_key)
