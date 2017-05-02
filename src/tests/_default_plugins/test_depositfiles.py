###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
##
## This program is free software; you can redistribute it and/or modify
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

import sys
import os.path
import base_tests

from core.service_config import ServiceConfig, SECTION_ANONYMOUS_DOWNLOAD
from depositfiles.anonymous_download import AnonymousDownload
from ui.gtk.captcha_dialog import CaptchaDialog

import core.cons as cons
import core.shared as shared

CONF_PATH = "../default_plugins/depositfiles"

SERVICE_NAME = "depositfiles"

TEST_INVALID_LINK = "http://depositfiles.com/en/files/19ixor0a"
TEST_LINK = "http://depositfiles.com/en/files/97lt4vvv2"
TEST_SIZE = 114
TEST_UNIT = "KB"

class TestAnonymous(base_tests.TestBaseDownload):
	""""""
	def setUp(self):
		""""""
		self.id = shared.events.connect(cons.EVENT_CAPTCHA_DIALOG, CaptchaDialog)
		config = ServiceConfig(os.path.join(os.path.dirname(sys.argv[0]), CONF_PATH))
		self.plugin = AnonymousDownload(config, SECTION_ANONYMOUS_DOWNLOAD)
		self.invalid_link = TEST_INVALID_LINK
		self.link = TEST_LINK
		self.size = TEST_SIZE
		self.unit = TEST_UNIT

	def tearDown(self):
		""""""
		shared.events.disconnect(cons.EVENT_CAPTCHA_DIALOG, self.id)
		del self.plugin
