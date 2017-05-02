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
import logging
logger = logging.getLogger(__name__)

from core.url_open import URLOpen
from core.misc import get_size

import core.cons as cons

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			id = [id for id in url.split("d=")][1].strip()
			if "&" in id:
				id = id.split("&")[0]
			tmp = URLOpen().open("http://www.megaupload.com/mgr_linkcheck.php", urllib.urlencode([("id0", id)])).read().split("&", 5)
			if len(tmp) > 4:
				name = tmp[5].split("n=")[1]
				size, unit = get_size(int(tmp[3].split("s=")[1]))
		except Exception, e:
			logger.exception(e)
		return name, size, unit
