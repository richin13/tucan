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

from base_types import Base

class Link(Base):
	""""""
	def __init__(self, url, service):
		""""""
		Base.__init__(self, url)
		self.active = False
		self.service = service

	def set_active(self, active=True):
		""""""
		self.active = active

	def get_active(self):
		""""""
		return self.active

	def get_url(self):
		""""""
		return self.name

	def get_service(self):
		""""""
		return self.service
