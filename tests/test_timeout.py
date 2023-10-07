# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '0.9.0'
# ---------------------------------------------------------------------------

import logging
import time

import pytest

from src.pycodehelper.context import timeout


@pytest.fixture(scope='module')
def logger() -> logging.Logger:
    log = logging.getLogger('test.timeout')

    yield log
    # end def


def test_non_timeout(logger):
    test_value = 0
    with timeout(100):
        logger.info('timeout block start')
        test_value = 100
        logger.info('timeout block end')
        # end with

    assert test_value == 100
    # end def


def test_timeoutAsException(logger):
    with pytest.raises(TimeoutError):
        test_value = 0
        with timeout(5):
            logger.info('timeout block start')
            time.sleep(10)
            # end with
        # end with
    assert test_value == 0
    # end def
