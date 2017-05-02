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

import random

class StopUpload(Exception):
	""""""

class Uploader(threading.Thread):
	""""""
	def __init__(self, item, parse, parse_result):
		""""""
		threading.Thread.__init__(self)
		self.item = item
		self.parse = parse
		self.parse_result = parse_result
		self.max_speed = 0
		self.stop_flag = False

		self.tmp_size = 0
		self.diff_size = 0
		self.last_speed = 0
		self.update_time = 0
		self.remaining_time = 1
		self.elapsed_time = time.time()

	def limit_speed(self, speed):
		""""""
		self.max_speed = speed

	def update_cb(self, multipart_param, current_size, total_size):
		""""""
		if self.stop_flag:
			raise StopUpload
		else:
			self.diff_size += current_size - self.tmp_size
			self.tmp_size = current_size
			#total_size includes headers so its bigger than file size
			if not self.update_time:
				self.item.set_total_size(total_size)
			#last update independent of remaining_time
			elif current_size == total_size:
				self.update_item(self.last_speed)
			elif self.remaining_time > 0:
				if self.max_speed and self.diff_size >= self.max_speed:
					time.sleep(self.remaining_time)
					self.update_item()
				else:
					self.remaining_time -= time.time() - self.update_time
			else:
				self.update_item()
			self.update_time = time.time()

	def update_item(self, speed=None):
		""""""
		if not speed:
			speed = self.diff_size / (time.time() - self.elapsed_time)
		self.elapsed_time = time.time()
		self.item.update(self.diff_size, speed - self.last_speed)
		self.last_speed = speed
		self.diff_size = 0
		self.remaining_time = 1

	def run(self):
		""""""
		url = None
		self.item.set_status(cons.STATUS_ACTIVE)
		size = self.item.current_size
		if size:
			self.item.update(-size, 0)
		try:
			encoder = self.parse(self.item.path)
			#MultipartEncoder.open blocks while uploading
			handler = encoder.open(self.update_cb)
			url = self.parse_result(handler)
		except StopUpload:
			self.item.set_status(cons.STATUS_STOP)
		except IOError, e:
			logger.error(e)
			self.item.set_status(cons.STATUS_ERROR)
		except Exception, e:
			logger.exception(e)
			self.item.set_status(cons.STATUS_ERROR)
		else:
			if url:
				self.item.url = url
				self.item.set_status(cons.STATUS_CORRECT)
			else:
				logger.error("No upload URL!")
				self.item.set_status(cons.STATUS_ERROR)

	def stop(self):
		"""stops in the next encoder callback"""
		self.stop_flag = True
