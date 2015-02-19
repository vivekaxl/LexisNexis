import collections

from witschey import base
from unittest import TestCase

from nose.tools import assert_equal, assert_true
import mock


class TestPairs(TestCase):

    def test_iterable(self):
        assert_true(isinstance(base.pairs([1, 2]), collections.Iterable))

    def test_empty(self):
        assert_equal(list(base.pairs([])), [])

    def test_tuple(self):
        assert_equal(list(base.pairs((1, 2, 3))), [(1, 2), (2, 3)])

    def test_one_element(self):
        assert_equal(list(base.pairs([1])), [])

    def test_many_elements(self):
        ps = list(base.pairs([x for x in xrange(15)]))
        assert_equal(len(ps), 14)
        for p in ps:
            assert_equal(p[0], p[1] - 1)


class TestMemo(TestCase):

    def test_basic(self):
        v = 1
        m = base.memo(a=v)
        assert_equal(m.a, v)

    def test_nested(self):
        v = 1
        m = base.memo(a=base.memo(a=v))
        assert_equal(m.a.a, v)

    def test_multiple(self):
        v1 = 't'
        v2 = 3
        m = base.memo(a=v1, b=v2)
        assert_equal(m.a, v1)
        assert_equal(m.b, v2)

    def test_string(self):
        m = base.memo(a=base.memo(a=1, b=2), b=2)
        s = '{\n    b: 2\n    a: {\n        a: 1, b: 2\n    }\n}'
        assert_equal(m.to_str(), s)


class TestPrettyInput(TestCase):

    def test_empty(self):
        assert_equal(base.pretty_input(tuple()), "")

    def test_one(self):
        assert_equal(base.pretty_input((-55.2,)), "-55.20")

    def test_many(self):
        t = (44.85555, 3.14, 10)
        s = '44.86, 3.14, 10.00'
        assert_equal(base.pretty_input(t), s)


class TestMemoizer(TestCase):

    def setUp(self):  # noqa
        self.mock = mock.MagicMock()
        self.mock.method.__name__ = 'foo'
        self.memo_mock = base.memoize(self.mock.method)

    def test_called_once(self):
        a = 1
        self.memo_mock(a)
        self.mock.method.assert_called_once_with(a)

        # and again! call should hit the dict, not the mock
        self.memo_mock(a)
        self.mock.method.assert_called_once_with(a)

    def test_called_with_two_values(self):
        a, b = 1, 2
        self.memo_mock(a)
        self.memo_mock(b)
        assert_equal(self.mock.method.mock_calls,
                     [mock.call(a), mock.call(b)])

        # and again! calls should hit the dict, not the mock
        self.memo_mock(a)
        self.memo_mock(b)
        assert_equal(self.mock.method.mock_calls,
                     [mock.call(a), mock.call(b)])

    def test_memo_sqrt(self):
        assert_equal(base.memo_sqrt(4), 2)
        assert_equal(base.memo_sqrt(9), 3)
        assert_equal(base.memo_sqrt(4), 2)
