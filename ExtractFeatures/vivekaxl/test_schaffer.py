from __future__ import division, print_function

from nose.tools import assert_equal
from unittest import TestCase

from witschey.models import Schaffer


class TestSchaffer(TestCase):
    def setUp(self):  # noqa
        self.model = Schaffer()

    def test_unique_names(self):
        names = set(y.__name__ for y in self.model.ys)
        assert_equal(len(names), len(self.model.ys))

    def test_inputs_length(self):
        i = 10
        model = Schaffer(ivs=i)
        x = len(model.xs)
        assert_equal(x, i)

    def test_default_inputs_length(self):
        x = len(self.model.xs)
        assert_equal(x, 1)

    def test_f1(self):
        f1 = next(y for y in self.model.ys if y.__name__ == 'f1')
        assert_equal(f1((0,)), 0)
        assert_equal(f1([2]), 4)
        assert_equal(f1((-2, 2)), 8)

    def test_f2(self):
        f2 = next(y for y in self.model.ys if y.__name__ == 'f2')
        assert_equal(f2((0,)), 4)
        assert_equal(f2([2]), 0)
        assert_equal(f2((0, 0)), 8)
