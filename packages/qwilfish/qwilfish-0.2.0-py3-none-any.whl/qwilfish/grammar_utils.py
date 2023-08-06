# Standard lib imports
import re
import random

# Local imports
from qwilfish.derivation_tree import all_terminals

HEX_MAP = {"0": "0000", "1": "0001", "2": "0010", "3": "0011",
           "4": "0100", "5": "0101", "6": "0110", "7": "0111",
           "8": "1000", "9": "1001", "A": "1010", "B": "1011",
           "C": "1100", "D": "1101", "E": "1110", "F": "1111"}

def srange(characters):
    return [c for c in characters]

def to_binstr(subtree, *args):
    symbol, children = subtree

    if children == []:
        if symbol == "x":
            return ("", []) # Turn single x:es into null expansions to remove
        else:
            new_symbol = \
                re.sub("x[0-9a-fA-F]{2}",
                       lambda hex: HEX_MAP[hex.group(0)[1:].upper()[0]] +
                                   HEX_MAP[hex.group(0)[1:].upper()[1]],
                       symbol)
            return (new_symbol, [])
    else:
        if symbol == "<hex>":
            child_symbol, _ = children[0]
            return (symbol, [(HEX_MAP[child_symbol], [])])

    return (symbol, [to_binstr(c, "") for c in children if children])

def fix_tlv_length(tl_bitlength):

    def fix_tlv_length_inner(subtree, *args):
        symbol, children = subtree
        n_bits = len(all_terminals(subtree)) - tl_bitlength

        assert n_bits % 8 == 0

        length = int(n_bits/8)
        bin_length = ["1" if length & (1 << i) else "0"
                      for i in range(8, -1, -1)]

        for i, c in enumerate(children):
            if c[0] == "<tlv-len>":
                children[i] = (children[i][0],
                               [("".join(bin_length), [])])

        return (symbol, children)

    return fix_tlv_length_inner

def gen_random_data(min_size, max_size):

    def gen_random_data_inner():
        length = random.randint(min_size, max_size)*8
        bin_data = [str(random.randint(0,1)) for i in range(0, length)]

        return "".join(bin_data)

    return gen_random_data_inner

