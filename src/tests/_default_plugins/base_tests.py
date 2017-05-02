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

import time
import os.path
import unittest
import ConfigParser

import __builtin__
from core.events import Events

from core.base_types import Link
from core.url_open import set_proxy
set_proxy(None)
#set_proxy("proxy.alu.uma.es", 3128)

import core.cons as cons
import core.shared as shared

shared.events = Events()

ACCOUNTS_FILE = "test.accounts"

OPTION_NAME = "name"
OPTION_PASSWORD = "password"

TEST_DIR = "/tmp/"
TEST_NAME = "prueba.bin"
FILE_DIR = "_default_plugins"

TIMEOUT = 500

class TestBaseUpload(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.plugin = None

	def test_check_files(self):
		""""""
		error_path = ""
		correct_path = os.path.join(FILE_DIR, TEST_NAME)
		result = self.plugin.check_files([error_path, correct_path])
		self.assertFalse(result[0], "%s: valid file!" % error_path)
		self.assertTrue(result[1], "%s: invalid file!" % correct_path)
		self.plugin.max_size = 1024
		result = self.plugin.check_files([correct_path])
		self.assertFalse(result[0], "%s: file too big!" % correct_path)

	def test_upload(self):
		""""""
		path = os.path.join(FILE_DIR, TEST_NAME)
		#path = "/home/crak/tmp_deb/tucan_0.3.10.orig.tar.gz"
		link = Link(None, path, None)
		link.set_callback(lambda x, y=None, z=None: x)
		link.set_total_size(os.stat(path).st_size)
		th = self.plugin.process(link)
		if th:
			#th.limit_speed(24*1024)
			th.start()
			while th.isAlive():
				#print link.get_speed()
				time.sleep(1)
			#print link.status, link.get_progress(), link.get_time(), link.get_name()
		self.assertEqual(link.status, cons.STATUS_CORRECT, "s%: Error uploading")

class TestBaseDownload(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.plugin = None
		self.invalid_link = None
		self.link = None
		self.size = None
		self.unit = None

	def check_link(self, link, name, size, unit):
		""""""
		n, s, u = self.plugin.check_links(link)
		self.assertEqual(n, name, "%s != %s" % (n, name))
		self.assertEqual(s, size, "%s != %i" % (s, size))
		self.assertEqual(u, unit, "%s != %s" % (u, unit))
		
	def test_check_invalid_link(self):
		""""""
		self.check_link(self.invalid_link, None, -1, None)

	def test_check_valid_link(self):
		""""""
		self.check_link(self.link, TEST_NAME, self.size, self.unit)

	def test_download(self):
		""""""
		self.check_link(self.link, TEST_NAME, self.size, self.unit)
		self.assertTrue(self.plugin.add(TEST_DIR, self.link, TEST_NAME), "check slots or limits")
		status = cons.STATUS_WAIT
		start_time = time.time()
		while ((status != cons.STATUS_ERROR) and (status != cons.STATUS_CORRECT)):
			status, progress, actual_size, unit, speed, time_ = self.plugin.get_status(TEST_NAME)
			self.assertTrue(start_time + TIMEOUT > time.time(), "Force timeout")
			time.sleep(1)
		self.assertEqual(status, cons.STATUS_CORRECT, "s%: Error downloading")
		name = "%s%s" % (TEST_DIR, TEST_NAME)
		self.assertTrue(os.path.exists(name), "Not Found: %s" % name)
		f1 = file(os.path.join(FILE_DIR, TEST_NAME), "r")
		f2 = file(name, "r")
		local = f1.read()
		remote = f2.read()
		f1.close()
		f2.close()
		os.remove(name)
		self.assertEqual(local, remote, "%i != %i" % (len(local), len(remote)))

class TestBaseCookie(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.cookie = None
		self.service_name = ""

	def get_mocked_config(self, config):
		""""""
		account_name, account_password = self.get_account_data()
		if account_name and account_password:
			config.get_accounts = lambda x: {account_name: (account_password, True, True)}
		return config
	
	def get_account_data(self):
		"""
		ACCOUNTS_FILE should be populated like this:
		
		[service_name]
		name = something
		password = something_else
		
		"""
		account_name = ""
		account_password = ""
		
		name = os.path.join(FILE_DIR, ACCOUNTS_FILE)
		self.assertTrue(os.path.exists(name), "Not Found: %s" % name)
		
		config = ConfigParser.SafeConfigParser()
		
		try:
			config.read(name)
			account_name = config.get(self.service_name, OPTION_NAME, raw=True)
			account_password = config.get(self.service_name, OPTION_PASSWORD, raw=True)
		except Exception, e:
			self.fail(e)
		else:
			self.assertTrue(account_name, "Name shouldn't be empty")
			self.assertTrue(account_password, "Password shouldn't be empty")
		return account_name, account_password

	def test_invalid_cookie(self):
		""""""
		self.assertFalse(self.cookie.get_cookie(None, None), "Cookie should be None")

	def test_valid_cookie(self):
		""""""
		account_name, account_password = self.get_account_data()
		self.assertTrue(self.cookie.get_cookie(account_name, account_password), "Cookie shouldn't be None")
