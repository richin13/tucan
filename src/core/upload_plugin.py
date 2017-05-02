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

import os
import logging
logger = logging.getLogger(__name__)

from uploader import Uploader

import cons

class UploadPlugin:
	""""""
	def __init__(self, max_size=0):
		""""""
		self.max_size = max_size

	def parse(self, path):
		""""""
		pass
	
	def parse_result(self, handler):
		""""""
		pass

	def process(self, item):
		""""""
		return Uploader(item, self.parse, self.parse_result)

	def check_files(self, file_list):
		""""""
		result = []
		for path in file_list:
			check = False
			if os.path.exists(path) and os.path.isfile(path):
				if not self.max_size or self.max_size > os.stat(path).st_size:
					check = True
				else:
					logger.warning("File too big: %s" % path)
			else:
				logger.error("Invalid file: %s" % path)
			result.append(check)
		return result
