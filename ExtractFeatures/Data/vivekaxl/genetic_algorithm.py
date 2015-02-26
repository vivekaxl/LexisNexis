from __future__ import division, print_function

from itertools import chain, combinations, cycle, izip, tee
import random
from collections import Iterable

from witschey import base
from searcher import Searcher, SearchReport
from witschey.log import NumberLog
from witschey.models import ModelInputException

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
# Structure from:
# www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html


def _random_crossover_points(n, length):
    # get n random valid crossover points for a sequence of len length
    r = list(xrange(1, length - 1))
    if len(r) <= length:
        return r
    xovers = sorted(random.sample(xrange(1, length - 1), n))
    return xovers


def _crossover_at(seq1, seq2, xovers):
    # takes two sequences and a single crossover point or a list of points
    if not isinstance(xovers, Iterable):
        xovers = [xovers]
    cycle_seq = cycle((seq1, seq2))

    # iter. of start and stop points for sections
    xovers = chain((None,), xovers, (None,))
    parent_point_zip = izip(cycle_seq, base.pairs(xovers))

    segments = tuple(parent[start_stop[0]:start_stop[1]]
                     for parent, start_stop in parent_point_zip)

    return tuple(chain(*segments))


class GeneticAlgorithm(Searcher):
    """
    A searcher that searches the input space by modeling a population of
    organisms that 'breed', are selected for their good qualities, and
    mutate slightly from generation to generation.

    For more information, see https://github.com/timm/sbse14/wiki/Ga and
    http://en.wikipedia.org/wiki/Genetic_algorithm.
    """

    def _mutate(self, child):
        i = base.random_index(child)
        return base.tuple_replace(child, i, self.model.xs[i]())

    def _crossover(self, parent1, parent2, xovers=None):
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')
        if len(parent1) == 1:
            return random.choice((parent1, parent2))
        if xovers is None:
            xovers = self.spec.crossovers

        x_pts = _random_crossover_points(xovers, len(parent1))

        return _crossover_at(parent1, parent2, x_pts)

    def _select_parents(self):
        """
        Return an iterator with 2 copies of each pair of parents in the
        population
        """
        return chain(*tee(combinations(self._population, 2)))

    def _breed_next_generation(self):
        children = []
        for parent1, parent2 in self._select_parents():
            failures = 0
            child = None
            while child is None:
                xs = self._crossover(parent1.xs, parent2.xs)
                if random.random() < self.spec.p_mutation or failures > 0:
                    # mutate more if the parents don't work well together
                    for _ in range(max(failures + 1, len(xs))):
                        xs = self._mutate(xs)
                try:
                    child = self.model(xs, io=True)
                except ModelInputException:
                    failures += 1
            children.append(child)
        self._evals += len(children)
        return tuple(children[:self.spec.population_size])

    def run(self, text_report=True):
        init_xs = tuple(self.model.random_input_vector()
                        for _ in xrange(self.spec.population_size))
        get_energy = lambda x: x.energy
        best_era = None

        report = base.StringBuilder() if text_report else base.NullObject()

        self._population = tuple(self.model.compute_model_io(xs)
                                 for xs in init_xs)

        best = min(self._population, key=get_energy)

        self._evals, lives = 0, 4

        for gen in xrange(self.spec.iterations):
            if self._evals > self.spec.iterations or lives <= 0:
                break

            prev_best_energy = best.energy

            self._population = self._breed_next_generation()

            best_in_generation = min(self._population, key=get_energy)
            best = min(best, best_in_generation, key=get_energy)

            report += str(best.energy)
            report += ('+' if x.energy < prev_best_energy else '.'
                       for x in self._population)
            report += '\n'

            energies = NumberLog(inits=(c.energy for c in self._population))
            try:
                improved = energies.better(prev_energies)
            except NameError:
                improved = False
            prev_energies = energies  # noqa: flake8 doesn't catch use above

            if improved:
                best_era = energies
            else:
                lives -= 1

        if best_era is None:
            best_era = energies

        return SearchReport(best=best.energy,
                            best_era=best_era,
                            evaluations=self._evals,
                            searcher=self.__class__,
                            spec=self.spec,
                            report=None)
