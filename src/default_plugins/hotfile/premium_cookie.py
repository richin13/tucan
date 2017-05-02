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
import hashlib
from core.url_open import URLOpen
import logging
logger = logging.getLogger(__name__)

class PremiumCookie:
	""""""
	def __init__(self):
		""""""
		self.digestURL = URLOpen()

	def get_cookie(self, user, password, url=None):
		""""""
		if user == None or password == None:
			return None

		DigestURLHandler = self.digestURL.open('http://api.hotfile.com/?action=getdigest')
		
		# retrieve MD5 digest
		md5Digest = DigestURLHandler.readline()
		md5pw = hashlib.md5(password).hexdigest()
		md5pw = hashlib.md5(md5pw+md5Digest).hexdigest()
		return '&username='+user+'&passwordmd5dig='+md5pw+'&digest='+md5Digest
