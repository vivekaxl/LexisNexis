from __future__ import division, print_function

from unittest import TestCase, skip
from nose.tools import assert_true, assert_false, assert_equals  # noqa
from nose.tools import assert_greater
from nose.tools import assert_is_instance

from witschey import basic_stats


@skip
class TestMath(TestCase):

    def test_mean_return_value(self):
        xs = [-2.9, -64.34, 98.76, 56.14, 20.62, 120.62, 22.33, 277.13, 45.1,
              -80.51, 114.01, 209.34, -79.91, 200.83, 144.65, -53.38, -92.95,
              208.1, 84.47, 138.65]
        assert_equals(basic_stats.mean(xs), 68.338)

    def test_mean_doesnt_mutate_argument(self):
        xs = [-2.9, -64.34, 98.76, 56.14, 20.62, 120.62, 22.33, 277.13, 45.1,
              -80.51, 114.01, 209.34, -79.91, 200.83, 144.65, -53.38, -92.95,
              208.1, 84.47, 138.65]
        copy = xs[:]
        basic_stats.mean(xs)
        assert_equals(xs, copy)

    def test_median_even(self):
        xs = [1, 2, 3, 4]
        assert_equals(basic_stats.median(xs), 2.5)

    def test_median_odd(self):
        xs = [1, 2, 3, 4, 5]
        assert_equals(basic_stats.median(xs), 3)

    def test_median_doesnt_mutate_argument(self):
        xs = [1, 2, 3, 4, 5]
        copy = xs[:]
        basic_stats.median(xs)
        assert_equals(xs, copy)

    def test_standard_deviation(self):
        xs = list(range(20)) + list(range(40, 60))
        ys = list(range(-40, -20)) + list(range(40, 60))
        assert_greater(basic_stats.standard_deviation(ys),
                       basic_stats.standard_deviation(xs))

@skip
class TestXtile(TestCase):

    def test_string(self):
        s = '      -----------       *|          ----------    ,   ' +\
            '4.00,  14.00,  24.00,  34.00,  44.00'
        assert_equals(basic_stats.xtile(list(xrange(50))), s)

    def test_as_list(self):
        assert_is_instance(
            basic_stats.xtile(list(xrange(100)), as_list=True), list)
