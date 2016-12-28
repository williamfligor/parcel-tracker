#!/usr/bin/python
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

"""Code to add AppIndicator."""

from gi.repository import Gtk  # pylint: disable=E0611
from gi.repository import AppIndicator3  # pylint: disable=E0611

from parcel_tracker_lib.helpers import get_media_file

import locale
from locale import gettext as _
locale.textdomain('parcel-tracker')


class Indicator:
    def __init__(self, window):
        self.indicator = AppIndicator3.Indicator.new('parcel-tracker', 'parcel-tracker-normal', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.indicator.set_attention_icon("parcel-tracker-new")

        self.menu = Gtk.Menu()

        # Add items to Menu and connect signals.

        self.mainwindow = Gtk.MenuItem(_("Show main window"))
        self.mainwindow.connect("activate", lambda x: window.show())
        self.mainwindow.show()
        self.menu.append(self.mainwindow)

        #Adding preferences button
        #window represents the main Window object of your app
        self.preferences = Gtk.MenuItem(_("Preferences"))
        self.preferences.connect("activate", window.on_mnu_preferences_activate)
        self.preferences.show()
        self.menu.append(self.preferences)

        self.quit = Gtk.MenuItem(_("Quit"))
        self.quit.connect("activate", window.on_mnu_close_activate)
        self.quit.show()
        self.menu.append(self.quit)

        # Add more items here

        self.menu.show()
        self.indicator.set_menu(self.menu)

    def setNewMessages(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)

    def unsetNewMessages(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)


def new_application_indicator(window):
    ind = Indicator(window)
    return ind
