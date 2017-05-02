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
import time
import os.path
import logging
logger = logging.getLogger(__name__)

import cons
import misc

STATUS_HIERARCHY = [
cons.STATUS_ACTIVE,
cons.STATUS_WAIT,
cons.STATUS_PEND,
cons.STATUS_ERROR,
cons.STATUS_STOP,
cons.STATUS_CORRECT
]

def create_upload_package(file_list, name=None):
	""""""
	items = []
	if not name:
		name = misc.name_package()
	package = Package(name)
	items.append(package)
	package_total_size = 0
	for path, size, services in file_list:
		file = File(package, path)
		items.append(file)
		file_total_size = 0
		for service_name, plugin_type, plugin_info in services:
			file_total_size += size
			link = Link(file, path, service_name)
			link.set_plugin(plugin_type, plugin_info)
			link.set_total_size(size)
			items.append(link)
		file.set_total_size(file_total_size)
		package_total_size += file.total_size
	package.set_total_size(package_total_size)
	return items

class Item:
	""""""
	def __init__(self, item_type, parent=None):
		""""""
		self.id = str(uuid.uuid1())
		self.type = item_type
		self.parent = parent
		self.parent_id = parent.id if parent else None
		self.status = cons.STATUS_PEND
		self.current_size = 0
		self.total_size = 0
		self.normalized_total_size = ""
		self.current_speed = 0
		self.started_time = 0
		self.elapsed_time = ""
		self.callback = None
		
	def __getstate__(self):
		"""can't pickle instancemethod objects"""
		tmp =  self.__dict__.copy()
		tmp["callback"] = None
		if self.get_active():
			tmp["status"] = cons.STATUS_PEND
			tmp["current_speed"] = 0
		return tmp

	def get_name(self):
		""""""
		pass

	def get_progress(self):
		""""""
		if self.status == cons.STATUS_CORRECT:
			return 100
		else:
			return int((float(self.current_size)/self.total_size)*100)

	def get_current_size(self):
		""""""
		if self.status == cons.STATUS_CORRECT:
			return self.normalized_total_size
		elif self.current_size:
			return misc.normalize(self.current_size)

	def get_total_size(self):
		""""""
		return self.normalized_total_size

	def get_speed(self):
		""""""
		if self.status == cons.STATUS_ACTIVE:
			return misc.normalize(self.current_speed, "%.1f%s/s")
		else:
			self.current_speed = 0

	def get_time(self):
		""""""
		if self.status == cons.STATUS_CORRECT:
			if not self.elapsed_time:
				self.elapsed_time = misc.normalize_time(time.time()-self.started_time)
			return self.elapsed_time
		elif self.current_speed:
			return misc.normalize_time((self.total_size-self.current_size)/self.current_speed)

	def get_info(self):
		""""""
		pass
	
	def get_active(self):
		""""""
		if self.status in [cons.STATUS_ACTIVE, cons.STATUS_WAIT]:
			return self.status

	def get_pending(self):
		""""""
		if self.status in [cons.STATUS_PEND, cons.STATUS_ERROR]:
			return self.status

	def update(self, diff_size, diff_speed):
		""""""
		self.current_size += diff_size
		self.current_speed += diff_speed
		if self.parent:
			self.parent.update(diff_size, diff_speed)
		self.callback(self)

	def set_total_size(self, size):
		""""""
		self.total_size = size
		self.normalized_total_size = misc.normalize(size)

	def set_status(self, status):
		""""""
		if status == cons.STATUS_ACTIVE:
			if not self.started_time:
				self.started_time = time.time()
		else:
			if status == cons.STATUS_STOP:
				self.started_time = 0
			self.current_speed = 0
		self.status = status
		self.callback(self, status)

	def set_callback(self, callback):
		""""""
		self.callback = callback

class Link(Item):
	""""""
	def __init__(self, parent, path, service_name):
		""""""
		Item.__init__(self, cons.ITEM_TYPE_LINK, parent)
		self.url = None
		self.path = path
		self.service_name = service_name
		self.plugin_type = None
		self.plugin_info = None
		
	def set_plugin(self, plugin_type, info):
		""""""
		self.plugin_type = plugin_type
		self.plugin_info = info
	
	def get_plugin(self):
		""""""
		return self.service_name, self.plugin_type

	def get_name(self):
		""""""
		if self.url:
			return self.url
		else:
			return "http://www.%s" % self.service_name

	def get_info(self):
		""""""
		return self.plugin_info

class File(Item):
	""""""
	def __init__(self, parent, path):
		""""""
		Item.__init__(self, cons.ITEM_TYPE_FILE, parent)
		self.path = path
		self.name = os.path.basename(path)

	def get_name(self):
		""""""
		return self.name

	def get_info(self):
		""""""
		return self.path

class Package(Item):
	""""""
	def __init__(self, name):
		""""""
		Item.__init__(self, cons.ITEM_TYPE_PACKAGE)
		self.name = name
		self.desc = "Uploaded by %s - %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION)

	def get_name(self):
		""""""
		return self.name

	def get_info(self):
		""""""
		return self.desc
