from __future__ import division
# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

import random
import operator
from functools import wraps


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

    def __init__(self, lo=None, hi=None,
                 gen_type=None, valid_inputs=None, name=None):
        self._lo = lo
        self._hi = hi
        self._type = gen_type
        if name is not None:
            self.__name__ = name
        if valid_inputs is not None:
            self._valid_inputs = tuple(valid_inputs)
        else:
            self._valid_inputs = None

        self._get = None

        if valid_inputs is not None:
            if self._type is not None:
                raise ValueError()

            types = tuple(type(s) for s in valid_inputs)
            t0 = next(iter(types))
            if all(t == t0 for t in types):
                self._type = t0

            self._get = lambda x, y: random.choice(self._valid_inputs)
        elif self._type is None:
            self._type = float

        if self._get is None:
            if self._type == float:
                self._get = random.uniform
            elif self._type == int:
                self._get = random.randint

    def __call__(self):
        return self._get(self.lo, self.hi)

    def valid(self, x):
        '''
        Test if the input is a valid value for this independent variable.
        '''
        if self._valid_inputs is not None:
            return x in self._valid_inputs
        else:
            return self._lo <= x <= self._hi

    def clip(self, x):
        """
        Clip the input number within the bounds of the independent variable.
        """
        try:
            rv = max(self.lo, min(self.hi, x))
            if self._type == int:
                return int(round(rv))
            return rv
        except:
            return x

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

    def enumerable(self):
        return bool(self._valid_inputs)
