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

import threading
import logging
logger = logging.getLogger(__name__)

from downloader import Downloader
from slots import Slots
from misc import get_size

import cons

class DownloadPlugin(Slots):
	""""""
	def __init__(self, config, section):
		""""""
		Slots.__init__(self, config.get_slots(section), config.get_wait(section))
		self.active_downloads = {}
		
	def link_parser(self, link, wait_func, range=None):
		""""""
		pass

	def add(self, path, url, file_name):
		""""""
		if file_name not in self.active_downloads:
			if self.get_slot():
				logger.info("Started %s" % (file_name))
				th = Downloader(path, url, file_name, self.link_parser)
				self.active_downloads[file_name] = th
				th.start()
				return True

	def delete(self, file_name):
		""""""
		if file_name in self.active_downloads:
			logger.info("Stopped %s: %s" % (file_name, self.return_slot()))
			th = threading.Thread(group=None, target=self.stop_thread, name=None, args=(self.active_downloads[file_name],))
			th.start()
			del self.active_downloads[file_name]
			return True
			
	def stop_thread(self, thread):
		""""""
		while thread.isAlive():
			thread.stop_flag = True
			thread.join(0.5)

	def stop_all(self):
		""""""
		active_downloads = self.active_downloads.values()
		while active_downloads:
			for th in active_downloads:
				if th.isAlive():
					th.stop_flag = True
					th.join(0.1)
				else:
					active_downloads.remove(th)

	def get_status(self, file_name, speed=0):
		"""return (status, progress, actual_size, unit, speed, time)"""
		result = cons.STATUS_ERROR, 0, 0, None, 0, 0
		th = None
		if file_name in self.active_downloads:
			th = self.active_downloads[file_name]
			#if th.stop_flag:
			#	del self.active_downloads[file_name]
		if th:
			actual_size, unit = get_size(th.actual_size)
			progress = int((float(th.actual_size)/float(th.total_size))*100)
			if th.status == cons.STATUS_ACTIVE:
				th.max_speed = speed
				speed = th.speed
				if speed > 0:
					time = int(float((th.total_size - th.actual_size)/1024)/float(speed))
				else:
					time = 0
			else:
				#if not th.status == cons.STATUS_CORRECT:
				#	actual_size = 0
				speed = 0
				time = int(th.time_remaining)
			result = th.status, progress, actual_size, unit, speed, time
		return result
