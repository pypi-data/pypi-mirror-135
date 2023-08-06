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
import sys
from contextlib import contextmanager
import time
import threading
from itertools import cycle, chain
import colorama
import shutil


if os.name == 'nt':
    import win_unicode_console
    win_unicode_console.enable()


@contextmanager
def nocursor():
    if os.name == 'posix':
        try:
            sys.stdout.write('\033[?25l')   # hide cursor
            yield
        finally:
            sys.stdout.write('\033[?25h')   # show cursor

    if os.name == 'nt':
        # import msvcrt
        import ctypes
        from ctypes import windll

        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

        ci = _CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))

        try:
            ci.visible = False
            windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
            yield
        finally:
            ci.visible = True
            windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


class _CliBase:
    cols, lines = shutil.get_terminal_size()
    fractions = ' ▏▎▍▌▋▊▉'
    empty = ' '
    full = '█'

    def __init__(self, func):
        self.func = func

    def _c_k(self):
        sys.stdout.write('\033[K')  # clear to the end of the line

    def _print(self, *args, **kwargs):
        print(*args, **kwargs, end='\r')


class Pulsate(_CliBase):
    delay = 0.1/_CliBase.cols
    width = 8

    def __call__(self, *args, **kwargs):
        t = threading.Thread(target=self.func, args=args, kwargs=kwargs,
                             daemon=True)
        t.start()
        with nocursor():
            forward_steps = list(self._go_forwards())

            for line in cycle(chain(
                    forward_steps,
                    reversed(forward_steps),
            )):
                if not t.isAlive():
                    break
                time.sleep(self.delay)
                self._c_k()
                self._print(line)

            self._c_k()

    def _go_forwards(self):
        for i in range(self.cols - self.width):
            for f in self.fractions:
                yield ''.join((
                    i*self.empty,
                    colorama.Back.WHITE,
                    colorama.Fore.BLACK,
                    f,
                    # (self.width - 1)*self.empty,
                    colorama.Back.BLACK,
                    colorama.Fore.WHITE,
                    (self.width - 1)*self.full,
                    f,
                    colorama.Style.NORMAL,
                    colorama.Back.RESET,
                    colorama.Fore.RESET,
                ))


class Progress(_CliBase):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        with nocursor():
            for i in self.func(*args, **kwargs):
                length = i*self.cols
                fulls = int(length)
                fraction_idx = int((length % 1)*8)

                self._c_k()
                self._print(self.full*fulls + self.fractions[fraction_idx])

            self._c_k()


@Pulsate
def pulsate(message):
    import time
    time.sleep(5)


@Progress
def progress(message):
    import time
    import numpy as np

    duration = 3
    ps = 100
    cycles = duration
    space = 0.5 + 0.5*np.sin(np.linspace(0, 2*np.pi*cycles, num=ps*duration))
    delay = 1/ps

    for i in space:
        time.sleep(delay)
        # print("%f: %s" % (i, message))
        yield i


if __name__ == '__main__':
    pulsate('asdf')
    # progress('asdf')
