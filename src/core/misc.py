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
import time
import shutil
import urllib
import logging
logger = logging.getLogger(__name__)

import url_open
import cons
import shared
import traceback

REPORT_URL = "http://crak.appspot.com/add"

def remove_conf_dir():
	""""""
	if ".tucan" in cons.CONFIG_PATH:
		logging.shutdown()
		shutil.rmtree(cons.CONFIG_PATH)
	else:
		raise Exception("Failed to remove: %s" % cons.CONFIG_PATH)

def main_info(log=logger):
	""""""
	log.info("%s %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
	log.debug("OS: %s" %  cons.OS_VERSION)
	log.debug("PYTHON: %s" % cons.OS_PYTHON)
	log.debug("Main path: %s" % cons.PATH)
	log.debug("Configuration path: %s" % cons.CONFIG_PATH)

def report_log(email="", comment=""):
	""""""
	try:
		f = open(cons.LOG_FILE, "r")
		log = f.read()
		f.close()
	except Exception, e:
		logger.exception("%s" % e)
	else:
		form = urllib.urlencode([("uuid", shared.configuration.get_uuid()), ("email", email), ("comment", urllib.quote(comment)), ("log", urllib.quote(log))])
		try:
			id = url_open.URLOpen().open(REPORT_URL, form).read().strip()
			logger.info("REPORT ID: %s" % id)
		except Exception, e:
			logger.exception("Could not report: %s" % e)
		else:
			return id

def get_exception_info(type, value, trace):
	""""""

	try:
		return "".join(traceback.format_exception(type, value, trace))
	except:
		return "Unhandled Error! No info available"

def normalize(value, format="%.2f%s"):
	""""""
	if value:
		value = float(value)
		for unit in [cons.UNIT_B, cons.UNIT_KB, cons.UNIT_MB, cons.UNIT_GB]:
			if value < 1024:
				return format % (value, unit)
			else:
				value /= 1024

def get_size(num):
	""""""
	result = 0, cons.UNIT_KB
	if num:
		result = 1, cons.UNIT_KB
		tmp = int(num/1024)
		if  tmp > 0:
			result = tmp, cons.UNIT_KB
			tmp = int(tmp/1024)
			if tmp > 0:
				result = tmp, cons.UNIT_MB
	return result

def normalize_time(value):
	""""""
	if value:
		days, remainder = divmod(value, cons.TIME_DAY)
		hours, remainder = divmod(remainder, cons.TIME_HOUR)
		minutes, seconds = divmod(remainder, cons.TIME_MINUTE)
		if days:
			return "%.0fd%.0fh%.0fm%.0fs" % (days, hours, minutes, seconds)
		elif hours:
			return "%.0fh%.0fm%.0fs" % (hours, minutes, seconds)
		elif minutes:
			return "%.0fm%.0fs" % (minutes, seconds)
		else:
			return "%.0fs" % seconds

def calculate_time(time):
	""""""
	result = None
	hours = 0
	minutes = 0
	while time >= cons.TIME_HOUR:
		time = time - cons.TIME_HOUR
		hours += 1
	while time >= cons.TIME_MINUTE:
		time = time - cons.TIME_MINUTE
		minutes += 1
	seconds = time
	if hours > 0:
		result = str(hours) + "h" + str(minutes) + "m" + str(seconds) + "s"
	elif minutes > 0:
		result =  str(minutes) + "m" + str(seconds) + "s"
	elif seconds > 0:
		result = str(seconds) + "s"
	return result

def name_package():
	""""""
	return "package-%s" % time.strftime("%Y%m%d%H%M%S")
