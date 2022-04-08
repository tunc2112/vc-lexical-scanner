import os
import sys
from collections import defaultdict
import string
import re


class AutomatonData:
    INVALID_STATE = "-1"

    def __init__(self, filename):
        with open(filename, "r") as data_file:
            file_lines = [line.rstrip("\r\n") for line in data_file.readlines()]
            splitting_index = [i for i in range(len(file_lines)) if file_lines[i] == ""]
            for start_idx, end_idx in zip([-1] + splitting_index, splitting_index + [len(file_lines)]):
                # print(start_idx+1, end_idx)
                a_table = [
                    file_lines[i].split(" ")
                    for i in range(start_idx+1, end_idx)
                ]
                a_table_column_names = a_table.pop(0)
                a_table_name = a_table_column_names[0]
                # print(a_table_name, a_table_column_names, a_table)
                if a_table_name == "state":
                    self.state_table = AutomatonData.get_info_state_table(a_table_column_names, a_table)
                    self.valid_input_list = a_table_column_names
                elif a_table_name == "starting_state":
                    self.starting_states = [row[0] for row in a_table]
                elif a_table_name == "ending_state":
                    self.ending_states = {row[0]: row[1] for row in a_table}
                    self.ignored_states = [row[0] for row in a_table if row[2] != "0"]
                elif a_table_name == "special_label":
                    self.special_labels = {row[0]: row[1].split("|") for row in a_table}

    @staticmethod
    def get_info_state_table(column_names, table):
        state_table = defaultdict(list)

        for i in range(len(table)):
            src_state = table[i][0]
            for j, dst_state in enumerate(table[i][1:], 1):
                input_symbols = column_names[j]
                if dst_state != AutomatonData.INVALID_STATE:
                    # print(src_state, repr(input_symbols), dst_state)
                    state_table[src_state].append((input_symbols, dst_state))

        return state_table

    def get_label(self, current_state, str_):
        result = ""
        if current_state in self.ending_states:
            result = self.ending_states[current_state]
            for special_label, token_list in self.special_labels.items():
                if str_ in token_list:
                    result = special_label
                    break

        return result

    def is_state_valid(self, state):
        return state != AutomatonData.INVALID_STATE and state in self.state_table

    def get_next_state(self, current_state, char):
        if current_state not in self.state_table:
            return AutomatonData.INVALID_STATE

        for input_symbols, dst_state in self.state_table[current_state]:
            if char == input_symbols:
                return dst_state

            if input_symbols == "\\d":
                if char in string.digits:
                    return dst_state

                continue

            elif input_symbols == "\\s":
                if char in string.whitespace:
                    return dst_state

                continue

            elif input_symbols == "\\n":
                if char == "\n":
                    return dst_state

                continue

            elif input_symbols.startswith("\\"):
                if "\\" + char == input_symbols:
                    return dst_state

                continue

            elif input_symbols.startswith("[") and input_symbols.endswith("]"):
                # TODO: remove importing re
                if re.match(input_symbols, char):
                    return dst_state

            # print(repr(char), repr(input_symbols))

        return AutomatonData.INVALID_STATE


class Parser:
    def __init__(self, automaton_data):
        self.automaton_data = automaton_data

    def parse(self, str_, is_token_unique=True):
        token_list = []
        _str = str_ + "\n"
        for starting_state in self.automaton_data.starting_states:
            parsing_str = ""
            current_state = starting_state
            for char in _str:
                if current_state in self.automaton_data.state_table:
                    next_state = self.automaton_data.get_next_state(current_state, char)
                    # print(current_state, parsing_str, repr(char), next_state)
                    if next_state != AutomatonData.INVALID_STATE:
                        parsing_str += char
                        current_state = next_state

                    # print("->", parsing_str, current_state)
                    if not self.automaton_data.is_state_valid(next_state):
                        parsed_label = self.automaton_data.get_label(current_state, parsing_str)
                        if parsed_label.startswith("err"):
                            raise Exception("SyntaxError: Error when compiling:\n" + parsing_str)

                        # print("-->", repr(parsing_str), parsed_label)
                        if current_state not in self.automaton_data.ignored_states and parsed_label != "":
                            token = (parsing_str, parsed_label)
                            if not is_token_unique or token not in token_list:
                                token_list.append(token)

                        parsing_str = ""
                        current_state = starting_state
                        next_state = self.automaton_data.get_next_state(starting_state, char)
                        # print("new str, state =", repr(char), next_state)
                        if self.automaton_data.is_state_valid(next_state) and next_state not in self.automaton_data.ignored_states:
                            parsing_str = char
                            current_state = next_state

                        # print("-> new str, state =", repr(parsing_str), current_state)

        return token_list


def write_token_data_to_file(data, filename):
    with open(filename, "w") as fo:
        for token_name, token_type in data:
            print(token_name, sep='\n', file=fo)


if __name__ == '__main__':
    p = Parser(AutomatonData("states.dat"))
    vc_filename = "input.vc"
    if len(sys.argv) > 1:
        vc_filename = sys.argv[1]

    if not vc_filename.endswith(".vc"):
        raise ValueError("Not a .vc file")

    if not os.path.exists(vc_filename):
        raise ValueError("Invalid .vc file directory")

    with open(vc_filename) as fi:
        content = fi.read()
        parsed_data = p.parse(content)
        write_token_data_to_file(parsed_data, vc_filename + "tok")
