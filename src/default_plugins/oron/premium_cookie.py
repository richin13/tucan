###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Ali Shah ahshah@airpost.net
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

import urllib
import cookielib

from core.url_open import URLOpen


class PremiumCookie:
	""""""
	def get_cookie(self, user, password, url=None):
		""""""
		if user == None or password == None:
			return None

		cookie = cookielib.CookieJar()
		opener = URLOpen(cookie)
		encoded_str = urllib.urlencode({
				"password": password,
				"login"   : user,
				"rand"    : "", 
				"redirect": "",
				"op"      : "login"
				})

		opener.open("http://www.oron.com/login", encoded_str)
		if len(cookie) > 0:
			return cookie
