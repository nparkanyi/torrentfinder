#!/usr/bin/python3
import urllib3, sys
from bs4 import BeautifulSoup

class TorrentInfo:
	def __init__(self, name, size, seeders, magnet):
		self.name = name
		self.size = size
		self.seeders = seeders
		self.magnet = magnet

class PageData:
	def __init__(self, url):
		self.http = urllib3.PoolManager()
		self.request = self.http.request('GET', url)
		self.html = BeautifulSoup(self.request.data)

		name_elems = self.html.find_all('a', attrs={ 'class' : 'cellMainLink'})	
		size_elems = self.html.find_all('td', attrs={ 'class' : 'nobr center'})
		seed_elems = self.html.find_all('td', attrs={ 'class' : 'green center'})
		magnet_elems = self.html.find_all('a', attrs={ 'class' : 'imagnet icon16'})
		
		self.torrent_list = [TorrentInfo(name_elems[i].text, size_elems[i].text,
								seed_elems[i].text, magnet_elems[i].get('href'))
								for i in range(len(name_elems))]
