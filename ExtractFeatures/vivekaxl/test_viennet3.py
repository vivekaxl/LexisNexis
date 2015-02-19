from __future__ import division, print_function

import math
import random
from nose.tools import assert_equal, assert_true
from unittest import TestCase, skip

from witschey.models import Viennet3

@skip
class TestViennet3(TestCase):

    def setUp(self):  # noqa
        self.m = Viennet3()

    def test_xs_length(self):
        assert_equal(len(self.m.xs), 2)

    def test_ys_length(self):
        assert_equal(len(self.m.ys), 3)

    def test_xs_values(self):
        for x in self.m.xs:
            assert_equal(x.lo, -3)
            assert_equal(x.hi, 3)
            assert_equal(x.type, float)

    def test_function_names(self):
        for a, b in zip(('f1', 'f2', 'f3'), (f.__name__ for f in self.m.ys)):
            assert_equal(a, b)

    def inputs_helper(self, n):
        for _ in range(25):
            yield (random.uniform(-3, 3), random.uniform(-3, 3))

    def test_f1(self):
        random.seed(1)
        f1 = next(y for y in self.m.ys if y.__name__ == 'f1')

        for xs in self.inputs_helper(25):
            x1, x2 = xs[0], xs[1]
            expected = ((0.5 * (x1 ** 2 + x2 ** 2)) +
                        math.sin(x1 ** 2 + x2 ** 2))
            assert_equal(f1(xs), expected)

    @skip
    def test_f2(self):
        random.seed(1)
        f2 = next(y for y in self.m.ys if y.__name__ == 'f2')

        for xs in self.inputs_helper(25):
            x1, x2 = xs[0], xs[1]

            a = ((3 * x1 + 2 * x2 + 4) ** 2) / 8
            b = ((x1 - x2 + 1) ** 2) / 27
            expected = a + b + 15

            assert_equal(f2(xs), expected)

    @skip
    def test_f3(self):
        assert_true(False)
