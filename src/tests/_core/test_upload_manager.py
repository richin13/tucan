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
import unittest

import core.cons as cons
from core.queue import Queue
from core.upload_manager import UploadManager

PACKAGE = [('/home/user/file.part1.rar', 1024, ['megaupload.anonymous_upload', 'rapidshare.anonymous_upload']), ('/home/user/file.part2.rar', 1024, ['megaupload.anonymous_upload', 'rapidshare.anonymous_upload'])]

class TestUploadManager(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.manager = UploadManager(Queue())
		#disable scheduler
		self.manager.scheduling = True
		self.manager.add_package(PACKAGE)

	def test_start(self):
		""""""
		package = self.manager.queue.get_children()[0]
		file1, file2 = self.manager.queue.get_children(package.id)
		link1, link2 = self.manager.queue.get_children(file1.id)
		link3, link4 = self.manager.queue.get_children(file2.id)
		self.manager.start(file1.id)
		self.manager.start(link3.id)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		self.assertEqual(file1.status, cons.STATUS_ACTIVE)
		self.assertEqual(link1.status, cons.STATUS_ACTIVE)
		self.assertEqual(link2.status, cons.STATUS_ACTIVE)
		self.assertEqual(link3.status, cons.STATUS_ACTIVE)
		time.sleep(1.5)
		self.assertEqual(package.status, cons.STATUS_PEND)
		self.assertEqual(file1.status, cons.STATUS_CORRECT)
		self.assertEqual(link1.status, cons.STATUS_CORRECT)
		self.assertEqual(link2.status, cons.STATUS_CORRECT)
		self.assertEqual(link3.status, cons.STATUS_CORRECT)
		self.manager.start(file2.id)
		time.sleep(1.5)
		self.assertEqual(package.status, cons.STATUS_CORRECT)
		self.assertEqual(file2.status, cons.STATUS_CORRECT)
		self.assertEqual(link4.status, cons.STATUS_CORRECT)
	
	def test_stop(self):
		""""""
		package = self.manager.queue.get_children()[0]
		file1, file2 = self.manager.queue.get_children(package.id)
		link1, link2 = self.manager.queue.get_children(file1.id)
		link3, link4 = self.manager.queue.get_children(file2.id)
		self.manager.start(file1.id)
		self.manager.stop(link1.id)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		self.assertEqual(file1.status, cons.STATUS_ACTIVE)
		self.assertEqual(link1.status, cons.STATUS_STOP)
		self.assertEqual(link2.status, cons.STATUS_ACTIVE)
		time.sleep(1.5)
		self.manager.start(file1.id)
		self.manager.stop(file1.id)
		self.assertEqual(package.status, cons.STATUS_PEND)
		self.assertEqual(file1.status, cons.STATUS_STOP)
		self.assertEqual(link1.status, cons.STATUS_STOP)
		self.assertEqual(link2.status, cons.STATUS_CORRECT)
		time.sleep(1.5)
		self.manager.start(file2.id)
		self.manager.stop(package.id)
		self.assertEqual(package.status, cons.STATUS_STOP)
		self.assertEqual(file1.status, cons.STATUS_STOP)
		self.assertEqual(file2.status, cons.STATUS_STOP)
		self.assertEqual(link1.status, cons.STATUS_STOP)
		self.assertEqual(link2.status, cons.STATUS_CORRECT)
		self.assertEqual(link3.status, cons.STATUS_STOP)
		self.assertEqual(link4.status, cons.STATUS_STOP)
		package.status = cons.STATUS_PEND
		file1.status = cons.STATUS_PEND
		link1.status = cons.STATUS_PEND
		link2.status = cons.STATUS_PEND
		self.manager.start(link1.id)
		self.manager.stop(package.id, package, False)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		self.assertEqual(file1.status, cons.STATUS_ACTIVE)
		self.assertEqual(link1.status, cons.STATUS_ACTIVE)
		self.assertEqual(link2.status, cons.STATUS_STOP)
		time.sleep(1.5)
		self.assertEqual(package.status, cons.STATUS_STOP)
		self.assertEqual(file1.status, cons.STATUS_STOP)
		self.assertEqual(link1.status, cons.STATUS_CORRECT)

	def clear(self):
		""""""
		pass

	def tearDown(self):
		""""""
		self.manager.quit()
		del self.manager
