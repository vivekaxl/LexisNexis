from __future__ import division, print_function

from unittest import TestCase
from nose.tools import assert_true, assert_false, assert_equals  # noqa
import random

from witschey import searchers
from witschey import models
from witschey.searchers import genetic_algorithm


class TestGeneticAlgorithm(TestCase):
    def setUp(self):  # noqa
        self.searcher = searchers.GeneticAlgorithm(models.Schaffer)

    def test_crossover_lengths(self):
        parent1 = tuple(i * 10 for i in range(10))
        parent2 = tuple((i * 10) + 1 for i in range(10))

        xo = self.searcher._crossover(parent1, parent2, 3)

        assert_equals(len(parent1), len(xo))
        assert_equals(len(xo), len(parent2))

    def test_crossover_values(self):
        random.seed(0)
        for _ in range(20):
            parent1 = tuple(i * 10 for i in range(10))
            parent2 = tuple((i * 10) + 1 for i in range(10))

            xo = self.searcher._crossover(parent1, parent2, 3)

            for i, x in enumerate(xo):
                print(x, parent1[i], parent2[i])
                assert x == parent1[i] or x == parent2[i]

    def test_get_0_crossover_points(self):
        xs = tuple(i * 10 for i in range(10))
        ys = tuple((i * 10) + 1 for i in range(10))
        assert ys == genetic_algorithm._crossover_at(xs, ys, 0)

    def test_get_1_crossover_point_arg_wrap(self):
        xs = tuple(i * 10 for i in range(10))
        ys = tuple((i * 10) + 1 for i in range(10))

        xat = genetic_algorithm._crossover_at
        for i in range(len(xs)):
            assert_equals(xat(xs, ys, i), xat(xs, ys, [i]))

    def test_get_1_crossover_point(self):
        xs = tuple(i * 10 for i in xrange(10))
        ys = tuple((i * 10) + 1 for i in xrange(10))

        for i in xrange(len(xs)):
            xover = genetic_algorithm._crossover_at(xs, ys, [i])
            assert_equals(xs[:i], xover[:i])
            assert_equals(ys[i:], xover[i:])
