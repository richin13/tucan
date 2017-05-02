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

API_URL = "http://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=nextuploadserver_v1&cbf=RSAPIDispatcher&cbid=1"

MAX_SIZE = 209796096

class AnonymousUpload(UploadPlugin):
	""""""
	def __init__(self):
		""""""
		UploadPlugin.__init__(self, MAX_SIZE)

	def parse(self, path):
		""""""
		tmp = URLOpen().open(API_URL).read()
		if tmp:
			#uploadid = str(int(time.time()))[-5:] + str(int(round(random.random()*1000000)))
			uploadid = "%s%i" % (str(int(time.time()))[-5:], random.randint(10000, 1000000))
			server = tmp.split('"')[1].split('"')[0]
			url = "http://rs%sl3.rapidshare.com/cgi-bin/upload.cgi?rsuploadid=%s" % (server,uploadid)
			form = {"rsapi_v1" : "1", "realfolder" : "0" , "filecontent": open(path, "rb")}
			#rapidshare boundary handler has a bug
			boundary = "--%s" % uuid.uuid4().hex
			return MultipartEncoder(url, form, boundary)

	def parse_result(self, handler):
		""""""
		for line in handler.readlines():
			if 'File1.1=' in line:
				return line.split('File1.1=')[1].strip()
