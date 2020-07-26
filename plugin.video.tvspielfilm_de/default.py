﻿# -*- coding: utf-8 -*-

'''
    Copyright (C) 2020 realvito

    TV Spielfilm - Das Beste aus den Mediatheken

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from resources.lib.common import *
from resources.lib import navigator


def run():
	if mode == 'root':
		navigator.mainMenu()
	elif mode == 'listChannel':
		navigator.listChannel(url)
	elif mode == 'listVideos_HighDayChannel':
		navigator.listVideos_HighDayChannel(url)
	elif mode == 'listVideos_Genre':
		navigator.listVideos_Genre(url)
	elif mode == 'playVideo':
		navigator.playVideo(url)
	elif mode == 'AddToQueue':
		navigator.AddToQueue()
	elif mode == 'aSettings':
		navigator.addon.openSettings()

run()
