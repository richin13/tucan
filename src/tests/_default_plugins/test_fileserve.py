###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
##                         Ali Shah    ahshah@airpost.net
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

from core.service_config import ServiceConfig, SECTION_ANONYMOUS_DOWNLOAD, SECTION_PREMIUM_DOWNLOAD
from fileserve.anonymous_download import AnonymousDownload
from fileserve.premium_cookie import PremiumCookie
from fileserve.premium_download import PremiumDownload
from ui.gtk.captcha_dialog import CaptchaDialog

import core.cons as cons
import core.shared as shared

CONF_PATH = "../default_plugins/fileserve"

SERVICE_NAME = "fileserve"

TEST_INVALID_LINK = "http://www.fileserve.com/file/ywuKrv"
TEST_LINK = "http://www.fileserve.com/file/ywuKrvz"
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

class TestPremium(base_tests.TestBaseCookie, base_tests.TestBaseDownload):
	""""""
	def setUp(self):
		""""""
		self.cookie = PremiumCookie()
		self.service_name = SERVICE_NAME
		
		config = ServiceConfig(os.path.join(os.path.dirname(sys.argv[0]), CONF_PATH))
		self.plugin = PremiumDownload(self.get_mocked_config(config), SECTION_PREMIUM_DOWNLOAD)
		self.invalid_link = TEST_INVALID_LINK
		self.link = TEST_LINK
		self.size = TEST_SIZE
		self.unit = TEST_UNIT

	def tearDown(self):
		""""""
		del self.cookie
