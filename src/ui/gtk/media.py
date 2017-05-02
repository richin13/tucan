###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it andor modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os.path
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk

from core.cons import PATH

try:
	EXT = ".svg"
	PATH_MEDIA = os.path.join(PATH, "media", "scalable", "")
	gtk.gdk.pixbuf_new_from_file("%stucan%s" % (PATH_MEDIA, EXT))
except Exception, e:
	EXT = ".png"
	PATH_MEDIA = os.path.join(PATH, "media", "")
	logger.debug("Using PNG icons: %s" % e)

ICON_TUCAN = "%stucan%s" % (PATH_MEDIA, EXT)
ICON_DOWNLOAD = "%sdocument-save%s" % (PATH_MEDIA, EXT)
ICON_UPLOAD = "%ssystem-software-update%s" % (PATH_MEDIA, EXT)
ICON_CLEAR = "%sedit-delete%s" % (PATH_MEDIA, EXT)
ICON_DOWN = "%sgo-down%s" % (PATH_MEDIA, EXT)
ICON_UP = "%sgo-up%s" % (PATH_MEDIA, EXT)
ICON_START = "%smedia-playback-start%s" % (PATH_MEDIA, EXT)
ICON_STOP = "%smedia-playback-stop%s" % (PATH_MEDIA, EXT)
ICON_CHECK = "%ssoftware-update-available%s" % (PATH_MEDIA, EXT)
ICON_PACKAGE = "%spackage-x-generic%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES = "%spreferences-system%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_MAIN = "%spreferences-desktop%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_SERVICES = "%scontact-new%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_ADVANCED = "%sapplications-system%s" % (PATH_MEDIA, EXT)
ICON_LANGUAGE = "%spreferences-desktop-locale%s" % (PATH_MEDIA, EXT)
ICON_FOLDER = "%suser-home%s" % (PATH_MEDIA, EXT)
ICON_NETWORK = "%snetwork-error%s" % (PATH_MEDIA, EXT)
ICON_ADVANCED = "%sapplication-x-executable%s" % (PATH_MEDIA, EXT)
ICON_MISSING = "%simage-missing%s" % (PATH_MEDIA, EXT)
ICON_ACCOUNT = "%ssystem-users%s" % (PATH_MEDIA, EXT)
ICON_UPDATE = "%ssoftware-update-urgent%s" % (PATH_MEDIA, EXT)
ICON_SEND = "%smail-reply-sender%s" % (PATH_MEDIA, EXT)
