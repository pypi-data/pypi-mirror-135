# -*- coding: utf-8 -*-

"""Konstanten.

Die Konstanten werden von dem Modul `mrmath` bereitgestellt.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>
"""

from math import pi

RAD: float = pi / 180.0
r"""Konstante zum umrechnen von Grad ins Bogenmass.

:math:`\text{RAD} = \frac{\pi}{180}`
"""

DEG: float = 180.0 / pi
r"""Konstante zum umrechnen vom Bogenmass in Grad.

:math:`\text{DEG} = \frac{180}{\pi}`
"""

ARCS: float = 3600.0 * 180.0 / pi
r"""Bogensekunden pro Radian.

:math:`\text{ARCS} = \frac{3600 \cdot 180}{\pi}`
"""

if __name__ == '__main__':
    pass
