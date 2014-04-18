from __future__ import with_statement
import urllib as urllib
import os

from dingus import Dingus, patch, isolate


class WhenPatchingObjects:
    @patch('urllib.request.urlopen')
    def should_replace_object_with_dingus(self):
        assert isinstance(urllib.request.urlopen, Dingus)

    def should_restore_object_after_patched_function_exits(self):
        @patch('urllib.request.urlopen')
        def patch_urllib():
            pass
        patch_urllib()
        assert not isinstance(urllib.request.urlopen, Dingus)

    def should_be_usable_as_context_manager(self):
        with patch('urllib.request.urlopen'):
            assert isinstance(urllib.request.urlopen, Dingus)
        assert not isinstance(urllib.request.urlopen, Dingus)

    def should_be_able_to_provide_explicit_dingus(self):
        my_dingus = Dingus()
        with patch('urllib.request.urlopen', my_dingus):
            assert urllib.request.urlopen is my_dingus

    def should_name_dingus_after_patched_object(self):
        with patch('urllib.request.urlopen'):
            assert str(urllib.request.urlopen) == '<Dingus urllib.request.urlopen>'

    def should_set_wrapped_on_patched_function(self):
        def urllib():
            pass
        patch_urllib = patch('urllib.request.urlopen')(urllib)
        assert patch_urllib.__wrapped__ == urllib


class WhenIsolating:
    def should_isolate(self):
        @isolate("os.popen")
        def ensure_isolation():
            assert not isinstance(os.popen, Dingus)
            assert isinstance(os.walk, Dingus)

        assert not isinstance(os.walk, Dingus)
        ensure_isolation()
        assert not isinstance(os.walk, Dingus)


class WhenIsolatingSubmoduleObjects:
    def should_isolate(self):
        @isolate("os.path.isdir")
        def ensure_isolation():
            assert not isinstance(os.path.isdir, Dingus)
            assert isinstance(os.path.isfile, Dingus)

        assert not isinstance(os.path.isfile, Dingus)
        ensure_isolation()
        assert not isinstance(os.path.isfile, Dingus)
