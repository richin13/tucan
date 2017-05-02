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

import os
import time
import threading
import logging
logger = logging.getLogger(__name__)

import cons

BASE_SIZE = 4
BUFFER_SIZE = BASE_SIZE * 1024

PART_EXTENSION = ".part"

class Downloader(threading.Thread):
	""""""
	def __init__(self, path, url, file_name, parser):
		""""""
		threading.Thread.__init__(self)

		self.max_speed = 0

		self.link_parser = parser
		self.status = cons.STATUS_WAIT
		self.path = path
		self.url = url
		self.file = file_name
		self.stop_flag = False
		self.start_time = time.time()
		self.time_remaining = 0
		self.total_size = 1
		self.actual_size = 0
		self.speed = 0
		self.tmp_time = 0
		self.tmp_size = 0
		self.range = None

	def run(self):
		""""""
		name = os.path.join(self.path, self.file)
		try:
			#check files
			if not os.path.exists(self.path):
				os.makedirs(self.path)
			elif os.path.exists("%s%s" % (name, PART_EXTENSION)):
				tmp_size = os.path.getsize("%s%s" % (name, PART_EXTENSION))
				if tmp_size > 0:
					self.range = tmp_size
			handle = self.link_parser(self.url, self.wait, self.range)
			if handle == cons.EVENT_LIMIT_ON:
				self.stop_flag = True
				self.status = cons.STATUS_PEND
			elif handle:
				info = handle.info()
				size = info.getheader("Content-Length", None)
				if info.getheader("Content-Range", None):
					size = info.getheader("Content-Range").split("/")[1]
				else:
					self.range = None
				if size:
					self.status = cons.STATUS_ACTIVE
					logger.debug("%s :%s" % (self.file, handle.info().getheader("Content-Type")))
					self.total_size = int(size)
					if os.path.exists(name):
						if os.path.getsize(name) == self.total_size:
							logger.info("%s already on disk" % name)
							self.actual_size = self.total_size
							self.status = cons.STATUS_CORRECT
						else:
							os.remove(name)
							logger.warning("%s already on disk but different size" % name)
							self.download(name, handle)
					elif os.path.exists("%s%s" % (name, PART_EXTENSION)) and self.range:
						#this should be tested  exhaustively
						logger.info("Resuming %s%s (%i)" % (name, PART_EXTENSION, self.range))
						self.actual_size = self.range
						self.download(name, handle, True)
					else:
						self.download(name, handle)
				else:
					self.stop_flag = True
					self.status = cons.STATUS_ERROR
			else:
				self.stop_flag = True
				self.status = cons.STATUS_ERROR
		except Exception, e:
			self.stop_flag = True
			logger.exception("%s: %s" % (self.file, e))
			self.status = cons.STATUS_ERROR
			
	def download(self, name, handle, resume=False):
		""""""
		data = "None"
		if resume:
			mode = "ab"
		else:
			mode = "wb"
		f = open("%s%s" % (name, PART_EXTENSION), mode)
		self.start_time = time.time()
		while ((len(data) > 0) and not self.stop_flag):
			tmp_size = 0
			if self.max_speed > 0:
				max_size = self.max_speed/BASE_SIZE
			else:
				max_size = 0
			start_seconds = time.time()
			while (time.time() - start_seconds) < 1:
				if max_size == 0 or tmp_size < max_size:
					data = handle.read(BUFFER_SIZE)
					f.write(data)
					self.actual_size += len(data)
					tmp_size += 1
				else:
					time.sleep(0.1)
			self.speed = BASE_SIZE * tmp_size
		self.time_remaining = time.time() - self.start_time
		f.flush()
		os.fsync(f.fileno())
		f.close()
		if self.stop_flag:
			#os.remove("%s.part" % name)
			self.status = cons.STATUS_PEND
		else:
			#self.stop_flag = True
			if self.actual_size == self.total_size:
				os.rename("%s%s" % (name, PART_EXTENSION), name)
				self.status = cons.STATUS_CORRECT
			else:
				self.status = cons.STATUS_ERROR

	def get_speed(self):
		"""return int speed KB/s"""
		elapsed_time = time.time() - self.tmp_time
		size = self.actual_size - self.tmp_size
		if size > 0:
			self.speed = int(float(size/1024)/float(elapsed_time))
			self.tmp_time = time.time()
			self.tmp_size = self.actual_size
		return self.speed
		
	def wait(self, wait=0):
		"""non-blocking wait"""
		while ((wait > 0) and not self.stop_flag):
			time.sleep(1)
			wait -= 1
			self.time_remaining = wait
		if not self.stop_flag:
			return True
