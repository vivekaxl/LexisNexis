from __future__ import division


import random
from itertools import repeat, izip

from log import NumberLog
import texttable
from basic_stats import xtile
from witschey import basic_stats
from witschey.base import memo_sqrt


def a12(xs, ys):
    gt, eq = 0, 0
    for x in xs:
        for y in ys:
            if x > y:
                gt += 1
            if x == y:
                eq += 1

    return (gt + eq / 2) / (len(xs) * len(ys))


def a12_fast(xs, ys):
    """
    Non-parametric statistical test. Answers the question: "If you pick a
    random x from xs, and a random y from ys, what's the probability that
    x will be greater than y?"
    """

    xs_i = izip(sorted(xs, reverse=True), repeat(0))
    ys_i = izip(sorted(ys, reverse=True), xrange(len(ys), 0, -1))

    gt, eq = 0, 0

    cs, ds = xs_i, ys_i
    c, d = cs.next(), ds.next()
    while True:
        try:
            while d[0] < c[0]:
                gt += d[1]
                # gt += 1
                print(d)
                d = ds.next()
            else:
                if d[0] == c[0]:
                    eq += 1
                    d = ds.next()
                else:
                    cs, ds = ds, cs
        except StopIteration:
            break

    gt += sum(1 for _ in xs_i)

    print('gt: {}\t eq: {}'.format(gt, eq))
    return (gt + eq / 2) / (len(xs) * len(ys))


def test_statistic(y, z):
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    delta = z.mean() - y.mean()
    sd_y = y.standard_deviation()
    sd_z = z.standard_deviation()

    if sd_y + sd_z:
        delta /= memo_sqrt(sd_y / len(y) + sd_z / len(z))

    return delta


def bootstrap(y0, z0, conf=0.01, b=1000):
    """
    The bootstrap hypothesis test from p220 to 223 of Efron's book 'An
    introduction to the boostrap.

    Simple way to describe: "If you randomly generate 1000 similar datasets,
    is a likely to be significantly different to b?"
    """
    y, z = NumberLog(y0), NumberLog(z0)
    x = NumberLog(inits=(y, z))
    observed_mean_difference = test_statistic(y, z)
    yhat = tuple(y1 - y.mean() + x.mean() for y1 in y.contents())
    zhat = tuple(z1 - z.mean() + x.mean() for z1 in z.contents())
    bigger = 0
    for i in range(b):
        # sample with replacement for yhat and zhat
        swr_yhat = (random.choice(yhat) for _ in yhat)
        swr_zhat = (random.choice(zhat) for _ in zhat)
        sampled_mean_difference = test_statistic(
            NumberLog(swr_yhat, max_size=None),
            NumberLog(swr_zhat, max_size=None))
        if sampled_mean_difference > observed_mean_difference:
            bigger += 1
    return bigger / b < conf


def different(xs, ys):
    """
    Quick test to see if 2 things are different. A12 is a reasonable first
    approximation, and fast, and if it gets past A12, run the slower, more
    authoritative, bootstrap.
    """
    return a12(xs, ys) and bootstrap(xs, ys)


def scottknott(data, max_rank_size=3, epsilon=0.01):
    """
    Recursively split data, maximizing delta of the expected value of the
    mean before and after the splits. Reject splits with under max_rank_size
    items.
    """
    flat_data = [x for log in data for x in log.contents()]
    data_mean = basic_stats.mean(flat_data)

    def recurse_and_rank(parts, rank=0):
        "Split, then recurse_and_rank on each part."

        cut = min_mu(parts, data_mean, len(flat_data), max_rank_size, epsilon)
        if cut:
            # if cut, rank "right" higher than "left"
            rank = recurse_and_rank(parts[:cut], rank) + 1
            rank = recurse_and_rank(parts[cut:], rank)
        else:
            # if no cut, then all get same rank
            for part in parts:
                part.rank = rank
        return rank

    recurse_and_rank(sorted(data, key=lambda x: x.median()))

    return data


def min_mu(parts, data_mean, data_size, max_rank_size, epsilon):
    """Find a cut in the parts that maximizes the expected value of the
    difference in the mean before and after the cut. Reject splits that are
    insignificantly different or that generate very small subsets.
    """
    cut = None
    max_delta = 0
    mrs = max_rank_size
    for i, left, right in left_right(parts, epsilon):
        if len(parts[:i]) >= mrs and len(parts[i:]) >= mrs:
            delta = len(left) / data_size * (data_mean - left.mean()) ** 2
            delta += len(right) / data_size * (data_mean - right.mean()) ** 2

            if abs(delta) > max_delta and different(parts[i-1], parts[i]):
                max_delta, cut = abs(delta), i
    return cut


def left_right(parts, epsilon=0.01):
    """For each item in 'parts', yield the splitting index, everything to the
    beginning (including the item) and everything to the end.
    """
    for i in range(1, len(parts)):
        if parts[i].median() - parts[i - 1].median() > epsilon:
            left = NumberLog((p for p in parts[:i]), max_size=None)
            right = NumberLog((p for p in parts[i:]), max_size=None)
            yield i, left, right


def rdiv_report(data):
    """
    Generate a tabular report on the data. Assumes data is in lists, where the
    first element of each list is its name.
    """
    # wrap each line in a NumberLog
    data = map(lambda xs: NumberLog(label=xs[0], inits=xs[1:], max_size=None),
               data)

    # sort by rank & median within each rank
    # sorting is stable, so sort by median first, then rank
    ranked = sorted((x for x in scottknott(data, max_rank_size=1)),
                    key=lambda y: y.median())
    ranked = tuple(sorted(ranked, key=lambda y: y.rank))

    # get high and low values for entire dataset
    lo = min(log.lo for log in data)
    hi = max(log.hi for log in data)

    # generate column names
    rows = [['rank', 'name', 'med', 'iqr', '',
            '10%', '30%', '50%', '70%', '90%']]

    # generate rows
    for x in ranked:
        # each row starts with 'rank label, median, iqr'
        next_row = [x.rank + 1]
        next_row.append(x.label + ',')
        next_row.append('{0:0.2},'.format(float(x.median())))
        next_row.append('{0:0.2}'.format(float(x.iqr())))

        # get xtile: '( -* | -- ) ##, ##, ##, ##, ##'
        xtile_out = xtile(x.contents(), lo=lo, hi=hi, width=30, as_list=True)
        # xtile is displayed as the whisker plot, then comma-separated values
        row_xtile = [xtile_out[0]]
        # don't use `join`, we want each to be its own list element
        row_xtile.extend(map(lambda x: x + ',', xtile_out[1:-1]))
        row_xtile.append(xtile_out[-1])

        next_row.extend(row_xtile)
        rows.append(next_row)

    table = texttable.Texttable(200)
    table.set_precision(2)
    table.set_cols_dtype(['t', 't', 't', 't', 't', 't', 't', 't', 't', 't'])
    table.set_cols_align(['r', 'l', 'l', 'r', 'c', 'r', 'r', 'r', 'r', 'r'])
    table.set_deco(texttable.Texttable.HEADER)
    table.add_rows(rows)
    return table.draw()
