from __future__ import division, print_function

import random
import functools
import collections
import itertools

from sortedcontainers import SortedList

from witschey import base


class Log(object):
    """Keep a random sample of stuff seen so far. Based on Dr. Menzies'
    implementation."""

    MAX_SIZE = 256

    def __init__(self, inits=None, label=None, max_size=MAX_SIZE):
        self._cache = SortedList()
        self._report = None
        self.label = label or ''
        self._n = 0
        self.max_size = max_size
        self._valid_statistics = False
        self._invalidate_statistics()
        if inits:
            map(self.__iadd__, inits)

    def random_index(self):
        return base.random_index(self._cache)

    @classmethod
    def wrap(cls, x, max_size=MAX_SIZE):
        if isinstance(x, cls):
            return x
        return cls(inits=x, max_size=max_size)

    def __len__(self):
        return len(self._cache)

    def extend(self, xs):
        if not isinstance(xs, collections.Iterable):
            raise TypeError()
        map(self.__iadd__, xs)

    def __iadd__(self, x):
        if x is None:
            return x

        self._n += 1

        if issubclass(x.__class__, Log):
            map(self.__iadd__, x._cache)
            return self

        changed = False

        # if cache has room, add item
        if self.max_size is None or len(self._cache) < self.max_size:
            changed = True
            self._cache.add(x)
        # cache is full: maybe replace an old item
        else:
            # items less likely to be replaced later in the run:
            # leads to uniform sample of entire run
            if random.random() <= self.max_size / len(self):
                changed = True
                self._cache.remove(random.choice(self._cache))
                self._cache.add(x)

        if changed:
            self._invalidate_statistics()
            self._change(x)

        return self

    def __add__(self, x, max_size=MAX_SIZE):
        inits = itertools.chain(self._cache, x._cache)
        return self.__class__(inits=inits, max_size=max_size)

    def any(self):
        return random.choice(self._cache)

    def report(self):
        if self._report is None:
            self._report = self._generate_report()
        return self._report

    def setup(self):
        raise NotImplementedError()

    def as_list(self):
        return self._cache.as_list()

    def _invalidate_statistics(self):
        '''
        default implementation. if _valid_statistics is something other than
        a boolean, reimplement!
        '''
        self._valid_statistics = False

    def ish(self, *args, **kwargs):
        raise NotImplementedError()

    def _change(self, x):
        '''
        override to add incremental updating functionality
        '''
        pass

    def _prepare_data(self):
        s = '_prepare_data() not implemented for ' + self.__class__.__name__
        raise NotImplementedError(s)

    def __iter__(self):
        return iter(self._cache)

    def contents(self):
        return self._cache.as_list()


def statistic(f):
    '''
    decorator for log functions that return statistics about contents.
    if _valid_statistics is False, generate valid stats before calling
    the wrapped function.
    '''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self._valid_statistics:
            self._prepare_data()
        return f(*args, **kwargs)

    return wrapper
