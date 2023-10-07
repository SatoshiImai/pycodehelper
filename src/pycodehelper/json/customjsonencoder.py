# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '0.9.0'
# ---------------------------------------------------------------------------

import json
from datetime import date, datetime
from decimal import Decimal


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
                # end if
        elif isinstance(o, (datetime, date)):
            return o.isoformat(sep='T', timespec='seconds')
            # end if
        return super(CustomJsonEncoder, self).default(o)
        # end def

    # end class
