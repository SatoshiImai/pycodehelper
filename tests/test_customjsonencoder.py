"""
    __author__ = 'Satoshi Imai'
    __credits__ = ['Satoshi Imai']
    __version__ = '0.9.1'
"""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest
from dateutil import tz

from src.pycodehelper.json import CustomJsonEncoder


@pytest.mark.run(order=500)
def test_CustomJsonEncoder():
    jst = tz.gettz('Asia/Tokyo')

    test_json = {
        'str': 'simple',
        'int': 1,
        'float': 1.1,
        'Decimal_1': Decimal(1.1),
        'Decimal_2': Decimal(2),
        'datetime_1': datetime(2022, 5, 3),
        'datetime_2': datetime(2022, 5, 3, tzinfo=jst),
        'date_1': datetime(2022, 5, 3).date(),
        'date_2': datetime(2022, 5, 3, tzinfo=jst).date(),
    }
    expected = '{"str": "simple", "int": 1, "float": 1.1, "Decimal_1": 1.1, "Decimal_2": 2, "datetime_1": "2022-05-03T00:00:00", "datetime_2": "2022-05-03T00:00:00+09:00", "date_1": "2022-05-03", "date_2": "2022-05-03"}'
    dumped = json.dumps(test_json, cls=CustomJsonEncoder)

    assert expected == dumped
    # end def


@pytest.mark.run(order=510)
def test_CustomJsonEncoder_exception():

    test_json = {'tempdir': Path('/tmp')}

    with pytest.raises(TypeError):
        json.dumps(test_json, cls=CustomJsonEncoder)
        # end with
    # end def
