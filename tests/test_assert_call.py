from dingus import Dingus
from nose.tools import raises


class AssertCallTest(object):

    def setup(self):
        self.ding = Dingus('ding')

class WhenCallsExists(AssertCallTest):

    def should_not_raise_any_error_simple_call(self):
        self.ding.foo()

        self.ding.foo.assert_call()

    def should_not_raise_any_error_with_args(self):
        self.ding.foo('bar')

        self.ding.foo.assert_call()
        self.ding.foo.assert_call('bar')

    def should_not_raise_any_error_with_args_and_kwargs(self):
        self.ding.foo('bar', qux=1)

        self.ding.foo.assert_call()
        self.ding.foo.assert_call('bar')
        self.ding.foo.assert_call('bar', qux=1)

class WhenThereIsNoCallsForTheMatchedArgs(AssertCallTest):

    @raises(AssertionError)
    def should_raise_an_assertion_error(self):
        self.ding.foo.assert_call()

    @raises(AssertionError)
    def should_raise_an_assertion_error_other_method_call(self):
        self.ding.bar()

        self.ding.foo.assert_call()

    @raises(AssertionError)
    def should_raise_an_assertion_error_with_args(self):
        self.ding.foo()

        self.ding.foo.assert_call('bar')

    @raises(AssertionError)
    def should_raise_an_assertion_error_with_args_and_kargs(self):
        self.ding.foo('bar')

        self.ding.foo.assert_call('bar', qux=1)

    def should_show_a_friendly_error_message(self):
        self._test_expectation_message('foo')

    def should_show_a_friendly_error_message_with_args(self):
        self._test_expectation_message('foo', 'baz', 'qux')

    def should_show_a_friendly_error_message_with_args_and_kargs(self):
        self._test_expectation_message('foo', 'baz', 'qux', one=1, two=2)

    def _test_expectation_message(self, method, *args, **kwargs):
        try:
            dingus = getattr(self.ding, method)
            dingus.assert_call(*args, **kwargs)
        except AssertionError as e:
            self._assert_message(e.args[0], dingus, args, kwargs)
        else:
            assert False, 'should not be here'

    def _assert_message(self, message, dingus, args, kwargs):
            expected, recorded_calls = message.split('\n')

            assert "Expected a call to: '%s', args: %s, kwargs: %s, " % (dingus, args, kwargs)

            if not self.ding.calls:
                assert "No calls recorded" == recorded_calls
            else:
                assert ("Recorded calls: %s" % self.ding.calls) == recorded_calls
