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
import ctypes

import cons

class PidFile:
	""""""
	def __init__(self, file_name):
		""""""
		self.pid_file = file_name

	def start(self):
		""""""
		try:
			f = open(self.pid_file, "r")
			pid = int(f.read())
			f.close()
			if cons.OS_WINDOWS:
				if ctypes.windll.kernel32.OpenProcess(1, False, pid) > 0:
					return False
				else:
					return self.set_pid()
			else:
				os.kill(pid, 0)
		except:
			return self.set_pid()

	def set_pid(self):
		""""""
		try:
			f = open(self.pid_file, "w")
			f.write(str(os.getpid()))
			f.close()
		except:
			return False
		else:
			return True


	def destroy(self):
		""""""
		try:
			os.remove(self.pid_file)
		except:
			pass
