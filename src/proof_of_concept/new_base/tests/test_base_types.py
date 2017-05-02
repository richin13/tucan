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

from core.base_types import Base
from core.base_types import Container
from core.base_types import Item

NAME = "something"
NAME2 = "another"
PATH = ""
SIZE = 0

class TestBase(unittest.TestCase):
	def setUp(self):
		self.base = Base(NAME)

	def test_id(self):
		self.assertEqual(len(self.base.get_id()), 36, "id should have 36 characters")

	def test_name(self):
		self.assertTrue(self.base.get_name(), "name should not be empty")

	def test_set_name(self):
		self.base.set_name(NAME2)
		self.assertNotEqual(self.base.get_name(), NAME, "name should be updated")
		self.assertEqual(self.base.get_name(), NAME2, "name should be updated")

	def tearDown(self):
		del self.base

class TestContainer(unittest.TestCase):
	def setUp(self):
		self.container = Container(NAME)

	def test_add_item(self):
		item = Base(NAME)
		self.assertTrue(self.container.add_item(item), "item should be added")
		self.assertFalse(self.container.add_item(item), "item should not be added")

	def tearDown(self):
		del self.container

class TestItem(unittest.TestCase):
	def setUp(self):
		self.item = Item(PATH, SIZE)

	def test_(self):
		pass

	def tearDown(self):
		del self.item
