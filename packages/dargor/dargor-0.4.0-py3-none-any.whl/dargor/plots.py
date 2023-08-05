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

import numpy as np


class CursorLines:

    def __init__(self, fig, *, color='black', ls=':'):
        lineprops = {
            'color': color,
            'ls': ls,
            'visible': False,
            'animated': True,
        }
        self.fig = fig
        self.hlines = {
            ax: ax.axhline(np.nan, **lineprops)
            for ax in fig.axes
        }
        self.vlines = [
            ax.axvline(np.nan, **lineprops)
            for ax in fig.axes
        ]
        self.background = None
        self.background_rotten = True
        # we need to keep these references to avoid garbage collection
        self._on_draw = fig.canvas.mpl_connect('draw_event',
                                               self.on_draw)
        self._on_resize = fig.canvas.mpl_connect('resize_event',
                                                 self.on_resize)
        self._on_motion = fig.canvas.mpl_connect('motion_notify_event',
                                                 self.on_motion)
        # this one is needed if you patch your figure with CursorLines(fig)
        # instead of cl = CursorLines(fig)
        self.fig._CursorLines = self

    def on_draw(self, _ev):
        self.background_rotten = True

    def on_resize(self, _ev):
        self.background_rotten = True

    def on_motion(self, ev):
        canvas = self.fig.canvas

        try:
            canvas.widgetlock(self)
        except ValueError:
            # already locked
            return

        try:
            if self.background_rotten:
                canvas.draw()
                self.background = canvas.copy_from_bbox(canvas.figure.bbox)
                self.background_rotten = False
            else:
                canvas.restore_region(self.background)
            for vline in self.vlines:
                if not ev.inaxes:
                    continue
                ax = vline.axes
                vline.set_xdata((ev.xdata, ev.xdata))
                vline.set_visible(True)
                ax.draw_artist(vline)
                if ev.inaxes != ax:
                    continue
                hline = self.hlines[ax]
                hline.set_ydata((ev.ydata, ev.ydata))
                hline.set_visible(True)
                ax.draw_artist(hline)
            canvas.blit(canvas.figure.bbox)
        finally:
            canvas.widgetlock.release(self)
