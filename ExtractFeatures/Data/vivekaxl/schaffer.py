# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from model import Model
from independent_variable import IndependentVariable as IV  # noqa


class Schaffer(Model):

    def __init__(self, ivs=1):
        independents = tuple(IV(lo=-10 ** 5, hi=10 ** 5) for _ in xrange(ivs))

        # use def instead of lambdas so the functions keep their __name__s
        def f1(xs):
            return sum(x ** 2 for x in xs)

        def f2(xs):
            return sum((x - 2) ** 2 for x in xs)

        super(Schaffer, self).__init__(
            independents=independents, dependents=(f1, f2))
