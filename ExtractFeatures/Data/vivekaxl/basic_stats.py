from __future__ import division, print_function

import itertools
import base


def median(xs, is_sorted=False):
    """
    Return the median of the integer-indexed object passed in. To save sorting
    time, the client can pass in is_sorted=True to skip the sorting step.
    """
    # implementation from http://stackoverflow.com/a/10482734/3408454
    if not is_sorted:
        xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2] + xs[n // 2 - 1]) / 2


def mean(xs):
    "Returns the mean of the iterable argument."
    return sum(xs) / len(xs)


def iqr(xs):
    n = len(xs)
    return xs[int(n * .75)] - xs[int(n * .25)]


_mean = mean  # `mean` alias for use by standard_deviation, which shadows it


def standard_deviation(xs, mean=None):
    if mean is None:
        mean = _mean(xs)
    return base.memo_sqrt(sum((x - mean) ** 2 for x in xs))


def norm(x, a, b):
    lo, hi = min(a, b), max(a, b)
    try:
        return (x - lo) / (hi - lo)
    except ZeroDivisionError:
        return .5


def value_at_proportion(p, xs):
    return xs[int(round(len(xs) - 1) * p)]


def percentile(x, xs, is_sorted=False):
    if not is_sorted:
        xs = sorted(xs)
    before = len(tuple(itertools.takewhile(lambda y: y < x, xs)))
    return before / len(xs)


def xtile(xs, lo=0, hi=0.001, width=50,
          chops=[0.1, 0.3, 0.5, 0.7, 0.9], marks=["-", " ", " ", "-", " "],
          bar="|", star="*", show=" {: >6.2f}",
          as_list=False):
    """Take an iterable of numbers and present them as a horizontal xtile
    ascii chart. The default is a contracted quintile showing the 10th, 30th,
    50th, 70th, and 90th percentiles. These breaks can be customized with the
    chops parameter.
    """

    xs = sorted(xs)

    lo, hi = min(lo, xs[0]), max(hi, xs[-1])
    if hi == lo:
        hi += .001  # ugh

    out = [' '] * width

    out_index_for_value = lambda x: min(width-1,
                                        int(len(out) * norm(x, lo, hi)))

    values_at_chops = tuple(xs[int(len(xs) * p)] for p in chops)
    where = [out_index_for_value(n) for n in values_at_chops]

    for one, two in base.pairs(where):
        for i in range(one, two):
            out[i] = marks[0]
        marks = marks[1:]

    out[int(width / 2)] = bar
    out[out_index_for_value(xs[int(len(xs) * 0.5)])] = star

    if as_list:
        rv = ['(' + ''.join(out) + ")"]
        rv.extend(show.format(x) for x in values_at_chops)
        return rv

    return ''.join(out) + "," + ','.join([show.format(x)
                                         for x in values_at_chops])
