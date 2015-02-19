from __future__ import division, print_function

import random

from nose.tools import assert_true, assert_equal  # noqa
from unittest import TestCase, skip

from witschey import rdiv


def slow_a12(xs, ys):
    gt, eq = 0, 0
    for x in xs:
        for y in ys:
            if x > y:
                gt += 1
            if x == y:
                eq += 1

    print('gt: {}\t eq: {}'.format(gt, eq))

    return (gt + eq / 2) / (len(xs) * len(ys))

@skip
class TestA12(TestCase):
    def test_small(self):
        xs = [2, 2, 2, 2, 10]
        ys = [5, 5, 5, 5, 5]

        assert_equal(rdiv.a12(xs, ys), 5 / 25)

    def test_fuzz(self):
        for _ in range(1):
            len_x, len_y = random.randint(5, 50), random.randint(5, 50)
            xs = tuple(random.uniform(-100, 100) for _ in range(len_x))
            ys = tuple(random.uniform(-100, 100) for _ in range(len_y))

            slow = slow_a12(xs, ys)
            fast = rdiv.a12(xs, ys)
            if slow != fast:
                print('xs =', xs)
                print('ys =', ys)
                assert_equal(slow, fast)

@skip
class TestA12Fast(TestCase):
    def test_small(self):
        xs = [2, 2, 2, 2, 10]
        ys = [5, 5, 5, 5, 7]

        assert_equal(rdiv.a12_fast(xs, ys), 5 / 25)

    def test_fuzz(self):
        for _ in range(100):
            len_x, len_y = random.randint(5, 200), random.randint(5, 200)
            xs = tuple(random.uniform(-100, 100) for _ in range(len_x))
            ys = tuple(random.uniform(-100, 100) for _ in range(len_y))

            slow = slow_a12(xs, ys)
            fast = rdiv.a12_fast(xs, ys)
            if slow != fast:
                print('xs =', xs)
                print('ys =', ys)
                assert_equal(slow, fast)
