from __future__ import division, unicode_literals

from datetime import datetime
import abc
from types import NoneType
from collections import namedtuple, OrderedDict

from witschey.base import memo
from witschey.models import Model
from witschey.config import CONFIG


class Searcher(object):
    # allows us to get all subclasses with __subclasses__()
    __metaclass__ = abc.ABCMeta

    def __new__(cls, *args, **kwargs):
        # construct our object
        future_self = super(Searcher, cls).__new__(cls, *args, **kwargs)

        name = cls.__name__
        # initialize a dict with searcher's name
        # and the initialization time
        d = dict(searcher=name, initialized=datetime.now())

        # if there are global options for this class or its bases in CONFIG
        for k in [k.__name__ for k in cls.__bases__] + [name]:
            if hasattr(CONFIG, k):
                # add them to the dict
                d.update(getattr(CONFIG, k).__dict__)

        # then, add the kwargs to the constructor call to the dict.
        # NB: this happens after adding options from The, so
        #     call-specific options override the globals
        d.update(kwargs)

        # set our spec with the contents of the dict
        future_self.spec = memo(**d)

        return future_self

    def __init__(self, model, *args, **kw):
        self.model = model()

    def run(*args, **kwargs):
        raise NotImplementedError()


class SearcherConfig(object):

    def __init__(self, searcher=None, model=None, **kwargs):
        self.searcher, self.model = searcher, model
        self._kw_dict = kwargs

    def get_searcher(self, searcher=None, model=None, **kwargs):
        s = searcher or self.searcher
        m = model or self.model
        kw = self._kw_dict.copy().update(kwargs) or {}
        return s(m, **kw)

    @property
    def searcher(self):
        return self._searcher

    @searcher.setter
    def searcher(self, value):
        if isinstance(value, NoneType) or issubclass(value, Searcher):
            self._searcher = value
        else:
            raise TypeError('{} is not a Searcher or None'.format(value))

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if isinstance(value, NoneType) or issubclass(value, Model):
            self._model = value
        else:
            raise TypeError('{} is not a Model or None'.format(value))

    def update(self, searcher=None, model=None, **kwargs):
        if searcher is not None:
            self.searcher = searcher
        if model is not None:
            self.model = model
        self._kw_dict.update(kwargs)

    def as_dict(self):
        "returns a OrderedDict with the searcher and model first"
        return OrderedDict(searcher=self._searcher,
                           model=self._model, **self._kw_dict)

    def __repr__(self):
        kw_string = ', '.join('{0}={1}'.format(k, v)
                              for k, v in self.as_dict().iteritems())
        return '{0}({1})'.format(self.__class__.__name__, kw_string)


SearchReport = namedtuple('SearchReport',
                          ['best', 'best_era', 'evaluations', 'searcher',
                           'spec', 'report'])
