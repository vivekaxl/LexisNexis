from __future__ import division, print_function

import random

from witschey import base
from witschey.searchers import Searcher, SearchReport
from witschey.log import NumberLog
from witschey.models import ModelInputException

from witschey.models import IndependentVariable as IV
from witschey.models import Model, ModelInputException
from functools import partial

class DifferentialEvolution(Searcher):

    def run(self, text_report=True):
        n_candiates = self.spec.n_candiates
        self._frontier = [self.model.random_model_io()
                          for _ in xrange(n_candiates)]
        self._evals, lives = 0, 4

        for _ in xrange(self.spec.generations):
            if lives <= 0:
                break
            old_frontier_energies = NumberLog(x.energy
                                              for x in self._frontier)
            self._update_frontier()
            new_frontier_energies = NumberLog(x.energy
                                              for x in self._frontier)
            if not new_frontier_energies.better(old_frontier_energies):
                lives -= 1

        return SearchReport(
            best=min(self._frontier, key=lambda x: x.energy).energy,
            best_era=NumberLog(inits=(x.energy for x in self._frontier)),
            evaluations=self._evals,
            searcher=self.__class__,
            spec=self.spec,
            report=None)

    def _update_frontier(self):
        '''for each member of the frontier, generate a new individual, have
        them compete, then keep the best of the two.'''
        bested, better = [], []
        for x in self._frontier:
            new = None
            while new is None:
                extrapolated = self._extrapolate_xs(x)
                try:
                    new = self.model(extrapolated, io=True)
                except ModelInputException:
                    pass

            self._evals += 1
            if new.energy < x.energy:
                bested.append(x)
                better.append(new)

        keep = lambda x: id(x) not in map(id, bested)

        self._frontier = filter(keep, self._frontier) + list(better)

    def _sample_frontier_exclude(self, ex, n=3):
        '''Samples n (default 3) items from the current frontier.
        Returns a shallow copy of the frontier if n is as large or larger
        than the frontier.
        '''
        try:
            # pigeonhole principle: sample n+1 things; at least n aren't ex
            samp = random.sample(self._frontier, n+1)
        except ValueError:
            # if n is too big, just return the frontier
            return self._frontier[:]

        # remove ex if it's there; otherwise remove a random thing
        try:
            samp.remove(ex)
        except ValueError:
            samp.remove(random.choice(samp))

        return samp

    def _extrapolate_x(self, x, sample, iv):
        if iv.enumerable():
            return random.choice(tuple(sample))
        a, b, c = sample
        return iv.clip(a + self.spec.f * (b - c))

    def _extrapolate_xs(self, current):
        '''generate a new individual based on individuals in the frontier'''
        sample = self._sample_frontier_exclude(current, n=3)
        rv_list = [x for x in current.xs]

        # randomly pick at least one x-position to change
        change_indices = [i for i in xrange(len(rv_list))
                          if random.random() < self.spec.p_crossover]
        if not change_indices:
            change_indices = [base.random_index(rv_list)]

        # extrapolate a new value for each of the chosen indices
        for i in change_indices:
            rv_list[i] = self._extrapolate_x(x, (s.xs[i] for s in sample), self.model.xs[i])

        return tuple(rv_list)
