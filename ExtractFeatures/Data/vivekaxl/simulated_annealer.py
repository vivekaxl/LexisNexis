from __future__ import division, print_function

import random
import math

from searcher import Searcher, SearchReport
from witschey.base import NullObject, StringBuilder
from witschey.log import NumberLog
from witschey.models import ModelInputException


class SimulatedAnnealer(Searcher):
    """
    A searcher that works by mostly-dumb stochastic search that starts with
    lots of random jumps, then makes fewer random jumps, simulating a cooling
    process. See http://en.wikipedia.org/wiki/Simulated_annealing and
    https://github.com/timm/sbse14/wiki/sa for more information.
    """

    def __init__(self, *args, **kwargs):
        super(SimulatedAnnealer, self).__init__(*args, **kwargs)
        self._current = self.model.random_model_io()
        self._best = self._current  # assumes current is immutable
        self._lives = 4
        self._best_era = None
        self._current_era_energies = NumberLog(max_size=None)

    def run(self, text_report=True):
        """
        Run the SimulatedAnnealer on the model specified at object
        instantiation time.
        """
        self._report = StringBuilder() if text_report else NullObject()
        evals = None

        for k in range(self.spec.iterations):
            if self._lives <= 0 and self.spec.terminate_early:
                evals = k
                break
            self._update(k / self.spec.iterations)
            if k % self.spec.era_length == 0 and k != 0:
                self._end_era()

        if evals is None:
            evals = self.spec.iterations
        return SearchReport(best=self._best.energy, evaluations=evals,
                            best_era=self._best_era, spec=self.spec,
                            searcher=self.__class__, report=self._report)

    def _mutate(self, xs):
        return tuple(xs[i] if random.random() < self.spec.p_mutation else v
                     for i, v in enumerate(self.model.random_input_vector()))

    def _get_neighbor(self, model_io):
        neighbor = None
        while neighbor is None:
            gen = self._mutate(model_io.xs)
            try:
                neighbor = self.model(tuple(gen), io=True)
            except ModelInputException:
                pass

        return neighbor

    def _end_era(self):
        self._report += ('\n', '{: .2}'.format(self._best.energy), ' ')
        if not self._best_era:
            self._best_era = self._current_era_energies

        try:
            improved = self._current_era_energies.better(
                self._prev_era_energies)
        except AttributeError:
            improved = False
        if improved:
            self._best_era = self._current_era_energies
        else:
            self._lives -= 1

        self._prev_era_energies = self._current_era_energies
        self._current_era_energies = NumberLog(max_size=None)

    def _update(self, temperature):
        """update the state of the annealer"""
        # generate new neighbor
        neighbor = self._get_neighbor(self._current)
        self._current_era_energies += neighbor.energy

        # compare neighbor and update best
        if neighbor.energy < self._best.energy:
            self._best, self._current = neighbor, neighbor
            self._report += '!'

        if neighbor.energy < self._current.energy:
            self._current = neighbor
            self._report += '+'
        else:
            # if neighbor is worse than current, we still jump there sometimes
            cnorm = self.model.normalize(self._current.energy)
            nnorm = self.model.normalize(neighbor.energy)
            # occasionally jump to neighbor, even if it's a bad idea
            if self._good_idea(cnorm, nnorm, temperature) < random.random():
                self._current = neighbor
                self._report += '?'

        self._report += '.'

    def _good_idea(self, old, new, temp):
        """
        sets the threshold we compare to to decide whether to jump

        returns e^-((new-old)/temp)
        """
        numerator = new - old

        if not 0 <= numerator <= 1:
            numerator = old - new
        try:
            exponent = numerator / temp
        except ZeroDivisionError:
            return 0
        rv = math.exp(-exponent)
        if rv > 1:
            raise ValueError('p returning greater than one',
                             rv, old, new, temp)
        return rv * self.spec.cooling_factor
