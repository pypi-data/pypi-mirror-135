import unittest
import logging
import io
import os
import sys
import shutil
import threading
import traceback
import time
from tempfile import gettempdir
import regex as re
import requests
from checklogs import no_logs
from gitbuilding.__main__ import main


class ThreadExceptionWatcher():
    """
    Re-raises exceptions raised by threads executed in this context
    Exception is only raised when thread exits.
    """

    def __init__(self):
        self._exceptions = None
        self._org_hook = None

    def _store_excepthook(self, args):
        '''
        Uses as an exception handlers which stores any uncaught exceptions.
        '''
        self._org_hook(args)
        formated_exc = traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
        self._exceptions.append('\n'.join(formated_exc))
        return formated_exc

    def __enter__(self):
        '''
        Register us to the hook.
        '''
        self._exceptions = []
        self._org_hook = threading.excepthook
        threading.excepthook = self._store_excepthook

    def __exit__(self, _, value, __):
        '''
        Remove us from the hook, assure no exception were thrown.
        '''
        threading.excepthook = self._org_hook
        if len(self._exceptions) != 0:
            tracebacks = os.linesep.join(self._exceptions)
            raise Exception(f'Exceptions in other threads: {tracebacks}')


class MainArgsTestCase(unittest.TestCase):
    """
    Test case for simple arguments into main.
    """
    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_no_args(self):
        main([])
        self.assertEqual(self.stdout.getvalue(), 'Invalid gitbuilding command None\n')

    def test_bad_args(self):
        with self.assertRaises(SystemExit):
            main(['foo'])

    def test_version(self):
        main(['--version'])
        self.assertIsNotNone(re.match(r'^[0-9]+\.[0-9]+\.[0-9]+(?:\.dev[0-9]+)?$',
                                      self.stdout.getvalue()))


def _make_and_enter_clean_temp_dir(dirname):
    """
    Makes a clean temporary directory of the given name. Deletes the contents
    if dir exists
    """
    temp_dir = os.path.join(gettempdir(), dirname)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    os.chdir(temp_dir)


class RunMainTestCase(unittest.TestCase):
    """
    Test case running main and checking there are no errors.
    This probably creates a lot of weak coverage that needs to be tested
    again, but is important to check that the core functions run without
    errors.
    """

    @no_logs('BuildUp')
    def test_example_build(self):
        """
        Check build with no logs for `gitbuilding new` project
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestBuild')
        main(['new'])
        main(['build'])

    def test_example_build_missing_dict(self):
        """
        Rename the dictionary. Should warn but not error.
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestBuild_missing_dict')
        main(['new'])
        os.rename('Parts.yaml', 'Prts.yaml')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_missing_step(self):
        """
        Rename a step. Should warn but not error.
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestBuild_missing_step')
        main(['new'])
        os.rename('testpage2.md', 'testpage3.md')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_invalid_yaml(self):
        """
        Rename a step. Should warn but not error.
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestBuild_invalid_yaml')
        main(['new'])
        with open('buildconf.yaml', 'w') as yml:
            yml.write('asdas: ? asd?')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_invalid_data_in_yaml(self):
        """
        Rename a step. Should warn but not error.
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestBuild_invalid_data_in_yaml')
        main(['new'])
        with open('buildconf.yaml', 'a') as yml:
            yml.write('CustomCategories:\n  CatName: stuff')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    @no_logs('BuildUp')
    def test_example_build_html(self):
        """
        Check build HTML site with no logs for `gitbuilding new` project
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestHTML')
        main(['new'])
        main(['build-html'])

    @no_logs('BuildUp')
    def test_example_serve(self):
        """
        Check serve with no logs for `gitbuilding new` project, but errors when
        starting a second server.
        """
        _make_and_enter_clean_temp_dir('GB_ExampleTestServe')
        main(['new'])
        t_server = threading.Thread(name='Server', target=main, args=(['serve'],))
        t_server.setDaemon(True)
        t_server.start()
        time.sleep(2)
        requests.get('http://localhost:6178')
        with self.assertRaises(Exception):
            with ThreadExceptionWatcher():
                # Test that we can't start a second server because the first one is running
                t_server2 = threading.Thread(name='Server2', target=main, args=(['serve'],))
                t_server2.setDaemon(True)
                t_server2.start()
                time.sleep(2)
                t_server2.join()
