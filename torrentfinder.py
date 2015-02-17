#!/usr/bin/python3
#See 'LICENSE' for license details. 
import urllib3, sys, getopt
from bs4 import BeautifulSoup

usage_text = """
torrentfinder.py Copyright 2015 Nicholas Parkanyi
Usage: torrentfinder.py [-h] [-n results] [-s min_seeders] search terms
"""

class TorrentInfo:
  def __init__(self, name, size, seeders, magnet):
    self.name = name
    self.size = size
    self.seeders = seeders
    self.magnet = magnet
  
  def print_info(self):
    print(' ' + '_' * len(self.name))
    print('/' + ' ' * len(self.name) + '\\')
    print(' ' + self.name)
    print(' Size: ', self.size, '    Seeders: ', self.seeders)
    print(' Magnet: ', self.magnet)
    print('\\' + '_' * len(self.name) + '/')

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
  
  def filter_torrents(self, func):
    self.torrent_list = list(filter(func, self.torrent_list))

max_results = 4
min_seeders = 0
search_terms = ''

try:
  optlist, args = getopt.getopt(sys.argv[1:], 'hn:s:') 
except getopt.GetoptError as err:
  print(err)
  print(usage_text)
  sys.exit(2)

if len(args) == 0:
  print(usage_text)
  sys.exit()

for o, a in optlist:
  if o == '-n':
    max_results = int(a)
  elif o == '-h':
    print(usage_text)
    sys.exit()
  elif o == '-s':
    min_seeders = int(a)
  else:
    print('Error: missing argument')
    sys.exit(2)

for i in range(len(args)):
  search_terms = search_terms + args[i] + '%20'

page = PageData('http://kickass.to/usearch/' + search_terms + '/')
page.filter_torrents(lambda x: int(x.seeders) >= min_seeders)

for i in range(min(max_results, len(page.torrent_list))):
  page.torrent_list[i].print_info()
