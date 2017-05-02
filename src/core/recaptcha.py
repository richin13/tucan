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

from url_open import URLOpen

import cons
import shared

TIMEOUT = 60

class Recaptcha:
	""""""
	def __init__(self, service, url):
		""""""
		self.service_name = service
		self.captcha_link = url
		self.timeout = TIMEOUT

	def solve_captcha(self):
		""""""
		self.captcha_challenge = None
		self.captcha_response = None
		self.wait_for_response = True
		try:
			shared.events.trigger_captcha_dialog(self.service_name, self.get_captcha, self.set_response)
			while self.wait_for_response:
				if self.timeout:
					self.timeout -= 1
					time.sleep(1)
				else:
					logger.warning("No response for %s event" % cons.EVENT_CAPTCHA_DIALOG)
					break
		except Exception, e:
			logger.exception("%s :%s" % (self.captcha_link, e))
		return self.captcha_challenge, self.captcha_response

	def get_captcha(self):
		""""""
		image_type = None
		image_data = None
		self.timeout = TIMEOUT
		try:
			for line in URLOpen().open(self.captcha_link).readlines():
				if "challenge : " in line:
					self.captcha_challenge = line.split("'")[1]
					handle = URLOpen().open("http://www.google.com/recaptcha/api/image?c=%s" % self.captcha_challenge)
					image_data = handle.read()
					image_type = handle.info()["Content-Type"].split("/")[1]
					break
		except Exception, e:
			logger.exception("%s :%s" % (self.captcha_link, e))
		return image_type, image_data

	def set_response(self, solution):
		""""""
		self.captcha_response = solution
		self.wait_for_response = False
