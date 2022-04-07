import unittest

from main import AutomatonData, Parser


class LexemeTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(AutomatonData("../states.dat"))

    def test_int_literal(self):
        testcases = [
            ("0", True),
            ("12", True),
            ("345", True),
            ("67.", False),
            (".89", False),
            ("x", False),
        ]
        for k, (sys_input, exp_output) in enumerate(testcases):
            with self.subTest(msg='test_%d: %r' % (k, sys_input)):
                self.assertEqual(self.parser.parse(sys_input) == [(sys_input, "int_literal")], exp_output)

    def test_float_literal(self):
        testcases = [
            ("1.2", True),
            ("1.", True),
            (".1", True),
            ("1e2", True),
            ("1.2E+2", True),
            ("1.2e-2", True),
            (".1E2", True),
            (".", False),
        ]
        for k, (sys_input, exp_output) in enumerate(testcases):
            with self.subTest(msg='test_%d: %r' % (k, sys_input)):
                self.assertEqual(self.parser.parse(sys_input) == [(sys_input, "float_literal")], exp_output)

    def test_string_literal(self):
        testcases = [
            ('""', True),
            ('"ae1"', True),
            ('"."', True),
            ('"+-*/<=>!&|"', True),
            ('"\\b"', True),
            ('"\\x123"', False),
            ('"\n"', False),
        ]
        for k, (sys_input, exp_output) in enumerate(testcases):
            with self.subTest(msg='test_%d: %r' % (k, sys_input)):
                self.assertEqual(self.parser.parse(sys_input) == [(sys_input, "string_literal")], exp_output)


if __name__ == '__main__':
    unittest.main()