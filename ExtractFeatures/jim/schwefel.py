from __future__ import print_function, division

import math
import random
import functools

from model import Model
from independent_variable import IndependentVariable as IV  # noqa
from witschey import base


def _randint_matrix(x, lo=-100, hi=100):
    "returns x by x matrix of random integers in [lo, hi]"
    return [[random.randint(lo, hi) for i in xrange(x)]
            for j in xrange(x)]


class Schwefel(Model):
    """Schwefel's problem 2.13, as described in "Problem Definitions and
    Evaluation Criteria for the CEC 2005 Special Session on Real-Parameter
    Optimization", p. 15. Quotes in comments are from this description unless
    otherwise"""

    def __init__(self, d=10):
        f_bias = -460  # magic number from model specification

        # input space is d values from -pi to pi
        independents = tuple((IV(lo=-math.pi, hi=math.pi)
                             for _ in xrange(d)))

        # "q_ij, r_ij are integer random numbers in the range [-100, 100]"
        q, r = _randint_matrix(d), _randint_matrix(d)
        # "alpha... [is a vector] of random numbers in [-pi, pi]"
        alpha = [random.uniform(-math.pi, math.pi) for _ in xrange(d)]

        # 1D matrix of d sums
        a = [sum(q[i][j] * math.sin(alpha[j]) + r[i][j] * math.cos(alpha[j])
             for j in xrange(d)) for i in xrange(d)]

        def b_sum(i):
            # generate a function for b_i = sum(q_ij sin(x) + r_ij cos(x))
            q_sin = lambda j, x: q[i][j] * math.sin(x)
            r_cos = lambda j, x: r[i][j] * math.cos(x)
            f = lambda x: sum(q_sin(j, x) + r_cos(j, x) for j in xrange(d))
            return f

        # generate 1D matrix of functions b_i
        b = [base.memoize(b_sum(i)) for i in xrange(d)]

        # and finally, here's the function to minimize
        def f12(xs):
            if len(xs) != d:
                e = 'len of input vector to {0} must be {0}.d = {1}'.format(
                    self.__name__, d)
                raise ValueError(e)

            return sum((a[i] - b[i](x))**2 + f_bias for i, x in enumerate(xs))

        super(Schwefel, self).__init__(
            independents=independents, dependents=(f12,))

    @classmethod
    def initalizer_with(cls, d):
        rv = functools.partial(cls, d)
        rv.__name__ = ''.join(('Schwefel', '(', str(d), ')'))
        return rv
