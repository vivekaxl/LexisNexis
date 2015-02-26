from __future__ import division, print_function, unicode_literals

import random
import functools
import math
import itertools
import collections


def pretty_input(t):
    float_format = lambda x: '{:.2f}'.format(x)
    str_tuple = tuple(float_format(x) for x in t)
    return ', '.join(s for s in str_tuple)


def pairs(xs):
    # from https://docs.python.org/2/library/itertools.html
    a, b = itertools.tee(xs)
    next(b, None)
    for p in itertools.izip(a, b):
        yield p


class memo(object):  # noqa -- TODO: rethink this name
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_str(self, depth=0, indent=4, infix=': ', sep=', ', d=None):
        return '{' + self._to_str(
            depth=depth + 1,
            indent=indent,
            infix=infix,
            sep=sep,
            d=self.__dict__ if d is None else d) + '}'

    def _to_str(self, depth, indent, infix, sep, d):
        after, before = [], []
        rv = ''
        for k in sorted([s for s in d.keys() if s[0] != '_']):
            val = d[k]
            if isinstance(val, memo) or type(val) == dict:
                after.append(k)
            else:
                before.append('{}{}{}'.format(k, infix, repr(val)))
        if before:
            rv += '\n' + ' ' * depth * indent
            rv += sep.join(before)
        rv += '\n'

        for k in after:
            rv += ''.join([' ' * depth * indent, k, infix, '{'])
            k = d[k]
            k = k if type(k) == dict else k.__dict__
            rv += ''.join([self._to_str(depth=depth+1, indent=indent,
                           infix=infix, sep=sep, d=k),
                           ' ' * depth * indent,
                           '}\n'])

        return rv


def memoize(f):
    'memoizer for single-arg functions'
    d = {}

    @functools.wraps(f)
    def wrapper(x):
        try:
            return d[x]
        except KeyError:
            d[x] = f(x)
            return d[x]

    return wrapper


@memoize
def memo_sqrt(x):
    return math.sqrt(x)


def tuple_replace(t, replace_at, value):
    return tuple(value if i == replace_at else v for i, v in enumerate(t))


def random_index(x):
    '''
    Given a dict, list, tuple, or a subclass of one of these, return a random
    valid key for it.
    '''
    if isinstance(x, dict) or issubclass(x.__class__, dict):
        return random.choice(x.keys)
    if isinstance(x, (list, tuple)) or issubclass(x.__class__, (list, tuple)):
        return random.randint(0, len(x) - 1)
    raise ValueError('{} is not a dict, list, or tuple'.format(x))


class StringBuilder(object):
    def __init__(self, *args):
        self._s = ''.join(args)
        self._next = []

    def append(self, arg):
        'recurse through iterables in args, adding all strings to _next '
        'raises TypeError if it finds a non-Iterable non-string'
        if isinstance(arg, basestring):
            self._next.append(arg)
        elif isinstance(arg, collections.Iterable):
            map(self.append, arg)
        else:
            raise TypeError('{} not a string or iterable'.format(arg))

    def __iadd__(self, arg):
        self.append(arg)
        return self

    def as_str(self):
        'build and cache _s if necessary, then return it.'
        if self._next:
            self._s += ''.join(self._next)
            self._next = []
        return self._s

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.as_str())


class NullObject(object):
    __slots__ = ()

    def __init__(self, *args, **kw):
        return None

    def _return_self(self, *name, **kw):
        return self

    __getattribute__ = _return_self
    __setattr__ = _return_self
    __iadd__ = _return_self
    __call__ = _return_self

    def __bool__(self, *args, **kw):
        return False
    __nonzero__ = __bool__
