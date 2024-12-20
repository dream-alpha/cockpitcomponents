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


from Components.Element import cached
from Components.Sources.Source import Source


class COCDiskSpace(Source):
	def __init__(self, player):
		Source.__init__(self)
		self.__player = player

	@cached
	def getDiskSpace(self):
		return self.__player.getBookmarksSpaceInfo()

	space = property(getDiskSpace)
