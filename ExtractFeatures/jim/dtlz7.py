# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division
import math

from model import Model
from independent_variable import IndependentVariable as IV  # noqa


class DTLZ7(Model):
    def __init__(self, ivs=30, dvs=20):

        # dynamically generate these suckers
        # h/t http://stackoverflow.com/a/13184536/3408454
        generated_fs = []
        for x in xrange(1, dvs):
            f = lambda xs: xs[x]
            f.__name__ = 'f{}'.format(x)
            generated_fs.append(f)

        def g(xs):
            # avoid divide by 0 errors
            denom = abs(xs[-1]) or .0001
            return 1 + (9 / denom) * sum(xs)

        def h(xs, fs=generated_fs, g=g):
            s = 0
            for f in fs:
                fxs = f(xs)
                a = fxs / (1 + g(xs))
                b = 1 + math.sin(3 * math.pi * fxs)
                s += a * b

            return dvs - s

        def final_f(xs):
            return (1 + g(xs)) * h(xs)
        final_f.__name__ = 'f{}'.format(dvs)

        fs = tuple(generated_fs + [final_f])

        independents = tuple(IV(lo=0, hi=1) for _ in xrange(ivs))
        super(DTLZ7, self).__init__(independents=independents, dependents=fs)
