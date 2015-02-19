from __future__ import division, print_function

from nose.tools import assert_equal
from unittest import TestCase

from witschey.models import DTLZ7


class TestDTLZ7(TestCase):
    def correct_names(self, m):
        z = zip((f.__name__ for f in m.ys),
                ('f{}'.format(x) for x in range(1, len(m.ys) + 1)))
        for act, corr in z:
            assert_equal(act, corr)

    def generated_fs_correct(self, x):
        m = DTLZ7(dvs=x)
        assert_equal(len(m.ys), x)
        self.correct_names(m)

    def test_default_fs(self):
        m = DTLZ7()
        assert_equal(len(m.ys), 20)

        self.correct_names(m)

    def test_generated_fs(self):
        self.generated_fs_correct(30)
        self.generated_fs_correct(100)
