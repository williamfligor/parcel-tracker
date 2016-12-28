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
import urllib

from dateutil.parser import parse as parsedate


class RoyalmailComService(TrackingService):
    """Brittish Royal Mail service"""

    name = "Royalmail.com"
    url = "http://www.royalmail.com/trackdetails"
    post = 'form_id=bt_tracked_track_trace_form&form_build_id=%(formId)s&tracking_number=%(number)s'

    def __init__(self, number):
        super(RoyalmailComService, self).__init__(number)
        self.additional_fields = {}

    def _get_page(self):
        page = self._fetch_url(self.url, data=None, headers={}, use_cookies=True).decode('utf-8', 'ignore')
        form_build_id = urllib.quote(re.findall(r'name="form_build_id".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')
        self.additional_fields.update({'formId': form_build_id})
        return super(RoyalmailComService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'Your tracked items details.*?<table.*?<tbody>(.*?)</tbody>', html, re.DOTALL | re.IGNORECASE | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)

        results = []
        for (date, time, action, location) in re.findall(r'<tr[^>]*><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>', html, re.UNICODE):
            datetime = parsedate("{0} {1}".format(date, time))
            results.append((action, datetime, location))
        return results

