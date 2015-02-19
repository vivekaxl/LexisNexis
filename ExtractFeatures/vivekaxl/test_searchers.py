from __future__ import division

from nose.tools import assert_equals, assert_is_instance, assert_is_none
from nose.tools import assert_greater_equal, assert_less_equal  # noqa

from witschey import searchers
from unittest import TestCase
from witschey import models


class TestSearcherConfig(TestCase):

    def test_empty_config(self):
        sc = searchers.SearcherConfig()
        assert_is_none(sc._model)
        assert_is_none(sc._searcher)
        assert_equals(sc._kw_dict, {})

    def test_empty_config_repr(self):
        sc = searchers.SearcherConfig()
        sc_str_ref = 'SearcherConfig(searcher=None, model=None)'

        assert_equals(repr(sc), sc_str_ref)
        assert_equals(str(sc),  sc_str_ref)

    def test_update_model_and_searcher(self):
        sc = searchers.SearcherConfig()
        sc.update(model=models.Schaffer, searcher=searchers.SimulatedAnnealer)
        assert sc.model == models.Schaffer
        assert sc.searcher == searchers.SimulatedAnnealer

    def test_update_kw_dict(self):
        for s in (searchers.SimulatedAnnealer, None):
            for m in (models.Schaffer, None):
                sc = searchers.SearcherConfig(searcher=s, model=m)
                sc.update(p_mutation=1/3)
                assert sc.as_dict()['p_mutation'] == 1/3
                assert len(sc.as_dict()) == 3
                assert sc.searcher == s
                assert sc.model == m

    def test_get_searcher_no_args(self):
        s, m = searchers.SimulatedAnnealer, models.Schaffer
        sc = searchers.SearcherConfig(model=m, searcher=s)

        searcher = sc.get_searcher()
        assert_is_instance(searcher.model, m)
        assert_is_instance(searcher, s)
