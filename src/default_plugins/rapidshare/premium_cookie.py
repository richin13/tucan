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

import urllib
import cookielib

from core.url_open import URLOpen

API_URL = "http://api.rapidshare.com/cgi-bin/rsapi.cgi"

class PremiumCookie:
	""""""
	def get_cookie(self, user, password, url=None):
		""""""
		opener = URLOpen()
		data = urllib.urlencode([("sub", "getaccountdetails_v1"), ("type", "prem"), ("login", user), ("password", password), ("withcookie", 1)])
		for line in opener.open(API_URL, data).readlines():
			if "ERROR" in line:
				return
			elif "cookie" in line:
				tmp_cookie = cookielib.Cookie(version=0, name='enc', value=line.split("=")[1].strip(), port=None, port_specified=False, domain='.rapidshare.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
				cookie = cookielib.CookieJar()
				cookie.set_cookie(tmp_cookie)
				return cookie
