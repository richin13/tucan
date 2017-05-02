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

import logging
logger = logging.getLogger(__name__)

from events import Events
from service_manager import ServiceManager
from download_manager import DownloadManager
from history import History

import cons
import shared

class Core(ServiceManager):
	""""""
	def __init__(self):
		""""""
		if not shared.configuration.configured:
			logger.warning("No configuration found!")

		#events system
		shared.events = Events()

		shared.max_downloads = shared.configuration.get_max_downloads()
		shared.max_download_speed = shared.configuration.get_max_download_speed()

		ServiceManager.__init__(self)
		self.history = History()
		self.download_manager = DownloadManager(self.get_download_plugin, self.services)
		
	def stop_all(self):
		""""""
		self.download_manager.quit()
		ServiceManager.stop_all(self)
