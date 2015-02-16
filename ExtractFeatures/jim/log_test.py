from witschey.log import NumberLog
from unittest import TestCase

import random

from nose.tools import assert_equal


class TestNumberLog(TestCase):
    def setUp(self):  # noqa
        self.max_size = 64
        self.log = NumberLog(max_size=self.max_size)
        random.seed(7)

    def test_validation(self):
        self.log += 48.8
        self.log += 14.24

        # given current implementation, should always be sorted,
        # regardless of insertion order
        assert_equal(sorted(self.log._cache), self.log._cache)
        assert not self.log._valid_statistics

        self.log._prepare_data()

        assert self.log._valid_statistics
        assert_equal(sorted(self.log._cache), self.log._cache)

    def test_invalidation(self):
        self.log += 48.8
        self.log += 14.24
        self.log._prepare_data()

        # make sure validness actually changes
        assert self.log._valid_statistics

        self.log += 56.4

        assert not self.log._valid_statistics

    def test_len_n(self):
        n = 2000
        for _ in xrange(n):
            self.log += 2
        assert_equal(self.log._n, n)
        assert_equal(len(self.log), self.max_size)

    def test_max_size(self):
        for x in xrange(2000):
            self.log += 2
        assert len(self.log._cache) == self.max_size
