#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018-2023 dream-alpha
#
# In case of reuse of this source code please do not remove this copyright.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For more information on the GNU General Public License see:
# <http://www.gnu.org/licenses/>.


from time import time
from Components.Element import cached
from Components.Converter.Converter import Converter
from Poll import Poll


class COCEventTime(Poll, Converter):
	POSITION = 1
	REMAINING = 2

	def __init__(self, atype):
		Converter.__init__(self, atype)
		Poll.__init__(self)
		self.poll_interval = 1000
		self.poll_enabled = True
		args = atype.split(",")
		atype = args.pop(0)
		self.negate = "Negate" in args
		if atype == "Position":
			self.type = self.POSITION
		elif atype == "Remaining":
			self.type = self.REMAINING

	@cached
	def getText(self):
		text = ""
		event = self.source.event
		if event:
			value = 0
			start_time = event.getBeginTime()
			duration = event.getDuration()
			now = int(time())
			if self.type == self.REMAINING:
				value = start_time + duration - now
			elif self.type == self.POSITION:
				value = now - start_time
			mins = value / 60
			secs = value % 60
			if self.negate:
				mins *= -1
			text = "%+d:%02d" % (mins, secs)

		return text

	text = property(getText)
