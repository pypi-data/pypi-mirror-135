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

from abc import ABC
from contextlib import suppress

import geoip2.database as db

CITY_DB = '/usr/share/GeoIP/GeoLite2-City.mmdb'
COUNTRY_DB = '/usr/share/GeoIP/GeoLite2-Country.mmdb'


class _GeoIP(ABC):

    def __init__(self, what, locale):

        if what == 'city':
            self.reader = db.Reader(CITY_DB).city
        elif what == 'country':
            self.reader = db.Reader(COUNTRY_DB).country
        else:
            raise ValueError

        self.locale = locale or 'en'

    def resolve(self, addr):

        def safe_get(what):

            with suppress(Exception):
                return getattr(geo, what).names[self.locale]

        geo = self.reader(addr)

        return {
            'continent': safe_get('continent'),
            'country': safe_get('country'),
            'city': safe_get('city'),
        }


class City(_GeoIP):

    def __init__(self, locale=None):
        super().__init__('city', locale)


class Country(_GeoIP):

    def __init__(self, locale=None):
        super().__init__('country', locale)
