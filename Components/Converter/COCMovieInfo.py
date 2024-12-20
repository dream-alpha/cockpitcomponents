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


from Components.Element import cached, ElementError
from Components.Converter.Converter import Converter
from enigma import iServiceInformation
from ServiceReference import ServiceReference


class COCMovieInfo(Converter):
	MOVIE_SHORT_DESCRIPTION = 0  # meta description when available.. when not .eit short description
	MOVIE_META_DESCRIPTION = 1  # just meta description when available
	MOVIE_REC_SERVICE_NAME = 2  # name of recording service
	MOVIE_REC_FILESIZE = 3  # filesize of recording
	MOVIE_EVENT_DURATION = 4  # duration of recorded event

	def __init__(self, atype):
		if atype == "ShortDescription":
			self.type = self.MOVIE_SHORT_DESCRIPTION
		elif atype == "MetaDescription":
			self.type = self.MOVIE_META_DESCRIPTION
		elif atype == "RecordServiceName":
			self.type = self.MOVIE_REC_SERVICE_NAME
		elif atype == "FileSize":
			self.type = self.MOVIE_REC_FILESIZE
		elif atype == "MovieDuration":
			self.type = self.MOVIE_EVENT_DURATION
		else:
			raise ElementError("'%s' is not <ShortDescription|MetaDescription|RecordServiceName|FileSize|MovieDuration> for MovieInfo converter" % type)
		Converter.__init__(self, atype)

	@cached
	def getText(self):
		text = ""
		service = self.source.service
		info = self.source.info
		if info and service:
			if self.type == self.MOVIE_EVENT_DURATION:
				event = self.source.event
				if event:
					text = str(event.getDuration())
			if self.type == self.MOVIE_SHORT_DESCRIPTION:
				event = self.source.event
				if event:
					text = info.getInfoString(service, iServiceInformation.sDescription)
					if text == "":
						text = event.getShortDescription()
			elif self.type == self.MOVIE_META_DESCRIPTION:
				text = info.getInfoString(service, iServiceInformation.sDescription)
			elif self.type == self.MOVIE_REC_SERVICE_NAME:
				rec_ref_str = info.getInfoString(service, iServiceInformation.sServiceref)
				text = ServiceReference(rec_ref_str).getServiceName()
			elif self.type == self.MOVIE_REC_FILESIZE:
				filesize = info.getInfoObject(service, iServiceInformation.sFileSize)
				if filesize is not None:
					filesize /= 1024 * 1024
					if filesize > 0:
						if filesize < 1000:
							text = "%d MB" % filesize
						else:
							text = "%d GB" % (filesize / 1024)
		return text

	text = property(getText)

	@cached
	def getTime(self):
		duration = 0
		event = self.source.event
		if event:
			duration = event.getDuration()
		return duration

	time = property(getTime)
