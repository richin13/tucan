###############################################################################
## Tucan Project
##
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

import urllib

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://filefactory.com"
WAIT = 30 #Default, also parsed in the page if possible

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		#Remove the filename from the url
		tmp = url.split("/file/")[1].split("/")[0]
		url = "%s/file/%s" % (BASE_URL,tmp)

		link = None
		retry = 3
		try:
			opener = URLOpen()
			for line in opener.open(url):
				if 'check:' in line:
					check = line.split("check:'")[1].replace("'","").strip()
				elif "Recaptcha.create" in line:
					tmp = line.split('("')[1].split('"')[0]
					recaptcha_link = "http://www.google.com/recaptcha/api/challenge?k=%s" % tmp 
					if not wait_func():
						return
					c = Recaptcha(BASE_URL, recaptcha_link)
					while not link and retry:
						challenge, response = c.solve_captcha()
						if response:
							if not wait_func():
								return

							#Filefactory perfoms as check on its server by doing an
							#Ajax request sending the following data
							form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response), ("recaptcha_shortencode_field", "undefined"),("check", check)])
							url = "%s/file/checkCaptcha.php" % BASE_URL

							#Getting the result back, status:{"ok"|"fail"}
							for line in opener.open(url, form):
								if 'status:"ok"' in line:
									tmp = line.split('path:"')[1].strip('"')
									tmp_link = "%s%s" %(BASE_URL,tmp)
									for line in opener.open(tmp_link):
										if '<span class="countdown">' in line:
											#Try to get WAIT from the page
											try:
												tmp = line.split('"countdown">')[1].split("</span")[0]
												tmp = int(tmp)
											except ValueError:
												pass
											else:
												if tmp > 0:
													WAIT = tmp
										if "Download with FileFactory Basic" in line:
											link = line.split('<a href="')[1].split('"')[0]
											break
						retry -= 1
					break
			if link:
				if not wait_func(WAIT):
					return
				return opener.open(link, None, content_range, True)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if '/img/manager/mime/' in line:
					if ("generic" in line) or ("audio" in line) or ("archive" in line):
						tmp = line.split('/>')[1].split("</h1>")[0]
					if "video" in line:
						tmp = line.split('</a>')[1].split("<")[0]
						
					tmp = tmp.replace("&nbsp;","")
					tmp = tmp.replace("&#8203;","")
					name = tmp.replace("&#8203","")
					
				elif '<div id="info" class="metadata">' in line:
					tmp = it.next()
					tmp = tmp.split("<span>")[1].split("file")[0].strip()
					size = int(round(float(tmp.split(" ")[0])))
					unit = tmp.split(" ")[1].upper()
				elif 'Retry Download' in line:
					name = line.split('href="')[1].split('"')[0].split("/").pop()
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
