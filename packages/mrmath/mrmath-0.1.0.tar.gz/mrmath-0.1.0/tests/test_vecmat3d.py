"""
Test for the module mod:`mrmath.vecmat3d`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

import math
import unittest

import numpy
from mrmath.vecmat3d import Vec3D


class TestVec3D(unittest.TestCase):
    """Tests the class `mrmath.vecmat3d.Vec3D`."""

    def test_nullvec(self) -> None:
        """Nullvektor."""
        nullvector = Vec3D()
        self.assertEqual(nullvector, Vec3D([0, 0, 0]))

    def test_init(self) -> None:
        """initialisierung."""
        _ = Vec3D()
        _ = Vec3D((1, 2, 3))
        _ = Vec3D([1, 2, 3])
        _ = Vec3D(theta=math.pi / 2, phi=math.pi / 2, r=1)
        with self.assertRaises(TypeError):
            _ = Vec3D((1, 2, 3, 4))

    def test_init_polar(self) -> None:
        """initialisierung."""
        vector = Vec3D(phi=math.pi / 4, theta=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, 1)
        self.assertAlmostEqual(vector.y, 1)
        self.assertAlmostEqual(vector.z, 0)
        vector = Vec3D(phi=-math.pi / 4, theta=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, 1)
        self.assertAlmostEqual(vector.y, -1)
        self.assertAlmostEqual(vector.z, 0)
        vector = Vec3D(phi=3 * math.pi / 4, theta=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, -1)
        self.assertAlmostEqual(vector.y, 1)
        self.assertAlmostEqual(vector.z, 0)
        vector = Vec3D(phi=5 * math.pi / 4, theta=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, -1)
        self.assertAlmostEqual(vector.y, -1)
        self.assertAlmostEqual(vector.z, 0)
        vector = Vec3D(phi=7 * math.pi / 4, theta=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, 1)
        self.assertAlmostEqual(vector.y, -1)
        self.assertAlmostEqual(vector.z, 0)
        with self.assertRaises(TypeError):
            _ = Vec3D(phi=0, theta=1, r='test')
        with self.assertRaises(TypeError):
            _ = Vec3D(phi=0, theta='test', r=2)
        with self.assertRaises(TypeError):
            _ = Vec3D(phi='test', theta=1, r=3)
        vector = Vec3D(az=math.pi / 4, elev=0, r=math.sqrt(2))
        self.assertAlmostEqual(vector.x, 1)
        self.assertAlmostEqual(vector.y, 1)
        self.assertAlmostEqual(vector.z, 0)
        vector = Vec3D(az=math.pi / 4, elev=math.pi / 4)
        self.assertAlmostEqual(vector.x, 0.5)
        self.assertAlmostEqual(vector.y, 0.5)
        self.assertAlmostEqual(vector.z, 1 / math.sqrt(2))
        with self.assertRaises(TypeError):
            _ = Vec3D(az=0, elev='test', r=3)
        with self.assertRaises(TypeError):
            _ = Vec3D(az='test', elev=1, r=5)
        with self.assertRaises(TypeError):
            _ = Vec3D(az=0, elev=1, r='test')

    def test_x_y_z(self) -> None:
        """propertys: x, y, z."""
        vector = Vec3D()
        vector.x = 9.9
        vector.y = 5
        vector.z = 1.1
        self.assertEqual(vector, Vec3D([9.9, 5, 1.1]))
        self.assertEqual(vector.x, 9.9)
        self.assertEqual(vector.y, 5)
        self.assertEqual(vector.z, 1.1)
        with self.assertRaises(TypeError):
            vector.x = 'string'
        with self.assertRaises(TypeError):
            vector.y = 'string'
        with self.assertRaises(TypeError):
            vector.z = 'string'

    def test_xyz(self) -> None:
        """property: xyz."""
        vec = Vec3D()
        self.assertIsInstance(vec.xyz, list)
        self.assertEqual(len(vec.xyz), 3)

    def test_polar(self) -> None:
        """property: polar."""
        polar_vector = Vec3D((1, 1, 1)).polar
        self.assertAlmostEqual(polar_vector[0], math.pi / 4)
        self.assertAlmostEqual(polar_vector[1], math.acos(math.sqrt(2) / math.sqrt(3)))
        self.assertAlmostEqual(polar_vector[2], math.sqrt(3))
        self.assertAlmostEqual(polar_vector[0], Vec3D([1, 1, 1]).phi)
        self.assertAlmostEqual(polar_vector[1], Vec3D([1, 1, 1]).theta)
        self.assertAlmostEqual(polar_vector[2], Vec3D([1, 1, 1]).r)
        vector = Vec3D((0, 0, 1))
        self.assertEqual(vector.phi, 0.0)
        vector = Vec3D((-1, -1, 1))
        self.assertEqual(vector.phi, 5 * math.pi / 4)
        vector = Vec3D()
        vector.x = 0
        vector.y = 0
        vector.z = 0
        self.assertAlmostEqual(vector.theta, 0.0)

    def test_array(self) -> None:
        """property: ``array``."""
        vector = Vec3D((3, 7, 9))
        self.assertIsInstance(vector.array, numpy.ndarray)
        self.assertEqual(len(vector.array), 3)

    def test__abs(self) -> None:
        """macig: ``__abs__``."""
        vector = Vec3D((1, 1, 1))
        self.assertAlmostEqual(abs(vector), math.sqrt(3))

    def test__getitem(self) -> None:
        """macig: ``__getitem__``."""
        vector = Vec3D((3, 7, 13))
        self.assertEqual(vector[0], vector.x)
        self.assertEqual(vector[1], vector.y)
        self.assertEqual(vector[2], vector.z)
        with self.assertRaises(IndexError):
            _ = vector[4]

    def test__setitem(self) -> None:
        """macig: ``__getitem__``."""
        vector = Vec3D()
        vector[0] = 3
        vector[1] = 5
        vector[2] = 7
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 5)
        self.assertEqual(vector.z, 7)
        with self.assertRaises(IndexError):
            vector[3] = 13

    def test__repr(self) -> None:
        """macig: ``__repr__``."""
        vector = Vec3D()
        self.assertEqual(repr(vector), 'Vec3D([0, 0, 0])')

    def test__neg(self) -> None:
        """macig: ``__neg__``."""
        vector = Vec3D((5, -4.3, .99))
        vector_neg = -vector
        self.assertAlmostEqual(vector_neg.x, -5)
        self.assertAlmostEqual(vector_neg.y, 4.3)
        self.assertAlmostEqual(vector_neg.z, -0.99)

    def test__add(self) -> None:
        """macig: ``__add__``."""
        vector1 = Vec3D()
        vector2 = Vec3D((1, 2, 3))
        self.assertEqual(vector1 + vector2, vector2)
        self.assertEqual(vector1 + 4, Vec3D((4, 4, 4)))
        self.assertEqual(vector2 + 5.1, Vec3D((6.1, 7.1, 8.1)))
        with self.assertRaises(TypeError):
            _ = vector1 + [0, 1, 2]

    def test__radd(self) -> None:
        """macig: ``__radd__``."""
        vector1 = Vec3D()
        vector2 = Vec3D((1, 2, 3))
        self.assertEqual(vector1 + vector2, vector2)
        self.assertEqual(4 + vector1, Vec3D((4, 4, 4)))
        self.assertEqual(5.1 + vector2, Vec3D((6.1, 7.1, 8.1)))
        with self.assertRaises(TypeError):
            _ = [0, 1, 2] + vector1

    def test__iadd(self) -> None:
        """macig: ``__iadd__``."""
        vector1 = Vec3D()
        vector2 = Vec3D((1, 2, 3))
        vector1 += vector2
        self.assertEqual(vector1, vector2)
        vector1 = Vec3D()
        vector1 += 4
        self.assertEqual(vector1, Vec3D((4, 4, 4)))
        vector2 = Vec3D((1, 2, 3))
        vector2 += 5.1
        self.assertEqual(vector2, Vec3D((6.1, 7.1, 8.1)))
        with self.assertRaises(TypeError):
            vector1 += [0, 1, 2]

    def test__truediv(self) -> None:
        """macig: ``__truediv__``."""
        dividend = Vec3D([1, 2, 3])
        quotient = dividend / 2
        self.assertEqual(quotient, Vec3D([0.5, 1.0, 1.5]))
        with self.assertRaises(TypeError):
            quotient = dividend / 'string'

    def test__itruediv(self) -> None:
        """macig: ``__itruediv__``."""
        quotient = Vec3D([1, 2, 3])
        quotient /= 2
        self.assertEqual(quotient, Vec3D([0.5, 1.0, 1.5]))

        quotient = Vec3D([2, 3, 5])
        quotient /= 2.0
        self.assertEqual(quotient, Vec3D([1.0, 1.5, 2.5]))

        quotient = Vec3D([1.0, 2.0, 3.4])
        quotient /= 2
        self.assertEqual(quotient, Vec3D([0.5, 1.0, 1.7]))

        quotient = Vec3D([2.4, 3.3, 5.5])
        quotient /= 2.2
        self.assertAlmostEqual(quotient.x, 1.090909090909)
        self.assertAlmostEqual(quotient.y, 1.5)
        self.assertAlmostEqual(quotient.z, 2.5)

        with self.assertRaises(TypeError):
            quotient /= 'string'

    def test__eq(self) -> None:
        """macig: ``__eq__``."""
        self.assertEqual(Vec3D([1, 2, 3]) == Vec3D([1, 2, 3]), True)
        self.assertEqual(Vec3D([1, 2, 3]) == Vec3D([3, 2, 1]), False)
        self.assertEqual(Vec3D([1, 2, 3]) == 3, False)
