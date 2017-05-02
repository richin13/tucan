###############################################################################
## Tucan Project
## Copyright (C) 2008-2011 Fran Lupion crak@tucaneando.com
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
				if 'fileInfo filename' in line:
					name = line.split('<strong>')[1].split('</strong>')[0]
				elif 'fileInfo filesize' in line:
					it.next()
					tmp = it.next().split('class="size">')[1].split("<")[0]
					if "KB" in tmp:
						size = int(round(float(tmp.split("KB")[0])))
						unit = "KB"
					elif "MB" in tmp:
						size = float(tmp.split("MB")[0])
						if int(round(size)) > 0:
							size = int(round(size))
							unit = "MB"
						else:
							size = int(round(1024 * size))
							unit = "KB"
					elif "GB" in tmp:
						size = int(round(float(tmp.split("GB")[0])))
						unit = "GB"
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
