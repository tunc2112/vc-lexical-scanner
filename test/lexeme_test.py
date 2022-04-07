import unittest


class LexemeTest(unittest.TestCase):
    def test_int_literal(self):
        testcases = [
            ("0", True),
            ("12", True),
            ("345", True),
            ("6789", True),
        ]
        for k, (sys_input, exp_output) in enumerate(testcases):
            with self.subTest(msg='test_%d: %r' % (k, sys_input)):
                self.assertEqual(is_int_literal(*sys_input), exp_output)

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
                self.assertEqual(is_float_literal(*sys_input), exp_output)



if __name__ == '__main__':
    unittest.main()