import pandas as pd
import pytz

from cpython.datetime cimport datetime
from cpython.datetime cimport datetime_tzinfo
from cpython.datetime cimport timedelta
from cpython.unicode cimport PyUnicode_Contains
from libc.stdint cimport int64_t
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.math cimport lround


# UNIX epoch is the UTC time at 00:00:00 on 1/1/1970
# https://en.wikipedia.org/wiki/Unix_time
cdef datetime UNIX_EPOCH = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc)

# Time unit conversion constants
cdef int64_t MILLISECONDS_IN_SECOND = 1_000
cdef int64_t MICROSECONDS_IN_SECOND = 1_000_000
cdef int64_t NANOSECONDS_IN_SECOND = 1_000_000_000
cdef int64_t NANOSECONDS_IN_MILLISECOND = 1_000_000
cdef int64_t NANOSECONDS_IN_MICROSECOND = 1_000
cdef int64_t NANOSECONDS_IN_DAY = 86400 * NANOSECONDS_IN_SECOND

cpdef int64_t dt_to_unix_millis(datetime dt) except *:
    """
    Return the round UNIX timestamp (milliseconds) from the given `datetime`.
    Parameters
    ----------
    dt : datetime
        The datetime to convert.
    Returns
    -------
    int64
    Raises
    ------
    TypeError
        If timestamp is None.
    """
    # If timestamp is None then `-` unsupported operand for `NoneType` and `timedelta`
    return lround((dt - UNIX_EPOCH).total_seconds() * MILLISECONDS_IN_SECOND)
