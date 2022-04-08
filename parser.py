from rule import AutomatonData


class Parser:
    def __init__(self, automaton_filename):
        self.automaton_data = AutomatonData(automaton_filename)

    def parse(self, str_, is_token_unique=True):
        token_list = []
        _str = str_ + "\n"
        for starting_state in self.automaton_data.starting_states:
            if not self.automaton_data.is_state_valid(starting_state):
                continue

            parsing_str = ""
            current_state = starting_state
            for char in _str:
                if not self.automaton_data.is_state_valid(current_state):
                    parsing_str = ""
                    current_state = starting_state

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
