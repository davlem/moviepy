"""
test.unit._core - method module.
"""
import time
import resource


def print_memory_usage():
    """print memory usage method
    """
    print 'Memory usage: %i (kilobytes on Linux).' % (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        )


def count_elapsed_time(method, args, show=None):
    """count elapsed time in method call
    """
    _me = method
    _ar = args
    _sh = show or False
    _sta = time.time()
    _re = _me(*_ar[0], **_ar[1])
    _end = time.time()
    _time = _end - _sta
    if _sh:
        print 'Elapsed time:', _time
    return _re, _time
