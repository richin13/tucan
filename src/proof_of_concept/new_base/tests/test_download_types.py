###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
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

import unittest

from core.download_types import Link

LINK = "http://megaupload.com/?d=9CE8MEPF"
SERVICE = "megaupload.com"

class TestLink(unittest.TestCase):
	def setUp(self):
		self.link = Link(LINK, SERVICE)

	def test_active(self):
		self.assertFalse(self.link.get_active(), "should be inactive by default")

	def test_set_active(self):
		self.link.set_active()
		self.assertTrue(self.link.get_active(), "should be active")

	def test_url(self):
		self.assertTrue(self.link.get_url(), "url should not be empty")

	def test_name(self):
		self.assertEqual(self.link.get_name(), self.link.get_url(), "name and url should be equal")

	def test_service(self):
		self.assertTrue(self.link.get_service(), "service should not be empty")

	def tearDown(self):
		del self.link
