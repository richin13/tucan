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

API_URL = "%supload_done.php?UPLOAD_IDENTIFIER=%s&user=undefined&s=%s"

MAX_SIZE = 209796096

class AnonymousUpload(UploadPlugin):
	""""""
	def __init__(self):
		""""""
		UploadPlugin.__init__(self, MAX_SIZE)

	def parse(self, path):
		""""""
		tmp = URLOpen().open("http://www.megaupload.com/")
		if tmp:
			server = None
			for line in tmp:
				if 'flashvars.server = "' in line:
					server = line.split('"')[1].split('"')[0]
			if server:
				identifier = "".join([str(random.randint(0,9)) for i in range(32)])
				s = "".join([str(random.randint(0,9)) for i in range(5)])
				url = API_URL % (server, identifier, s)
				form = {"message" : "desc", "Filedata": open(path, "rb")}
				return MultipartEncoder(url, form, None)

	def parse_result(self, handler):
		""""""
		for line in handler.readlines():
			if 'parent.downloadurl' in line:
				return line.split("'")[1].split("'")[0]
