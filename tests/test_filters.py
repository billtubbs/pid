import unittest
from filters import zoh_Fy, Fy
from numpy.testing import assert_allclose


class TestFilters(unittest.TestCase):

    def test_zoh_Fy(self):
        a11, a12, a21, a22, b1, b2 = zoh_Fy(1.0, Tx=1.0)
        self.assertEqual(
            (a11, a12, a21, a22, b1, b2),
            (0.7357588823428847, 0.36787944117144233, -0.36787944117144233, 
             0.0, 0.26424111765711533, 0.36787944117144233)
        )
        # Compare to Test 1 result - from Octave implementation
        assert_allclose(
            (a11, a12, a21, a22, b1, b2),
            (0.735758882343, 0.367879441171, -0.367879441171, 
             0.0, 0.264241117657, 0.367879441171)
        )
        # Compare to Test 2 result - from Octave implementation
        a11, a12, a21, a22, b1, b2 = zoh_Fy(10.0, Tx=1.0)
        assert_allclose(
            (a11, a12, a21, a22, b1, b2),
            (0.995321159840, 0.904837418036, -0.009048374180, 
             0.814353676232, 0.004678840160, 0.009048374180)
        )


if __name__ == '__main__':
    unittest.main()
