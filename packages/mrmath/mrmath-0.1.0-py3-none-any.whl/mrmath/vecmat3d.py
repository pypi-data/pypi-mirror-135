# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines

r"""Klassen für dreidimensionale Vektoren und 3*3-Matrizen.

.. moduleauthor:: Michael Rippstein <info@comlab.ch>

Idea and parts of the source from [Montenbruck2004a]_.


For the classes `Vec3D` and `Mat3D` the following operation are definde.

===========  =========  =========  ========  ===================  ============================
Funktion     Arg_1 (a)  Arg_2 (b)  Wert (c)  Notation             Bedeutung
===========  =========  =========  ========  ===================  ============================
`-`          `Vec3D`               `Vec3D`   .. math:: c = -a     Unäres Minus
\            `Mat3D`               `Mat3D`   .. math:: C = -A
`-`          `Vec3D`    `Vec3D`    `Vec3D`   .. math:: c = a - b  Vektor-Subtraktion
\            `Mat3D`    `Mat3D`    `Mat3D`   .. math:: C = A - B  Matrix-Subtraktion
`+`          `Vec3D`    `Vec3D`    `Vec3D`   .. math:: c = a + b  Vektor-Addition
\            `Mat3D`    `Mat3D`    `Mat3D`   .. math:: C = A + B  Matrix-Addition
`*`          `int`      `Vec3D`    `Vec3D`   .. math:: c = ab     Skalar-Multiplikation
\            `float`    `Vec3D`    `Vec3D`   .. math:: c = ab
\            `Vec3D`    `int`      `Vec3D`   .. math:: c = ab
\            `Vec3D`    `float`    `Vec3D`   .. math:: c = ab
\            `int`      `Mat3D`    `Mat3D`   .. math:: C = aB
\            `float`    `Mat3D`    `Mat3D`   .. math:: C = aB
\            `Mat3D`    `int`      `Mat3D`   .. math:: C = Ab
\            `Mat3D`    `float`    `Mat3D`   .. math:: C = Ab
`*`          `Mat3D`    `Vec3D`    `Vec3D`   .. math:: c = Ab     Matrix/Vektor-Multiplikation
`/`          `Vec3D`    `int`      `Vec3D`   .. math:: c = a/b    Skalar-Division
\            `Vec3D`    `float`    `Vec3D`   .. math:: c = a/b
\            `Mat3D`    `int`      `Mat3D`   .. math:: C = A/b
\            `Mat3D`    `float`    `Mat3D`   .. math:: C = A/b
`abs`        `Vec3D`               `float`   .. math:: c = |a|
`dot`        `Vec3D`    `Vec3D`    `float`   .. math:: c = ab     Skalarprodukt
`cross` `@`  `Vec3D`    `Vec3D`    `Vec3D`   .. math:: c = a × b  Vektorprodukt, Kreuzprodukt
`tranp`      `Mat3D`               `Mat3D`   .. math:: C = A^T    Transponierte
`einmat`                           `Mat3D`                        Einheitsmatrix
`rotmatx`    `float`               `Mat3D`                        Elementare Drehmatrix
`rotmaty`    `float`               `Mat3D`
`rotmatz`    `float`               `Mat3D`
`==`         `Vec3D`    `Vec3D`    `bool`
===========  =========  =========  ========  ===================  ============================

Bedeutung der Winkel bei den Kugelkoordinaten
---------------------------------------------
.. todo:: Korekte winkel bezeichungen im den bilder!

.. image:: _static/sphere.png
   :scale: 50 %

References
----------
.. [Montenbruck2004a] Montenbruck, Oliver; Pfleger, Thomas:
                      "Astronomie mit dem Personal
                      Computer"; 4. Auflage; Springer-Verlag; Berlin,
                      Heidelberg 2004
"""

import math
from typing import List, Optional, Tuple, Union

import numpy as np

__all__ = ['Vec3D', 'Mat3D', 'cross', 'dot', 'transp', 'einmat', 'rotmatx', 'rotmaty', 'rotmatz', 'polar2kart']

_TYPEERRORTEXT = "unsupported operand type(s) for '{}': '{}' and '{}'"


class Vec3D:
    r"""Dreidimensionaler Vector.

    Der Aufruf ohne die angabe von Parameter initialisiert einen Null-Vector.

    .. code-block:: python

       null_vector = Vec3D()

    Parameters
    ----------
    \**kwargs
        siehe unten
    arg
        siehe unten

        .. code-block:: python

            Vec3D([x, y, z])
            Vec3D((x, y, z))

    Keyword Arguments
    -----------------
    phi, theta, r
        Polarkoordinaten

        .. code-block:: python

            Vec3D(theta=, phi=, r=)

    az, elev
        Polarkoordinaten

        .. code-block:: python

            Vec3D(az=, elev=)

    az, elev, r : float
        Polarkoordinaten

        .. code-block:: python

            Vec3D(az=, elev=, r=)

    Raises
    ------
    TypeError

    Examples
    --------
    .. testsetup:: vec

       import math
       from mrmath.vecmat3d import Vec3D

    .. doctest:: vec

       >>> nullvector = Vec3D()
       >>> print(nullvector)
       Vec3D([0, 0, 0])

       >>> print(nullvector.xyz)
       [0, 0, 0]

       >>> repr(nullvector.array)
       'array([[0],\n       [0],\n       [0]])'

       >>> print("x: {}, y: {}, z: {}".format(nullvector.x, nullvector.y, nullvector.z))
       x: 0, y: 0, z: 0

       >>> print("phi: {}, theta: {}, r: {}".format(nullvector.phi,
       ...                                          nullvector.theta,
       ...                                          nullvector.r))
       phi: 0, theta: 0, r: 0

       >>> print(Vec3D([1, 2, 3]))
       Vec3D([1, 2, 3])

       >>> print(Vec3D([1.0, 2.0, 3.0]))
       Vec3D([1.0, 2.0, 3.0])

       >>> vector = Vec3D()
       >>> vector.x = 9.9
       >>> vector.y = 5
       >>> vector.z = 1.1
       >>> print(vector)
       Vec3D([9.9, 5, 1.1])

       >>> polar = Vec3D(theta=math.pi/2, phi=math.pi/2, r=1)
       >>> '{:.3f}, {:.3f}, {:.3f}'.format(polar.x, polar.y, polar.z)
       '0.000, 0.000, 1.000'

       >>> vector.x = 'text'
       Traceback (most recent call last):
       ...
       TypeError: unsupported type for setter: '<class 'str'>'
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(  # pylint: disable=too-many-branches
        self, arg: Union[None, Tuple, List] = None, **kwargs: Optional[float]
    ) -> None:
        self.__x = 0.0
        self.__y = 0.0
        self.__z = 0.0               #: Komponenten des Vektors
        self.__phi: float            #: Polarwinkel (Azimut)
        self.__theta: float          #: Polarwinkel (Elevation)
        self.__r: float              #: Betrag des Vektors
        self.__polarvalid = False    #: zeigt, ob Polarkomponenten gueltig sind

        if (arg is None) and not kwargs:
            # initialisierung: null vector
            self.__x = 0
            self.__y = 0
            self.__z = 0               #: Komponenten des Vektors
            self.__phi = 0             #: Polarwinkel (Azimut)
            self.__theta = 0           #: Polarwinkel (Elevation)
            self.__r = 0               #: Betrag des Vektors
            self.__polarvalid = True   #: zeigt, ob Polarkomponenten gueltig sind
        elif isinstance(arg, (list, tuple)) and len(arg) == 3:
            self.x = arg[0]
            self.y = arg[1]
            self.z = arg[2]
        elif (arg is None) and 'phi' in kwargs and 'theta' in kwargs and 'r' in kwargs:
            if (
                isinstance(kwargs['phi'], (int, float))
                and isinstance(kwargs['theta'], (int, float))
                and isinstance(kwargs['r'], (int, float))
            ):
                self.__phi = kwargs['phi']
                self.__theta = kwargs['theta']
                self.__r = kwargs['r']
                self.__polarvalid = True
                self.x = self.__r * math.cos(self.__phi) * math.cos(self.__theta)
                self.y = self.__r * math.sin(self.__phi) * math.cos(self.__theta)
                self.z = self.__r * math.sin(self.__theta)
            else:
                raise TypeError
        elif (arg is None) and 'az' in kwargs and 'elev' in kwargs:
            if isinstance(kwargs['az'], (int, float)) and isinstance(kwargs['elev'], (int, float)):
                self.__phi = kwargs['az']
                self.__theta = kwargs['elev']
                if 'r' in kwargs:
                    if isinstance(kwargs['r'], (int, float)):
                        self.__r = kwargs['r']
                    else:
                        raise TypeError
                else:
                    self.__r = 1.0
                self.__polarvalid = True
                self.x = self.__r * math.cos(self.__phi) * math.cos(self.__theta)
                self.y = self.__r * math.sin(self.__phi) * math.cos(self.__theta)
                self.z = self.__r * math.sin(self.__theta)
            else:
                raise TypeError
        else:
            raise TypeError

    @property
    def xyz(self) -> List[float]:
        """Gibt die kartesischen Koordinaten zurück.

        Returns
        -------
        List[float]
            Kartesischekoordinaten ``[x, y, z]``

        """
        return [self.__x, self.__y, self.__z]

    @property
    def polar(self) -> List[float]:
        """Gibt die polar Koordinaten zurück.

        Returns
        -------
        List[float]
            Polarkoordinaten: ``[phi, theta, r]``

        """
        return [self.phi, self.theta, self.r]

    @property
    def array(self) -> np.ndarray:
        """Gibt die kartesischen Koordinaten als Spaltenvector in einem `numpy.array` zurück.

        Returns
        -------
        numpy.ndarray
            Spaltenvektor ``[[x][y][z]]``

        """
        return np.array([[self.__x], [self.__y], [self.__z]])

    @property
    def x(self) -> float:
        """x-axis in the cartesian coordinate system.

        Returns
        -------
        float
            x-axis

        """
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        if isinstance(value, (int, float)):
            self.__x = value
            self.__polarvalid = False
        else:
            raise TypeError("unsupported type for setter: '{}'".format(type(value)))

    @property
    def y(self) -> float:
        """y-axis in the cartesian coordinate system."""
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        if isinstance(value, (int, float)):
            self.__y = value
            self.__polarvalid = False
        else:
            raise TypeError("unsupported type for setter: '{}'".format(type(value)))

    @property
    def z(self) -> float:
        """z-axis in the cartesian coordinate system."""
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        if isinstance(value, (int, float)):
            self.__z = value
            self.__polarvalid = False
        else:
            raise TypeError("unsupported type for setter: '{}'".format(type(value)))

    @property
    def phi(self) -> float:
        """Azimut in den Polarkoordinaten."""
        if not self.__polarvalid:
            self._calcpolar()
        return self.__phi

    @property
    def theta(self) -> float:
        """Elevation in den Polarkoordinaten."""
        if not self.__polarvalid:
            self._calcpolar()
        return self.__theta

    @property
    def r(self) -> float:
        """Radius in den Polarkoordinaten."""
        if not self.__polarvalid:
            self._calcpolar()
        return self.__r

    def __abs__(self) -> float:
        """Betrag (Radius).

        Returns
        -------
        float
            Betrag des Vektors

        Examples
        --------
        .. testsetup:: vecabs

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecabs

           >>> vector = Vec3D([1, 0, 0])
           >>> print('{:.4f}'.format(abs(vector)))
           1.0000

           >>> vector = Vec3D([1, 1, 0])
           >>> print('{:.4f}'.format(abs(vector)))
           1.4142

           >>> vector = Vec3D([1, 0, 1])
           >>> print('{:.4f}'.format(abs(vector)))
           1.4142

        """
        return self.r

    def __getitem__(self, key: int) -> float:
        """Implement the ``self[key]`` call.

        Returns
        -------
        float
            for key = 0: x
            for key = 1: y
            for key = 2: z

        Raises
        ------
        IndexError
            When key outside of 0…2

        Examples
        --------
        .. testsetup:: vecitem

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecitem

           >>> vector = Vec3D([3, 7, 13])
           >>> print(vector[0])
           3

           >>> print(vector[1])
           7

           >>> print(vector[2])
           13

           >>> print(vector[3])
           Traceback (most recent call last):
           ...
           IndexError: list index out of range

           >>> for m in vector:
           ...     print(m)
           3
           7
           13

        """
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        raise IndexError('list index out of range')

    def __setitem__(self, key: int, value: float) -> None:
        """Implement the assignment to ``self[key]``.

        Parameters
        ----------
        key
            Schlüssel
        value
            Wert

        Raises
        ------
        IndexError:
            When key outside of 0…2

        Examples
        --------
        .. testsetup:: vecitem

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecitem

           >>> vector = Vec3D()
           >>> vector[0] = 3
           >>> vector[1] = 7
           >>> vector[2] = 13
           >>> print(vector)
           Vec3D([3, 7, 13])

           >>> vector[3] = 17
           Traceback (most recent call last):
           ...
           IndexError: list index out of range

           >>> for m in vector:
           ...     print(m)
           3
           7
           13

        """
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError('list index out of range')

    def _calcpolar(self) -> None:
        """Berechne polare Komponenten.

        Berechnet die polaren Komponenten des Vektors mit den
        aktuellen kartesischen Daten. Setzt `__polarvalid` auf
        `True`.

        Examples
        --------
        .. testsetup:: veccalpol

           from mrmath.vecmat3d import Vec3D

        .. doctest:: veccalpol

           >>> vector1 = Vec3D([1, 0, 0])
           >>> print("phi: {}, theta: {}, r: {}".format(vector1.phi,
           ...                                          vector1.theta,
           ...                                          vector1.r))
           phi: 0.0, theta: 0.0, r: 1.0

           >>> vector2 = Vec3D([0, 1, 0])
           >>> print("phi: {:.4f}, theta: {}, r: {}".format(vector2.phi,
           ...                                              vector2.theta,
           ...                                              vector2.r))
           phi: 1.5708, theta: 0.0, r: 1.0

           >>> vector3 = Vec3D([0, 0, 1])
           >>> print("phi: {}, theta: {:.4f}, r: {}".format(vector3.phi,
           ...                                              vector3.theta,
           ...                                              vector3.r))
           phi: 0.0, theta: 1.5708, r: 1.0

           >>> vector4 = Vec3D([-1, -1, -1])
           >>> print("phi: {:.4f}, theta: {:.4f}, r: {:.4f}".format(vector4.phi,
           ...                                                      vector4.theta,
           ...                                                      vector4.r))
           phi: 3.9270, theta: -0.6155, r: 1.7321
        """
        # Laenge der Projektion des Vektors in die x-y-Ebene
        rho_sqr = self.__x ** 2 + self.__y ** 2

        # Betrag des Vektors
        self.__r = math.sqrt(rho_sqr + self.__z ** 2)

        # Azimut des Vektors
        if (self.__x == 0.0) and (self.__y == 0.0):
            self.__phi = 0.0
        else:
            self.__phi = math.atan2(self.__y, self.__x)
        if self.__phi < 0.0:
            self.__phi += math.tau

        # Elevation des Vektors
        rho = math.sqrt(rho_sqr)
        if (self.__z == 0.0) and (rho == 0.0):
            self.__theta = 0.0
        else:
            self.__theta = math.atan2(self.__z, rho)
        self.__polarvalid = True

    def __repr__(self) -> str:
        """Reprentation des Vectors.

        Returns
        -------
        str
            Reprepresantation
        """
        return 'Vec3D([{}, {}, {}])'.format(self.x, self.y, self.z)

    def __neg__(self) -> 'Vec3D':
        """Negation: `-self`.

        Returns
        -------
        Vec3D
            inverted vector

        Examples
        --------
        .. testsetup:: vecneg

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecneg

           >>> vector = Vec3D([1, 2, 3])
           >>> print(-vector)
           Vec3D([-1, -2, -3])

           >>> vector = Vec3D([-1, -2, -3])
           >>> print(-vector)
           Vec3D([1, 2, 3])
        """
        return Vec3D([-self.__x, -self.__y, -self.__z])

    def __add__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Addition: ``self + other``.

        Parameters
        ----------
        other
            Summand

        Returns
        -------
        Vec3D
            Summe

        Examples
        --------
        .. testsetup:: vecadd

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecadd

           >>> summand = Vec3D([2, 6, 20])
           >>> summe = summand + -9
           >>> print(summe)
           Vec3D([-7, -3, 11])

           >>> summand1 = Vec3D([2, 6, 20])
           >>> summand2 = Vec3D([-9.0, -9.0, -9.0])
           >>> summe = summand1 + summand2
           >>> print(summe)
           Vec3D([-7.0, -3.0, 11.0])
        """
        if isinstance(other, self.__class__):
            tempx = self.__x + other.x
            tempy = self.__y + other.y
            tempz = self.__z + other.z
        elif isinstance(other, (int, float)):
            tempx = self.__x + other
            tempy = self.__y + other
            tempz = self.__z + other
        else:
            return NotImplemented
        return Vec3D([tempx, tempy, tempz])

    def __radd__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Addition: ``other + self``.

        Parameters
        ----------
        other
            Summand

        Returns
        -------
        Vec3D
            Summe

        Examples
        --------
        .. testsetup:: vecadd

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecadd

           >>> summand = Vec3D([2, 6, 20])
           >>> summe = -9 + summand
           >>> print(summe)
           Vec3D([-7, -3, 11])
        """
        # if isinstance(other, self.__class__):
        #     tempx = other.x + self.__x
        #     tempy = other.y + self.__y
        #     tempz = other.z + self.__z
        if isinstance(other, (int, float)):
            tempx = other + self.__x
            tempy = other + self.__y
            tempz = other + self.__z
        else:
            return NotImplemented
        return Vec3D([tempx, tempy, tempz])

    def __iadd__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Addition: ``self += other``.

        Parameters
        ----------
        other
            Summand

        Returns
        -------
        Vec3D
            Summe

        Examples
        --------
        .. testsetup:: vecadd

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecadd

           >>> summe = Vec3D([2, 6, 20])
           >>> summe += -9
           >>> print(summe)
           Vec3D([-7, -3, 11])

           >>> summe = Vec3D([2, 6, 20])
           >>> summand = Vec3D([-9.0, -9.0, -9.0])
           >>> summe += summand
           >>> print(summe)
           Vec3D([-7.0, -3.0, 11.0])
        """
        if isinstance(other, self.__class__):
            self.__x += other.x
            self.__y += other.y
            self.__z += other.z
            self.__polarvalid = False
        elif isinstance(other, (int, float)):
            self.__x += other
            self.__y += other
            self.__z += other
            self.__polarvalid = False
        else:
            return NotImplemented
        return self

    def __sub__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Subtraktion: `self - other`.

        Parameters
        ----------
        other
            Subtrahend


        Returns
        -------
        Vec3D
            Differenz

        Exampels
        --------
        .. testsetup:: vecsub

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecsub

           >>> minuend = Vec3D([4, 8, 16])
           >>> subtrahend = Vec3D([3, 9, 27])
           >>> differenz = minuend - 2
           >>> print(differenz)
           Vec3D([2, 6, 14])

           >>> differenz = minuend - subtrahend
           >>> print(differenz)
           Vec3D([1, -1, -11])
        """
        if isinstance(other, self.__class__):
            tempx = self.__x - other.x
            tempy = self.__y - other.y
            tempz = self.__z - other.z
        elif isinstance(other, (int, float)):
            tempx = self.__x - other
            tempy = self.__y - other
            tempz = self.__z - other
        else:
            return NotImplemented
        return Vec3D([tempx, tempy, tempz])

    def __rsub__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Subraktion: `other - self`.

        Parameters
        ----------
        other
            Minuend

        Returns
        -------
        Vec3D
            Differenz

        Exampels
        --------
        .. testsetup:: vecsub

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecsub

           >>> minuend = Vec3D([4, 8, 16])
           >>> subtrahend = Vec3D([3, 9, 27])
           >>> differenz = 2 - subtrahend
           >>> print(differenz)
           Vec3D([-1, -7, -25])

           >>> differenz = minuend - subtrahend
           >>> print(differenz)
           Vec3D([1, -1, -11])
        """
        if isinstance(other, self.__class__):
            tempx = other.x - self.__x
            tempy = other.y - self.__y
            tempz = other.z - self.__z
        elif isinstance(other, (int, float)):
            tempx = other - self.__x
            tempy = other - self.__y
            tempz = other - self.__z
        else:
            return NotImplemented
        return Vec3D([tempx, tempy, tempz])

    def __isub__(self, other: Union['Vec3D', float]) -> 'Vec3D':
        """Subtraktion: `self -= other`.

        Parameters
        ----------
        other
            Subtrahend

        Returns
        -------
        Vec3D
            Differenz

        Exampels
        --------
        .. testsetup:: vecsub

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecsub

           >>> differenz = Vec3D([4, 8, 16])
           >>> differenz -= 2
           >>> print(differenz)
           Vec3D([2, 6, 14])

        """
        if isinstance(other, self.__class__):
            self.__x -= other.x
            self.__y -= other.y
            self.__z -= other.z
            self.__polarvalid = False
        elif isinstance(other, (int, float)):
            self.__x -= other
            self.__y -= other
            self.__z -= other
            self.__polarvalid = False
        else:
            return NotImplemented
        return self

    def __mul__(self, other: Union['Mat3D', float]) -> 'Vec3D':
        """Multiplikation `self * other`.

        Parameters
        ----------
        other
            Multiplikatand

        Returns
        -------
        Vec3D
            Produkt

        Exampels
        --------
        .. testsetup:: vecmul

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecmul

           >>> faktor1 = Vec3D((2,4,6))
           >>> produkt = faktor1 * 3.75
           >>> print(produkt)
           Vec3D([7.5, 15.0, 22.5])

           >>> produkt = faktor1 * 'text'
           Traceback (most recent call last):
           ...
           TypeError: unsupported operand type(s) for '*': '<class '__main__.Vec3D'>' and '<class 'str'>'
        """
        if isinstance(other, (int, float)):
            tempx = self.__x * other
            tempy = self.__y * other
            tempz = self.__z * other
            result = [tempx, tempy, tempz]
        elif isinstance(other, Mat3D):
            result = [0, 0, 0]
            for j in range(3):
                scalp = 0.0
                for i in range(3):
                    scalp += self[i] * other._mat[i][j]
                result[j] = scalp
        else:
            return NotImplemented
        return Vec3D(result)

    def __rmul__(self, other: Union['Mat3D', float]) -> 'Vec3D':
        """Multiplikation `other * self`.

        Parameters
        ----------
        other
            Multiplikator

        Returns
        -------
        Vec3D
            Produkt

        Exampels
        --------
        .. testsetup:: vecmul

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecmul

           >>> faktor2 = Vec3D((2,4,6))
           >>> produkt = 3.75 * faktor2
           >>> print(produkt)
           Vec3D([7.5, 15.0, 22.5])

           >>> produkt = faktor2 * 'text'
           Traceback (most recent call last):
           ...
           TypeError: ...
        """
        if isinstance(other, (int, float)):
            tempx = other * self.__x
            tempy = other * self.__y
            tempz = other * self.__z
            result = [tempx, tempy, tempz]
        elif isinstance(other, Mat3D):
            result = [0, 0, 0]
            for i in range(3):
                scalp = 0.0
                for j in range(3):
                    scalp += other._mat[i][j] * self[j]
                result[i] = scalp
        else:
            return NotImplemented
        return Vec3D(result)

    def __imul__(self, other: Union['Mat3D', float]) -> 'Vec3D':
        """Multiplikation: `self = self * other`.

        Parameters
        ----------
        other
            Multiplikand

        Returns
        -------
        Vex3D
            Produkt

        Exampels
        --------
        .. testsetup:: vecmul

           import math
           from mrmath.vecmat3d import Vec3D, rotmatx

        .. doctest:: vecmul

           >>> faktor1 = Vec3D((2, 4, 6))
           >>> produkt = faktor1 * 3.75
           >>> print(produkt)
           Vec3D([7.5, 15.0, 22.5])

           >>> faktor1 = Vec3D((2, 4, 6))
           >>> faktor2 = rotmatx(0.5 * math.pi)
           >>> produkt = faktor1 * faktor2
           >>> print(produkt)
           Vec3D([2, -4, 6])

           >>> produkt = faktor1 * 'text'
           Traceback (most recent call last):
           ...
           TypeError: unsupported operand type(s) for '*': '<class '__main__.Vec3D'>' and '<class 'str'>'
        """
        if isinstance(other, (int, float)):
            self.__x *= other
            self.__y *= other
            self.__z *= other
            self.__polarvalid = False
        elif isinstance(other, Mat3D):
            result = [0.0, 0.0, 0.0]
            for j in range(3):
                scalp = 0.0
                for i in range(3):
                    scalp += other._mat[i][j] * self[i]
                result[j] = scalp
            self.__x *= result[0]
            self.__y *= result[1]
            self.__z *= result[2]
            self.__polarvalid = False
        else:
            return NotImplemented
        return self

    def __truediv__(self, other: float) -> 'Vec3D':
        """Division `self / other`.

        Parameters
        ----------
        other
            Divisor

        Returns
        -------
        Vec3D
            Quotient

        Examples
        --------
        .. testsetup:: vecdiv

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecdiv

           >>> dividend = Vec3D([1, 2, 3])
           >>> quotient = dividend / 2
           >>> print(quotient)
           Vec3D([0.5, 1.0, 1.5])

        """
        if isinstance(other, (int, float)):
            tempx = self.__x / other
            tempy = self.__y / other
            tempz = self.__z / other
        else:
            return NotImplemented
        return Vec3D([tempx, tempy, tempz])

    def __itruediv__(self, other: Union[int, float]) -> 'Vec3D':
        """Division `self /= other`.

        Parameters
        ----------
        other
            Divisor

        Returns
        -------
        Vec3D
            Quotient

        Exampels
        --------
        .. testsetup:: vecdiv

           from mrmath.vecmat3d import Vec3D

        .. doctest:: vecdiv

           >>> quotient = Vec3D([1, 2, 3])
           >>> quotient /= 2
           >>> print(quotient)
           Vec3D([0.5, 1.0, 1.5])

           >>> quotient /= 'string'
           Traceback (most recent call last):
           ...
           TypeError: unsupported operand type(s) for '/=': '<class '__main__.Vec3D'>' and '<class 'str'>'
        """
        if isinstance(other, (int, float)):
            self.__x /= other
            self.__y /= other
            self.__z /= other
            self.__polarvalid = False
        else:
            return NotImplemented
        return self

    def __eq__(self, other: object) -> bool:
        """Comparisons ``self == other``."""
        if not isinstance(other, Vec3D):
            return NotImplemented
        return self.__x == other.x and self.__y == other.y and self.__z == other.z


class Mat3D:
    """3x3 Matrix."""

    def __init__(self, args: List) -> None:    # noqa: D107
        self._mat = args  # [[None, None, None], [None, None, None], [None, None, None]]

    def __getitem__(self, key: int) -> float:
        """FIXME! briefly describe function."""
        return self._mat[key]

    # def __setitem__(self, key: int, value: Union[int, float]) -> None:
    #     """FIXME! briefly describe function.
    #
    #     :param key:
    #     :type: int or (int, int)
    #     :param value:
    #     :type: int or float
    #
    #     """
    #     pass

    def __repr__(self) -> str:
        """FIXME! briefly describe function."""
        return 'Mat3D([[{},{},{}],[{},{},{}],[{},{},{}]])'.format(  # noqa: F524
            self._mat[0][0],
            self._mat[1][0],
            self._mat[2][0],
            self._mat[0][1],
            self._mat[1][1],
            self._mat[2][1],
            self._mat[0][2],
            self._mat[1][2],
            self._mat[2][2],
        )

    def __mul__(self, other: Union['Mat3D', int, float]) -> 'Mat3D':
        """Multiplikation: 'self * other'.

        Parameters
        ----------
        other
            Multiplikator

        Returns
        -------
        Mat3D
            Produkt
        """
        if isinstance(other, Mat3D):
            res = Mat3D([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        res._mat[i][k] += self._mat[i][j] * other._mat[j][k]
            return res
        if isinstance(other, (int, float)):
            # res = Mat3D(self._mat * other)
            return NotImplemented
        return NotImplemented

    # def __rmul__(self, other):
    #     """Multiplikation: 'other * self'.
    #
    #     :param other: Multiplikator
    #     :type other: int, float or Mat3D
    #     :returns: Produkt
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(other._mat * self._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(other * self._mat)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __imul__(self, other):
    #     """Multiplikation: 'self *= other'.
    #
    #     :param other: Multiplikator
    #     :type other: int, float or Mat3D
    #     :returns: Produkt
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         self.__mat = self.__mat * other._mat
    #     elif isinstance(other, (int, float)):
    #         self.__mat =  self.__mat * other
    #     else:
    #         return NotImplemented
    #     return self
    #
    # def __truediv__(self, other):
    #     """Division: 'self / other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(self._mat / other._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(self._mat / other)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __rtruediv__(self, other):
    #     """Division: 'other / self'.
    #
    #     :param other: Dividend
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(other._mat / self._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(other / self._mat)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __itruediv__(self, other):
    #     """Division: 'self /= other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         self.__mat =  self.__mat / other._mat
    #     elif isinstance(other, (int, float)):
    #         self.__mat = self._mat / other
    #     else:
    #         return NotImplemented
    #     return self
    #
    # def __floordiv__(self, other):
    #     """Ganzzahlige Division: 'self // other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(self._mat // other._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(self._mat // other)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __rfloordiv__(self, other):
    #     """Ganzzahlige Division: 'other // self'.
    #
    #     :param other: Dividend
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(other._mat // self._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(other // self._mat)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __ifloordiv__(self, other):
    #     """Ganzzahlige Division: 'self //= other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         self.__mat =  self.__mat // other._mat
    #     elif isinstance(other, (int, float)):
    #         self.__mat = self._mat // other
    #     else:
    #         return NotImplemented
    #     return self
    #
    # def __mod__(self, other):
    #     """Division mit Rest: 'self % other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(self._mat % other._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(self._mat % other)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __rmod__(self, other):
    #     """Division mit Rest: 'other % self'.
    #
    #     :param other: Dividend
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = Mat3D(other._mat % self._mat)
    #     elif isinstance(other, (int, float)):
    #         res = Mat3D(other % self._mat)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __imod__(self, other):
    #     """Division mit Rest: 'self %= other'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         self.__mat =  self.__mat % other._mat
    #     elif isinstance(other, (int, float)):
    #         self.__mat = self._mat % other
    #     else:
    #         return NotImplemented
    #     return self
    #
    # def __divmod__(self, other):
    #     """Ganzzahlige Division mit Rest: 'divmod(self, other)'.
    #
    #     :param other: Divisor
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = divmod(self._mat % other._mat)
    #     elif isinstance(other, (int, float)):
    #         res = divmod(self._mat % other)
    #     else:
    #         return NotImplemented
    #     return res
    #
    # def __rdivmod__(self, other):
    #     """Ganzzahlige Division mit Rest: 'divmod(other, self)'.
    #
    #     :param other: Dividend
    #     :type other: int, float or Mat3D
    #     :returns: Quotient
    #     :rtype: Mat3D
    #     """
    #     if isinstance(other, Mat3D):
    #         res = divmod(other._mat % self._mat)
    #     elif isinstance(other, (int, float)):
    #         res = divmod(other % self._mat)
    #     else:
    #         return NotImplemented
    #     return res


# -- funktionen
def cross(left: Vec3D, right: Vec3D) -> Vec3D:
    """Vektorprodukt (Kreuzprodukt).

    Parameters
    ----------
    left
        Linker Vektor
    right
        Rechter Vektor

    Returns
    -------
    Vec3D
        Kreuzprodukt

    Raises
    ------
    TypeError
        If `left` or `right` is not from type :class:`Vec3D`
    """
    if isinstance(left, Vec3D) and isinstance(right, Vec3D):
        cross_x = left.y * right.z - left.z * right.y
        cross_y = left.z * right.x - left.x * right.z
        cross_z = left.x * right.y - left.y * right.x
        return Vec3D((cross_x, cross_y, cross_z))
    raise TypeError(_TYPEERRORTEXT.format('cross', type(left), type(right)))


def dot(left: Vec3D, right: Vec3D) -> float:
    """Skalarprodukt zweier Vektoren.

    Parameters
    ----------
    left
        Linker Vektor
    right
        Rechter Vektor

    Returns
    -------
    float
        Skalarprodukt

    Raises
    ------
    TypeError
        If `left` or `right` is not from type :class:`Vec3D`
    """
    if isinstance(left, Vec3D) and isinstance(right, Vec3D):
        return left.x * right.x + left.y * right.y + left.z * left.z
    raise TypeError(_TYPEERRORTEXT.format('dot', type(left), type(right)))


def transp(matrix: Mat3D) -> Mat3D:
    """Transponierte einer Matrix.

    Parameters
    ----------
    matrix
        Originalmatrix

    Returns
    -------
    Mat3D
        Transponierte Matrix
    """
    return Mat3D(
        [
            [  # pylint: disable=protected-access  # noqa: E501
                matrix._mat[0][0],
                matrix._mat[1][0],
                matrix._mat[2][0],
            ],
            [  # pylint: disable=protected-access  # noqa: E501
                matrix._mat[0][1],
                matrix._mat[1][1],
                matrix._mat[2][1],
            ],
            [  # pylint: disable=protected-access  # noqa: E501
                matrix._mat[0][2],
                matrix._mat[1][2],
                matrix._mat[2][2],
            ],
        ]
    )


def einmat() -> Mat3D:
    """Einheitsmatrix.

    Returns
    -------
    Mat3D
        Einheitsmatrix
    """
    return Mat3D([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def rotmatx(alpha: float) -> Mat3D:
    """Matrix für die rotation um die x-achse.

    .. image:: _static/rotmatx.png
       :scale: 20 %

    Parameters
    ----------
    alpha
        Drehwinkel

    Returns
    -------
    Mat3D
        Rotationsmatrix

    Examples
    --------
    .. testsetup:: rotmatx

        import math
        from mrmath.vecmat3d import rotmatx, Vec3D

    .. doctest:: rotmatx

        >>> a = rotmatx(0.25 * math.pi)
        >>> a._mat
        [[1, 0, 0], [0, 0.7071067811865476, 0.7071067811865475], [0, -0.7071067811865475, 0.7071067811865476]]

        >>> a = rotmatx(0.5 * math.pi)
        >>> b = Vec3D((0.0, 1.0, 0.0))
        >>> a * b
        Vec3D([0.0, 6.123233995736766e-17, -1.0])

    """
    return Mat3D([[1, 0, 0], [0, math.cos(alpha), math.sin(alpha)], [0, -math.sin(alpha), math.cos(alpha)]])


def rotmaty(alpha: float) -> Mat3D:
    """Matrix für die rotation um die y-achse.

    .. image:: _static/rotmaty.png
       :scale: 20 %

    Parameters
    ----------
    alpha
        Drehwinkel

    Returns
    -------
    Mat3D
        Rotationsmatrix
    """
    return Mat3D([[math.cos(alpha), 0, -math.sin(alpha)], [0, 1, 0], [math.sin(alpha), 0, math.cos(alpha)]])


def rotmatz(alpha: float) -> Mat3D:
    """Matrix für die Rotation um die Z-Achse.

    .. image:: _static/rotmatz.png
       :scale: 20 %

    Parameters
    ----------
    alpha
        Drehwinkel

    Returns
    -------
    Mat3D
        Rotationsmatrix
    """
    return Mat3D([[math.cos(alpha), math.sin(alpha), 0], [-math.sin(alpha), math.cos(alpha), 0], [0, 0, 1]])


def polar2kart(phi: float, theta: float, r: float) -> Tuple[float, float, float]:
    """Polarkoordinaten zu Kartesischenkoordinaten.

    .. image:: _static/sphere.png
       :scale: 50 %

    Parameters
    ----------
    phi
        winkel zwischen z-achse und vektor
    theta
        winkel zwischen x-achse und vektor
    r
        länge des vector

    Returns
    -------
    (x, y, z) kart.-koord.
    """
    x = r * math.cos(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.cos(theta)
    z = r * math.sin(theta)
    return x, y, z


if __name__ == '__main__':
    pass
