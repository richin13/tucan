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
module = __import__("sendspace.anonymous_download", None, None, [''])

import core.cons as cons

CONF_PATH = "../default_plugins/sendspace"

TEST_INVALID_LINK = "http://www.sendspace.com/file/000000"
TEST_LINK = "http://www.sendspace.com/file/hbgjaf"
TEST_SIZE = 114
TEST_UNIT = "KB"

class TestAnonymous(base_tests.TestBaseDownload):
	""""""
	def setUp(self):
		""""""
		config = ServiceConfig(os.path.join(os.path.dirname(sys.argv[0]), CONF_PATH))
		self.plugin = module.AnonymousDownload(config, SECTION_ANONYMOUS_DOWNLOAD)
		self.invalid_link = TEST_INVALID_LINK
		self.link = TEST_LINK
		self.size = TEST_SIZE
		self.unit = TEST_UNIT

	def tearDown(self):
		""""""
		del self.plugin
