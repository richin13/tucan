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

import threading
import logging
logger = logging.getLogger(__name__)

import cons

MAX_SINGLE_CHECK = 2

LINKS = {'4shared.com': ['http://www.4shared.com/file/90502048/dec68d50/AIEW_09.html', 'http://www.4shared.com/file/88730971/dcc20011/01-_DJ_kairuz__Salta_-_Capital__By_Dj_isaco__GuilloteMix.html', 'http://www.4shared.com/file/88733068/a1611d95/02-_DJ_MAK__Salta_-_Capital__By_Dj_isaco__GuilloteMix.html', 'http://www.4shared.com/file/88838353/398f1c53/03-_DJ_MAGO__Caleta_Olivia_-_Santa_Cruz_.html'], 'megaupload.com': ['http://www.megaupload.com/?d=2OOV9OJ3', 'http://www.megaupload.com/?d=RDAJ2PYH', 'http://www.megaupload.com/?d=7H602RK1', 'http://www.megaupload.com/?d=9CO71ZFB'], 'sendspace.com': ['http://www.sendspace.com/file/x1itz8', 'http://www.sendspace.com/file/lpd6p3'], 'filefactory.com': ['http://www.filefactory.com/file/4460d3/n/Intelligent_Sounds_Music_BazzISM_VSTi_v2_0d_MAC_OSX_UB_Incl_Keygen-ArCADE_rar', 'http://www.filefactory.com/file/574c35/n/SM_Music_1_pm_txt', 'http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi'], 'zshare.net': ['http://www.zshare.net/download/58856573188bda3b/', 'http://www.zshare.net/image/59597487e1eaa2ec/'], 'uploading.com': ['http://uploading.com/files/mqj6tlcw/roxy_music_-_avalon.mp3.html', 'http://uploading.com/files/sye0ha4g/john_miles_-_music.mp3.html'], 'unsupported': ['http://www.gigasize.com/get.php?d=726jhznl0pc', 'http://www.badongo.com/file/2038549', 'http://www.badongo.com/file/14020041', 'http://www.badongo.com/file/8765848'], 'mediafire.com': ['http://www.mediafire.com/download.php?0zhaznzw3oz', 'http://www.mediafire.com/download.php?d4j2nyyr4qy', 'http://www.mediafire.com/download.php?z0gjmnwk1d0', 'http://www.mediafire.com/download.php?4ttzlmazj2g'], 'hotfile.com': ['http://hotfile.com/dl/13746086/7c9e740/Californication.S03E01.FQM.cHoPPaHoLiK.avi', 'http://hotfile.com/dl/37208850/d185f13/_Tomoetenbu_-_Wise_Ass.part1.rar.html'], 'rapidshare.com': ['http://rapidshare.com/files/28369474/30_-_Buscate_la_Vida_-_Novia_2000_by_shagazz.part1.exe', 'http://rapidshare.com/files/28374629/30_-_Buscate_la_Vida_-_Novia_2000_by_shagazz.part2.rar'], 'depositfiles.com': ['http://depositfiles.com/files/939zt4eya', 'http://depositfiles.com/files/3826244', 'http://depositfiles.com/files/hh5emnb1c'], 'easy-share.com': ['http://www.easy-share.com/1903816814/Frank%20Gehry%20-%20The%20City%20and%20the%20Music.pdf', 'http://www.easy-share.com/1699551079.html']}

class LinkDispatcher:
	""""""
	def __init__(self, sorted_links, get_check):
		""""""
		self.cancel_flag = False
		shared.events.connect(cons.EVENT_CHECK_CANCEL, self.cancel_check)
		for service, links in sorted_links.items():
			th = threading.Thread(group=None, target=self.threaded_check, name=None, args=(service, links, get_check))
			th.start()

	def threaded_check(self, service, links, get_check_links):
		""""""
		check_links, plugin_type, max_single_check = get_check_links(service)
		#mover la funcionalidad de cancelar y del limite a download_plugin
		for max_links in [links[i:max_single_check+i] for i in range(0, len(links), max_single_check)]:
			if self.cancel_flag:
				return
			else:
				for link, (name, size, unit) in check_links(max_links).items():
					shared.events.trigger_link_checked(service, link, name, size, unit, plugin_type)
		shared.events.trigger_check_completed(service)

	def cancel_check(self):
		""""""
		self.cancel_flag = True

if __name__ == "__main__":
	import random
	import time
	import shared
	from events import Events
	
	logging.basicConfig(level=logging.DEBUG)
	shared.events = Events()
	
	def check_links(links):
		result = {}
		m = random.randint(2, 15)
		time.sleep(m)
		for link in links:
			result[link] = (link, m, "KB")
		return result

	l = LinkDispatcher(LINKS, lambda x: (check_links, "PREMIUM", MAX_SINGLE_CHECK))
	time.sleep(10)
	shared.events.trigger_check_cancel()