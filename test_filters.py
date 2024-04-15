import unittest
from filters import zoh_Fy, Fy


class TestFitlers(unittest.TestCase):

    def test_zoh_Fy(self):
        a11, a12, a21, a22, b1, b2 = zoh_Fy(1.0, Tx=1.0)
        self.assertEqual(
            (a11, a12, a21, a22, b1, b2),
            (0.7357588823428847, 0.36787944117144233, -0.36787944117144233, 
             0.0, 0.26424111765711533, 0.36787944117144233)
        )


if __name__ == '__main__':
    unittest.main()
