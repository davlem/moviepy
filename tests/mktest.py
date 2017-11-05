#!/usr/bin/env python
"""
mktest script for do a test from module.
"""
import os
import sys
import codecs
import importlib
import inspect

DEFAULT_TESTS_PATH = './test/unit'
SKIP_CLASSES = [
    'os', 'sys', 'ArgumentParser', 'datetime', 'timedelta', 'tz',
    'functools', 'inspect', 'warnings'
    ]

def _create_test_module(filename):
    """create test module from filename method
    """


def print_message(message):
    """print message method
    """
    _line = '-' * 80
    print '\n'.join((
        _line, message, _line
        ))


def get_test_method_template(level):
    """get test method template
    """
    _lev = level or 0
    _sp = ' ' * (_lev * 4)
    _tmp = """raise NotImplementedError()
_in = 0
for _n0, _e0 in enumerate(self._d0[_in]):
    _d0 = _e0
    _r0 = self._r0[_in][_n0]
    self.assertEqual(_d0, _r0)\n"""
    _tmpl = [
        '%s%s' % (_sp, _e0) for _e0 in _tmp.split('\n')
        ]
    _tmp = '\n'.join(_tmpl)
    return _tmp


def get_test_method(method, level=None):
    """get a test method string for a method
    
    args:
        method: (function) method to get test.
        level: (int) level to insert spaces.
    """
    _me = method
    _lev = level or 0
    _sp = ' ' * (4 * _lev)

    _re = '%sdef test_%s_%s(self, ):\n%s' % (
        _sp,
        _me.__name__,
        ('method', 'class')[isinstance(_me, type)],
        get_test_method_template(_lev + 1)
        )

    return _re


def get_test_module_filename(module):
    """get test module filename method
    """
    _mod = module
    _mpath, _modn = os.path.split(_mod)
    _modn = os.path.splitext(_modn)[0]
    _libp = _mod.split('/')[0]
    _mpath = os.path.join(
        '%s_test' % _libp,
        _mpath[len(_libp) + 1:]
        )
    _tp = os.path.normpath(
        os.path.join(
            DEFAULT_TESTS_PATH, '.', _mpath, '%s_test.py' % _modn
            )
        )
    return _tp


def _try_start_test(module):
    """try start test method
    """
    _tp = get_test_module_filename(module)
    _re = not os.path.exists(_tp)
    return _re


def make_test_file():
    """make test file method
    """
    _mod = sys.argv[1]
    print_message(u'Doing test module for: %s' % _mod)
    
    # if exist a test module file dont do anything
    if _try_start_test(_mod) is False:
        print_message(u'Test for %s already exist.' % _mod)
        sys.exit(0)

    # ----
    # import module
    # ----
    _mpath, _modn = os.path.split(_mod)
    _modn = os.path.splitext(_modn)[0]
    sys.path.insert(0, _mpath)
    try:
        _mo = importlib.import_module(_modn)
    except ValueError:
        # relative import in non-package
        _mo = importlib.import_module('.%s' % _modn, _mpath.replace('/', '.'))
    _mopy = inspect.getsourcefile(_mo)

    # ----
    # find method and classes
    # if methods name start with '_' don't use
    # ----
    _ml, _cl = [], []
    for _e0 in dir(_mo):
        _atr = getattr(_mo, _e0)
        if callable(_atr) and isinstance(_atr, type):
            if _e0 not in SKIP_CLASSES:
                # remove classes that are in other file
                if inspect.getsourcefile(_atr) == _mopy:
                    _cl.append(_atr)
            
        else:
            if (_e0[0] != '_') and ('.' not in _e0):
                if _e0 not in SKIP_CLASSES:
                    _ml.append(_atr)

    print 'found: %i classes, %i methods.' % (
        len(_cl), len(_ml)
        )

    _re = get_test_source(
        _modn, _mpath, _mo,
        _ml, _cl
        )

    _re = save_test_file(_mod, _re)
    sys.exit(_re)


def save_test_file(path, source):
    """save test file method

    save test source to folder ./test/unit/%path%
    if exist don't do
    """
    _mod = path

    # if exist a test module file dont do anything
    if _try_start_test(_mod) is False:
        print_message(u'Test for %s already exist.' % _mod)
        sys.exit(0)

    _tp = get_test_module_filename(_mod)

    try:
        _fi = codecs.open(_tp, 'w')
        _modc = _fi.write(source)
        _fi.close()
        _re = True
    except IOError as _err:
        print _err
        _re = False
    except:
        _re = False
    return _re


def get_imports_string(filename, path):
    """get imports string method
    """
    _fn = filename
    def _do_import_string(module, alias=None, from_=None):
        """do import string method
        """
        _re = ['import %s' % module]
        if alias is not None:
            _re.append('as %s' % (alias))
        if from_ is not None:
            _re.insert(0, 'from %s' % (from_))
        return ' '.join(_re)
        
    _re = [
        _do_import_string('unittest2', alias='unittest'),
        ]
    
    if _fn in ('__init__', ):
        _re.extend([
            _do_import_string(path, alias='_mo'),
            ])        
    else:
        _re.extend([
            _do_import_string(filename, alias='_mo', from_=path),
            ])
    _re = ['%s' % _e0 for _e0 in _re]
    return '%s\n\n' % '\n'.join(_re)


def get_test_class(filename):
    """get test class method
    """
    _re = [
        """class test_%s(unittest.TestCase):\n""" % filename,
        # setup
        '''    def setUp(self):
        """setup method tests
        """
        # data to test
        self._d0 = (
            # method_method
            (0, 1, 2, 3,),
            )

        # test results
        self._r0 = (
            # method_method
            (0, 1, 2, 3,),
            )\n''',
        ]
    return '\n'.join(_re)


def get_test_source(filename, path, module, methods, classes):
    """get test source method
    """
    _fn, _mo, _ml, _cl = filename, module, methods, classes

    def _source_head():
        # ----
        # make test header with imports
        # ----
        _mi = path.replace('/', '.')
        _re = [
            # __doc__
            '''"""%s\n"""\n''' % (
                '%s - %s test module.' % (
                    _mi, _fn
                    )
                ),
            
            # imports
            get_imports_string(_fn, _mi),

            # test class
            get_test_class(_fn),
            ]
        return '\n'.join(_re)

    def _source_body():
        # ----
        # make test methods
        # ----
        _tm = []
        for _e0 in _ml:
            _tm.append(get_test_method(_e0, 1))

        # ----
        # make classes test
        # ----
        for _e0 in _cl:
            _tm.append(get_test_method(_e0, 1))

        return '\n'.join(_tm)

    def _source_foot():
        # ----
        # make test header with imports
        # ----
        _re = '''
if __name__=='__main__':
    unittest.main()\n'''
        return _re

    _re = [
        _source_head(), _source_body(), _source_foot()
        ]
    return '\n'.join(_re)


if __name__=='__main__':
    make_test_file()

