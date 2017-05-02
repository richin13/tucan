###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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
import cookielib
logger = logging.getLogger(__name__)

import urllib

import ImageOps

from core.tesseract import Tesseract
from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

import time

WAIT = 60 #Default, also parsed in the page if possible
BASE_URL = "http://www.badongo.com"
JS_URL = "/ajax/prototype/ajax_api_filetemplate.php"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			link = [] #One link at the end is in two parts
			captcha_url = None
			wait = WAIT
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			if not wait_func():
				return
			#Get the captcha url
			data = urllib.urlencode([("rs", "refreshImage"), ("rst", ""), ("rsrnd", int(time.time()))])
			tmp = opener.open(url, data).read().split("+:var res = '")[1].split("'; res;")[0].replace('\\"', '"')
			form_action = tmp.split('action="')[1].split('"')[0]
			cap_id = tmp.split('name=cap_id value=')[1].split('>')[0]
			cap_secret = tmp.split('name=cap_secret value=')[1].split('>')[0]
			captcha_url = "%s%s" % (BASE_URL, tmp.split('img src="')[1].split('"')[0])

			if captcha_url:
				solved = False
				cont = 0
				while (not solved) and cont < 4:
					tes = Tesseract(opener.open(captcha_url).read(), self.filter_image)
					captcha = tes.get_captcha()
					#Crack trick to optimize the OCR
					if len(captcha) == 4 and captcha.isalnum():
					
						if not captcha.isalpha():
							for i, j in [("0", "O"),("1", "I"),("2", "Z"),("3", "B"),("4", "A"),("5", "S"),("6", "G"),("7", "T"),("8", "B"),("9", "B")]:
								captcha = captcha.replace(i,j)
								
					captcha = captcha.upper()
					#Captcha : 4 letters
					if len(captcha) == 4 and captcha.isalpha():
						if not wait_func():
							return
						logger.info("Captcha: %s" % captcha)
						
						data = urllib.urlencode([("user_code", captcha), ("cap_id",cap_id), ("cap_secret",cap_secret)])
						
						it = opener.open(form_action, data)
						z = None
						h = None
						for line in it:
							if "'z':'I!" in line:
								z = line.split("'z':'")[1].split("'")[0]
								h = line.split("'h':'")[1].split("'")[0]
							elif 'window.location.href = dlUrl' in line:
								it.next()
								link.append(it.next().split('"')[1].split('"')[0])
								solved = True #If there is this line, the captcha is good
								break

						cont += 1
						
						#If the captcha is good
						if solved and z and h:
							logger.info("Good captcha")
							if not wait_func():
								return
							data = urllib.urlencode([("id",form_action.split("/")[-1]), ("type","file"), ("ext",""),("f","download:init"),("z","zvar"),("h","hvar")])
							data = data.replace("zvar",z).replace("hvar",h)
							#The referer needs to be specify
							res = opener.open("%s%s" % (BASE_URL,JS_URL), data,None,True,form_action)
							t = None
							wait = None
							z = None
							h = None
							for line in res:
								if "'z'" in line:
									z = line.split("'z': '")[1].split("'")[0]
								elif "'h'" in line:
									h = line.split("'h': '")[1].split("'")[0]
								elif "'t'" in line:
									t = line.split("'t': '")[1].split("'")[0]
								elif "check_n" in line:
									wait = int(line.split('[\'check_n\'] = "')[1].split('"')[0])

							if not wait:
								wait = WAIT
						
							if not wait_func(wait):
								return
							
							data = urllib.urlencode([("id",form_action.split("/")[-1]), ("type","file"), ("ext",""),("f","download:check"),("z","zvar"),("h","hvar"),("t",t)])
							data = data.replace("zvar",z).replace("hvar",h)
						
							res = opener.open("%s%s" % (BASE_URL,JS_URL), data,None,True,form_action)
						
							t = None
							z = None
							h = None
							#Sometimes it sends another check_n
							while True:
								if not wait_func():
									return
								res = opener.open("%s%s" % (BASE_URL,JS_URL), data,None,True,form_action)
								wait = None
								for line in res:
									if "check_n" in line:
										wait = int(line.split("=")[1].split(";")[0])
										break
									elif "'z'" in line:
										z = line.split("'z': '")[1].split("'")[0]
									elif "'h'" in line:
										h = line.split("'h': '")[1].split("'")[0]
									elif "'t'" in line:
										t = line.split("'t': '")[1].split("'")[0]
								if not wait:
									break
								else:
									if not wait_func(wait):
										return
										
							if not wait_func():
								return
							
							data = urllib.urlencode([("rs","getFileLink"),("rst",""),("rsrnd",int(time.time())),("rsargs[]","0"),("rsargs[]","yellow"),("rsargs[]","zvar"),("rsargs[]","hvar"),("rsargs[]",t),("rsargs[]","file"),("rsargs[]",form_action.split("/")[-1]),("rsargs[]","")])
							data = data.replace("zvar",z).replace("hvar",h)
							
							#This cookie needs to be added manually
							gflcur = cookielib.Cookie(version=0, name='_gflCur', value='0', port=None, port_specified=False, domain='www.badongo.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
							cookie.set_cookie(gflcur)
						
							res = opener.open(form_action, data,None,True,form_action).readlines()
							tmp = res[0].split('onclick')[2].split('(')[1].split("')")[0].replace('\\','').strip("'")
							link.append(tmp)
							
							if not wait_func():
								return
								
							url = "%s%s?zenc=" %(link[1],link[0])
							res = opener.open(url, data,None,True,form_action)
						
							for line in res:
								if "window.location.href = '" in line:
									final_url = line.split("window.location.href = '")[1].split("'")[0]
									break
							return opener.open("%s%s" % (BASE_URL,final_url), data,content_range,True,url)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = 0
		try:
			it = URLOpen().open(url)
			for line in it:
				if '<div class="finfo">' in line:
					name = line.split('>')[1].split('<')[0].strip()
				if '<div class="ffileinfo">' in line:
					tmp = line.split(":")[2].split("<")[0]
					unit = tmp[-2:]
					size = int(round(float(tmp[:-2].strip())))
					
					if size > 1024:
						if unit == "KB":
							size = size / 1024
							unit = "MB"
					break
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
		
	def filter_image(self, image):
		""""""
		image = ImageOps.grayscale(image)
		image = image.point(self.filter_pixel)
		return image

	def filter_pixel(self, pixel):
		""""""
		if pixel > 85:
			return 255
		else:
			return 1
