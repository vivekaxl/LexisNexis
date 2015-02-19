from __future__ import division, print_function

import random
from nose.tools import assert_equal
from unittest import TestCase

from witschey import models
from witschey.models.independent_variable import IndependentVariable
IV = IndependentVariable  # noqa


class TestRandomReplace(TestCase):

    def setUp(self):  # noqa
        ivs = tuple(IV(0, 5) for _ in range(4))
        self.model = models.Model(independents=ivs, dependents=())

    def test_default_replacement(self):
        random.seed(1)
        assert_equal(self.model.random_replace((5, 5, 5)),
                     (4.237168684686163, 5, 5))

    def test_replace_two(self):
        random.seed(1)
        assert_equal(self.model.random_replace((5, 5, 5), 2),
                     (3.8188730948830703, 1.2753451286971085, 5))
