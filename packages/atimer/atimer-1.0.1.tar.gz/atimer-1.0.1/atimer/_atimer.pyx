#
# atimer - timer library for asyncio
#
# Copyright (C) 2016-2021 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# cython: language_level=3str
#

import time

from posix.unistd cimport close
from posix.time cimport itimerspec, timespec, clock_gettime
from libc.time cimport time_t

NANOSEC = int(1e9)

cdef extern from "<sys/timerfd.h>":
    enum: CLOCK_BOOTTIME
    enum: TFD_TIMER_ABSTIME
    enum: TFD_NONBLOCK

    int timerfd_create(int, int)
    int timerfd_settime(int, int, itimerspec*, itimerspec*)
    int timerfd_gettime(int, itimerspec*)

def atimer_init():
    # CLOCK_BOOTIME: count number of expirations when running machine is
    # suspended
    # TFD_NONBLOCK: do not block on file descriptor, so in case of some
    # error, we do not block in event loop callback
    return timerfd_create(CLOCK_BOOTTIME, TFD_NONBLOCK)

def atimer_start(int fd, double interval):
    cdef itimerspec ts
    cdef timespec now
    cdef time_t sec, d_sec
    cdef long nsec, d_nsec

    sec, nsec = to_timespec(interval)

    # sync monotonic clock to the edge of realtime clock, then use
    # TFD_TIMER_ABSTIME to achieve first expiration at synchronized time
    clock_gettime(CLOCK_BOOTTIME, &now)
    d_sec, d_nsec = to_timespec(-time.time() % interval)
    ts.it_value = timespec_add(now, d_sec, d_nsec)

    ts.it_interval.tv_sec = sec
    ts.it_interval.tv_nsec = nsec

    return timerfd_settime(fd, TFD_TIMER_ABSTIME, &ts, NULL)

def atimer_close(int fd):
    cdef int r
    cdef itimerspec ts

    ts.it_value.tv_sec = 0
    ts.it_value.tv_nsec = 0
    ts.it_interval.tv_sec = 0
    ts.it_interval.tv_nsec = 0

    r = timerfd_settime(fd, 0, &ts, NULL)
    close(fd)

    return r

def to_timespec(double value):
    """
    Convert float number to `timespec` value.

    Tuple is returned

    - number of seconds
    - number of nanoseconds
    """
    cdef time_t sec
    cdef long nsec

    sec = <int> value

    assert sec <= value
    nsec = (value - sec) * NANOSEC

    return sec, nsec

def timespec_add(timespec now, time_t sec, long nsec):
    now.tv_sec += sec + (now.tv_nsec + nsec) / NANOSEC
    now.tv_nsec = (now.tv_nsec + nsec) % NANOSEC
    return now

# vim: sw=4:et:ai
