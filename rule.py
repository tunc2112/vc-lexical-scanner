import string


class Rules:
    CHARACTERS = string.ascii_letters + "_"
    DIGITS = string.digits

    def __init__(self, rules_str_list):
        """
        :param rules_str_list:
        self.rules is a dict { src_state: [(token, dest_state),...] }
        """
        self.rules = rules_str_list
