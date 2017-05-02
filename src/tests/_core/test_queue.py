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

from core.queue import Queue
import core.cons as cons

PATH1 = '/home/user/file.part1.rar'
PATH2 = '/home/user/file.part2.rar'
SIZE = 1024
LINK1 = 'megaupload.anonymous_upload'
LINK2 = 'rapidshare.anonymous_upload'

FILE_LIST = [
(PATH1, SIZE, [LINK1, LINK2]), 
(PATH2, SIZE, [LINK1, LINK2])]


class TestQueue(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.queue = Queue()
		self.queue.add_package(FILE_LIST)

	def test_delete_package(self):
		""""""
		package = self.queue.add_package(FILE_LIST)
		packages = self.queue.get_children()
		self.assertEqual(len(packages), 2)
		self.queue.delete(package)
		self.assertEqual(len(self.queue.get_children()), 1)
		self.assertEqual(self.queue.get_item(package.id), None)

	def test_delete_file(self):
		""""""
		package = self.queue.add_package(FILE_LIST)
		file1, file2 = self.queue.get_children(package.id)
		old_size = self.queue.get_item(package.id).total_size
		self.queue.delete(file1)
		size = self.queue.get_item(package.id).total_size
		self.assertEqual(size, old_size-file1.total_size)
		self.assertEqual(len(self.queue.get_children(package.id)), 1)
		self.assertEqual(self.queue.get_item(file1.id), None)
		self.queue.delete(file2)
		self.assertEqual(self.queue.get_item(file2.id), None)
		self.assertEqual(self.queue.get_item(package.id), None)

	def test_delete_link(self):
		""""""
		package = self.queue.add_package(FILE_LIST)
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		p_size = self.queue.get_item(package.id).total_size
		f_size = file1.total_size
		self.queue.delete(link1)
		size = self.queue.get_item(file1.id).total_size
		self.assertEqual(size, f_size-link1.total_size)
		size = self.queue.get_item(package.id).total_size
		self.assertEqual(size, p_size-link1.total_size)
		self.assertEqual(len(self.queue.get_children(file1.id)), 1)
		self.assertEqual(self.queue.get_item(link1.id), None)
		self.queue.delete(file2)
		self.queue.delete(link2)
		self.assertEqual(self.queue.get_item(link2.id), None)
		self.assertEqual(self.queue.get_item(file1.id), None)
		self.assertEqual(self.queue.get_item(package.id), None)
		
	def test_move_up_link(self):
		package = self.queue.get_children().pop()
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		self.queue.move_up(link2)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link4)
		self.assertEqual(link2, link3)
		self.queue.move_up(link1)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link3)
		self.assertEqual(link2, link4)
		self.queue.move_up(link1)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link3)
		self.assertEqual(link2, link4)
	
	def test_move_down_link(self):
		package = self.queue.get_children().pop()
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		self.queue.move_down(link1)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link4)
		self.assertEqual(link2, link3)
		self.queue.move_down(link2)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link3)
		self.assertEqual(link2, link4)
		self.queue.move_down(link2)
		link3, link4 = self.queue.get_children(file1.id)
		self.assertEqual(link1, link3)
		self.assertEqual(link2, link4)
		
	def test_move_up_file(self):
		package = self.queue.get_children().pop()
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		link3, link4 = self.queue.get_children(file2.id)
		self.queue.move_up(file2)
		file3, file4 = self.queue.get_children(package.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.assertEqual(file1, file4)
		self.assertEqual(file2, file3)
		self.assertEqual(link1, link7)
		self.assertEqual(link2, link8)
		self.assertEqual(link3, link5)
		self.assertEqual(link4, link6)
		self.queue.move_up(file2)
		file3, file4 = self.queue.get_children(package.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.assertEqual(file1, file4)
		self.assertEqual(file2, file3)
		self.assertEqual(link1, link7)
		self.assertEqual(link2, link8)
		self.assertEqual(link3, link5)
		self.assertEqual(link4, link6)

	def mtest_move_down_file(self):
		package = self.queue.get_children().pop()
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		link3, link4 = self.queue.get_children(file2.id)
		self.queue.move_down(file1)
		file3, file4 = self.queue.get_children(package.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.assertEqual(file1, file4)
		self.assertEqual(file2, file3)
		self.assertEqual(link1, link7)
		self.assertEqual(link2, link8)
		self.assertEqual(link3, link5)
		self.assertEqual(link4, link6)
		self.queue.move_down(file1)
		file3, file4 = self.queue.get_children(package.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.assertEqual(file1, file4)
		self.assertEqual(file2, file3)
		self.assertEqual(link1, link7)
		self.assertEqual(link2, link8)
		self.assertEqual(link3, link5)
		self.assertEqual(link4, link6)


	def test_move_up_package(self):
		""""""
		self.queue.add_package(FILE_LIST)
		package1, package2 = self.queue.get_children()
		file1, file2 = self.queue.get_children(package1.id)
		file3, file4 = self.queue.get_children(package2.id)
		link1, link2 = self.queue.get_children(file1.id)
		link3, link4 = self.queue.get_children(file2.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.queue.move_up(package2)
		package3, package4 = self.queue.get_children()
		file5, file6 = self.queue.get_children(package3.id)
		file7, file8 = self.queue.get_children(package4.id)
		link9, link10 = self.queue.get_children(file5.id)
		link11, link12 = self.queue.get_children(file6.id)
		link13, link14 = self.queue.get_children(file7.id)
		link15, link16 = self.queue.get_children(file8.id)
		self.assertEqual(package1, package4)
		self.assertEqual(package2, package3)
		self.assertEqual(file1, file7)
		self.assertEqual(file2, file8)
		self.assertEqual(file3, file5)
		self.assertEqual(file4, file6)
		self.assertEqual(link1, link13)
		self.assertEqual(link2, link14)
		self.assertEqual(link3, link15)
		self.assertEqual(link4, link16)
		self.assertEqual(link5, link9)
		self.assertEqual(link6, link10)
		self.assertEqual(link7, link11)
		self.assertEqual(link8, link12)
		self.queue.move_up(package2)
		package3, package4 = self.queue.get_children()
		file5, file6 = self.queue.get_children(package3.id)
		file7, file8 = self.queue.get_children(package4.id)
		link9, link10 = self.queue.get_children(file5.id)
		link11, link12 = self.queue.get_children(file6.id)
		link13, link14 = self.queue.get_children(file7.id)
		link15, link16 = self.queue.get_children(file8.id)
		self.assertEqual(package1, package4)
		self.assertEqual(package2, package3)
		self.assertEqual(file1, file7)
		self.assertEqual(file2, file8)
		self.assertEqual(file3, file5)
		self.assertEqual(file4, file6)
		self.assertEqual(link1, link13)
		self.assertEqual(link2, link14)
		self.assertEqual(link3, link15)
		self.assertEqual(link4, link16)
		self.assertEqual(link5, link9)
		self.assertEqual(link6, link10)
		self.assertEqual(link7, link11)
		self.assertEqual(link8, link12)

	def test_move_down_package(self):
		""""""
		package_id = self.queue.add_package(FILE_LIST)
		package1, package2 = self.queue.get_children()
		file1, file2 = self.queue.get_children(package1.id)
		file3, file4 = self.queue.get_children(package2.id)
		link1, link2 = self.queue.get_children(file1.id)
		link3, link4 = self.queue.get_children(file2.id)
		link5, link6 = self.queue.get_children(file3.id)
		link7, link8 = self.queue.get_children(file4.id)
		self.queue.move_down(package1)
		package3, package4 = self.queue.get_children()
		file5, file6 = self.queue.get_children(package3.id)
		file7, file8 = self.queue.get_children(package4.id)
		link9, link10 = self.queue.get_children(file5.id)
		link11, link12 = self.queue.get_children(file6.id)
		link13, link14 = self.queue.get_children(file7.id)
		link15, link16 = self.queue.get_children(file8.id)
		self.assertEqual(package1, package4)
		self.assertEqual(package2, package3)
		self.assertEqual(file1, file7)
		self.assertEqual(file2, file8)
		self.assertEqual(file3, file5)
		self.assertEqual(file4, file6)
		self.assertEqual(link1, link13)
		self.assertEqual(link2, link14)
		self.assertEqual(link3, link15)
		self.assertEqual(link4, link16)
		self.assertEqual(link5, link9)
		self.assertEqual(link6, link10)
		self.assertEqual(link7, link11)
		self.assertEqual(link8, link12)
		self.queue.move_down(package1)
		package3, package4 = self.queue.get_children()
		file5, file6 = self.queue.get_children(package3.id)
		file7, file8 = self.queue.get_children(package4.id)
		link9, link10 = self.queue.get_children(file5.id)
		link11, link12 = self.queue.get_children(file6.id)
		link13, link14 = self.queue.get_children(file7.id)
		link15, link16 = self.queue.get_children(file8.id)
		self.assertEqual(package1, package4)
		self.assertEqual(package2, package3)
		self.assertEqual(file1, file7)
		self.assertEqual(file2, file8)
		self.assertEqual(file3, file5)
		self.assertEqual(file4, file6)
		self.assertEqual(link1, link13)
		self.assertEqual(link2, link14)
		self.assertEqual(link3, link15)
		self.assertEqual(link4, link16)
		self.assertEqual(link5, link9)
		self.assertEqual(link6, link10)
		self.assertEqual(link7, link11)
		self.assertEqual(link8, link12)

	def test_propagate_status(self):
		""""""
		package = self.queue.get_children().pop()
		file1, file2 = self.queue.get_children(package.id)
		link1, link2 = self.queue.get_children(file1.id)
		link3, link4 = self.queue.get_children(file2.id)
		#p : pend, f: pend pend, l: pend pend pend pend
		link1.set_status(cons.STATUS_ACTIVE)
		#p : active, f: active pend, l: active pend pend pend
		self.assertEqual(file1.status, cons.STATUS_ACTIVE)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		link2.set_status(cons.STATUS_WAIT)
		#p : active, f: active pend, l: active wait pend pend
		self.assertEqual(file1.status, cons.STATUS_ACTIVE)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		link1.set_status(cons.STATUS_PEND)
		#p : wait, f: wait pend, l: pend wait pend pend
		self.assertEqual(file1.status, cons.STATUS_WAIT)
		self.assertEqual(package.status, cons.STATUS_WAIT)
		link1.set_status(cons.STATUS_ACTIVE)
		#p : active, f: active pend, l: active wait pend pend
		link1.set_status(cons.STATUS_ERROR)
		link2.set_status(cons.STATUS_ERROR)
		#p : pend, f: error pend, l: error error pend pend
		self.assertEqual(file1.status, cons.STATUS_ERROR)
		self.assertEqual(package.status, cons.STATUS_PEND)
		link1.set_status(cons.STATUS_WAIT)
		#p : wait, f: wait pend, l: wait error pend pend
		self.assertEqual(file1.status, cons.STATUS_WAIT)
		self.assertEqual(package.status, cons.STATUS_WAIT)
		link1.set_status(cons.STATUS_CORRECT)
		link2.set_status(cons.STATUS_CORRECT)
		#p : pend, f: correct pend, l: correct correct pend pend
		self.assertEqual(file1.status, cons.STATUS_CORRECT)
		self.assertEqual(package.status, cons.STATUS_PEND)
		link3.set_status(cons.STATUS_ACTIVE)
		#p : active, f: correct active, l: correct correct active pend
		self.assertEqual(file2.status, cons.STATUS_ACTIVE)
		self.assertEqual(package.status, cons.STATUS_ACTIVE)
		link3.set_status(cons.STATUS_CORRECT)
		link4.set_status(cons.STATUS_CORRECT)
		#p : correct, f: correct correct, l: correct correct correct correct
		self.assertEqual(file2.status, cons.STATUS_CORRECT)
		self.assertEqual(package.status, cons.STATUS_CORRECT)

	def test_sort_status(self):
		tmp = self.queue.sort_status(cons.STATUS_CORRECT, cons.STATUS_STOP)
		self.assertEqual(tmp, cons.STATUS_STOP)
		tmp = self.queue.sort_status(cons.STATUS_STOP, cons.STATUS_ERROR)
		self.assertEqual(tmp, cons.STATUS_ERROR)
		tmp = self.queue.sort_status(cons.STATUS_ERROR, cons.STATUS_PEND)
		self.assertEqual(tmp, cons.STATUS_PEND)
		tmp = self.queue.sort_status(cons.STATUS_PEND, cons.STATUS_WAIT)
		self.assertEqual(tmp, cons.STATUS_WAIT)
		tmp = self.queue.sort_status(cons.STATUS_WAIT, cons.STATUS_ACTIVE)
		self.assertEqual(tmp, cons.STATUS_ACTIVE)

	def tearDown(self):
		""""""
		del self.queue
