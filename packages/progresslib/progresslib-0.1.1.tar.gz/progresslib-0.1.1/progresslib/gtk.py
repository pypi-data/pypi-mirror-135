# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
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

import threading
import warnings
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk     # noqa: E402


warnings.filterwarnings('ignore')


class ProgressBarWindow(Gtk.Window):
    """Just a window with a progressbar.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Loading…")

        self.set_border_width(10)
        self.set_resizable(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)
        # self.progressbar.pulse()

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

        self.connect("delete-event", Gtk.main_quit)
        self.connect("show", self.set_center)
        self.connect('key_press_event', self.on_key_press_event)

    def main(self):
        """Start the main GUI loop.
        """
        self.show_all()
        Gtk.main()

    def __call__(self):
        self.main()

    def set_center(self, widget):
        """Move the window to the center of a screen.
        """
        self.set_gravity(Gdk.Gravity.CENTER)
        res = complex(Gdk.Screen.width(), Gdk.Screen.height())
        size = complex(*self.get_size())
        p = (res - size)/2
        self.move(p.real, p.imag)

    def on_key_press_event(self, widget, event):
        if event.keyval in (65307, 65293):    # Escape, Enter
            self.close()

    def on_timeout(self):
        pass


class Pulsate(ProgressBarWindow):
    def __init__(self, func):
        super(Pulsate, self).__init__()
        self.func = func

    def __call__(self, *args, **kwargs):
        t = threading.Thread(name="progressbar", target=self.main, daemon=True)
        t.start()
        self.func(*args, **kwargs)

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        self.progressbar.pulse()
        return True


class Progress(ProgressBarWindow):
    def __init__(self, func):
        super(Progress, self).__init__()
        self.func = func

    def __call__(self, *args, **kwargs):
        t = threading.Thread(name="progressbar", target=self.main, daemon=True)
        t.start()
        for i in self.func(*args, **kwargs):
            self.progressbar.set_fraction(i)

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        return False


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


if __name__ == "__main__":
    # pulsate(1, "message")
    progress("message")
