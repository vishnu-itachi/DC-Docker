from collections import Counter
from pprint import pprint
from typing import List, Dict


def read_lines(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.readlines()


def process_file(lines: List[str]) -> Dict:
    frequency_dict = {}
    for line in lines:
        f_dict = Counter(line)
        frequency_dict = frequency_dict | f_dict
    return frequency_dict


if __name__ == "__main__":
    lines = read_lines("./shared/input.txt")
    frequency_dict = process_file(lines)
    pprint(frequency_dict)
