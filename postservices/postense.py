#!/usr/bin/env python
# -*- coding: utf-8 -*-

### BEGIN LICENSE
# Copyright © 2012-2016 Vsevolod Velichko <torkvema@gmail.com>
# Copyright © 2012 Carlos da Costa <c.costa@outlook.com>
# Copyright © 2012-2013 Erik Christiansson <erik@christiansson.net>
# Copyright © 2013 Pål Sollie <sollie@sparkz.no>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from . import TrackingService

import re
from dateutil.parser import parse as parsedate

class PostenSeService(TrackingService):
    """Swedish postal service"""

    name = 'Posten.se'
    url = 'http://server.logistik.posten.se/servlet/PacTrack?lang=GB&kolliid=%(number)s'

    def _parse_page(self, html):
        html = html.decode('ISO-8859-1', 'ignore')
        return [(r[3], parsedate('%s %s' % (r[0], r[1])), r[2]) for r in re.findall(r'<event>.*?<date>(.*?)</date>.*?<time>(.*?)</time>.*?<location>(.*?)</location>.*?<description>(.*?)</description>.*?</event>', html, re.DOTALL)]

