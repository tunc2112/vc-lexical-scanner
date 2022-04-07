from rule import Rules


class Parser:
    def __init__(self):
        self.rule = Rules({
            "0": [(Rules.CHARACTERS, "1"), (Rules.DIGITS, "2"),],
            "1": [(Rules.CHARACTERS, "1"), (Rules.DIGITS, "1"),],
            "2": [(Rules.DIGITS, "2"),],
        })