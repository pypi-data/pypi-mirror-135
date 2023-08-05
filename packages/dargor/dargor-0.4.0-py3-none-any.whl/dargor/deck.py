#! /usr/bin/env python3
#
# Copyright (c) 2020, Gabriel Linder <linder.gabriel@gmail.com>
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

from collections import deque
from contextlib import suppress
from itertools import islice


class deck(deque):

    def __getitem__(self, val):

        if type(val) is slice:

            with suppress(TypeError):
                if val.start < 0:
                    start = max(val.start + len(self), 0)
                    val = slice(start, val.stop, val.step)
            assert val.start is None or val.start >= 0, val.start

            with suppress(TypeError):
                if val.stop < 0:
                    stop = max(val.stop + len(self), 0)
                    val = slice(val.start, stop, val.step)
            assert val.stop is None or val.stop >= 0, val.stop

            return list(islice(self, val.start, val.stop, val.step))

        return super().__getitem__(val)


if __name__ == '__main__':

    def sample(population):
        import random as rn
        rn.seed(42)
        return rn.sample(population, 13)

    l = list(range(30))
    h = deck(list(range(30)))

    assert l[10] == h[10]
    assert l[-10] == h[-10]

    assert l[10:] == h[10:]
    assert l[-10:] == h[-10:]

    assert l[:10] == h[:10]
    assert l[:-10] == h[:-10]

    assert l[1:10] == h[1:10]
    assert l[-1:10] == h[-1:10]
    assert l[1:-10] == h[1:-10]

    assert l[100:] == h[100:]
    assert l[-100:] == h[-100:]

    assert l[:100] == h[:100]
    assert l[:-100] == h[:-100]

    assert sample(l) == sample(h)
