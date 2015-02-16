from __future__ import division

from log import Log
from witschey import base
from witschey import basic_stats


class NumberLog(Log):

    def __init__(self, *args, **kwargs):
        super(NumberLog, self).__init__(*args, **kwargs)

        self._invalidate_statistics()

    @property
    def hi(self):
        return self._cache[-1]  # assumes SortedList implementation

    @property
    def lo(self):
        return self._cache[0]  # assumes SortedList implementation

    def _invalidate_statistics(self):
        self._cached_mean, self._cached_median = None, None
        self._cached_sd, self._cached_iqr = None, None

        super(NumberLog, self)._invalidate_statistics()

    def norm(self, x):
        "normalize the argument with respect to maximum and minimum"
        if self.hi == self.lo:
            raise ValueError('hi and lo of {} are equal'.format(self.__name__))
        return basic_stats.norm(x, self.lo, self.hi)

    def _prepare_data(self):
        if not self._valid_statistics:
            pass
        self._valid_statistics = True

    def _generate_report(self):
        return base.memo(median=self.median(), iqr=self.iqr(),
                         lo=self.lo, hi=self.hi)

    def ish(self, f=0.1):
        """return a num likely to be similar to/representative of
        nums in the distribution"""
        return self.any() + f*(self.any() - self.any())

    def median(self):
        if self._cached_median is not None:
            return self._cached_median
        self._cached_median = basic_stats.median(self._cache)
        return self._cached_median

    def mean(self):
        if self._cached_mean is not None:
            return self._cached_mean
        self._cached_mean = basic_stats.mean(self._cache)
        return self._cached_mean

    def standard_deviation(self):
        if self._cached_sd is not None:
            return self._cached_sd
        self._cached_sd = basic_stats.standard_deviation(
            self._cache, mean=self.mean())
        return self._cached_sd

    def iqr(self):
        if self._cached_iqr is not None:
            return self._cached_iqr
        self._cached_iqr = basic_stats.iqr(self._cache)
        return self._cached_iqr

    def xtile(self, *args, **kw):
        return basic_stats.xtile(self._cache, *args, **kw)

    def value_at_proportion(self, p):
        return basic_stats.value_at_proportion(p, self._cache)

    def better(self, log2):
        if log2 is None:
            return ValueError
        if not self._cache or not log2._cache:
            return False
        if self.median() < log2.median():
            return True
        if self.iqr() < log2.iqr():
            return True
        return False
