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

import uuid
import logging
logger = logging.getLogger(__name__)

import cons

VALID_STATUS = [cons.STATUS_PEND, cons.STATUS_ACTIVE, cons.STATUS_WAIT, cons.STATUS_STOP, cons.STATUS_CORRECT, cons.STATUS_ERROR]

class Base:
	""""""
	def __init__(self, name):
		""""""
		self.id = str(uuid.uuid1())
		self.name = name

	def get_id(self):
		""""""
		return self.id

	def get_name(self):
		""""""
		return self.name

	def set_name(self, name):
		""""""
		self.name = name

class Container(Base):
	""""""
	def __init__(self, name):
		""""""
		Base.__init__(self, name)
		self.items = []

	def add_item(self, item):
		""""""
		if item.get_id() in [item.get_id() for item in self.items]:
			logger.warning("Item already present: %s" % item.get_name())
		else:
			self.items.append(item)
			return True

	def add_items(self, items):
		""""""
		for item in items:
			self.add_item(item)

	def get_item(self, id):
		""""""
		pass

	def remove_item(self, id):
		""""""
		pass

	def remove_items(self, ids):
		""""""
		for id in ids:
			self.remove_item(id)

class Item:
	""""""
	def __init__(self, path, size):
		""""""
		self.status = cons.STATUS_PEND
		self.path = path
		self.total_size = size
		self.actual_size = 0
		self.elapsed_time = 0

	def get_status(self):
		""""""
		return self.status

	def set_status(self, status):
		""""""
		if status in VALID_STATUS:
			self.status = status
			return True
		else:
			logger.error("Invalid status: %s" % status)
