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
import threading
import logging
logger = logging.getLogger(__name__)

import cons
import shared

MAX_UPLOADS = 2

import random

class UploadMockup(threading.Thread):
	""""""
	def __init__(self, item):
		""""""
		threading.Thread.__init__(self)
		self.item = item
		self.speed = 0
		self.max_speed = 0
		self.stop_flag = False
	
	def limit_speed(self, speed):
		""""""
		self.max_speed = speed

	def upload(self):
		""""""
		time.sleep(random.random()*0.01)
		return 1024*4

	def run(self):
		"""Parsing and Poster work"""
		size = self.item.current_size
		self.item.set_status(cons.STATUS_ACTIVE)
		if size:
			self.item.update(-size, 0)
		while not self.stop_flag and self.item.current_size < self.item.total_size:
			remaining_time = 1
			size = 0
			total_time = time.time()
			while remaining_time > 0 and not self.stop_flag:
				start_time = time.time()
				size += self.upload()
				remaining_time -= time.time() - start_time
				if self.max_speed and size >= self.max_speed:
					if remaining_time > 0:
						time.sleep(remaining_time)
					break
			if self.item.current_size + size > self.item.total_size:
				size = self.item.total_size - self.item.current_size
			self.item.update(size, size-self.speed)
			self.speed = size
		if self.stop_flag:
			self.item.set_status(cons.STATUS_STOP)
		else:
			self.item.set_status(cons.STATUS_CORRECT)

	def stop(self):
		"""Set a flag so that it stops"""
		self.stop_flag = True

class UploadManager:
	""""""
	def __init__(self, queue):
		""""""
		self.queue = queue

		self.timer = None
		self.schedules = 0
		self.scheduling = False
		self.max_speed = 0

		self.threads = {}

	def dump_session(self):
		""""""
		return self.queue.dump()

	def load_session(self, data):
		""""""
		if self.queue.load(data):
			self.timer = threading.Timer(0, self.scheduler)
			self.timer.start()
			return True
	
	def set_max_speed(self, speed):
		""""""
		if speed > 0:
			self.max_speed = speed

	def limit_not_reached(self):
		""""""
		cont = 0
		for id, th in self.threads.items():
			if th.isAlive():
				cont += 1
			else:
				del self.threads[id]
		return cont < MAX_UPLOADS

	def add_package(self, items):
		""""""
		if self.queue.add(items):
			logger.info("Added: %s" % items[0].get_name())
			self.timer = threading.Timer(0, self.scheduler)
			self.timer.start()

	def delete(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if not item.get_active():
			logger.info("Deleted: %s" % item.get_name())
			self.queue.delete(item)
			return True

	def clear(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if item.status == cons.STATUS_CORRECT:
			logger.info("Clear: %s" % item.get_name())
			self.queue.delete(item)

	def move_up(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		logger.info("Move up: %s" % item.get_name())
		self.queue.move_up(item)

	def move_down(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		logger.info("Move down: %s" % item.get_name())
		self.queue.move_down(item)

	def start(self, id, item=None, force=True):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if item.status != cons.STATUS_CORRECT:
			#start Links when not active
			if not self.queue.for_all_children(id, self.start, force) and not item.get_active():
				if self.limit_not_reached() or force:
					logger.info("Started %s: %s" % (item.get_info(), item.parent.get_name()))
					#th = item.plugin.process(item)
					th = UploadMockup(item)
					th.start()
					self.threads[id] = th
				elif item.status != cons.STATUS_PEND:
					logger.info("Pending %s: %s" % (item.get_info(), item.parent.get_name()))
					item.set_status(cons.STATUS_PEND)

	def stop(self, id, item=None, force=True):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if item.status != cons.STATUS_CORRECT:
			#stop active Links if force 
			if not self.queue.for_all_children(id, self.stop, force) and force or not item.get_active():
				item.set_status(cons.STATUS_STOP)
				logger.info("Stoped: %s" % item.get_name())
				if id in self.threads:
					self.threads[id].stop()

	def scheduled_start(self):
		""""""
		if self.limit_not_reached():
			items = [item for item in self.queue.items if item.type == cons.ITEM_TYPE_LINK]
			for item in items:
				if item.get_pending():
					self.start(item.id, item)
					if not self.limit_not_reached():
						break

	def keep_scheduling(self):
		""""""
		for item in self.queue.get_children():
			if item.get_pending() or item.get_active():
				return True

	def scheduler(self):
		""""""
		if not self.scheduling:
			self.scheduling = True
			self.calculate_speed()
			if self.keep_scheduling():
				if self.schedules < 59:
					self.schedules += 1
				else:
					self.schedules = 0
					logger.debug("scheduled.")
				self.scheduled_start()
				if self.timer:
					self.timer.cancel()
				self.timer = threading.Timer(1, self.scheduler)
				self.timer.start()
			else:
				self.timer = None
				shared.events.trigger_all_complete()
			self.scheduling = False

	def calculate_speed(self):
		""""""
		if self.max_speed:
			num = len(self.threads)
			if num:
				used_speed = 0
				threads_to_limit = []
				speed, remainder = divmod(self.max_speed, num)
				for th in self.threads.values():
					if th.speed < speed:
						th.limit_speed(0)
						used_speed += th.speed
					else:
						threads_to_limit.append(th)
				num = len(threads_to_limit)
				if num:
					speed, remainder = divmod(self.max_speed - used_speed, num)
					for th in threads_to_limit:
						th.limit_speed(speed)
				#self.threads.values()[2].limit_speed(1024*30)

	def quit(self):
		""""""
		threads = self.threads.values()
		for th in threads:
			th.stop()
		if self.timer:
			self.scheduling = True
			while self.timer.isAlive():
				self.timer.cancel()
				self.timer.join(0.5)
		while [th for th in threads if th.isAlive()]:
			th.join(0.5)
