"""
    __author__ = 'Satoshi Imai'
    __credits__ = ['Satoshi Imai']
    __version__ = '0.9.1'
"""

import json
from datetime import date, datetime
from decimal import Decimal


class CustomJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling specific data types.

    Args:
        json (_type_): _description_
    """

    def default(self, o):
        """Custom method for serializing objects.

        Args:
            o (Any): The object to serialize.

        Returns:
            Any: The serialized object.
        """

        if isinstance(o, Decimal):
            if o == o.to_integral_value():
                return int(o)
            else:
                return float(o)
            # end if
        elif isinstance(o, datetime):
            return o.isoformat(sep='T', timespec='seconds')
        elif isinstance(o, date):
            return o.isoformat()
            # end if

        return super().default(o)
        # end def
