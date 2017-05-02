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
import time
import logging
logger = logging.getLogger(__name__)

from ConfigParser import SafeConfigParser

import cons
import shared

HISTORY = "tucan.history"

#main options
OPTION_PLAYED = "played"
OPTION_DATE = "date"
OPTION_NAME = "name"
OPTION_LINK = "link"
OPTION_SIZE = "size"

class History(SafeConfigParser):
	""""""
	def __init__(self):
		""""""
		SafeConfigParser.__init__(self)
		if not os.path.exists(cons.CONFIG_PATH + HISTORY):
			self.save()
		self.read(cons.CONFIG_PATH + HISTORY)
		self.id = len(self.sections())
		shared.events.connect(cons.EVENT_FILE_COMPLETE, self.add_history)

	def get_all(self):
		""""""
		total_size = 0.0
		unit = cons.UNIT_MB
		history = []
		try:
			tmp = [int(s) for s in self.sections()]
			tmp.sort()
			for section in [str(s) for s in tmp]:
				played = self.getboolean(section, OPTION_PLAYED)
				date = self.get(section, OPTION_DATE)
				name = self.get(section, OPTION_NAME)
				size = self.get(section, OPTION_SIZE)
				tmp_size, tmp_unit = size.split(" ")
				if tmp_unit == cons.UNIT_MB:
					total_size += float(tmp_size)
				elif tmp_unit == cons.UNIT_GB:
					total_size += float(tmp_size)*1024
				elif tmp_unit == cons.UNIT_KB:
					total_size += float(tmp_size)/1024
				link = self.get(section, OPTION_LINK)
				history.append((section, played, link, date, name, size))
			if total_size > 1024:
				total_size /= 1024
				unit = cons.UNIT_GB
		except Exception, e:
			logger.error("Could not get history: %s" % e)
		return "%.2f %s" % (total_size, unit), len(tmp), history

	def set_played(self, id, value):
		""""""
		if self.has_section(id):
			self.set(id, OPTION_PLAYED, str(value))
			self.save()

	def add_history(self, name, size, unit, links):
		id = str(self.id)
		self.id += 1
		self.add_section(id)
		self.set(id, OPTION_PLAYED, "False")
		self.set(id, OPTION_DATE, time.strftime("%Y-%m-%d"))
		self.set(id, OPTION_NAME, name)
		self.set(id, OPTION_SIZE, "%i %s" % (size, unit))
		for link in links:
			if link.active:
				self.set(id, OPTION_LINK, link.url.replace("%","%%"))
				break
		self.save()

	def save(self):
		""""""
		f = open(cons.CONFIG_PATH + HISTORY, "w")
		self.write(f)
		f.close()

if __name__ == "__main__":
	from events import Events
	shared.events = Events()
	c = History()
	shared.events.trigger_file_complete("puta", 323, "MB", "megaupload.com")
	c.set_played("5", True)
	print c.get_all()
