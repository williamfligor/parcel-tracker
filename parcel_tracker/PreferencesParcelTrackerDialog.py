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

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.parcel-tracker.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio, Gtk  # pylint: disable=E0611

import locale
from locale import gettext as _
locale.textdomain('parcel-tracker')

import logging
from parcel_tracker_lib import post_services
logger = logging.getLogger('parcel_tracker')

from parcel_tracker_lib.PreferencesDialog import PreferencesDialog


class PreferencesParcelTrackerDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesParcelTrackerDialog"

    def toggle_search(self, widget, unused):
        disabled = set(self.settings.get_strv('disabled-searches'))

        name = widget.get_name()
        if widget.get_active():
            try:
                disabled.remove(name)
            except KeyError:
                pass
        else:
            disabled.add(name)
        self.settings.set_strv('disabled-searches', list(disabled))

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesParcelTrackerDialog, self).finish_initializing(builder)

        update_widget = self.builder.get_object('update_period')
        self.settings.bind("update-period", update_widget, "value", Gio.SettingsBindFlags.DEFAULT)

        grid = self.builder.get_object('searches_grid')
        index = 0

        disabled_searches = self.settings.get_strv('disabled-searches')
        for search, searcher in post_services.get_services().iteritems():
            name = searcher.name

            slabel = Gtk.Label()
            slabel.set_label(name)  # TODO: Change name
            slabel.set_visible(True)
            slabel.set_can_focus(False)
            slabel.set_halign(Gtk.Align.START)
            slabel.set_hexpand(True)
            grid.attach(slabel, 0, index, 1, 1)

            sswitch = Gtk.Switch()
            sswitch.set_visible(True)
            sswitch.set_halign(Gtk.Align.END)
            sswitch.set_can_focus(True)
            sswitch.set_name(search)
            sswitch.set_active(search not in disabled_searches)
            sswitch.connect('notify::active', self.toggle_search)
            # sswitch.use_action_appearance(False)
            grid.attach(sswitch, 1, index, 1, 1)
            index += 1

        # Code for other initialization actions should be added here.
