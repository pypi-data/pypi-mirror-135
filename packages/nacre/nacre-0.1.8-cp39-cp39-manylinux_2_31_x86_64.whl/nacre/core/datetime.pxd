from cpython.datetime cimport datetime
from cpython.datetime cimport timedelta
from libc.stdint cimport int64_t


cpdef int64_t dt_to_unix_millis(datetime dt) except *
