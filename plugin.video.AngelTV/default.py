#   Copyright (C) 2017 Lunatixz
#
#
# This file is part of filmriseTV.
#
# filmriseTV is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# filmriseTV is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with filmriseTV.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import os, sys
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

# Plugin Info
ADDON_ID = 'plugin.video.AngelTV'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
ADDON_PATH = (REAL_SETTINGS.getAddonInfo('path').decode('utf-8'))
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
SETTINGS_LOC = REAL_SETTINGS.getAddonInfo('profile')
ICON = REAL_SETTINGS.getAddonInfo('icon')
FANART = REAL_SETTINGS.getAddonInfo('fanart')

def start():
    addDir(
        title="Ich geh Angeln",
        url="plugin://plugin.video.youtube/user/ichgehangelnde/")
    addDir(
        title="BissclipsTV",
        url="plugin://plugin.video.youtube/user/bissclipstvvideos/")
    addDir(
        title="Big Fish Media",
        url="plugin://plugin.video.youtube/channel/UCoS9uIhvCzfNMV_rEphWMsQ/")
    addDir(
        title="Babs World of Fishing",
        url="plugin://plugin.video.youtube/channel/UCvc-QVUyrKUVaxZaVQB8QSQ/")
    addDir(
        title="Big L Fishing",
        url="plugin://plugin.video.youtube/channel/UClfc5w-snHQh9g_NkM3hfsA/")
    addDir(
        title="Benni Angelt",
        url="plugin://plugin.video.youtube/channel/UCspkmsdBbnkc_7L-gl1kIXg/")
    addDir(
        title="Catchtastic",
        url="plugin://plugin.video.youtube/channel/UC8x1YQ4D4NsO2yERA4SbVrA/")
    addDir(
        title="JM Angeln",
        url="plugin://plugin.video.youtube/channel/UCMq-1kxw85KCwgmiwuuP4iQ/")
    addDir(
        title="Matze Wendt",
        url="plugin://plugin.video.youtube/channel/UCuKffkk4A-E6m0Moiwi0-TA/")
    addDir(
        title="Angeln ist so",
        url="plugin://plugin.video.youtube/channel/UC7CIT2H7DeEbBYVVYSPalLw/")
    addDir(
        title="Angeln am Teich TV",
        url="plugin://plugin.video.youtube/channel/UCxzZteAGD0KJp438FcnZXpQ/")
    addDir(
        title="Carsten Zeck",
        url="plugin://plugin.video.youtube/channel/UC8QfAnvZ4ID49JrOjW3_YdA/")
    addDir(
        title="AnglerboardTV",
        url="plugin://plugin.video.youtube/channel/UCg8gcYhqJjTqMguHf9s-PLw/")
    addDir(
        title="South Florida Fishing Channel",
        url="plugin://plugin.video.youtube/channel/UCjzjlGDXx28Gkl4nY8uUnrA/")
    addDir(
        title="Catch em All Fishing",
        url="plugin://plugin.video.youtube/channel/UC7MCFUG5oKKsfVDl7gT7BRA/")
    addDir(
        title="BlacktipH",
        url="plugin://plugin.video.youtube/user/BlacktipH/")
    addDir(
        title="JohnB",
        url="plugin://plugin.video.youtube/user/j0j0barz33/")
    addDir(
        title="Milliken Fishing",
        url="plugin://plugin.video.youtube/channel/UCdJs_Dva2m2OT014oB1zWlg/")
    addDir(
        title="SB Fishing TV",
        url="plugin://plugin.video.youtube/channel/UCflF6NDw0Q-S2MCLTpkNl-g/")
    addDir(
        title="Fishermans Life",
        url="plugin://plugin.video.youtube/channel/UCC7WFw42VnywQRvewSq29eg/")
    addDir(
        title="Joshinator",
        url="plugin://plugin.video.youtube/channel/UCrWjed7AJjBM_2HkkhbBGQA/")
    addDir(
        title="Fisch und Fang",
        url="plugin://plugin.video.youtube/channel/UCFNOZMo54_hdulbrXxHndJA/")
    addDir(
        title="Topwater Production",
        url="plugin://plugin.video.youtube/user/TopwaterProductions/")
    addDir(
        title="CatchMagazin",
        url="plugin://plugin.video.youtube/channel/UCHUXPkQosjVxl8rt8hzbTNw/")
    addDir(
        title="Fishing Bros",
        url="plugin://plugin.video.youtube/channel/UCQXQOX_wfx2Rvnw6BQZMTGg/")
    addDir(
        title="Benjamin Gruender",
        url="plugin://plugin.video.youtube/channel/UCuplNyAXGCVmIX-4oZkM-0g/")
    addDir(
        title="JenziPerformance",
        url="plugin://plugin.video.youtube/channel/UCJ9kqRAgj5s5bEDFgFbbZKg/")
    addDir(
        title="YouFishTV",
        url="plugin://plugin.video.youtube/channel/UCUUU29AwqBBdItwah3CfbDQ/")
    addDir(
        title="Fishing King",
        url="plugin://plugin.video.youtube/channel/UC7NGBAnSF1y0NIr97lLF_ow/")
    addDir(
        title="Realfishing",
        url="plugin://plugin.video.youtube/channel/UC6J0JwxHlr4qOVBxDGV9NjA/")
    addDir(
        title="Quantum Fishing Europe",
        url="plugin://plugin.video.youtube/channel/UCLNxO2CSMFkYFicPJ--Q5ZQ/")
    addDir(
        title="Zandidos Fishing Channel",
        url="plugin://plugin.video.youtube/channel/UC4oMyLrQ3qmDi-LfC6i-sew/")
    addDir(
        title="SaengerTV",
        url="plugin://plugin.video.youtube/channel/UC5qMeNdwVmA0jkD18-325Cg/")
    addDir(
        title="Stefan Seuss",
        url="plugin://plugin.video.youtube/user/wallerseuss/")
    
def addDir(title, url):
    liz=xbmcgui.ListItem(title)
    liz.setProperty('IsPlayable', 'false')
    liz.setInfo(type="Video", infoLabels={"label":title,"title":title} )
    liz.setArt({'thumb':ICON,'fanart':FANART})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
    
start()
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
