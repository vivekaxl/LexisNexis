from __future__ import division, print_function

import random
from itertools import izip

from searcher import Searcher, SearchReport
from witschey.base import memo_sqrt as sqrt
from witschey.log import NumberLog
from witschey.models import ModelInputException


def _random_scaled_velocity(iv, scale=.1):
    try:
        magnitude = max(iv.hi, iv.lo) - min(iv.hi, iv.lo)
        return random.uniform(-magnitude, magnitude) * scale
    except:
        return iv()


class ParticleSwarmOptimizer(Searcher):
    """
    A searcher that models a "flock" of individuals roaming the search space.
    Individuals make decisions about where to go next based both on their
    own experience and on the experience of the whole group. For more
    information, see https://github.com/timm/sbse14/wiki/pso#details and
    http://en.wikipedia.org/wiki/Particle_swarm_optimization
    """

    def __init__(self, *args, **kwargs):
        super(ParticleSwarmOptimizer, self).__init__(*args, **kwargs)

        self._flock = tuple(self._new_particle()
                            for _ in range(self.spec.population_size))
        self._evals = len(self._flock)
        self._current_flock_energies = NumberLog(p.energy
                                                 for p in self._flock)
        self._best = min(self._flock, key=lambda x: x.energy)
        self._lives = 4
        self._best_flock = None

    def _new_particle(self):
        return Particle(self.model, self.spec.phi1, self.spec.phi2)

    def _update(self):
        self._prev_flock_energies = self._current_flock_energies

        for p in self._flock:
            p._update(self._best)
        self._evals += len(self._flock)
        self._current_flock_energies = NumberLog(p.energy
                                                 for p in self._flock)

        self._best = min(self._best, *self._current_flock_energies)
        if self._current_flock_energies.better(self._prev_flock_energies) or self._best_flock is None:
            self._best_flock = self._flock
        else:
            self._lives -= 1

    def run(self, text_report=False):
        for i in range(self.spec.generations):
            self._update()
            if self._lives <= 0 or self._evals >= self.spec.iterations:
                break

        best_flock_energies = NumberLog(p.energy for p in self._best_flock)
        return SearchReport(best=self._best,
                            best_era=best_flock_energies,
                            evaluations=self._evals,
                            searcher=self.__class__,
                            spec=self.spec,
                            report=None)


class Particle(object):
    """
    A particle in the "flock".
    """

    def __init__(self, model, phi1, phi2):
        self._model = model
        self._current = model.random_model_io()
        self._best = self._current
        self._phi1, self._phi2 = phi1, phi2

        # calculate constriction factor
        phi = phi1 + phi2
        self._k = 2 / abs(2 - phi - sqrt(phi * phi) - 4 * phi)

        # initialize velocities
        self._velocity = tuple(_random_scaled_velocity(iv)
                               for iv in model.xs)
        # print(self._current)

    @property
    def energy(self):
        return self._current.energy

    def _compute_new_velocity(self, local_best):
        to_local = tuple(a - b
                             for a, b in izip(local_best.xs, self._current.xs))
        to_personal = tuple(a - b
                            for a, b in izip(self._best.xs, self._current.xs))
        v = tuple((self._k * (v + self._phi1 * loc + self._phi2 * pers)
                   for v, loc, pers in izip(
                       self._velocity, to_local, to_personal)))
        return v

    def _update(self, local_best):
        """
        Given local_best, the best value seen by this particle's neighbors,
        find the particle's new velocity.
        """


        init_loc = self._current.xs
        init_vel = self._velocity
        candidate_xs = tuple(x.clip(p + v) for x, p, v in izip(self._model.xs, init_loc, init_vel))

        updated = False
        while not updated:
            try:
                self._current = self._model.compute_model_io(candidate_xs)
                updated = True
            except ModelInputException:
                candidate_xs = self._model.random_replace(candidate_xs)

        self._velocity = self._compute_new_velocity(self._best)
