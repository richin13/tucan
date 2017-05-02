###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2011 Elie Melois eliemelois@gmail.com
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
		if user and password:
			tmp_cookie = cookielib.Cookie(version=0, name='enc', value="", port=None, port_specified=False, domain='.filesonic.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=user, comment_url=password, rest={'HttpOnly': None}, rfc2109=False)
			cookie = cookielib.CookieJar()
			cookie.set_cookie(tmp_cookie)
			return cookie
