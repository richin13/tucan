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

import subprocess
import logging
logger = logging.getLogger(__name__)

import cons

class Dependencies:
	""""""
	def __init__(self):
		""""""
		self.checked = {}
		
	def check(self, dependency):
		""""""
		if dependency in self.checked:
			message = self.checked[dependency]
			if message:
				raise Exception(message)
		elif dependency == cons.DEPENDENCY_RECAPTCHA:
			self.check_recaptcha()
		elif dependency == cons.DEPENDENCY_TESSERACT:
			self.check_tesseract()
			
	def set_recaptcha(self):
		""""""
		self.checked[cons.DEPENDENCY_RECAPTCHA] = None
		
	def check_recaptcha(self):
		""""""
		message = "recaptcha needs GUI."
		self.checked[cons.DEPENDENCY_RECAPTCHA] = message
		raise Exception(message)

	def check_tesseract(self):
		""""""
		self.checked[cons.DEPENDENCY_TESSERACT] = None
		try:
			import Image
		except:
			message = "PIL not found."
			self.checked[cons.DEPENDENCY_TESSERACT] = message
			raise Exception(message)
		try:
			import tesseract
			tesseract.check_installed()
		except:
			message = "tesseract not found."
			self.checked[cons.DEPENDENCY_TESSERACT] = message
			raise Exception(message)
