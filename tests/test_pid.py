import unittest
from pid import anti_windup, PID


class TestPID(unittest.TestCase):

    def test_anti_windup(self):
        test_cases = {
            (-10.0, 'none'): -10.0,
            (-10.0, 'lower'): 0.0,
            (-10.0, 'upper'): -10.0,
            (0.0, 'none'): 0.0,
            (0.0, 'lower'): 0.0,
            (0.0, 'upper'): 0.0,
            (10.0, 'none'): 10.0,
            (10.0, 'lower'): 10.0,
            (10.0, 'upper'): 0.0
        }
        for (Dui, windup), Dui_out in test_cases.items():
            self.assertEqual(anti_windup(Dui, windup), Dui_out)


if __name__ == '__main__':
    unittest.main()
