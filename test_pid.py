import unittest
from pid import zoh_Fy, anti_windup, PID


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

    def test_zoh_Fy(self):
        a11, a12, a21, a22, b1, b2 = zoh_Fy(1.0, Tx=1.0)
        self.assertEqual(
            (a11, a12, a21, a22, b1, b2),
            (0.7357588823428847, 0.36787944117144233, -0.36787944117144233, 
             0.0, 0.26424111765711533, 0.36787944117144233)
        )


if __name__ == '__main__':
    unittest.main()
