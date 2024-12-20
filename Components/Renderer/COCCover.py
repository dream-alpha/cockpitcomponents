#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018-2025 by dream-alpha
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


from enigma import ePixmap, gPixmapPtr, ePicLoad
from Components.Renderer.Renderer import Renderer
from Components.AVSwitch import AVSwitch


class COCCover(Renderer):
	GUI_WIDGET = ePixmap

	def __init__(self):
		self.skinAttributes = None
		Renderer.__init__(self)

	def destroy(self):
		Renderer.destroy(self)

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes
		for (attrib, value) in self.skinAttributes:
			if attrib == "type":
				self.type = value
				attribs.remove((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		if self.instance is not None:
			if what[0] != self.CHANGED_CLEAR:
				if self.source.cover:
					scale = AVSwitch().getFramebufferScale()
					size = self.instance.size()
					self.picload = ePicLoad()
					self.picload_conn = self.picload.PictureData.connect(self.displayPixmapCallback)
					self.picload.setPara((size.width(), size.height(), scale[0], scale[1], False, 1, "#ff000000"))
					self.picload.startDecodeBuffer(bytearray(self.source.cover), len(self.source.cover), False)
				else:
					self.instance.setPixmap(gPixmapPtr())
			else:
				self.instance.setPixmap(gPixmapPtr())

	def displayPixmapCallback(self, picinfo=None):
		if self.picload and picinfo:
			self.instance.setPixmap(self.picload.getData())
