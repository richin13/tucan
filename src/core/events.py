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

import cons

class Events:
	""""""
	def __init__(self):
		""""""
		self.event_id = 0
		self.registered = {}

	def connect(self, event, callback, *kargs):
		""""""
		self.event_id += 1
		event_queue = self.registered.get(event, {})
		event_queue[self.event_id] = (callback, kargs)
		self.registered[event] = event_queue
		return self.event_id

	def disconnect(self, event, id):
		""""""
		try:
			if event in self.registered:
				self.registered[event].pop(id)
				return True
		except Exception, e:
			logger.warning("Could not disconnect: %s %i" % (event, id))

	def trigger(self, event, *kargs):
		""""""
		if event in self.registered:
			for callback, kargs2 in self.registered[event].values():
				try:
					callback(*(kargs+kargs2))
				except Exception, e:
					logger.exception(e)

	def trigger_limit_off(self, module):
		""""""
		logger.debug("triggered: %s from %s" % (cons.EVENT_LIMIT_OFF, module))
		self.trigger(cons.EVENT_LIMIT_OFF, module)

	def trigger_limit_on(self, module, end_wait):
		""""""
		logger.debug("triggered: %s from %s" % (cons.EVENT_LIMIT_ON, module))
		self.trigger(cons.EVENT_LIMIT_ON, module, end_wait)

	def trigger_limit_cancel(self, module):
		""""""
		logger.debug("triggered: %s from %s" % (cons.EVENT_LIMIT_CANCEL, module))
		self.trigger(cons.EVENT_LIMIT_CANCEL, module)

	def trigger_file_complete(self, name, size, unit, links):
		""""""
		logger.debug("triggered: %s %s" % (cons.EVENT_FILE_COMPLETE, name))
		self.trigger(cons.EVENT_FILE_COMPLETE, name, size, unit, links)

	def trigger_package_complete(self, path, names):
		""""""
		logger.debug("triggered: %s %s %s" % (cons.EVENT_PACKAGE_COMPLETE, path, str(names)))
		self.trigger(cons.EVENT_PACKAGE_COMPLETE, path, names)

	def trigger_all_complete(self):
		""""""
		logger.debug("triggered: %s" % cons.EVENT_ALL_COMPLETE)
		self.trigger(cons.EVENT_ALL_COMPLETE)

	def trigger_link_checked(self, service, link, name, size, unit, plugin_type):
		""""""
		logger.debug("triggered: %s %s" % (cons.EVENT_LINK_CHECKED, link))
		self.trigger(cons.EVENT_LINK_CHECKED, service, link, name, size, unit, plugin_type)

	def trigger_check_completed(self, service):
		""""""
		logger.debug("triggered: %s %s" % (cons.EVENT_CHECK_COMPLETED, service))
		self.trigger(cons.EVENT_CHECK_COMPLETED, service)

	def trigger_check_cancel(self):
		""""""
		logger.debug("triggered: %s" % cons.EVENT_CHECK_CANCEL)
		self.trigger(cons.EVENT_CHECK_CANCEL)

	def trigger_captcha_dialog(self, service, get_captcha_img, return_solution):
		""""""
		logger.debug("triggered: %s" % cons.EVENT_CAPTCHA_DIALOG)
		self.trigger(cons.EVENT_CAPTCHA_DIALOG, service, get_captcha_img, return_solution)