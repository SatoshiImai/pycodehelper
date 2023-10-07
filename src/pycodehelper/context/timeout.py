# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '0.9.0'
# ---------------------------------------------------------------------------

import signal
from contextlib import contextmanager
from typing import Any


@contextmanager
def timeout(seconds: int):
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(seconds)

    try:
        yield
    except TimeoutError:
        raise TimeoutError(f'Timeout is set to {seconds} second(s).')
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        # end try
    # end def


def raise_timeout(signal_number: Any, stack_frame: Any):
    raise TimeoutError
    # end def
