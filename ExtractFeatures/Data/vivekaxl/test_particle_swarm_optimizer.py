from __future__ import division, print_function

from nose.tools import assert_equal, assert_true, assert_false  # noqa
from nose.tools import assert_less, assert_greater  # noqa
import random
from unittest import TestCase

from witschey.models import Osyczka
from witschey.searchers.particle_swarm_optimizer import Particle


class TestParticle(TestCase):

    def setUp(self):  # noqa
        random.seed(0)
        self.model = Osyczka()
        self.particles = (Particle(self.model, 0, 0) for _ in range(30))

    def test_valid_xs(self):
        '''
        A new particle's position should be in bounds in each dimension.
        '''
        for particle in self.particles:
            for iv, x in zip(self.model.xs, particle._current.xs):
                assert_true(iv.lo <= x <= iv.hi)

    def test_reasonable_velocities(self):
        '''
        A new particle's velocity shouldn't be bigger than the distance
        between the bounds in that dimension.
        '''
        for particle in self.particles:
            for i, iv in enumerate(particle._model.xs):
                assert_less(particle._velocity[i], iv.hi - iv.lo)
