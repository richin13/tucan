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
import logging
logger = logging.getLogger(__name__)

import cons
import shared

class Slots:
	""""""
	def __init__(self, slots=1, wait=300):
		""""""
		self.time_limit = wait
		self.limit = False
		self.end_wait = 0
		self.max = slots
		self.slots = slots
		shared.events.connect(cons.EVENT_LIMIT_CANCEL, self.cancel_limit)

	def get_slot(self):
		""""""
		if self.wait_finished():
			if self.max < 0:
				return True
			elif self.slots > 0:
				self.slots -= 1
				return True
				
	def return_slot(self):
		""""""
		if self.slots < self.max:
			self.slots += 1
			return True
			
	def wait_finished(self):
		""""""
		if self.end_wait == 0:
			return True
		else:
			if time.time() > self.end_wait:
				self.end_wait = 0
				shared.events.trigger_limit_off(self.__module__)
				self.limit = False
				return True

	def set_limit_exceeded(self, wait=0):
		""""""
		if not wait:
			wait = self.time_limit
		self.end_wait = time.time() + wait
		shared.events.trigger_limit_on(self.__module__, self.end_wait)
		logger.warning("Wait %i seconds." % wait)
		self.return_slot()
		self.limit = True
		return cons.EVENT_LIMIT_ON

	def cancel_limit(self, module):
		""""""
		if module == self.__module__:
			self.limit = False
			self.end_wait = 0
			logger.info("Limit canceled manually: %s" % self.__module__)
