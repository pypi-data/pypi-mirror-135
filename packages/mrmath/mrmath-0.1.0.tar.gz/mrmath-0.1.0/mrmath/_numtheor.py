# -*- coding: utf-8 -*-

"""Zahlenteoretische und "darstellende" Funktionen.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>
"""

import math


def frac(x: float) -> float:
    """Liefert den Nachkommateil einer Zahl.

    Returns
    -------
    Nachkommanteil

    Notes
    -----
    Der Nachkommanteil ist immer positive.

    Examples
    --------
    .. testsetup:: ntfrac

        from mrmath import frac

    .. doctest:: ntfrac

        >>> frac(1.123)
        0.123

        >>> frac(-1.123)
        0.123

        >>> frac(0.123)
        0.123

        >>> frac(-0.123)
        0.123

        >>> round(frac(7654321.123456789),9)
        0.123456789

    """
    if x < 0:
        return -(x - math.ceil(x))
    return x - math.floor(x)


def modulo(x: float, y: float) -> float:
    """Berechnet x mod y.

    :param float x:
    :param float y:
    :return:
    :rtype: float

    .. testsetup:: ntmod

       from mrmath import modulo

    .. doctest:: ntmod

       >>> round(modulo(370, 360), 1)
       10.0

       >>> round(modulo(-370, 360), 1)
       350.0

       >>> round(modulo(-30, 360), 1)
       330.0

       >>> round(modulo(-0, 360), 1)
       0.0

       >>> round(modulo(360, 360), 1)
       0.0

       >>> round(modulo(370, -360), 1)
       -10.0

       >>> round(modulo(-370, -360), 1)
       -350.0

       >>> round(modulo(-30, -360), 1)
       -330.0

       >>> round(modulo(-0, -360), 1)
       0.0

       >>> round(modulo(360, -360), 1)
       0.0

    """
    return y * (frac(x / y) if x >= 0 else (1 - frac(x / y)))


def iseven(number: int) -> bool:
    """Prüft ob eine ganzzahl gerade ist.

    Parameters
    ----------
    number
        ganze zahl

    Returns
    -------
    bool
        ist `n` gerade

    Examples
    --------
    .. testsetup:: nteven

        from mrmath import iseven

    .. doctest:: nteven

        >>> iseven(0)
        True

        >>> iseven(1)
        False

        >>> iseven(2)
        True

        >>> iseven(-1)
        False

        >>> iseven(-2)
        True
    """
    return not bool(number % 2)


def isodd(number: int) -> bool:
    """Prüft ob eine ganzzahl ungerade ist.

    Parameters
    ----------
    n
        ganze zahl

    Returns
    -------
    boolean
        ist ``n`` ungerade

    Exampels
    --------
    .. testsetup:: ntodd

        from mrmath import isodd

    .. doctest:: ntodd

        >>> isodd(0)
        False

        >>> isodd(1)
        True

        >>> isodd(2)
        False

        >>> isodd(-1)
        True

        >>> isodd(-2)
        False
    """
    return bool(number % 2)


if __name__ == '__main__':
    pass
