from __future__ import division, print_function

import re
import random
from unittest import TestCase
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_not_in
from nose.tools import assert_regexp_matches, assert_not_regexp_matches

from witschey.models import ModelInputException, Osyczka


class TestOsyczka(TestCase):

    def setUp(self):  # noqa
        self.model = Osyczka()
        self.c1_pattern = re.compile(
            'x\[0\] \+ x\[1\] - 2 >= 0',
            re.MULTILINE)
        self.c2_pattern = re.compile(
            '6 - x\[0\] - x\[1\] >= 0',
            re.MULTILINE)
        self.c3_pattern = re.compile(
            '2 - x\[1\] \+ x\[0\] >= 0',
            re.MULTILINE)
        self.c4_pattern = re.compile(
            '2 - x\[0\] \+ 3 \* x\[1\] >= 0',
            re.MULTILINE)
        self.c5_pattern = re.compile(
            '4 - \(x\[2\] - 3\) \*\* 2 - x\[3\] >= 0',
            re.MULTILINE)
        self.c6_pattern = re.compile(
            '\(x\[4\] - 3\) \*\* 2 \+ x\[5\] - 4 >= 0',
            re.MULTILINE)

    def test_constraint(self):
        try:
            self.model((1, .5, 5, 5, 3, 3))
        except ModelInputException as e:
            assert_regexp_matches(e.message, self.c1_pattern)
            assert_not_regexp_matches(e.message, self.c2_pattern)
            assert_not_regexp_matches(e.message, self.c3_pattern)
            assert_not_regexp_matches(e.message, self.c4_pattern)
            assert_regexp_matches(e.message, self.c5_pattern)
            assert_regexp_matches(e.message, self.c6_pattern)

    def test_one_line_exception_on_single_constraint_violation(self):
        try:
            self.model((4.27, 5.35, 2.86, 0.25, 2.75, 8.72))
        except ModelInputException as e:
            assert_not_in(e.message, '\n')

    def test_valid_input(self):
        assert_false(self.model.valid_input((1, .5, 5, 5, 3, 5)))
        assert_true(self.model.valid_input(
            (1.83, 3.37, 2.81, 3.14, 2.61, 5.51)))

    def test_call_on_valid_input(self):
        assert_equal((-9.2072, 69.6337),
                     self.model((1.83, 3.37, 2.81, 3.14, 2.61, 5.51)))

    def test_valid_random_input_vector(self):
        random.seed(1)
        for _ in xrange(25):
            v = self.model.random_input_vector()
            assert_true(self.model.valid_input(v))
