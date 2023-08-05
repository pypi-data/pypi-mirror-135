# -*- coding: utf-8 -*-

"""Mathematische funktionen.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>
"""

from math import fabs
from typing import Tuple

from ._const import ARCS, DEG, RAD
from ._hyperbol import coth
from ._numtheor import frac, iseven, isodd, modulo

__all__ = ['coth', 'RAD', 'DEG', 'ARCS', 'iseven', 'isodd', 'frac', 'modulo', 'ddd', 'dms']


def ddd(deg: int, min_: int, sec: float) -> float:
    """Umrechnung eines in Grad, bogenminuten und bogensekunden gegebenen winkels in dezimale darstellung.

    Parameters
    ----------
    deg
        winkelgrad
    min
        bogenminuten
    sec
        bogensekunden

    Returns
    -------
    float
        winkel in dezimaler darstellung

    Examples
    --------
    .. testsetup:: ddd

       from mrmath import ddd

    .. doctest:: ddd

       >>> round(ddd(15, 30, 0.0), 1)
       15.5

       >>> round(ddd(-8, 9, 10.0), 5)
       -8.15278

       >>> round(ddd(0, 1, 0.0), 5)
       0.01667

       >>> round(ddd(0, -5, 0.0), 5)
       -0.08333
    """
    if deg < 0 or min_ < 0 or sec < 0:
        sign = -1.0
    else:
        sign = 1.0
    return sign * (abs(deg) + abs(min_) / 60.0 + abs(sec) / 3600.0)


def dms(angle: float) -> Tuple[int, int, float]:
    """Ermittelt Grad, Bogenminuten und Bogensekunden zu gegebenem Winkel.

    Parameters
    ----------
    dd
        Winkel in Grad in dezimaler Darstellung

    Returns
    -------
    D : int
        Winkelgrade
    M : int
        Bogenminuten
    S : float
        Bogensekunden

    Examples
    --------
    .. testsetup:: dms

       from mrmath import dms

    .. doctest:: dms

      >>> dms(0.5)
      (0, 30, 0.0)

      >>> dms(-0.5)
      (0, -30, 0.0)
    """
    x = fabs(angle)
    deg = int(x)
    x = (x - deg) * 60.0
    min_ = int(x)
    sec = (x - min_) * 60.0
    if angle < 0.0:
        if deg != 0:
            deg *= -1
        else:
            if min_ != 0:
                min_ *= -1
            else:
                sec *= -1.0
    return deg, min_, sec


if __name__ == '__main__':
    pass
