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

from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse, urlunparse
from cStringIO import StringIO
import os
import Cookie
import socket
import logging
import htmlentitydefs
import re


def unescape(text):
    """Removes HTML or XML character references and entities from a text string."""
    # @param text The HTML (or XML) source text.
    # @return The plain text, as a Unicode string, if necessary.
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def untagify(text):
    inTag = False
    quote = None
    result = StringIO()
    for i in xrange(len(text)):
        char = text[i]
        if inTag:
            if not quote and char in ('"', "'"):
                quote = char
            elif quote and char == quote and text[i - 1] != '\\':
                quote = None
            elif char == '>':
                inTag = False
        elif char == '<':
            inTag = True
        else:
            result.write(char)
    return result.getvalue()


class TrackingService(object):
    url = None
    number = None
    post = None
    post_type = 'application/x-www-form-urlencoded'
    additional_fields = None
    referer = None
    cookie = None
    logger = logging.getLogger('parcel_tracker_lib')
    name = 'Unknown Service'
    service_classes = {}

    class __metaclass__(type):
        def __new__(mcs, name, bases, dict):
            newType = type.__new__(mcs, name, bases, dict)
            if dict.get('__doc__', None):
                assert name not in TrackingService.service_classes, "Service collision: {0} is already defined".format(name)
                TrackingService.service_classes[name] = newType
            return newType

    def _parse_page(self, html):
        '''This method should parse an html string and return
        the list of tuples (operation, date, post_office)'''
        raise NotImplementedError

    def _fetch_url(self, url, data, headers, use_cookies=False):
        purl = urlparse(url)
        qpath = purl.path
        if qpath == '':
            qpath = '/'

        port = 80
        if purl.query:
            qpath += '?' + purl.query

        https = False
        if purl.scheme == 'https':
            port = 443
            https = True
        if purl.port is not None:
            port = purl.port

        conn = None
        try:
            if https:
                conn = HTTPSConnection(host=purl.hostname, port=port, timeout=10)
            else:
                conn = HTTPConnection(host=purl.hostname, port=port, timeout=10)
            _headers = {
                'Host': purl.hostname,
                'User-Agent': 'Mozilla/5.0 (X13; Pupuntu; Lelix x88_44; rv:24.0; compatible; ParcelTracker/1.0) Gecko/20100101 Firefox/24.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us',
                'Connection': 'close'
            }
            if use_cookies and self.cookie is not None:
                _headers.update({'Cookie': self.cookie.output(header='', attrs='', sep=';').strip()})
            _headers.update(headers)
            #self.logger.debug(_headers)
            #self.logger.debug(data)
            method = 'POST' if data is not None else 'GET'
            self.logger.debug("%s %s", method, url)
            conn.request(method, qpath, data, _headers)

            # Get the response
            response = conn.getresponse()
            statuscode, statusmessage = response.status, response.reason
            self.logger.debug("Response (status/message): %s, %s", statuscode, statusmessage)
            #self.logger.debug(response.getheaders())
            try:
                cookie = self.cookie
                if cookie is None:
                    cookie = Cookie.SimpleCookie()
                self.logger.debug("Got cookies: %s" % response.getheader('Set-Cookie'))
                cookie.load(response.getheader('Set-Cookie'))
                self.cookie = cookie
            except AttributeError:
                pass
            if statuscode in (301, 302):
                newLocation = response.getheader('Location')
                parts = newLocation.split('?', 1)
                _headers.update({'Referer': url})
                newUrl = newLocation if not newLocation.startswith('/') else urlunparse((purl.scheme, purl.netloc, parts[0], '', parts[1] if len(parts) > 1 else None, ''))
                return self._fetch_url(newUrl, None, _headers, use_cookies)
            if statuscode != 200:
                #self.logger.debug(resp)
                raise Exception("%s service returned non-200 response: %d" % (self.__class__.__name__, statuscode))
            resp = response.read()
            return resp
        except socket.gaierror, e:
            self.logger.error("Network error: %s" % e)
            raise
        finally:
            if conn is not None:
                conn.close()

    def _get_page(self):
        fields = {'number': self.number}
        if self.additional_fields is not None:
            fields.update(self.additional_fields)

        url = self.url % fields

        data = self.post % fields if self.post is not None else None

        headers = {}
        if self.referer is not None:
            headers['Referer'] = self.referer
        if data is not None:
            headers['Content-Type'] = self.post_type
        return self._fetch_url(url, data, headers, self.cookie is not None)

    def __init__(self, number):
        self.number = number

    def fetch(self):
        try:
            page = self._get_page()
            updates = self._parse_page(page)
            return updates
        except Exception, e:
            self.logger.exception(unicode(e).encode('utf-8', 'ignore'))
            return []


for i in os.walk(__path__[0]):
    if i[0] != __path__[0]:
        continue
    for j in i[2]:
        if j.startswith('__init__') or not j.endswith('.py'):
            continue
        j = j.split('.')[0]
        __import__(j, globals(), locals())
