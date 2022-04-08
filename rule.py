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
                    self.valid_states = (set(self.state_table.keys()) | {
                        dst_state
                        for state_info in self.state_table.values()
                        for input_info, dst_state in state_info
                    }) - set(AutomatonData.INVALID_STATE)
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

    def is_state_ignored(self, state):
        return self.is_state_valid(state) and state in self.ignored_states

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
