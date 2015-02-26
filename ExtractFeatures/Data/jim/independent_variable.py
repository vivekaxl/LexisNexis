from __future__ import division, print_function
# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

import random


class IndependentVariable(object):
    """
    An independent variable for a model.

    >>> iv = IndependentVariable(0, 10)
    >>> iv.lo, iv.hi
    (0, 10)

    Call an independent variable object to generating random variables within
    its range:

    >>> random.seed(1); iv(), iv(), iv()
    (1.3436424411240122, 8.474337369372327, 7.6377461897661405)

    Provides a `clip` method to return a variable clipped within the bounds
    of the variable:

    >>> iv.clip(10.5), iv.clip(-100), iv.clip(4.2)
    (10, 0, 4.2)

    The optional third argument to __init__ specifies the type of the
    IndependentVariable. Valid values are `float` and `int`, and the default
    is `float`.

    >>> iv = IndependentVariable(0, 10, int)
    >>> iv(), iv(), iv()
    (2, 5, 4)
    """

    def __init__(self, lo, hi, gen_type=float):
        self._lo = lo
        self._hi = hi
        self._type = gen_type

        if self._type == float:
            self._get = random.uniform
        elif self._type == int:
            self._get = random.randint

    def __call__(self):
        return self._get(self.lo, self.hi)

    def clip(self, x):
        """
        Clip the input number within the bounds of the independent variable.
        """
        return max(self.lo, min(self.hi, x))

    @property
    def lo(self):
        """
        Return the lower bound on values for this independent variable.
        Read-only.
        """
        return self._lo

    @property
    def hi(self):
        """
        Return the upper bound on values for this independent variable.
        Read-only.
        """
        return self._hi

    @property
    def type(self):
        """
        Return the type of this independent variable.
        Read-only.
        """
        return self._type
