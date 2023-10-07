# pycodehelper

Simple code snippets for Python project.

## CommonCompression

CommonCompression supports [bz2, gzip, zip]. It is a simple wrapper snippet.

```python
import tempfile
from pathlib import Path

from pycodehelper.compression import CommonCompression

tempdir = Path(tempfile.mkdtemp())

compression = 'bz2'

raw_source = tempdir.joinpath('compression_test.csv')
comp_source = tempdir.joinpath('compression_test.csv.bz2')

compressor = CommonCompression()
compressor.compress('bz2', raw_source, comp_source)
```

## CustomJsonEncoder

```python
import json
from datetime import datetime
from decimal import Decimal

from pycodehelper.json import CustomJsonEncoder

jst = tz.gettz('Asia/Tokyo')

test_json = {
    'str': 'simple',
    'int': 1,
    'float': 1.1,
    'Decimal_1': Decimal(1.1),
    'Decimal_2': Decimal(2),
    'datetime_1': datetime(2022, 5, 3),
    'datetime_2': datetime(2022, 5, 3, tzinfo=jst)
}

json.dumps(test_json, cls=CustomJsonEncoder)
```

## timeout

```python
import time

from pycodehelper.context import timeout

test_value = 0

with timeout(5):
    logger.info('timeout block start')
    time.sleep(10)
    test_value = 100
```
