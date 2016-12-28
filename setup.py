#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
import glob
import shutil

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build parcel-tracker you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'


def update_config(libdir, values={}):
    filename = os.path.join(libdir, 'parcel_tracker_lib/parcel_trackerconfig.py')
    oldvalues = {}
    try:
        fin = file(filename, 'r')
        fout = file(filename + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)
    return oldvalues


def move_desktop_file(root, target_data, prefix):
    # The desktop file is rightly installed into install_data.  But it should
    # always really be installed into prefix, because while we can install
    # normal data files anywhere we want, the desktop file needs to exist in
    # the main system to be found.  Only actually useful for /opt installs.

    old_desktop_path = os.path.normpath(root + target_data +
                                        '/share/applications')
    old_desktop_file = old_desktop_path + '/parcel-tracker.desktop'
    desktop_path = os.path.normpath(root + prefix + '/share/applications')
    desktop_file = desktop_path + '/parcel-tracker.desktop'

    if not os.path.exists(old_desktop_file):
        print ("ERROR: Can't find", old_desktop_file)
        sys.exit(1)
    elif target_data != prefix + '/':
        # This is an /opt install, so rename desktop file to use extras-
        desktop_file = desktop_path + '/extras-parcel-tracker.desktop'
        try:
            os.makedirs(desktop_path)
            os.rename(old_desktop_file, desktop_file)
            os.rmdir(old_desktop_path)
        except OSError as e:
            print ("ERROR: Can't rename", old_desktop_file, ":", e)
            sys.exit(1)

    return desktop_file


def update_desktop_file(filename, target_pkgdata, target_scripts):
    try:
        fin = file(filename, 'r')
        fout = file(filename + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                #line = "Icon=%s\n" % (target_pkgdata + 'media/parcel-tracker.svg')
                line = "Icon=parcel-tracker\n"
            elif 'Exec=' in line:
                cmd = line.split("=")[1].split(None, 1)
                line = "Exec=%s" % (target_scripts + 'parcel-tracker')
                if len(cmd) > 1:
                    line += " %s" % cmd[1].strip()  # Add script arguments back
                line += "\n"
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)


def install_themed_icons(root, target_dir):
    for (path, _, filenames) in os.walk(root):
        basedir = os.path.relpath(path, root)
        destdir = os.path.join(target_dir, basedir)
        for filename in filenames:
            srcfile = os.path.join(path, filename)
            destfile = os.path.join(destdir, filename)
            print "copying {} to {}".format(srcfile, destfile)
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            shutil.copyfile(srcfile, destfile)

    for theme_dir in glob.glob(os.path.join(root, "*")):
        theme = os.path.basename(theme_dir)
        for size_dir in glob.glob(os.path.join(theme_dir, '*')):
            size = os.path.basename(size_dir)
            for category_dir in glob.glob(os.path.join(size_dir, '*')):
                category = os.path.basename(category_dir)
                dest_dir = os.path.join(target_dir, theme, size, category)
                for filename in glob.glob(os.path.join(category_dir, '*')):
                    basename = os.path.basename(filename)
                    target = os.path.join(dest_dir, basename)
                    if os.path.isfile(filename):
                        shutil.copyfile(filename, target)


def compile_schemas(root, target_data):
    if target_data == '/usr/':
        return  # /usr paths don't need this, they will be handled by dpkg
    schemadir = os.path.normpath(root + target_data + 'share/glib-2.0/schemas')
    if (os.path.isdir(schemadir) and
            os.path.isfile('/usr/bin/glib-compile-schemas')):
        os.system('/usr/bin/glib-compile-schemas "%s"' % schemadir)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        DistUtilsExtra.auto.install_auto.run(self)

        target_data = '/' + os.path.relpath(self.install_data, self.root) + '/'
        target_pkgdata = target_data + 'share/parcel-tracker/'
        target_scripts = '/' + os.path.relpath(self.install_scripts, self.root) + '/'

        values = {'__parcel_tracker_data_directory__': "'%s'" % (target_pkgdata),
                  '__version__': "'%s'" % self.distribution.get_version()}
        update_config(self.install_lib, values)

        desktop_file = move_desktop_file(self.root, target_data, self.prefix)
        update_desktop_file(desktop_file, target_pkgdata, target_scripts)
        install_themed_icons(os.path.join('data', 'icon-themes'), os.path.join(self.install_data, 'share', 'icons'))
        compile_schemas(self.root, target_data)

##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='parcel-tracker',
    version='16.12.5',
    license='GPL-3',
    author='Vsevolod Velichko',
    author_email='torkvema@gmail.com',
    description='Parcel tracking application',
    long_description='Application dedicated to help people track their post items that have a tracking number. It fetches information from different network post services and notify user when something new is available. Integration with Ubuntu is included.',
    url='https://launchpad.net/parcel-tracker',
    cmdclass={'install': InstallAndUpdateDataDirectory}
)
