# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import platform
import json
import socket
import time
from datetime import datetime, timedelta
import io
import gzip
PY2 = sys.version_info[0] == 2
if PY2:
	from urllib import urlencode, quote_plus, unquote_plus  # Python 2.X
	from urllib2 import urlopen, build_opener  # Python 2.X
else:
	from urllib.parse import urlencode, quote_plus, unquote_plus  # Python 3+
	from urllib.request import urlopen, build_opener  # Python 3+
	from functools import reduce  # Python 3+


global debuging
socket.setdefaulttimeout(30)
HOST_AND_PATH       = sys.argv[0]
ADDON_HANDLE         = int(sys.argv[1])
dialog                             = xbmcgui.Dialog()
addon                             = xbmcaddon.Addon()
addon_id                        = addon.getAddonInfo('id')
addon_name                 = addon.getAddonInfo('name')
addon_version              = addon.getAddonInfo('version')
addonPath                     = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath                         = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
defaultFanart                 = os.path.join(addonPath, 'fanart.jpg')
icon                                  = os.path.join(addonPath, 'icon.png')
artpic                                = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
prefSTREAM                    = addon.getSetting('streamSelection')
showDATE                       = addon.getSetting("enableDatetitle") == 'true'
showCHANNEL               = addon.getSetting('enableChannelID') == 'true'
showNOW                       = addon.getSetting('enableTVnow')
useThumbAsFanart       = addon.getSetting('useThumbAsFanart') == 'true'
enableAdjustment         = addon.getSetting('show_settings') == 'true'
DEB_LEVEL                      = (xbmc.LOGNOTICE if addon.getSetting('enableDebug') == 'true' else xbmc.LOGDEBUG)
BASE_URL                        = 'https://www.tvspielfilm.de'
API_ZDF                           = 'https://api.zdf.de'

xbmcplugin.setContent(ADDON_HANDLE, 'tvshows')

def py2_enc(s, encoding='utf-8'):
	if PY2:
		if not isinstance(s, basestring):
			s = str(s)
		s = s.encode(encoding) if isinstance(s, unicode) else s
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if not PY2 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def translation(id):
	return py2_enc(addon.getLocalizedString(id))

def failing(content):
	log(content, xbmc.LOGERROR)

def debug_MS(content):
	log(content, DEB_LEVEL)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	return xbmc.log('[{0} v.{1}]{2}'.format(addon_id, addon_version, msg), level)

def build_url(query):
	return '{0}?{1}'.format(HOST_AND_PATH, urlencode(query))

def get_userAgent():
	base = 'Mozilla/5.0 {0} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
	system = platform.system()
	# Mac OSX
	if system == 'Darwin':
		return base.format('(Macintosh; Intel Mac OS X 10_10_1)')
	# Windows
	if system == 'Windows':
		return base.format('(Windows NT 10.0; WOW64)')
	# ARM based Linux
	if platform.machine().startswith('arm'):
		return base.format('(X11; CrOS armv7l 7647.78.0)')
	# x86 Linux
	return base.format('(X11; Linux x86_64)')

def getUrl(url, header=None, data=None, agent=get_userAgent()):
	opener = build_opener()
	opener.addheaders = [('User-Agent', agent), ('Accept-Encoding', 'gzip, identity')]
	try:
		if header: opener.addheaders = header
		response = opener.open(url, data=data, timeout=30)
		if response.info().get('Content-Encoding') == 'gzip':
			content = py3_dec(gzip.GzipFile(fileobj=io.BytesIO(response.read())).read())
		else:
			content = py3_dec(response.read())
	except Exception as e:
		failure = str(e)
		failing("(getUrl) ERROR - ERROR - ERROR : ########## {0} === {1} ##########".format(url, failure))
		xbmcgui.Dialog().notification(translation(30521).format('URL'), "ERROR = [COLOR red]{0}[/COLOR]".format(failure), icon, 15000)
		return sys.exit(0)
	return content

def cleaning(text):
	text = py2_enc(text)
	for n in (('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'), ('&apos;', "'"), ("&#x27;", "'"), ('&#34;', '"'), ('&#39;', '\''), ('&#039;', '\''), ('►', '>'),
				('&#x00c4', 'Ä'), ('&#x00e4', 'ä'), ('&#x00d6', 'Ö'), ('&#x00f6', 'ö'), ('&#x00dc', 'Ü'), ('&#x00fc', 'ü'), ('&#x00df', 'ß'), ('&#xD;', ''), ('\xc2\xb7', '-'),
				('&quot;', '"'), ('&szlig;', 'ß'), ('&ndash;', '-'), ('&Auml;', 'Ä'), ('&Ouml;', 'Ö'), ('&Uuml;', 'Ü'), ('&auml;', 'ä'), ('&ouml;', 'ö'), ('&uuml;', 'ü'),
				('&agrave;', 'à'), ('&aacute;', 'á'), ('&acirc;', 'â'), ('&egrave;', 'è'), ('&eacute;', 'é'), ('&ecirc;', 'ê'), ('&igrave;', 'ì'), ('&iacute;', 'í'), ('&icirc;', 'î'),
				('&ograve;', 'ò'), ('&oacute;', 'ó'), ('&ocirc;', 'ô'), ('&ugrave;', 'ù'), ('&uacute;', 'ú'), ('&ucirc;', 'û'),
				("\\'", "'"), ('<wbr/>', ''), ('<br />', ' -'), ('Ã¶', 'ö')):
				text = text.replace(*n)
	return text.strip()

def cleanStation(channelID):
	ChannelCode = ('ARD','Das Erste','ONE','FES','ZDF','2NEO','ZNEO','2INFO','ZINFO','3SAT','Arte','ARTE','BR','HR','KIKA','MDR','NDR','N3','ORF','PHOEN','RBB','SR','SWR','SWR/SR','WDR','RTL','RTL2','VOX','SRTL','SUPER')
	if channelID in ChannelCode and channelID != "":
		for n in ((' ', ''), ('ARD', 'Das Erste'), ('DasErste', 'Das Erste'), ('FES', 'ONE'), ('Arte', 'ARTE'), ('2INFO', 'ZDFinfo'),
					('ZINFO', 'ZDFinfo'), ('2NEO', 'ZDFneo'), ('ZNEO', 'ZDFneo'), ('3SAT', '3sat'), ('N3', 'NDR'), ('PHOEN', 'PHOENIX'), ('SUPER', 'SRTL')):
					channelID = channelID.replace(*n)
		if ('SR' in channelID or 'SWR' in channelID) and not 'SRTL' in channelID:
			channelID = 'SWR'
	channelID = '  ('+channelID+')' if channelID != "" else channelID
	return channelID

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split('&')
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

params = parameters_string_to_dict(sys.argv[2])
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', 'root'))
extras = unquote_plus(params.get('extras', 'standard'))
