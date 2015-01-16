#!/usr/bin/python3
#See 'LICENSE' for license details. 
import urllib3, sys
from bs4 import BeautifulSoup

class TorrentInfo:
	def __init__(self, name, size, seeders, magnet):
		self.name = name
		self.size = size
		self.seeders = seeders
		self.magnet = magnet
	
	def print_info(self):
		print(' _____________________________________  ')
		print('/                                     \\')
		print(x.name)
		print('Size: ', x.size, '    Seeders: ', x.seeders)
		print('Magnet: ', x.magnet)
		print('\\                                      /')
		print(' --------------------------------------')

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

search_terms = ''
for i in range(1, len(sys.argv)):
	search_terms = search_terms + sys.argv[i] + '%20'

page = PageData('http://kickass.so/usearch/' + search_terms + '/')
for x in page.torrent_list:
	x.print_info()
