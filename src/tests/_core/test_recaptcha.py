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

import unittest


from core.events import Events
from core.recaptcha import Recaptcha
import core.cons as cons
import core.shared as shared

shared.events = Events()

NAME = "Recaptcha"
#LINK = "http://api.recaptcha.net/challenge?k=6LfRJwkAAAAAAGmA3mAiAcAsRsWvfkBijaZWEvkD"
LINK = "http://www.google.com/recaptcha/api/challenge?k=6LfRJwkAAAAAAGmA3mAiAcAsRsWvfkBijaZWEvkD"

class DialogMockup:
	""""""
	def __init__(self, name, get_captcha, return_solution, timeout=False):
		""""""
		image_type, image_data = get_captcha()
		if not timeout:
			return_solution(image_type)

class TestRecaptcha(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.recaptcha = Recaptcha(NAME, LINK)

	def test_captcha_mockup(self):
		""""""
		id = shared.events.connect(cons.EVENT_CAPTCHA_DIALOG, DialogMockup)
		challenge, solution = self.recaptcha.solve_captcha()
		shared.events.disconnect(cons.EVENT_CAPTCHA_DIALOG, id)
		self.assertTrue(challenge, "challenge should be a string: %s" % challenge)
		self.assertTrue(solution, "solution should be a string: %s" % solution)

	def test_timeout(self):
		""""""
		id = shared.events.connect(cons.EVENT_CAPTCHA_DIALOG, DialogMockup, True)
		challenge, solution = self.recaptcha.solve_captcha()
		shared.events.disconnect(cons.EVENT_CAPTCHA_DIALOG, id)
		self.assertTrue(challenge, "challenge should be a string: %s" % challenge)
		self.assertFalse(solution, "solution should be None: %s" % solution)

	def tearDown(self):
		""""""
		del self.recaptcha
