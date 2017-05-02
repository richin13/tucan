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

#Uses plowshare py

import urllib
import logging
logger = logging.getLogger(__name__)

import Image
import ImageFile

from HTMLParser import HTMLParser
from url_open import URLOpen

from megaupload_captcha import new_image_from_pixels, combinations_no_repetition, get_pair_inclussion, smooth, join_images_horizontal, filter_word, floodfill_image, get_zones, center_of_mass, union_sets, segment, get_error, get_zones, histogram

from tesseract import Tesseract

CAPTCHACODE = "captchacode"
MEGAVAR = "megavar"


class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.located = False
		self.captcha = None
		self.captchacode = ""
		self.megavar = ""
		self.feed(data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "td":
			if self.get_starttag_text() == '<TD width="100" align="center" height="40">':
				self.located = True
		elif tag == "img":
			if self.located:
				self.located = False
				self.captcha = attrs[0][1]
		elif tag == "input":
			if attrs[1][1] == CAPTCHACODE:
				self.captchacode = attrs[2][1]
			elif attrs[1][1] == MEGAVAR:
				self.megavar = attrs[2][1]

class CaptchaForm(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.link = None
		self.located = False
		while not self.link:
			p = CaptchaParser(URLOpen().open(url).read())
			if p.captcha:
				handle = URLOpen().open(p.captcha)
				if handle.info()["Content-Type"] == "image/gif":
					self.data = handle.read()
					captcha = self.captcha_solve()
					if captcha:
						handle = URLOpen().open(url, urllib.urlencode([(CAPTCHACODE, p.captchacode), (MEGAVAR, p.megavar), ("captcha", captcha)]))
						self.reset()
						self.feed(handle.read())
						self.close()
						logger.info("Captcha %s: %s" % (p.captcha, captcha))

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ((self.located) and (attrs[0][0] == "href")):
				self.located = False
				self.link = attrs[0][1]
		elif tag == "div":
			if ((len(attrs) > 1) and (attrs[1][1] == "downloadlink")):
				self.located = True

	def rotate_character(self, pixels, index, rotation=22):
		"""Rotate captcha character in position index."""
		image = new_image_from_pixels(pixels, 1)
		angle = rotation * (+1 if (index % 2 == 0) else -1)
		rotated_image = image.rotate(angle, expand=True)
		return rotated_image.point(lambda x: 0 if x == 1 else 255)

	def build_candidates(self, characters4_pixels_list, uncertain_pixels):
		"""Build word candidates from characters and uncertains groups."""
		for plindex, characters4_pixels in enumerate(characters4_pixels_list):
			logging.debug("Generating words (%d) %d/%d" % (2**len(uncertain_pixels), plindex+1, len(characters4_pixels_list)))
			for length in range(len(uncertain_pixels)+1):
				for groups in combinations_no_repetition(uncertain_pixels, length):
					characters4_pixels_test = [x.copy() for x in characters4_pixels]
					for pixels in groups: 
						pair = get_pair_inclussion(characters4_pixels_test, center_of_mass(pixels)[0], pred=lambda x: center_of_mass(x)[0])
						if not pair:
							continue
						char1, char2 = pair
						char1.update(pixels)
						char2.update(pixels)

					images = [self.rotate_character(pixels, cindex) for cindex, pixels in enumerate(characters4_pixels_test)]
					clean_image = smooth(join_images_horizontal(images), 0)

					ocr = Tesseract(self.data, lambda x: clean_image)
					text = ocr.get_captcha().strip()

					filtered_text = filter_word(text)
					if filtered_text:
						yield filtered_text

	def captcha_solve(self, maxiterations=1):
		"""Basado en el algoritmo de plowshare"""
		p = ImageFile.Parser()
		p.feed(self.data)
		original = p.close()

		# Get background zone
		width, height = original.size
		image = Image.new("L", (width+2, height+2), 255)
		image.paste(original, (1, 1))
		background_pixels = floodfill_image(image, (0, 0), 155)[1]
		logging.debug("Background pixels: %d" % len(background_pixels))

		# Get characters zones    
		characters_pixels = sorted(get_zones(image, background_pixels, 0, 10),key=center_of_mass)
		logging.debug("Characters: %d - %s" % (len(characters_pixels), [len(x) for x in characters_pixels]))
		if len(characters_pixels) >= 4:
			characters_pixels_list0 = [[union_sets(sets) for sets in x] for x in segment(characters_pixels, 4)]
			characters4_pixels_list = sorted(characters_pixels_list0, key=lambda pixels_list: get_error(pixels_list, image))[:maxiterations]
			seen = reduce(set.union, [background_pixels] + characters_pixels)
			max_uncertain_groups = 8

			# Get uncertain zones
			uncertain_pixels = list(sorted(get_zones(image, seen, 255, 20), key=len))[:max_uncertain_groups]
			logging.debug("Uncertain groups: %d - %s" % (len(uncertain_pixels), [len(x) for x in uncertain_pixels]))

			#build candidates
			candidates = self.build_candidates(characters4_pixels_list, uncertain_pixels)

			# Return best decoded word    
			best = list(histogram(candidates, reverse=True))
			if not best:
				logging.info("No word candidates")
			else:
				logging.info("Best words: %s" % best[:5])    
				return best[0][0]

if __name__ == "__main__":
	c = CaptchaForm("http://www.megaupload.com/?d=RDAJ2PYH")
	print c.link
