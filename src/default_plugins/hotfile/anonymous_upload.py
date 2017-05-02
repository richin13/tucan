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

import uuid
import time
import random
import logging
logger = logging.getLogger(__name__)

from core.upload_plugin import UploadPlugin
from core.url_open import URLOpen, MultipartEncoder

API_URL = "http://www.hotfile.com/"

MAX_SIZE = 209796096

class AnonymousUpload(UploadPlugin):
	""""""
	def __init__(self):
		""""""
		UploadPlugin.__init__(self, MAX_SIZE)

	def parse(self, path):
		""""""
		tmp = URLOpen().open(API_URL)
		if tmp:
			url = None
			for line in tmp:
				if 'multipart/form-data' in line:
					url = line.split('action="')[1].split('"')[0]
			if url:
				form = {"uploads[]": open(path, "rb")}
				return MultipartEncoder(url, form, None)

	def parse_result(self, handler):
		""""""
		for line in handler.readlines():
			if 'name="url"' in line:
				return line.split('value="')[1].split('"')[0]
