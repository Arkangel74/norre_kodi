# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import json
import time
from datetime import datetime, timedelta
PY2 = sys.version_info[0] == 2
if PY2:
	from urllib import urlencode, unquote_plus  # Python 2.X
	from urllib2 import urlopen  # Python 2.X
else: 
	from urllib.parse import urlencode, unquote_plus  # Python 3+
	from urllib.request import urlopen  # Python 3+
	from functools import reduce  # Python 3+

from .common import *


def mainMenu():
	i = 1
	while i <= 5:
		WU = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
		WT = (datetime.now() - timedelta(days=i)).strftime('%a~%d.%m.%Y')
		MD = WT.split('~')[0].replace('Mon', translation(30601)).replace('Tue', translation(30602)).replace('Wed', translation(30603)).replace('Thu', translation(30604)).replace('Fri', translation(30605)).replace('Sat', translation(30606)).replace('Sun', translation(30607))
		addDir(translation(30608).format(MD, WT.split('~')[1]), icon, {'mode': 'listVideos_HighDayChannel', 'url': BASE_URL+'/mediathek/nach-datum/?date='+WU})
		i += 1
	addDir(translation(30609), icon, {'mode': 'listChannel', 'url': BASE_URL+'/mediathek/nach-sender/'})
	addDir(translation(30610), icon, {'mode': 'listVideos_HighDayChannel', 'url': BASE_URL+'/mediathek/'})
	addDir(translation(30611), icon, {'mode': 'listVideos_Genre', 'url': 'Spielfilm'})
	addDir(translation(30612), icon, {'mode': 'listVideos_Genre', 'url': 'Serie'})
	addDir(translation(30613), icon, {'mode': 'listVideos_Genre', 'url': 'Report'})
	addDir(translation(30614), icon, {'mode': 'listVideos_Genre', 'url': 'Unterhaltung'})
	addDir(translation(30615), icon, {'mode': 'listVideos_Genre', 'url': 'Kinder'})
	addDir(translation(30616), icon, {'mode': 'listVideos_Genre', 'url': 'Sport'})
	if enableAdjustment:
		addDir(translation(30617), artpic+'settings.png', {'mode': 'aSettings'})
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listChannel(url):
	xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
	html = getUrl(url)
	debug_MS("(navigator.listChannel) SENDER-SORTIERUNG : Alle Sender in TV-Spielfilm")
	if showNOW == 'true':
		debug_MS("(navigator.listChannel) --- TVNOW - Sender EINGEBLENDET ---")
	else:
		debug_MS("(navigator.listChannel) --- TVNOW - Sender AUSGEBLENDET ---")
	content = html[html.find('<section class="mediathek-channels">'):]
	content = content[:content.find('</section>')]
	spl = content.split('title=')
	for i in range(1, len(spl), 1):
		entry = spl[i]
		try:
			urlFW = re.compile(r'href=["\'](https?://.*?mediathek/.*?)["\']>', re.DOTALL).findall(entry)[0]
			channelID = urlFW.split('channel=')[1].strip()
			channelID = cleanStation(channelID)
			title = channelID.replace('(', '').replace(')', '').replace('  ', '')
			if showNOW == 'false':
				if channelID in ['RTL', 'VOX', 'SUPER']: continue
			debug_MS("(navigator.listChannel) Link : {0}{1}".format(urlFW, channelID))
			addDir('[COLOR lime]'+title+'[/COLOR]', artpic+title.lower().replace(' ', '')+'.png', {'mode': 'listVideos_HighDayChannel', 'url': urlFW}, studio=title)
		except:
			failing("(listChannel) Fehler-Eintrag : {0}".format(str(entry)))
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listVideos_HighDayChannel(url):
	content = getUrl(url)
	debug_MS("(navigator.listVideos_HighDayChannel) MEDIATHEK : {0}".format(url))
	if showNOW == 'true':
		debug_MS("(navigator.listVideos_HighDayChannel) --- TVNOW - Sender EINGEBLENDET ---")
	else:
		debug_MS("(navigator.listVideos_HighDayChannel) --- TVNOW - Sender AUSGEBLENDET ---")
	if "?date=" in url or "?channel=" in url:
		results = re.findall('<section class="teaser-section">(.+?)</section>', content, re.S)
	else:
		results = re.findall('<div class="swiper-container"(.+?)<div class="swiper-button-prev"></div>', content, re.S)
	for chtml in results:
		spl = chtml.split('<div class="content-teaser') if "?date=" in url or "?channel=" in url else chtml.split('<div class="swiper-slide">')
		for i in range(1,len(spl),1):
			entry = spl[i]
			try:
				match1 = re.compile(r'<span class=["\']headline["\']>(.*?)</span>', re.DOTALL).findall(entry)
				match2= re.compile(r'<span class=["\']subline.+?>(.*?)</span>', re.DOTALL).findall(entry)
				match3 = re.compile(r'target=["\']_self["\'] title=["\'](.*?)["\']', re.DOTALL).findall(entry)
				if (match1[0] and not match2[0] and match3[0]):
					first = match1[0].replace('…', '').replace('...', '').strip()
					third = match3[0].replace('…', '').replace('...', '').strip()
					if first == third:
						title = cleaning(first)
					else:
						title = cleaning(first.strip())+" - "+cleaning(third.replace(first, "").strip())
					added = ""
					channelID = cleaning(url.split('/')[-1].replace('?channel=', '').strip())
					channelID = cleanStation(channelID)
					studio = channelID.replace('(', '').replace(')', '').replace('  ', '')
				elif (match1[0] and match2[0] and not match3[0]):
					title = cleaning(match1[0].strip())+" - "+cleaning(match2[0].split('|')[-1].strip())
					added = match2[0].split('|')[0].strip()
					channelID = cleaning(match2[0].split('|')[1].strip())
					channelID = cleanStation(channelID)
					studio = channelID.replace('(', '').replace(')', '').replace('  ', '')
				elif (match1[0] and match2[0] and match3[0]):
					first = match1[0].replace('…', '').replace('...', '').strip()
					third = match3[0].replace('…', '').replace('...', '').strip()
					if first == third:
						title = cleaning(first)
					else:
						testing3 = cleaning(third.replace(first, "").strip())
						if testing3 == "":
							title = cleaning(first)
						else:
							title = cleaning(first)+" - "+testing3
					added = match2[0].split('|')[0].strip()
					channelID = cleaning(match2[0].split('|')[1].strip())
					channelID = cleanStation(channelID)
					studio = channelID.replace('(', '').replace(')', '').replace('  ', '')
				if showDATE and added != "":
					title = added.strip()+"  "+title
				urlFW = re.compile(r'<a href=["\'](https?://.*?mediathek/.*?)["\']', re.DOTALL).findall(entry)[0]
				photo = re.compile(r'<img src=["\'](https?://.*?.jpg)["\']', re.DOTALL).findall(entry)[0]
				photo = photo.split(',')[0].rstrip()+'.jpg' if ',' in photo else photo
				if showCHANNEL and channelID != "":
					title += channelID
				if showNOW == 'false' and channelID != "":
					if channelID in ['RTL', 'VOX', 'SUPER']: continue
				debug_MS("(navigator.listVideos_HighDayChannel) Name : {0}".format(title))
				debug_MS("(navigator.listVideos_HighDayChannel) Link : {0}".format(urlFW))
				debug_MS("(navigator.listVideos_HighDayChannel) Icon : {0}".format(photo))
				addLink(title, photo, {'mode': 'playVideo', 'url': urlFW}, studio)
			except:
				failing("(listVideos_HighDayChannel) Fehler-Eintrag : {0}".format(str(entry)))
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listVideos_Genre(category):
	content = getUrl(BASE_URL+"/mediathek/")
	debug_MS("(navigator.listVideos_Genre) MEDIATHEK : {0}/mediathek/ - Genre = *{1}*".format(BASE_URL, category.upper()))
	if showNOW == 'true':
		debug_MS("(navigator.listVideos_Genre) --- TVNOW - Sender EINGEBLENDET ---")
	else:
		debug_MS("(navigator.listVideos_Genre) --- TVNOW - Sender AUSGEBLENDET ---")
	results = re.findall('<span>'+category+'</span>(.+?)<div class="scroll-box">', content, re.S)
	for chtml in results:
		spl = chtml.split('<li>')
		for i in range(1,len(spl),1):
			entry = spl[i]
			try:
				match1 = re.compile(r'class=["\']aholder["\'] title=["\'](.*?)["\']>', re.DOTALL).findall(entry)
				match2= re.compile('<strong>(.*?)</strong>\s+<span>(.*?)</span>', re.DOTALL).findall(entry)
				first = match1[0].strip()
				secondONE = match2[0][0].strip()
				secondTWO = match2[0][1].strip()
				if first == secondONE:
					title = cleaning(first)
				elif ('...' in secondONE and not '...' in secondTWO):
					title = cleaning(first.replace(secondTWO, "").strip())+" - "+cleaning(secondTWO.strip())
				elif ('...' in secondONE and '...' in secondTWO):
					title = cleaning(first)
				else:
					title = cleaning(secondONE.strip())+" - "+cleaning(first.replace(secondONE, "").strip())
				added = re.compile(r'<div class=["\']col["\']>(.*?)</div>', re.DOTALL).findall(entry)[0]
				if showDATE and added != "":
					title = added.strip()+"  "+title
				channel = re.compile(r'target=["\']_self["\'] title=["\'].+?["\']>(.*?)</a>', re.DOTALL).findall(entry)[0]
				channelID = cleanStation(channel)
				studio = channelID.replace('(', '').replace(')', '').replace('  ', '')
				urlFW = re.compile(r'<a href=["\'](https?://.*?mediathek/.*?)["\']', re.DOTALL).findall(entry)[0]
				try: photo = re.compile(r'src=["\'](https?://.*?.jpg)["\']', re.DOTALL).findall(entry)[0]
				except: photo = ""
				photo = photo.split(',')[0].rstrip()+'.jpg' if ',' in photo else photo
				if showCHANNEL and channelID != "":
					title += channelID
				if showNOW == 'false' and channelID != "":
					if channelID in ['RTL', 'VOX', 'SUPER']: continue
				debug_MS("(navigator.listVideos_Genre) Name : {0}".format(title))
				debug_MS("(navigator.listVideos_Genre) Link : {0}".format(urlFW))
				debug_MS("(navigator.listVideos_Genre) Icon : {0}".format(photo))
				addLink(title, photo, {'mode': 'playVideo', 'url': urlFW}, studio)
			except:
				failing("(listVideos_Genre) Fehler-Eintrag : {0}".format(str(entry)))
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def playVideo(url):
	finalURL = False
	ARD_SCHEMES = ('http://www.ardmediathek.de', 'https://www.ardmediathek.de', 'http://mediathek.daserste.de', 'https://mediathek.daserste.de')
	RTL_SCHEMES = ('http://www.nowtv.de', 'https://www.nowtv.de', 'http://www.tvnow.de', 'https://www.tvnow.de')
	log("(navigator.playVideo) --- START WIEDERGABE ANFORDERUNG ---")
	log("(navigator.playVideo) frei")
	try:
		content = getUrl(url)
		LINK = re.compile('<header class="broadcast-detail__header">.+?<a href="([^"]+)" class="mediathek-open col-hover-thek"', re.DOTALL).findall(content)[0]
		log("(navigator.playVideo) AbspielLink (Original) : {0}".format(LINK))
	except:
		log("(navigator.playVideo) MediathekLink-00 : MediathekLink der Sendung in TV-Today NICHT gefunden !!!")
		dialog.notification(translation(30521), translation(30522), icon, 8000)
		LINK = ""
	log("(navigator.playVideo) frei")
	if LINK.startswith("https://www.arte.tv"):
		videoID = re.compile("arte.tv/de/videos/([^/]+?)/", re.DOTALL).findall(LINK)[0]
		try:
			finalURL = 'plugin://plugin.video.tyl0re.arte/?mode=playVideo&url='+str(videoID)
			log("(navigator.playVideo) AbspielLink-1 (ARTE-TV) : {0}".format(finalURL))
		except:
			try:
				finalURL = 'plugin://plugin.video.arteplussept/play/SHOW/'+str(videoID)
				log("(navigator.playVideo) AbspielLink-2 (ARTE-plussept) : {0}".format(finalURL))
			except:
				if finalURL:
					log("(navigator.playVideo) AbspielLink-00 (ARTE) : *ARTE-Plugin* Der angeforderte -VideoLink- existiert NICHT !!!")
					dialog.notification(translation(30523).format('ARTE - Plugin'), translation(30525), icon, 8000)
				else:
					log("(navigator.playVideo) AbspielLink-00 (ARTE) : KEIN *ARTE-Addon* zur Wiedergabe vorhanden !!!")
					dialog.notification(translation(30523).format('ARTE - Addon'), translation(30524).format('ARTE-Addon'), icon, 8000)
	elif LINK.startswith(ARD_SCHEMES):
		videoURL = LINK
		return ArdGetVideo(videoURL)
	elif LINK.startswith("https://www.zdf.de"):
		cleanURL = LINK[:LINK.find('.html')]
		videoURL = unquote_plus(cleanURL)+".html"
		return ZdfGetVideo(videoURL)
	elif LINK.startswith(RTL_SCHEMES):
		LINK = LINK.replace('http://', 'https://').replace('www.nowtv.de/', 'www.tvnow.de/').replace('list/aktuell/', '').replace('/player', '')
		videoSE = LINK.split('/')[4].strip()
		videoEP = LINK.split('/')[-1].strip()
		log("(navigator.playVideo) --- RTL-Daten : ### Serie [{0}] ### Episode [{1}] ### ---".format(videoSE, videoEP))
		return RtlGetVideo(videoSE, videoEP, LINK)
	if finalURL:
		listitem = xbmcgui.ListItem(path=finalURL)
		xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem)
	log("(navigator.playVideo) --- ENDE WIEDERGABE ANFORDERUNG ---")

def ArdGetVideo(videoURL):
	finalURL = False
	m3u8_List = []
	ARD_Url = ""
	try:
		if 'documentId=' in videoURL:
			videoID = videoURL.split('documentId=')[1]
		else:
			secondURL = getUrl(videoURL)
			videoID = re.compile(r'["\']contentId["\']:([^,]+?),["\']metadataId["\']:', re.DOTALL).findall(secondURL)[0].replace('"', '').replace("'", "")
		debug_MS("(navigator.ArdGetVideo) ***** Extracted-videoID : {0} *****".format(videoID))
		# evtl. OLD = https://classic.ardmediathek.de/play/media/66597424 #
		content = getUrl('https://appdata.ardmediathek.de/appdata/servlet/play/media/'+videoID)
		debug_MS("(navigator.ArdGetVideo) ##### CONTENT : {0} #####".format(str(content)))
		result = json.loads(content)
		if len(result['_mediaArray']) > 1:
			video_data = result['_mediaArray'][1]
		else:
			video_data = result['_mediaArray'][0]
		if prefSTREAM == '0' and str(video_data['_mediaStreamArray'][0]['_quality']) == 'auto':
			if type(video_data['_mediaStreamArray'][0]['_stream']) == list:
				finalURL = str(video_data['_mediaStreamArray'][0]['_stream'][0])
				log("(navigator.ArdGetVideo) Wir haben mehrere *m3u8-Streams* in der Liste (ARD+3) - wähle den Ersten : {0}".format(finalURL))
			else:
				finalURL = str(video_data['_mediaStreamArray'][0]['_stream'])
				log("(navigator.ArdGetVideo) Wir haben 1 *m3u8-Stream* (ARD+3) - wähle Diesen : {0}".format(finalURL))
			if finalURL:
				finalURL = "https:"+finalURL if finalURL[:4] != "http" else finalURL
		if not finalURL:
			if type(video_data['_mediaStreamArray'][-1]['_stream']) == list:
				ARD_Url = str(video_data['_mediaStreamArray'][-1]['_stream'][-1])
				log("(navigator.ArdGetVideo) Wir haben mehrere *mp4-Streams* in der Liste (ARD+3) - wähle den Zweiten : {0}".format(ARD_Url))
			else:
				ARD_Url = str(video_data['_mediaStreamArray'][-1]['_stream'])
				log("(navigator.ArdGetVideo) Wir haben nur 1 *mp4-Stream* (ARD+3) - wähle Diesen : {0}".format(ARD_Url))
			if ARD_Url != "":
				ARD_Url = "https:"+ARD_Url if ARD_Url[:4] != "http" else ARD_Url
				finalURL = VideoBEST(ARD_Url, improve='ard-YES') # *mp4URL* Qualität nachbessern, überprüfen, danach abspielen
		if not finalURL:
			log("(navigator.ArdGetVideo) AbspielLink-00 (ARD+3) : *ARD-Intern* Der angeforderte -VideoLink- existiert NICHT !!!")
			dialog.notification(translation(30523).format('ARD - Intern'), translation(30525), icon, 8000)
		else:
			listitem = xbmcgui.ListItem(path=finalURL)
			xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem)
			log("(navigator.ArdGetVideo) END-Qualität (ARD+3) : {0}".format(finalURL))
	except:
		failing("(ArdGetVideo) AbspielLink-00 (ARD+3) : *ARD-Intern* Der angeforderte -VideoLink- existiert NICHT !!!")
		dialog.notification(translation(30523).format('ARD - Intern'), translation(30525), icon, 8000)
	log("(navigator.playVideo) --- ENDE WIEDERGABE ANFORDERUNG ---")

def RtlGetVideo(SERIES, EPISODE, REFERER):
	j_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "params": {"addonid":"plugin.video.rtlnow", "properties": ["enabled"]}, "id":1}')
	if '"enabled":false' in j_query:
		try: xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid":"plugin.video.rtlnow", "enabled":true}, "id":1}')
		except: pass
	if xbmc.getCondVisibility('System.HasAddon(plugin.video.rtlnow)'):
		#http://api.tvnow.de/v3/movies/shopping-queen/2361-lisa-marie-nuernberg-flower-power-praesentiere-dich-in-deinem-neuen-bluetenkleid?fields=manifest,isDrm,free,payed
		try: # https://bff.apigw.tvnow.de/module/player/%d" % int(assetID)
			content = getUrl('http://api.tvnow.de/v3/movies/{0}/{1}?fields=manifest,isDrm,free,payed'.format(SERIES, EPISODE))
			DATA = json.loads(content)
			PayType = True
			protected = '0'
			videoFREE = ""
			videoHD = ""
			if 'payed' in DATA and str(DATA['payed']) !="" and DATA['payed'] != None:
				PayType = DATA['payed']
			if 'isDrm' in DATA and DATA['isDrm'] == True:
				protected = '1'
				log("(navigator.RtlGetVideo) ~~~ Video ist DRM - geschützt ~~~")
			if 'manifest' in DATA and 'dash' in DATA['manifest'] and DATA["manifest"]["dash"] !="":
				videoFREE = DATA["manifest"]["dash"].replace('dash.secure.footprint.net', 'dash-a.akamaihd.net').split('.mpd')[0]+'.mpd'
				debug_MS("(navigator.RtlGetVideo) videoFREE : {0}".format(videoFREE))
			if 'manifest' in DATA and 'dashhd' in DATA['manifest'] and DATA["manifest"]["dashhd"] !="":
				videoHD = DATA["manifest"]["dashhd"].replace('dash.secure.footprint.net', 'dash-a.akamaihd.net').split('.mpd')[0]+'.mpd'
				debug_MS("(navigator.RtlGetVideo) videoHD : {0}".format(videoHD))
			listitem = xbmcgui.ListItem(path='plugin://plugin.video.rtlnow/?mode=playDash&xnormSD='+str(videoFREE)+'&xhighHD='+str(videoHD)+'&xlink='+REFERER+'&xdrm='+protected+'&xstat='+str(PayType))
			xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem)
		except:
			failing("(RtlGetVideo) AbspielLink-00 (TV-Now) : *TVNow-Plugin* Der angeforderte -VideoLink- existiert NICHT !!!")
			dialog.notification(translation(30523).format('TVNow - Plugin'), translation(30525), icon, 8000)
	else:
		log("(navigator.RtlGetVideo) AbspielLink-00 (TV-Now) : KEIN *TVNow-Addon* zur Wiedergabe vorhanden !!!")
		dialog.notification(translation(30523).format('TVNow - Addon'), translation(30524).format('TVNow-Addon'), icon, 8000)
	log("(navigator.playVideo) --- ENDE WIEDERGABE ANFORDERUNG ---")

def ZdfGetVideo(videoURL):
	videoFOUND = False
	try: 
		content = getUrl(videoURL)
		response = re.compile(r'data-zdfplayer-jsb=["\']({.+?})["\']', re.DOTALL).findall(content)[0]
		firstURL = json.loads(response)
		if firstURL:
			teaser = firstURL['content']
			secret = firstURL['apiToken']
			headerfields = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'), ('Api-Auth', 'Bearer '+secret)]
			log("(navigator.ZdfGetVideo) SECRET gefunden (ZDF+3) : ***** {0} *****".format(str(secret)))
			teaser = API_ZDF+teaser if teaser[:4] != "http" else teaser
			debug_MS("(navigator.ZdfGetVideo) ##### TEASER : {0} #####".format(teaser))
			secondURL = getUrl(teaser, header=headerfields)
			element = json.loads(secondURL)
			if element['profile'] == "http://zdf.de/rels/not-found":
				return False
			if element['contentType'] == "clip":
				component = element['mainVideoContent']['http://zdf.de/rels/target']
				#videoFOUND1 = API_ZDF+element['mainVideoContent']['http://zdf.de/rels/target']['http://zdf.de/rels/streams/ptmd']
				#videoFOUND2 = API_ZDF+element['mainVideoContent']['http://zdf.de/rels/target']['http://zdf.de/rels/streams/ptmd-template'].replace('{playerId}', 'ngplayer_2_3')
			elif element['contentType'] == "episode":
				if "mainVideoContent" in element:
					component = element['mainVideoContent']['http://zdf.de/rels/target']
				elif "mainContent" in element:
					component = element['mainContent'][0]['videoContent'][0]['http://zdf.de/rels/target']
			if "http://zdf.de/rels/streams/ptmd-template" in component and component['http://zdf.de/rels/streams/ptmd-template'] != "":
				videoFOUND = API_ZDF+component['http://zdf.de/rels/streams/ptmd-template'].replace('{playerId}', 'ngplayer_2_3').replace('\/', '/')
			if videoFOUND:
				debug_MS("(navigator.ZdfGetVideo) ##### videoFOUND : {0} #####".format(videoFOUND))
				thirdURL = getUrl(videoFOUND, header=headerfields)
				return ZdfExtractQuality(thirdURL)
	except:
		failing("(ZdfGetVideo) AbspielLink-00 (ZDF+3) : *ZDF-Intern* Der angeforderte -VideoLink- existiert NICHT !!!")
		log("(navigator.playVideo) --- ENDE WIEDERGABE ANFORDERUNG ---")
		dialog.notification(translation(30523).format('ZDF - Intern'), translation(30525), icon, 8000)

def ZdfExtractQuality(thirdURL):
	jsonObject = json.loads(thirdURL)
	MEDIAS = []
	m3u8_QUALITIES = ['auto', 'veryhigh', 'high', 'med']
	mp4_QUALITIES = ['hd', 'veryhigh', 'high', 'low']
	finalURL = False
	try:
		for each in jsonObject['priorityList']:
			vidType = each['formitaeten'][0]['mimeType'].lower()
			vidQuality = each['formitaeten'][0]['qualities']
			vidForm = each['formitaeten'][0]['type']
			vidMode = each['formitaeten'][0]['facets']
			if prefSTREAM == "0" and vidForm == "h264_aac_ts_http_m3u8_http" and vidType == "application/x-mpegurl":
				for found in m3u8_QUALITIES:
					for quality in vidQuality:
						if quality['quality'] == found and "mil/master.m3u8" in quality['audio']['tracks'][0]['uri']:
							MEDIAS.append({'url': quality['audio']['tracks'][0]['uri'], 'type': 'video', 'mimeType': vidType})
				finalURL = MEDIAS[0]['url']
				log("(navigator.ZdfExtractQuality) m3u8-Stream (ZDF+3) : {0}".format(finalURL))
			if not finalURL and vidForm == "h264_aac_mp4_http_na_na" and "progressive" in vidMode and vidType == "video/mp4":
				for found in mp4_QUALITIES:
					for quality in vidQuality:
						if quality['quality'] == found:
							MEDIAS.append({'url': quality['audio']['tracks'][0]['uri'], 'type': 'video', 'mimeType': vidType})
				log("(navigator.ZdfExtractQuality) ZDF-STANDARDurl : {0}".format(MEDIAS[0]['url']))
				finalURL = VideoBEST(MEDIAS[0]['url'], improve='zdf-YES') # *mp4URL* Qualität nachbessern, überprüfen, danach abspielen
		if not finalURL:
			log("(navigator.ZdfExtractQuality) AbspielLink-00 (ZDF+3) : *ZDF-Intern* VIDEO konnte NICHT abgespielt werden !!!")
		else:
			listitem = xbmcgui.ListItem(path=finalURL)
			xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem)
			log("(navigator.ZdfExtractQuality) END-Qualität (ZDF+3) : {0}".format(finalURL))
	except:
		failing("(ZdfExtractQuality) AbspielLink-00 (ZDF+3) : *ZDF-Intern* Fehler bei Anforderung des AbspielLinks !!!")
	log("(navigator.playVideo) --- ENDE WIEDERGABE ANFORDERUNG ---")

def VideoBEST(best_url, improve=False):
	# *mp4URL* Qualität nachbessern, überprüfen, danach abspielen
	standards = [best_url, "", ""]
	if improve == "ard-YES":
		first_repls = (('/960', '/1280'), ('.hq.mp4', '.hd.mp4'), ('.l.mp4', '.xl.mp4'), ('_C.mp4', '_X.mp4'))
		second_repls = (('/1280', '/1920'), ('.xl.mp4', '.xxl.mp4'))
	elif improve == "zdf-YES":
		first_repls = (('808k_p11v15', '2360k_p35v15'), ('1628k_p13v15', '2360k_p35v15'), ('1456k_p13v12', '2328k_p35v12'), ('1496k_p13v13', '2328k_p35v13'), ('1496k_p13v14', '2328k_p35v14'),
								('2256k_p14v11', '2328k_p35v11'), ('2256k_p14v12', '2328k_p35v12'), ('2296k_p14v13', '2328k_p35v13'), ('2296k_p14v14', '2328k_p35v14'))
		second_repls = (('2328k_p35v12', '3328k_p36v12'), ('2328k_p35v13', '3328k_p36v13'), ('2328k_p35v14', '3328k_p36v14'), ('2360k_p35v15', '3360k_p36v15'))
	standards[1] = reduce(lambda a, kv: a.replace(*kv), first_repls, standards[0])
	standards[2] = reduce(lambda b, kv: b.replace(*kv), second_repls, standards[1])
	for element in reversed(standards):
		if len(element) > 0:
			try:
				code = urlopen(element).getcode()
				if str(code) == "200":
					return element
			except: pass
	return best_url

def AddToQueue():
	return xbmc.executebuiltin('Action(Queue)')

def addDir(name, image, params={}, studio=None, plot=None):
	u = '{0}?{1}'.format(HOST_AND_PATH, urlencode(params))
	liz = xbmcgui.ListItem(name)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot, "Studio": studio})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	if useThumbAsFanart and image != icon and not artpic in image:
		liz.setArt({'fanart': image})
	return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=u, listitem=liz, isFolder=True)

def addLink(name, image, params={}, studio=None, plot=None, duration=None, seriesname=None, genre=None):
	u = '{0}?{1}'.format(HOST_AND_PATH, urlencode(params))
	liz = xbmcgui.ListItem(name)
	info = {}
	info['Tvshowtitle'] = seriesname
	info['Title'] = name
	info['Tagline'] = None
	info['Plot'] = plot
	info['Duration'] = duration
	info['Genre'] = genre
	info['Studio'] = studio
	info['Mediatype'] = 'video'
	liz.setInfo(type='Video', infoLabels=info)
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	if useThumbAsFanart and image != icon and not artpic in image:
		liz.setArt({'fanart': image})
	liz.addStreamInfo('Video', {'Duration': duration})
	liz.setProperty('IsPlayable', 'true')
	liz.setContentLookup(False)
	liz.addContextMenuItems([(translation(30654), 'RunPlugin('+HOST_AND_PATH+'?mode=AddToQueue)')])
	return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=u, listitem=liz)
