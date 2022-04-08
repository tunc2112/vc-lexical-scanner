import os
import sys

from rule import AutomatonData
from parser import Parser


def write_token_data_to_file(data, filename):
    with open(filename, "w") as fo:
        for token_name, token_type in data:
            print(token_name, sep='\n', file=fo)


def build_output_file(filename):
    with open(filename) as fi:
        content = fi.read()
        parsed_data = p.parse(content)
        write_token_data_to_file(parsed_data, filename + "tok")


if __name__ == '__main__':
    p = Parser("states.dat")
    vc_filename = "input.vc"
    if len(sys.argv) > 1:
        vc_filename = sys.argv[1]
    else:
        vc_filename = input("Enter .vc path: ")

    if not vc_filename.endswith(".vc"):
        raise ValueError("Not a .vc file")

    if not os.path.exists(vc_filename):
        raise ValueError("Invalid .vc file directory")

    build_output_file(vc_filename)
