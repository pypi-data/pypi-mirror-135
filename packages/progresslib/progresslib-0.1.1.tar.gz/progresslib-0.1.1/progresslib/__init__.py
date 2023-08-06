# Copyright (C) 2018  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.


import os


def terminal_connected():
    """Check if stdin, stdout and stderr are connected to a terminal"""
    try:
        os.ttyname(0)
        os.ttyname(1)
        os.ttyname(2)
    except OSError:
        return False
    return True


def has_x():
    """Screen is connected"""
    return 'DISPLAY' in os.environ


def dummy_decorator(func):
    return func


if has_x():
    from .gtk import Progress, Pulsate      # noqa: F401
elif terminal_connected():
    from .cli import Progress, Pulsate      # noqa: F401
else:
    Progress = Pulsate = dummy_decorator
