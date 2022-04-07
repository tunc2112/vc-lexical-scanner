from collections import defaultdict


def get_info_state_table(column_names, table):
    state_table = defaultdict(list)

    for i in range(len(table)):
        src_state = table[i][0]
        for j, dst_state in enumerate(table[i][1:], 1):
            input_symbols = column_names[j]
            if dst_state != "":
                print(src_state, input_symbols, dst_state)
                state_table[src_state].append((input_symbols, dst_state))

    return state_table


class AutomatonData:
    def __init__(self, filename):
        with open(filename, "r") as data_file:
            file_lines = [line.rstrip("\r\n") for line in data_file.readlines()]
            splitting_index = [i for i in range(len(file_lines)) if file_lines[i] == ""]
            for start_idx, end_idx in zip([-1] + splitting_index, splitting_index + [len(file_lines)]):
                print(start_idx+1, end_idx)
                a_table = [
                    file_lines[i].split(",")
                    for i in range(start_idx+1, end_idx)
                ]
                a_table_column_names = a_table.pop(0)
                print(a_table_column_names[0], a_table_column_names, a_table)
                if a_table_column_names[0] == "state":
                    self.state_table = get_info_state_table(a_table_column_names, a_table)


if __name__ == '__main__':
    data = AutomatonData("states.dat")
