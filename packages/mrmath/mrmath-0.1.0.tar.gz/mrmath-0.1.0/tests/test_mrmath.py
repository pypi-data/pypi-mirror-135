"""
Test for the module mod:`mrmath`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>
"""

import unittest

from mrmath import ddd, dms


class TestMrMath(unittest.TestCase):
    """Tests the module `mrmath`."""

    def test_ddd(self) -> None:
        """Test function `ddd`."""
        self.assertAlmostEqual(ddd(15, 30, 0.0), 15.5)
        self.assertAlmostEqual(ddd(-8, 9, 10.0), -8.15277777777777777)
        self.assertAlmostEqual(ddd(0, 1, 0), 0.0166666667)
        self.assertAlmostEqual(ddd(0, -5, 0), -0.0833333333333333333)

    def test_dms(self) -> None:
        """Test function `dms`."""
        self.assertTupleEqual(dms(15.5000000000000000000), (15, 30, 0))
        self.assertTupleEqual(dms(-8.1527777777777777778), (-8, 9, 10.000000000002842))
        self.assertTupleEqual(dms(0.0166666666666666667), (0, 1, 0))
        self.assertTupleEqual(dms(-0.0833333333333333333), (0, -5, 0))
        self.assertTupleEqual(dms(-0.00277777777777777777777), (0, 0, -10.000000000000002))
