#
# Copyright (c) 2022, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import curses
import locale
from contextlib import suppress

from .DelayedKeyboardInterrupt import DelayedKeyboardInterrupt


class Curses:

    # https://docs.python.org/3/library/curses.html

    def __enter__(self):

        locale.setlocale(locale.LC_ALL, '')
        current_locale = locale.getpreferredencoding()
        assert current_locale == 'UTF-8', current_locale

        with DelayedKeyboardInterrupt():

            self.stdscr = curses.initscr()
            curses.start_color()
            if curses.has_colors():
                curses.use_default_colors()
                for i in range(0, curses.COLORS):
                    curses.init_pair(i, i, -1)
                curses.COLOR_BLACK = 8
            else:
                curses.COLORS = 1

            curses.meta(1)
            curses.noecho()
            curses.cbreak()
            with suppress(Exception):
                curses.curs_set(0)

            self.stdscr.keypad(1)
            self.stdscr.leaveok(1)
            self.stdscr.scrollok(0)

            self.stdscr.clear()
            return self.stdscr

    def __exit__(self, exc_type, exc_value, _exc_traceback):

        if exc_type is not None:
            with suppress(Exception):
                self.show_error(exc_value)

        with DelayedKeyboardInterrupt():

            self.stdscr.scrollok(1)
            self.stdscr.leaveok(0)
            self.stdscr.keypad(0)

            with suppress(Exception):
                curses.curs_set(1)
            curses.nocbreak()
            curses.echo()
            curses.meta(0)

            curses.endwin()

    def show_error(self, e):

        y, x = self.stdscr.getmaxyx()
        if e.args:
            msg = e.args[0]
            try:
                msg = msg[:msg.index('\n')]
            except ValueError:
                pass
            m = f' {e.__class__.__name__}: {msg} '
        else:
            m = f' {e.__class__.__name__} '
        n = len(m)

        y = y // 2
        x = (x - n) // 2
        a = curses.A_BOLD | \
            curses.A_REVERSE | \
            curses.color_pair({
                False: curses.COLOR_RED,
                True: curses.COLOR_GREEN,
            }[e.__class__.__name__ == 'Done'])

        self.stdscr.addstr(y - 1, x, ' ' * n, a)
        self.stdscr.addstr(y, x, m, a | curses.A_BLINK)
        self.stdscr.addstr(y + 1, x, ' ' * n, a)

        self.stdscr.refresh()
        curses.flash()
        curses.flushinp()
        self.stdscr.getkey()
