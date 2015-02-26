from __future__ import division

import random

from nose.tools import assert_equals, assert_true, assert_false  # noqa
from nose.tools import assert_is_instance, assert_is_none  # noqa
from nose.tools import assert_greater_equal, assert_less_equal  # noqa

from witschey import searchers
from unittest import TestCase
from witschey import models


class TestMaxWalkSat(TestCase):

    def setUp(self):  # noqa
        self.mws = searchers.MaxWalkSat(models.Schaffer)

    def test_init(self):
        s = searchers.MaxWalkSat(models.Schaffer, iterations=222)
        assert_equals(s.spec.iterations, 222)

    def test_local_inputs_length(self):
        n = 15
        assert_equals(n, len(list(self.mws._local_search_xs(3, 6, n))))

    def test_local_inputs_contents(self):
        xs = self.mws._local_search_xs(0, 20, 20)
        random.seed(1)
        # this is stochastic, so run it 100 times & hope any errors are caught
        for _ in xrange(100):
            for i, x in enumerate(xs):
                assert_greater_equal(i + 1, x)
                assert_less_equal(i, x)

    def test_doesnt_fall_over(self):
        """this test doesn't help much, except to make sure there aren't any
        dumb type errors"""
        self.mws = searchers.MaxWalkSat(models.Schaffer, iterations=300)
