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

"""
`atimer` library implements asynchronous timer Python coroutine based on
POSIX timers. The coroutine can be used with Python `asyncio
<https://docs.python.org/3/library/asyncio.html>`_ module API.

The main features are

- timer expires at regular intervals
- track number of expirations if a long running task causes overrun
- start synchronized with system clock at the edge of an interval
- measure time while system is suspended
"""

import pkg_resources

from .glue import Timer

__version__ = pkg_resources.get_distribution('atimer').version

__all__ = ['Timer']

# vim: sw=4:et:ai
