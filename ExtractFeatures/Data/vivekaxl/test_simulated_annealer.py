from __future__ import division

from nose.tools import assert_equals, assert_true, assert_false  # noqa
from nose.tools import assert_is_instance, assert_is_none  # noqa
from nose.tools import assert_greater_equal, assert_less_equal  # noqa

from witschey.searchers import SimulatedAnnealer
from unittest import TestCase


class TestSimulatedAnnealer(TestCase):
    def setUp(self):  # noqa
        self.searcher = SimulatedAnnealer
