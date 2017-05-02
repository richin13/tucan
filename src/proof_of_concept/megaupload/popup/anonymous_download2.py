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

import sys
import subprocess
import os.path
import pickle
import logging
logger = logging.getLogger(__name__)

if "win" not in sys.platform:
	#from captcha import CaptchaForm, CheckLinks
	from captcha2 import CaptchaSolve, CheckLinks

from download_plugin import DownloadPlugin
from slots import Slots

import cons

WAIT = 45

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)

	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			if "win" in sys.platform:
				data = None
				try:
					subprocess.call([os.path.join(sys.path[0], "captcha.exe"), link], creationflags=134217728)
					f = open(os.path.join(cons.PLUGIN_PATH, "megaupload", "link.dat"), "rb")
					data = pickle.loads(f.read())
					f.close()
					f = open(os.path.join(cons.PLUGIN_PATH, "megaupload", "link.dat"), "wb")
					f.write("\n")
					f.close()
				except Exception, e:
					logger.exception("Download %s: %s" % (url, e))
				else:	
					if data:
						return self.start(path, data, file_name, WAIT)
					else:
						self.return_slot()
			else:
				parser = CaptchaSolve(link)
				if parser.link:
					return self.start(path, parser.link, file_name, WAIT)
				else:
					 self.return_slot()

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			logger.info("Stopped %s: %s" % (file_name, self.return_slot()))

	def check_links(self, url):
		""""""
		if "win" in sys.platform:
			try:
				subprocess.call([os.path.join(sys.path[0], "captcha.exe"), url, "check"], creationflags=134217728)
				f = open(os.path.join(cons.PLUGIN_PATH, "megaupload", "check.dat"), "rb")
				data = pickle.loads(f.read())
				f.close()
				f = open(os.path.join(cons.PLUGIN_PATH, "megaupload", "check.dat"), "wb")
				f.write("\n")
				f.close()
				name = data[0] 
				size = int(data[1])
				unit = data[2]
			except Exception, e:
				name = url
				size = -1
				unit = None
				logger.exception("Check %s: %s" % (url, e))
			return name, size, unit
		else:
			return CheckLinks().check(url)
