# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division
import math

from model import Model
from independent_variable import IndependentVariable as IV  # noqa


class Viennet3(Model):

    def __init__(self):

        def f1(xs):
            xs_2_sum = xs[0] ** 2 + xs[1] ** 2
            return (0.5 * xs_2_sum) + math.sin(xs_2_sum)

        def f2(xs):
            x_1 = xs[0]
            x_2 = xs[1]

            a = ((3 * x_1 - 2 * x_2 + 4) ** 2) / 8
            b = ((x_1 + x_2 + 1) ** 2) / 27

            return a + b + 15

        def f3(xs):
            x_1sq = xs[0] ** 2
            x_2sq = xs[1] ** 2

            a = 1 / (x_1sq + x_2sq + 1)
            b = 1.1 * math.exp(-x_1sq - x_2sq)

            return a - b

        ivs = (IV(lo=-3, hi=3), IV(lo=-3, hi=3))

        super(Viennet3, self).__init__(
            independents=ivs, dependents=(f1, f2, f3))
