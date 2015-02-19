from __future__ import division, print_function

from nose.tools import assert_equal, assert_is_instance, assert_true
from nose.tools import assert_in
import random
from unittest import TestCase

from witschey.models import IndependentVariable


class TestIndependentVariable(TestCase):

    def test_init_default(self):
        lo, hi = 0, 10
        iv = IndependentVariable(lo, hi)
        assert_equal(iv.lo, lo)
        assert_equal(iv.hi, hi)
        assert_equal(iv.type, float)

    def test_init_type(self):
        lo, hi = 0, 10
        iv = IndependentVariable(lo, hi, int)
        assert_equal(iv.lo, lo)
        assert_equal(iv.hi, hi)
        assert_equal(iv.type, int)

    def test_init_type_with_string_valid_inputs(self):
        iv = IndependentVariable(valid_inputs=('hello', 'and', 'welcome'))
        assert_equal(iv.type, str)

    def test_output_with_string_valid_inputs(self):
        valid = {'hello', 'and', 'welcome'}
        iv = IndependentVariable(valid_inputs=valid)
        for x in [iv() for _ in range(30)]:
            assert_in(x, valid)

    def valid_generated_helper(self, t):
        random.seed(1)
        lo, hi = -10, 10
        iv = IndependentVariable(lo, hi, t)
        for _ in range(50):
            x = iv()
            assert_true(lo <= x <= hi)
            assert_is_instance(x, t)

    def test_valid_generated_floats(self):
        self.valid_generated_helper(float)

    def test_valid_generated_ints(self):
        self.valid_generated_helper(int)

    def test_clipping_hi(self):
        iv = IndependentVariable(0, 10)
        assert_equal(iv.clip(10.5), 10)

    def test_clipping_lo(self):
        iv = IndependentVariable(0, 10)
        assert_equal(iv.clip(-100), 0)

    def test_clipping_in(self):
        iv = IndependentVariable(0, 10)
        assert_equal(iv.clip(4.2), 4.2)
