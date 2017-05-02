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

import cPickle
import logging
logger = logging.getLogger(__name__)

from base_types import STATUS_HIERARCHY

import cons

VALID_PREVIOUS_TYPES = {
cons.ITEM_TYPE_PACKAGE : [cons.ITEM_TYPE_LINK],
cons.ITEM_TYPE_FILE : [cons.ITEM_TYPE_LINK, cons.ITEM_TYPE_PACKAGE],
cons.ITEM_TYPE_LINK : [cons.ITEM_TYPE_LINK, cons.ITEM_TYPE_FILE]
}

class Queue:
	""""""
	def __init__(self):
		""""""
		self.items = []
		
	def dump(self):
		""""""
		return cPickle.dumps(self.items)

	def load(self, data):
		""""""
		try:
			return self.add(cPickle.loads(data))
		except Exception, e:
			logger.exception("Could not load session: %s" % e)

	def update_cb(self, item, status=None):
		"""updates and propagates status to parent"""
		if status and item.parent:
			self.propagate_status(item.parent, status)

	def sort_status(self, new_status, old_status):
		""""""
		status = STATUS_HIERARCHY
		return status[min(status.index(new_status), status.index(old_status))]

	def propagate_status(self, parent, status):
		""""""
		#check if the status change affects the parent
		if parent.status != status:
			#find the appropriate status in the brotherhood
			for item in self.get_children(parent.id):
				status = self.sort_status(item.status, status)
			#check again if the status change affects the parent
			if parent.status != status:
				parent.set_status(status)
				if parent.parent:
					self.propagate_status(parent.parent, status)

	def add(self, items):
		""""""
		new_items = []
		ids = [item.id for item in self.items]
		prev_item = self.items[-1] if ids else None
		for item in items:
			#IDs must be unique
			if item.id not in ids + [i.id for i in new_items]:
				item.set_callback(self.update_cb)
				if prev_item:
					if prev_item.type in VALID_PREVIOUS_TYPES[item.type]:
						prev_item = item
						new_items.append(item)
					else:
						logger.error("Invalid item sequence: adding %s after %s" % (item.type, prev_item.type))
						return
				elif item.type == cons.ITEM_TYPE_PACKAGE:
					prev_item = item
					new_items.append(item)
				else:
					logger.error("First item in queue must be a package: %s" % item.type)
					return
			else:
				logger.error("ID already present in queue: %s" % item.id)
				return
		if new_items:
			self.items += new_items
			return True

	def delete(self, item):
		""""""
		#if item:
		if item.type == cons.ITEM_TYPE_PACKAGE:
			self.delete_package(item)
		elif item.type == cons.ITEM_TYPE_FILE:
			self.delete_file(item)
		elif item.type == cons.ITEM_TYPE_LINK:
			self.delete_link(item)

	def delete_package(self, package):
		""""""
		files = self.get_children(package.id)
		self.items.remove(package)
		for file in files:
			links = self.get_children(file.id)
			self.items.remove(file)
			for link in links:
				self.items.remove(link)

	def delete_file(self, file):
		""""""
		if len(self.get_children(file.parent_id)) > 1:
			links = self.get_children(file.id)
			self.items.remove(file)
			for link in links:
				self.items.remove(link)
			package = self.get_item(file.parent_id)
			package.current_size -= file.current_size
			package.set_total_size(package.total_size - file.total_size)
		else:
			self.delete(file.parent)

	def delete_link(self, link):
		""""""
		if len(self.get_children(link.parent_id)) > 1:
			self.items.remove(link)
			file = self.get_item(link.parent_id)
			package = self.get_item(file.parent_id)
			file.current_size -= link.current_size
			file.set_total_size(file.total_size - link.total_size)
			package.current_size -= link.current_size
			package.set_total_size(package.total_size - link.total_size)
		else:
			self.delete(link.parent)
			
	def move_up(self, item):
		""""""
		self.move(item, -1)

	def move_down(self, item):
		""""""
		self.move(item, 1)

	def move(self, item, direction=-1):
		"""direction : -1 if the item goes up, 1 if it goes down."""
		if item:
			ind = self.items.index(item)
			items = self.get_children(item.parent_id)
			tmp = items.index(item) + direction
			if tmp >= 0 and tmp < len(items):
				ind2 = self.items.index(items[tmp])
				for type in [cons.ITEM_TYPE_PACKAGE, cons.ITEM_TYPE_FILE, cons.ITEM_TYPE_LINK]:
					if item.type == type and items[tmp].type == type:
						self.swap(ind, ind2, self.get_length(item.id), self.get_length(items[tmp].id))
						break

	def swap(self, old, new, l1, l2):
		""""""
		if old > new:
			old,new,l1,l2 = new,old,l2,l1
		self.items[old:old+l2],self.items[old+l2:old+l2+l1] = self.items[new:new+l2], self.items[old:old+l1]

	def get_length(self, id):
		""""""
		l = 1
		for item in self.get_children(id):
			l += 1
			subitems = self.get_children(item.id)
			for subitem in subitems:
				l += 1
		return l

	def get_item(self, id):
		""""""
		if id:
			for item in self.items:
				if item.id == id:
					return item

	def get_children(self, id=None):
		""""""
		return [item for item in self.items if item.parent_id == id]

	def for_all_children(self, id, func, *args):
		""""""
		children = self.get_children(id)
		if children:
			for child in children:
				func(child.id, child, *args)
			return True
