from __future__ import division, print_function

import inspect

from model import Model, ModelInputException
from independent_variable import IndependentVariable as IV  # noqa


def _lambda_string_strip(s):
    return inspect.getsource(s).split('lambda x: ')[1][:-2]


class Osyczka(Model):

    def __init__(self):
        self.checks = []
        self.checks.append(lambda x: x[0] + x[1] - 2 >= 0)
        self.checks.append(lambda x: 6 - x[0] - x[1] >= 0)
        self.checks.append(lambda x: 2 - x[1] + x[0] >= 0)
        self.checks.append(lambda x: 2 - x[0] + 3 * x[1] >= 0)
        self.checks.append(lambda x: 4 - (x[2] - 3) ** 2 - x[3] >= 0)
        self.checks.append(lambda x: (x[4] - 3) ** 2 + x[5] - 4 >= 0)

        independents = tuple(IV(lo=lo, hi=hi) for lo, hi in
                             ((0, 10), (0, 10), (1, 5),
                              (0, 6), (1, 5), (0, 10)))

        def f1(xs):
            return sum(((-25 * (xs[0] - 2) ** 2),
                        (- (xs[1] - 2) ** 2),
                        (- (xs[2] - 1) ** 2),
                        (- (xs[3] - 4) ** 2),
                        (- (xs[4] - 1) ** 2)))

        def f2(xs):
            return sum(x ** 2 for x in xs)

        super(Osyczka, self).__init__(independents=independents,
                                      dependents=(f1, f2))

    def random_input_vector(self):
        while True:
            candidate = super(Osyczka, self).random_input_vector()
            try:
                self._fail_on_constraint_violations(candidate, no_msg=True)
                return candidate
            except ModelInputException:
                pass

    def valid_input(self, xs):
        try:
            self._fail_on_constraint_violations(xs, no_msg=True)
        except ModelInputException:
            return False
        return True

    def _fail_on_constraint_violations(self, xs, no_msg=False):
        msgs = []
        for check in self.checks:
            if not check(xs):
                if no_msg:
                    raise ModelInputException(xs)
                msgs.append(_lambda_string_strip(check))

        if msgs:
            err = "{} failed on input {}:".format(self.__class__.__name__, xs)
            if len(msgs) == 1:
                err += ' {}'.format(msgs[0])
            else:
                pre = '\n\tviolated constraint: '
                err += pre + pre.join(msgs)
            raise ModelInputException(err)

    def __call__(self, xs, io=False):
        self._fail_on_constraint_violations(xs)
        return super(Osyczka, self).__call__(xs, io=io)
