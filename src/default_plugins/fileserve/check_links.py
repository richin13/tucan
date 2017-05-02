###############################################################################
## Tucan Project
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

from core.url_open import URLOpen

class CheckLinks():
	""""""
	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if '"panel file_download"' in line:
					it.next()
					name = it.next().split(">")[1].split("<")[0]
					it.next()
					tmp = it.next().split("<strong>")[1].split("<")[0]
					unit = tmp[-2:]
					#Fix me : GB bug
					if unit == "GB":
						size = int(1024*float(tmp[:-2]))
						unit = "MB"
					else:
						size = int(round(float(tmp[:-2])))
					
					if size > 1024:
						if unit == "KB":
							size = size / 1024
							unit = "MB"
					break
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
